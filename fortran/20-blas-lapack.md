---
title: 수치 라이브러리 연결
order: 20
permalink: /fortran/20-blas-lapack/
---

이 장에서는 선형대수 같은 기본 계산을 직접 짜지 않고 BLAS와 LAPACK 라이브러리를 불러 쓰는 방법을 배운다. 호출 규칙, 링크 옵션, 인터페이스 블록으로 인수를 검사받는 방법, 열 우선 순서와 선행 차원을 다룬다.

## 수치 소프트웨어

공학 계산의 대부분은 연립방정식 풀이나 푸리에 변환 같은 잘 알려진 계산으로 나뉜다. 이런 계산은 이미 만들어진 라이브러리가 있으므로 내 문제에 맞는 짧은 주 프로그램만 쓰면 된다.

[Netlib](https://www.netlib.org/)은 수학 소프트웨어, 논문, 데이터베이스를 모은 저장소다. 저장소는 테네시 대학(UTK)과 오크리지 국립연구소(ORNL)에 있고, 사이트에서 저장소를 찾아보고 검색할 수 있다. 원본은 전자우편과 ftp로 받는 방법을 설명했지만 이 가이드는 웹 주소만 적는다. Netlib의 소프트웨어는 소스를 내려받아 직접 컴파일해서 쓰는 것이 기본이다. 가장 많이 쓰이는 것이 BLAS와 LAPACK이다.

원본이 소개한 상용 라이브러리는 지금도 있다. 다음 내용은 각 사이트에서 확인했다.

- [NAG Library](https://nag.com/nag-library/): C, C++, Python, Java, .NET, Fortran에서 쓸 수 있는 수치 알고리즘 라이브러리다.
- [IMSL](https://www.perforce.com/products/imsl): 원본의 Visual Numerics가 아니라 지금은 Perforce가 제공하며, C, Fortran, Java, Python용이다.
- [Numerical Recipes](https://numerical.recipes/): 2판의 Fortran 판 책을 온라인으로 읽을 수 있고, 최신 3판은 C++이다.

원하는 코드가 어디에 있는지 모를 때는 먼저 동료에게 묻고, 다음으로 Netlib의 검색을 쓴다. NIST의 [GAMS](https://gams.nist.gov/)(Guide to Available Mathematical Software)는 문제의 종류별로 소프트웨어를 찾는 색인으로, 지금도 접속된다.

## BLAS

BLAS(Basic Linear Algebra Subprograms)는 벡터와 행렬의 기본 연산을 표준 호출 형식으로 모은 루틴이다. 호출 형식이 표준이므로 같은 프로그램을 어느 BLAS 구현에든 연결할 수 있다. 그래서 기계에 맞게 최적화한 구현으로 바꾸기만 해도 프로그램이 빨라진다. 원본이 BLAS의 장점으로 꼽은 점이고, 지금도 같다.

### 수준과 이름 규칙

루틴은 연산의 크기에 따라 세 수준으로 나뉜다.

| 수준 | 연산 | 데이터와 계산량 | 예 |
|---|---|---|---|
| 1 | 벡터와 벡터 | O(n), O(n) | `xCOPY`, `xSWAP`, `xSCAL`, `xAXPY`, `xDOT`, `xASUM`, `xNRM2`, `IxAMAX` |
| 2 | 행렬과 벡터 | O(n^2), O(n^2) | `xGEMV`, `xGER`, `xSYR2`, `xTRSV` |
| 3 | 행렬과 행렬 | O(n^2), O(n^3) | `xGEMM`, `xSYMM`, `xSYRK`, `xSYR2K` |

이름 첫 글자 `x`는 타입을 나타낸다. BLAS와 LAPACK은 같은 규칙을 쓴다.

| 글자 | 타입 |
|---|---|
| `s` | 단정밀도 실수 |
| `d` | 배정밀도 실수 |
| `c` | 단정밀도 복소수 |
| `z` | 배정밀도 복소수 |

그래서 내적은 `sdot`, `ddot`, `cdotc`와 `zdotc`처럼 타입마다 다른 이름이 된다. 위 표의 `d` 버전(`dcopy`, `dgemm` 등)이 이 가이드를 쓴 환경의 BLAS 라이브러리에 모두 있음을 확인했다. 이 장은 배정밀도(`d`)를 쓴다.

### 인터페이스 블록

BLAS와 LAPACK 루틴은 모듈이 아니라 따로 컴파일된 외부 프로시저라서 컴파일러가 가인수의 타입을 모른다. [19장](../19-debugging/)에서 본 것처럼 인터페이스가 없으면 타입이 어긋나도 컴파일이 통과한다. 호출하는 쪽에 인터페이스 블록을 써 주면 컴파일러가 모듈 프로시저와 똑같이 인수를 검사한다. 인터페이스 블록은 프로시저의 머리 부분만 적은 것이다. 이 가이드는 BLAS 루틴마다 아래처럼 직접 쓴다. 인터페이스 본문 안에서는 바깥의 이름이 기본적으로 보이지 않으므로(Fortran 2018 8.8절) `import`로 상수 `dp`를 가져온다.

내적 `ddot`과 `y := a*x + y`를 계산하는 `daxpy`의 예제다.

<!-- file: ch20/dot_axpy.f90 -->
```fortran
program dot_axpy
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    function ddot(n, x, incx, y, incy)
      import :: dp
      real(dp) :: ddot
      integer, intent(in) :: n, incx, incy
      real(dp), intent(in) :: x(*), y(*)
    end function ddot

    subroutine daxpy(n, a, x, incx, y, incy)
      import :: dp
      integer, intent(in) :: n, incx, incy
      real(dp), intent(in) :: a, x(*)
      real(dp), intent(inout) :: y(*)
    end subroutine daxpy
  end interface

  real(dp) :: x(4), y(4)

  x = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp]
  y = [4.0_dp, 3.0_dp, 2.0_dp, 1.0_dp]
  print '(a, f6.1)', 'ddot:        ', ddot(4, x, 1, y, 1)
  print '(a, f6.1)', 'dot_product: ', dot_product(x, y)
  print '(a, f6.1)', 'stride 2:    ', ddot(2, x, 2, y, 1)
  call daxpy(4, 2.0_dp, x, 1, y, 1)
  print '(a, 4f6.1)', 'daxpy:       ', y
end program dot_axpy
```

<!-- output: ch20/dot_axpy.out -->
```text
ddot:          20.0
dot_product:   20.0
stride 2:      13.0
daxpy:          6.0   7.0   8.0   9.0
```

`ddot(n, x, incx, y, incy)`의 `n`은 쓸 원소의 수, `incx`와 `incy`는 원소 사이의 간격이다. 보통 `1`이고 원소 둘 가운데 하나를 건너뛰려면 `2`를 준다. 예제의 `ddot(2, x, 2, y, 1)`은 `x(1)*y(1) + x(3)*y(2)`로 `13`이다. 내장 함수 `dot_product`도 같은 값을 낸다. `dot_product`는 라이브러리 없이 쓸 수 있지만 원소 사이의 간격을 지정할 수 없다. `ddot`은 간격을 지정할 수 있고 최적화된 구현을 쓸 수 있다.

실수 `x`를 배정밀도 가인수에 넘기는 실수는 인터페이스 블록이 컴파일 단계에서 잡는다.

<!-- file: ch20/blas_mismatch.f90 -->
```fortran
program blas_mismatch
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    subroutine daxpy(n, a, x, incx, y, incy)
      import :: dp
      integer, intent(in) :: n, incx, incy
      real(dp), intent(in) :: a, x(*)
      real(dp), intent(inout) :: y(*)
    end subroutine daxpy
  end interface

  real :: x(3), y(3)

  x = 1.0
  y = 0.0
  call daxpy(3, 2.0_dp, x, 1, y, 1)
  print '(3f6.1)', y
end program blas_mismatch
```

```text
blas_mismatch.f90:18:35:

   18 |   call daxpy(3, 2.0_dp, x, 1, y, 1)
      |                                   1
Error: Type mismatch in argument ‘x’ at (1); passed REAL(4) to REAL(8)
```

### 열 우선 순서와 선행 차원

Fortran은 배열을 열 우선 순서로 저장한다([10장](../10-arrays/)). BLAS와 LAPACK은 행렬을 `a(lda, *)` 형태로 받는다. `lda`가 선행 차원(leading dimension)이다. 이것은 호출하는 쪽에서 선언한 배열의 첫째 차원의 크기이고, 실제로 쓰는 행렬의 행 수가 아니다. 열 하나가 메모리에서 몇 칸마다 시작하는지를 알려 주는 값이다.

다음 예제는 `a(4, 3)`로 선언한 배열의 왼쪽 위 2×3 부분만 행렬로 쓴다. `m = 2`, `n = 3`이고 `lda = 4`다.

<!-- file: ch20/gemv_lda.f90 -->
```fortran
program gemv_lda
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    subroutine dgemv(trans, m, n, alpha, a, lda, x, incx, beta, y, incy)
      import :: dp
      character(len=1), intent(in) :: trans
      integer, intent(in) :: m, n, lda, incx, incy
      real(dp), intent(in) :: alpha, beta, a(lda, *), x(*)
      real(dp), intent(inout) :: y(*)
    end subroutine dgemv
  end interface

  real(dp) :: a(4, 3), x(3), y(2)

  a = 0.0_dp
  a(1:2, 1:3) = reshape([1.0_dp, 2.0_dp, 3.0_dp, &
                         4.0_dp, 5.0_dp, 6.0_dp], [2, 3], order=[2, 1])
  x = [1.0_dp, 2.0_dp, 3.0_dp]
  y = 0.0_dp
  call dgemv('N', 2, 3, 1.0_dp, a, 4, x, 1, 0.0_dp, y, 1)
  print '(a, 2f6.1)', 'y = ', y
end program gemv_lda
```

<!-- output: ch20/gemv_lda.out -->
```text
y =   14.0  32.0
```

`dgemv`는 `y := alpha*A*x + beta*y`를 계산한다. `trans`가 `'N'`이면 `A`를 그대로 쓴다. `reshape`의 `order=[2, 1]`은 값을 행 단위로 채운다는 뜻이므로 `A`는 첫 행이 `1 2 3`, 둘째 행이 `4 5 6`이다. 결과는 `1*1 + 2*2 + 3*3 = 14`와 `4*1 + 5*2 + 6*3 = 32`다.

행의 원소는 메모리에서 `lda`칸씩 떨어져 있다. 원본은 이 점을 `sdot`으로 `A*B`의 한 원소를 계산하는 예로 설명했다. 행 `i`와 열 `j`의 내적은 `ddot(p, a(i, 1), lda, b(1, j), 1)`이다. `a`의 간격이 `lda`이고 `b`의 열은 연속해서 놓여 있으므로 간격이 `1`이다.

### 행렬 곱: dgemm과 matmul

`dgemm`은 `C := alpha*op(A)*op(B) + beta*C`를 계산한다. `op`는 `transa`와 `transb`가 `'N'`이면 그대로, `'T'`이면 전치를 뜻한다. 내장 함수 `matmul`과 같은 값을 내는지 비교한다.

<!-- file: ch20/gemm.f90 -->
```fortran
program gemm
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    function ddot(n, x, incx, y, incy)
      import :: dp
      real(dp) :: ddot
      integer, intent(in) :: n, incx, incy
      real(dp), intent(in) :: x(*), y(*)
    end function ddot

    subroutine dgemm(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc)
      import :: dp
      character(len=1), intent(in) :: transa, transb
      integer, intent(in) :: m, n, k, lda, ldb, ldc
      real(dp), intent(in) :: alpha, beta, a(lda, *), b(ldb, *)
      real(dp), intent(inout) :: c(ldc, *)
    end subroutine dgemm
  end interface

  real(dp) :: a(2, 3), b(3, 2), c(2, 2)
  integer :: i

  a = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [2, 3], order=[2, 1])
  b = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [3, 2], order=[2, 1])
  call dgemm('N', 'N', 2, 2, 3, 1.0_dp, a, 2, b, 3, 0.0_dp, c, 2)
  do i = 1, 2
    print '(2f7.1)', c(i, :)
  end do
  print '(f4.1)', maxval(abs(c - matmul(a, b)))
  print '(f7.1)', ddot(3, a(1, 1), 2, b(1, 2), 1)
end program gemm
```

<!-- output: ch20/gemm.out -->
```text
   22.0   28.0
   49.0   64.0
 0.0
   28.0
```

첫째 결과는 2×2 행렬 `C`, 둘째 줄은 `dgemm`과 `matmul`의 차이의 최댓값, 마지막 줄은 앞에서 말한 `ddot`으로 계산한 `C(1, 2)`다. 같은 행렬 곱이므로 `C(1, 2) = 28`과 일치한다.

`matmul`과 `dot_product`는 언어에 들어 있는 내장 함수이므로 라이브러리 없이 쓸 수 있고, 인수의 형상도 컴파일러가 검사한다. 큰 행렬에서 속도가 필요하면 최적화한 BLAS를 쓸 수 있다. gfortran은 `-fexternal-blas`를 주면 일정 크기(`-fblas-matmul-limit`) 이상의 `matmul`을 BLAS 호출로 바꾸고, BLAS 라이브러리는 링크할 때 지정해야 한다고 매뉴얼에 적혀 있다. 코드를 고치지 않고 `matmul`을 빠르게 만들 수 있는 방법이다.

## LAPACK

LAPACK은 연립일차방정식, 최소제곱 문제, 고유값 문제, 특잇값 문제를 푸는 루틴을 모은 패키지로, BLAS 위에 만들어졌다. Fortran 90으로 쓰였고 [Netlib의 LAPACK](https://www.netlib.org/lapack/) 페이지에서 소스를 받는다. 해설서는 [LAPACK Users' Guide](https://www.netlib.org/lapack/lug/)다. LAPACK 사이트는 원래 목표가 EISPACK과 LINPACK을 공유 메모리를 쓰는 벡터 기계와 병렬 기계에서 효율적으로 돌리는 것이었다고 설명한다.

가장 많이 쓰는 루틴은 연립방정식 `AX = B`의 풀이 루틴이다.

| 루틴 | 행렬 `A` |
|---|---|
| `xGESV` | 일반 행렬 |
| `xPOSV` | 대칭 양의 정부호 행렬 |
| `xGBSV` | 띠 행렬 |

`dgesv`, `dposv`, `dgbsv`가 라이브러리에 있음을 확인했다. 이름 규칙은 BLAS와 같다.

### dgesv로 Ax = b 풀기

`dgesv(n, nrhs, a, lda, ipiv, b, ldb, info)`는 부분 피벗팅을 한 LU 분해로 `A = P*L*U`를 만들고 그것으로 방정식을 푼다. 인수는 다음과 같다.

- `n`: 방정식의 수, `nrhs`: 우변 벡터의 수(`b`의 열 수)
- `a`: 입력은 `n×n` 계수 행렬이고, 출력은 `L`과 `U`가 덮어쓴다. `lda >= max(1, n)`이어야 한다.
- `ipiv`: 피벗 행을 알려 주는 출력 정수 배열(길이 `n`)
- `b`: 입력은 우변이고, `info = 0`이면 출력은 해 `x`가 덮어쓴다.
- `info`: `0`이면 성공, 음수 `-i`이면 `i`번째 인수가 잘못되었다는 뜻이다. 양수 `i`이면 `U(i, i)`가 정확히 `0`이어서 분해는 끝났지만 해를 구할 수 없다.

다음은 해가 `x = (2, 3, -1)`인 3×3 연립방정식과 특이 행렬 하나를 푼다.

<!-- file: ch20/solve.f90 -->
```fortran
program solve
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    subroutine dgesv(n, nrhs, a, lda, ipiv, b, ldb, info)
      import :: dp
      integer, intent(in) :: n, nrhs, lda, ldb
      real(dp), intent(inout) :: a(lda, *), b(ldb, *)
      integer, intent(out) :: ipiv(*), info
    end subroutine dgesv
  end interface

  real(dp) :: a(3, 3), b(3), s(2, 2), t(2)
  integer :: ipiv(3), info

  a = reshape([2.0_dp, 1.0_dp, -1.0_dp, &
              -3.0_dp, -1.0_dp, 2.0_dp, &
              -2.0_dp, 1.0_dp, 2.0_dp], [3, 3], order=[2, 1])
  b = [8.0_dp, -11.0_dp, -3.0_dp]
  call dgesv(3, 1, a, 3, ipiv, b, 3, info)
  print '(a, i0)', 'info = ', info
  print '(a, 3f8.3)', 'x = ', b

  s = reshape([1.0_dp, 2.0_dp, 2.0_dp, 4.0_dp], [2, 2], order=[2, 1])
  t = [1.0_dp, 2.0_dp]
  call dgesv(2, 1, s, 2, ipiv, t, 2, info)
  print '(a, i0)', 'info = ', info
end program solve
```

<!-- output: ch20/solve.out -->
```text
info = 0
x =    2.000   3.000  -1.000
info = 2
```

첫 풀이는 `info = 0`이고 해가 정수로 나온다. 두 번째 행렬은 둘째 행이 첫 행의 두 배이므로 특이 행렬이고, `U(2, 2) = 0`이어서 `info = 2`가 돌아온다. 호출 뒤에는 `info`를 반드시 확인한다. `a`와 `b`는 입력 값을 잃으므로 필요하면 복사해 둔다.

## 링크

라이브러리의 이름은 `lib`로 시작해 `.a`(정적)나 `.so`(공유)로 끝나고, 링크할 때 `-l` 뒤에 `lib`와 확장자를 뺀 이름을 쓴다.

```sh
gfortran -std=f2018 -Wall -Wextra solve.f90 -o solve -llapack -lblas
```

이 가이드의 예제는 모두 위처럼 `-llapack -lblas`로 링크하고 `.flags` 옆 파일에 이 옵션을 적었다. LAPACK이 BLAS를 부르므로 `-llapack`을 `-lblas`보다 앞에 쓴다. 정적 라이브러리는 링커가 명령줄의 앞에서 뒤로 한 번만 읽으므로 순서가 맞지 않으면 `undefined reference` 오류가 난다. 직접 만든 정적 라이브러리 둘로 확인했다. 한 라이브러리가 다른 라이브러리의 루틴을 부르면 부르는 쪽을 앞에 쓴다. 이 가이드를 쓴 환경은 공유 라이브러리를 써서 `-lblas -llapack`으로 순서를 바꿔도 링크되었다. 그래도 정적 라이브러리나 다른 시스템에서 실패하지 않도록 순서를 지킨다.

Ubuntu에서는 `libblas-dev`와 `liblapack-dev` 패키지가 이 라이브러리를 제공한다. 라이브러리를 소스에서 컴파일해 만들 때는 `ar`로 묶는다. 원본의 `ranlib`은 `ar rcs`가 대신한다.

```sh
gfortran -c mysub.f90
ar rcs libmy_lib.a mysub.o
gfortran main.f90 -o main -L. -lmy_lib
```

### 최적화된 구현

Netlib의 BLAS는 기준 구현이어서 정확하지만 가장 빠르지는 않다. 호출 형식이 같으므로 최적화한 구현으로 바꿔도 소스를 고칠 필요가 없다. [OpenBLAS](https://www.openmathlib.org/OpenBLAS/)가 널리 쓰이는 예다. 이 가이드를 쓴 Ubuntu에서는 `/usr/lib/x86_64-linux-gnu/libblas.so`가 alternatives 링크를 거쳐 OpenBLAS를 가리켰다. 따라서 위의 `-llapack -lblas`가 실제로 OpenBLAS를 불렀다. OpenBLAS의 `-lopenblas`만으로 링크해도 `solve.f90`이 같은 결과를 냈다. 어느 구현이 연결되어 있는지는 `ls -l /etc/alternatives/libblas.so-x86_64-linux-gnu`처럼 링크를 따라가 보면 안다. 구현이 달라도 호출 형식과 결과의 의미는 같다.

## 흔한 실수

- 인터페이스 블록 없이 부른다. 타입이 어긋나도 컴파일이 통과한다.
- `lda`에 행렬의 행 수 대신 틀린 값을 준다. `lda`는 선언한 배열의 첫째 차원의 크기다.
- 행렬을 행 단위로 쓰고 `reshape`에 `order=[2, 1]`을 빼먹는다. 배열은 열 단위로 채워진다.
- `info`를 확인하지 않는다. `dgesv`가 특이 행렬에서 `b`를 해가 아닌 값으로 남겨도 프로그램은 계속된다.
- `-lblas -llapack`처럼 순서를 바꾸어 정적 라이브러리를 링크한다.
- 입력으로 다시 쓸 `a`를 `dgesv`에 그대로 넘긴다. `a`와 `b`는 덮어써진다.
