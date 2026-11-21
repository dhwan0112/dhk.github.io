---
title: 부프로그램과 배열
order: 15
permalink: /fortran/15-arrays-in-subprograms/
---

이 장에서는 배열을 프로시저에 넘기는 방법을 다룬다. 현대 코드의 기본인 가정 형상 배열과 배열 부분 전달을 먼저 설명하고, 옛 코드와 BLAS, LAPACK 호출에서 보이는 가정 크기 배열과 선행 차원(`lda`)을 읽는 법을 덧붙인다.

## 가정 형상 배열

원본은 `x(*)`로 길이를 모르는 배열을 받고 길이 `n`을 따로 넘겼다. 현대 Fortran에서는 가인수를 `x(:)`로 선언한다. 가정 형상 배열(assumed-shape array)이라 하며, 가인수가 실인수의 형상을 그대로 물려받는다(Fortran 2018 8.5.8.3). 차원 수는 콜론의 개수이므로 `a(:, :)`는 2차원이다. 크기를 따로 넘길 필요가 없고 `size()`로 얻는다.

| 식 | 뜻 |
|---|---|
| `size(x)` | `x`의 전체 원소 수 |
| `size(a, 1)`, `size(a, 2)` | `a`의 행 수, 열 수 |
| `shape(a)` | 각 차원의 크기를 담은 배열 |

가정 형상 배열의 아래 첨자는 실인수의 첨자와 상관없이 1부터 시작한다. `a(3:5)`를 넘겨도 가인수의 첫 원소는 `x(1)`이다.

가정 형상 가인수가 있는 프로시저는 반드시 명시적 인터페이스가 필요하다(15.4.2.2, [11장](../11-subprograms/) 참조). 호출하는 쪽이 가인수 선언을 모르면 컴파일러가 실인수와 맞추어 볼 수 없기 때문이다. 모듈 프로시저는 이 조건을 저절로 만족한다. 모듈 밖에 프로시저를 두고 인터페이스 없이 부르면 컴파일이 멈춘다.

<!-- file: ch15/no_interface.f90 -->
```fortran
program no_interface
  implicit none
  real :: v(3)

  v = [1.0, 2.0, 3.0]
  call show_sum(v)
end program no_interface

subroutine show_sum(x)
  implicit none
  real, intent(in) :: x(:)

  print *, sum(x)
end subroutine show_sum
```

gfortran 15.2의 메시지는 다음과 같다.

```text
no_interface.f90:6:15:

    6 |   call show_sum(v)
      |               1
Error: Explicit interface required for ‘show_sum’ at (1): assumed-shape argument
```

## saxpy와 matvec

원본의 `saxpy`는 `y := alpha*x + y`를 계산한다. 가정 형상 배열을 쓰면 길이 `n`이 필요 없고 계산은 배열 전체 연산 한 줄이다. 두 배열의 길이가 같은지는 `size`로 검사한다.

원본의 `matvec`은 `saxpy`를 열마다 불러 `y = A*x`를 만든다. 원본은 열의 첫 원소 `A(1,j)`를 넘기면서 포인터를 넘기는 것처럼 생각하면 된다고 설명했다. 지금은 열 전체를 배열 부분(array section) `a(:, j)`로 직접 쓴다. 행 수와 열 수도 `size(a, 1)`, `size(a, 2)`로 얻으므로 `m`, `n`, `lda`를 넘기지 않는다.

<!-- file: ch15/matvec.f90 -->
```fortran
module blas_like
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
contains
  subroutine saxpy(alpha, x, y)
    real(dp), intent(in) :: alpha, x(:)
    real(dp), intent(inout) :: y(:)

    if (size(x) /= size(y)) error stop 'saxpy: size mismatch'
    y = alpha * x + y
  end subroutine saxpy

  subroutine matvec(a, x, y)
    real(dp), intent(in) :: a(:, :), x(:)
    real(dp), intent(out) :: y(:)
    integer :: j

    y = 0.0_dp
    do j = 1, size(a, 2)
      call saxpy(x(j), a(:, j), y)
    end do
  end subroutine matvec
end module blas_like

program matvec_demo
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use blas_like, only: matvec
  implicit none
  real(dp) :: a(3, 2), x(2), y(3)

  a = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [3, 2])
  x = [10.0_dp, 100.0_dp]
  call matvec(a, x, y)
  print '(3f8.1)', y
  print '(a, f4.1)', 'difference from matmul: ', maxval(abs(y - matmul(a, x)))
end program matvec_demo
```

<!-- output: ch15/matvec.out -->
```text
   410.0   520.0   630.0
difference from matmul:  0.0
```

`reshape`는 원소를 열 우선 순서(column-major order)로 채우므로 `a`의 첫 열은 `1, 2, 3`이고 둘째 열은 `4, 5, 6`이다. `y`는 `1*10 + 4*100 = 410` 같은 값이 된다. 내장 함수 `matmul`의 결과와 비교해 맞는지 확인했다. 열 우선 순서는 [10장](../10-arrays/)에서 다뤘다.

`y`에는 `intent(out)`을 주었으므로 `matvec` 안에서 먼저 `y = 0.0_dp`로 채운다. 이 문장을 빼면 `y`의 처음 값이 정해지지 않는다.

## 배열 부분 전달과 연속성

`a(:, j)`는 `a`에서 열 하나를 고른 배열 부분이다. 열 우선 순서에서 한 열은 메모리에 연이어 놓이므로 이 부분은 연속적(contiguous)이다. 반면 `a(2, :)`처럼 행을 고르면 원소가 `a`의 행 수만큼 건너뛰어 놓여 연속적이지 않다(8.5.7).

가정 형상 가인수는 두 경우를 모두 받는다. 순서 결합(sequence association)은 가인수가 명시 형상이나 가정 크기 배열일 때만 적용되며(15.5.2.11), 가정 형상 가인수는 실인수의 형상을 그대로 물려받는다. 반대로 명시 형상이나 가정 크기 가인수는 실인수의 원소를 배열 원소 순서대로 이어진 열로 받는다. 연속적이지 않은 배열 부분이 이런 가인수에 대응하면 컴파일러가 연속적인 임시 배열에 복사해 넘기는 방법을 쓸 수 있다. 표준도 복사 후 되쓰는(copy-in/copy-out) 방식이 쓰일 수 있음을 언급한다(15.5.2.4 NOTE 5).

<!-- file: ch15/sections.f90 -->
```fortran
module norms
  implicit none
contains
  function norm_assumed(v) result(s)
    real, intent(in) :: v(:)
    real :: s

    s = sqrt(sum(v**2))
  end function norm_assumed

  function norm_explicit(n, v) result(s)
    integer, intent(in) :: n
    real, intent(in) :: v(n)
    real :: s

    s = sqrt(sum(v**2))
  end function norm_explicit
end module norms

program sections
  use norms, only: norm_assumed, norm_explicit
  implicit none
  real :: a(3, 4)
  integer :: i

  a = reshape([(real(i), i = 1, 12)], [3, 4])
  print '(f8.4)', norm_assumed(a(:, 2))
  print '(f8.4)', norm_assumed(a(2, :))
  print '(f8.4)', norm_explicit(4, a(2, :))
end program sections
```

<!-- output: ch15/sections.out -->
```text
  8.7750
 14.6287
 14.6287
```

세 호출의 결과는 모두 맞다. `-Warray-temporaries`를 주고 컴파일하면 gfortran 15.2는 임시 배열이 만들어지는 곳을 알려 준다.

```text
sections.f90:29:35:

   29 |   print '(f8.4)', norm_explicit(4, a(2, :))
      |                                   1
Warning: Creating array temporary at (1) for argument ‘v’ [-Warray-temporaries]
```

가정 형상 가인수를 쓰는 `norm_assumed(a(2, :))`에는 경고가 없다. 명시 형상 가인수 `v(n)`을 쓰는 호출에서만 임시 배열이 생긴다. 큰 배열에서 이런 호출이 반복문 안에 있으면 복사 비용이 쌓이므로 새 프로시저는 가정 형상 가인수를 쓴다. 가정 형상 가인수에 `contiguous` 속성을 주면 그 가인수가 연속적이라고 컴파일러에게 알릴 수 있다(8.5.7).

## 명시 형상과 가정 크기 배열

옛 코드에서는 배열 가인수가 다음 두 모양으로 보인다.

- 명시 형상 배열(explicit-shape array): `real :: x(n)`처럼 크기를 가인수나 상수로 선언한다. 크기 `n`은 다른 가인수로 받는다(8.5.8.2).
- 가정 크기 배열(assumed-size array): `real :: x(*)`, `real :: a(lda, *)`처럼 마지막 차원에 `*`를 쓴다. 크기는 실인수에서 물려받지만 마지막 차원의 크기가 없으므로 `size(a, 2)`나 `shape(a)`를 쓸 수 없다(8.5.8.5).

가정 크기 배열은 가인수에만 쓸 수 있다(C833).

두 가지는 가정 형상과 달리 실인수의 형상을 물려받지 않으므로(가정 크기는 전체 크기만 물려받는다), 크기를 `n`이나 `m`, `n`으로 따로 받는다. 2차원 배열은 행 수 `lda`(선행 차원, leading dimension)도 필요하다. 열 우선 순서에서 다음 열의 같은 행으로 가려면 `lda`개를 건너뛰어야 하기 때문이다. 배열의 선언된 행 수가 실제로 쓰는 행 수 `m`보다 클 수 있어서 둘은 다를 수 있다. 원본의 `mscale`이 그런 예다. 아래는 이를 현대 문법으로 옮긴 것이다. 모듈 안에 있어서 명시적 인터페이스를 갖는다.

<!-- file: ch15/legacy_style.f90 -->
```fortran
module old_style
  implicit none
contains
  subroutine scale(n, alpha, x)
    integer, intent(in) :: n
    real, intent(in) :: alpha
    real, intent(inout) :: x(*)
    integer :: i

    do i = 1, n
      x(i) = alpha * x(i)
    end do
  end subroutine scale

  subroutine mscale(m, n, alpha, a, lda)
    integer, intent(in) :: m, n, lda
    real, intent(in) :: alpha
    real, intent(inout) :: a(lda, *)
    integer :: j

    do j = 1, n
      call scale(m, alpha, a(1, j))
    end do
  end subroutine mscale
end module old_style

program legacy_style
  use old_style, only: mscale
  implicit none
  real :: a(4, 3)

  a = 1.0
  call mscale(3, 2, 5.0, a, 4)
  print '(3f5.1)', transpose(a)
end program legacy_style
```

<!-- output: ch15/legacy_style.out -->
```text
  5.0  5.0  1.0
  5.0  5.0  1.0
  5.0  5.0  1.0
  1.0  1.0  1.0
```

`a`는 `4 x 3`으로 선언했지만 `mscale`에는 왼쪽 위 `3 x 2` 부분만 처리하라고 `m=3`, `n=2`, `lda=4`를 넘겼다. `a`의 나머지는 `1.0`으로 남는다.

`call scale(m, alpha, a(1, j))`는 열의 첫 원소를 실인수로 준다. 가정 크기나 명시 형상 가인수는 그 원소부터 배열 끝까지를 가인수의 원소 열로 받으므로(8.5.8.5, 15.5.2.11), `scale`은 `x(1)`부터 `x(m)`까지 한 열을 본다. `scale`은 자기가 열을 받았는지 벡터를 받았는지 모른다. netlib의 참조 BLAS `dgemv`도 `DOUBLE PRECISION A(LDA,*), X(*), Y(*)`로 가인수를 선언하고 `LDA`를 호출하는 쪽에서 선언한 첫째 차원이라고 설명한다. 이 호출 규칙은 [20장](../20-blas-lapack/)에서 다시 나온다.

## 1차원과 2차원을 섞어 쓰기

원본은 같은 `scale` 서브루틴으로 행렬 전체를 줄이려고 `call scale(m*n, alpha, A)`처럼 2차원 배열을 1차원 가인수에 넘기는 방법을 보였다. 위의 순서 결합이 이를 허용하기 때문이다. 이 방법은 선언된 행 수가 실제 행 수와 같을 때만 맞다. 원본도 그 점을 경고하며 `mscale`을 대안으로 썼다.

새 코드는 이 기법을 쓰지 않는다. 다음 대체 방법이 더 읽기 쉽고 안전하다.

- 배열 전체 연산: `a = alpha * a`
- 부분 영역: `a(1:m, 1:n) = alpha * a(1:m, 1:n)`
- 열 단위 호출: 위의 `call saxpy(x(j), a(:, j), y)`처럼 가정 형상 가인수를 받는 프로시저에 열을 배열 부분으로 넘긴다.
- 모양을 바꿔 보기: `reshape(a, [m*n])`은 `a`를 1차원으로 만든 새 배열을 돌려준다. 복사본이라 원래 배열이 바뀌지 않는다.

<!-- file: ch15/new_style.f90 -->
```fortran
program new_style
  implicit none
  real :: a(4, 3)
  integer :: m, n

  a = 1.0
  m = 3
  n = 2
  a(1:m, 1:n) = 5.0 * a(1:m, 1:n)
  print '(3f5.1)', transpose(a)
end program new_style
```

<!-- output: ch15/new_style.out -->
```text
  5.0  5.0  1.0
  5.0  5.0  1.0
  5.0  5.0  1.0
  1.0  1.0  1.0
```

앞 예제의 `mscale` 호출과 결과가 같다.

## 자동 배열과 할당 가능 가인수

프로시저 안의 지역 배열 크기는 가인수로 정할 수 있다. 크기가 상수가 아닌 식에 달린 지역 배열을 자동 배열(automatic array)이라 하며, 프로시저가 호출될 때 크기가 정해진다(8.3). 원본은 지역 배열을 드물게 쓴다고 했다. 현대 코드에서는 가인수 `x`의 크기로 `tmp(size(x))`처럼 지역 배열의 크기를 정할 수 있다. 가인수 `y(size(x))`도 같은 식으로 크기를 정한 명시 형상 가인수다.

크기를 호출하는 쪽에서 정하지 못할 때는 `allocatable` 가인수로 받아 프로시저 안에서 할당한다. `intent(out)`이면 호출 시점에 이전 할당이 해제된다. 이런 가인수도 명시적 인터페이스가 필요하다.

<!-- file: ch15/auto_alloc.f90 -->
```fortran
module work_mod
  implicit none
contains
  subroutine smooth(x, y)
    real, intent(in) :: x(:)
    real, intent(out) :: y(size(x))
    real :: tmp(size(x))
    integer :: n

    n = size(x)
    tmp = x
    tmp(2:n-1) = (x(1:n-2) + x(2:n-1) + x(3:n)) / 3.0
    y = tmp
  end subroutine smooth

  subroutine make_ramp(n, v)
    integer, intent(in) :: n
    real, allocatable, intent(out) :: v(:)
    integer :: i

    allocate (v(n))
    v = [(real(i * i), i = 1, n)]
  end subroutine make_ramp
end module work_mod

program auto_alloc
  use work_mod, only: smooth, make_ramp
  implicit none
  real, allocatable :: v(:), s(:)

  call make_ramp(6, v)
  allocate (s(size(v)))
  call smooth(v, s)
  print '(6f7.2)', v
  print '(6f7.2)', s
end program auto_alloc
```

<!-- output: ch15/auto_alloc.out -->
```text
   1.00   4.00   9.00  16.00  25.00  36.00
   1.00   4.67   9.67  16.67  25.67  36.00
```

`smooth`의 `tmp`가 자동 배열이다. `tmp(2:n-1) = (x(1:n-2) + x(2:n-1) + x(3:n)) / 3.0`은 세 칸 이동 평균을 반복문 없이 쓴 것이다. `make_ramp`는 `n`을 받아 `v`를 할당하고 `1, 4, 9, ...`로 채운다.

## 흔한 실수

- 가정 형상 가인수를 쓰는 프로시저를 모듈 밖에 두고 인터페이스 없이 부른다. 컴파일 오류다.
- `intent(out)` 배열을 읽기부터 한다. 호출 시점에 값이 정해지지 않은 상태가 된다.
- 가정 크기 배열에 `size(a, 2)`를 쓴다. 마지막 차원의 크기가 없으므로 쓸 수 없다.
- `lda`를 `m`과 같다고 가정한다. 부분 행렬을 넘기면 틀린 열을 읽는다.
- 행(`a(i, :)`)을 명시 형상 가인수로 넘기는 호출을 반복문 안에서 되풀이한다. 매번 임시 배열이 생긴다.
