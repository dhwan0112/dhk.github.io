---
title: 프로그래밍 스타일
order: 18
permalink: /fortran/18-style/
---

이 장에서는 읽기 쉽고 컴파일러가 실수를 잡아 주는 코드를 쓰는 지침을 모은다. 원본의 지침을 현대 Fortran에 맞게 고쳤고, 확인 출처는 [fortran-lang.org의 모범 사례](https://fortran-lang.org/learn/best_practices/)다.

## 표준만 쓰기

원본은 이식성을 위해 표준 Fortran 77만 쓰라고 했다. 지금은 컴파일러에 표준을 지정해서 같은 약속을 지킨다. gfortran의 기본값인 `-std=gnu`는 최신 표준에 GNU 확장을 더한 것이고, `-std=f2018`은 표준을 벗어난 확장에 오류를 낸다.

```sh
gfortran -std=f2018 -Wall -Wextra main.f90 -o main
```

이 가이드의 모든 예제를 이 옵션으로 컴파일한다. 다음은 확장을 쓴 코드가 `-std=f2018`에서 거부되는 모습이다.

<!-- file: ch18/nonstandard.f90 -->
```fortran
program nonstandard
  implicit none
  real*8 :: x

  x = 1.0d0 / 3.0d0
  print '(f12.9)', x
end program nonstandard
```

gfortran 15.2는 첫 줄에서 멈춘다.

```text
nonstandard.f90:3:9:

    3 |   real*8 :: x
      |         1
Error: GNU Extension: Nonstandard type declaration REAL*8 at (1)
```

`real*8`의 `*8`은 표준이 아니다. 8바이트 실수가 필요하면 아래의 kind 매개변수를 쓴다.

## 프로그램을 모듈로 나누기

원본은 부프로그램 하나가 명확한 일 하나를 맡고, 가능하면 파일을 나누라고 했다. 이 지침은 그대로 유효하다. 다만 지금은 프로시저를 모듈 안에 둔다. 모듈 프로시저는 명시적 인터페이스를 가지므로 컴파일러가 호출마다 인수의 개수와 타입을 검사한다([16장](/fortran/16-modules/)). 모범 사례는 파일 하나에 모듈 하나를 두고 파일 이름을 모듈 이름과 맞추라고 한다. 모듈의 `implicit none`은 그 안의 모든 프로시저에 적용되므로 프로시저마다 다시 쓰지 않는다.

모듈은 내놓을 이름만 `public`으로 나열하고, 가져올 때는 `only`로 필요한 이름만 적는다. 그러면 소스의 앞부분만 읽어도 무엇을 주고받는지 보인다. 다음 예제는 정밀도를 정하는 모듈과 그것을 쓰는 모듈, 주 프로그램을 한 파일에 모았다. 지면 때문에 모았을 뿐이고, 실제 프로젝트에서는 모듈마다 파일을 나눈다.

<!-- file: ch18/statistics.f90 -->
```fortran
module kinds
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  private
  public :: dp
  integer, parameter :: dp = real64
end module kinds

module statistics
  use kinds, only: dp
  implicit none
  private
  public :: mean, variance

contains

  pure function mean(x) result(m)
    real(dp), intent(in) :: x(:)
    real(dp) :: m

    m = sum(x) / size(x)
  end function mean

  pure function variance(x) result(v)
    real(dp), intent(in) :: x(:)
    real(dp) :: v

    v = sum((x - mean(x))**2) / (size(x) - 1)
  end function variance
end module statistics

program report
  use kinds, only: dp
  use statistics, only: mean, variance
  implicit none
  real(dp) :: samples(5)

  samples = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
  print '(a, f6.2)', 'mean     = ', mean(samples)
  print '(a, f6.2)', 'variance = ', variance(samples)
end program report
```

<!-- output: ch18/statistics.out -->
```text
mean     =   3.00
variance =   2.50
```

`kinds` 모듈의 `dp` 한 줄이 프로그램 전체의 실수 정밀도를 정한다. 정밀도를 바꿀 때 이 줄만 고치면 된다. Fortran 2018 표준의 부속서 C.2.1도 kind 매개변수 값은 이식성이 없으므로 이름 붙은 상수로 한곳에서 정해 쓰라고 설명한다. `real64`는 `iso_fortran_env` 모듈이 주는 상수로, 64비트 실수의 kind 매개변수다. 상수는 `1.0_dp`처럼 값 뒤에 `_dp`를 붙여 같은 kind로 쓴다.

## 선언

원본은 모든 변수를 선언하라고 했고, 암시적 타입 지정을 나쁜 습관으로 꼽았다. `implicit none`이 그 약속을 컴파일러가 지키게 한다([3장](/fortran/03-basics/)). 여기에 가인수는 `intent`를 전부 쓴다.

- `intent(in)`은 읽기만 하는 가인수다. 값을 바꾸면 컴파일 오류가 난다.
- `intent(out)`은 프로시저가 값을 채워 돌려주는 가인수다.
- `intent(inout)`은 읽고 바꾸는 가인수다.

원본의 iswap 서브루틴을 현대식으로 쓰면 다음과 같다.

<!-- file: ch18/swap.f90 -->
```fortran
module swapping
  implicit none
contains
  subroutine swap(a, b)
    integer, intent(inout) :: a, b
    integer :: tmp

    tmp = a
    a = b
    b = tmp
  end subroutine swap
end module swapping

program swap_demo
  use swapping, only: swap
  implicit none
  integer :: m, n

  m = 1
  n = 2
  call swap(m, n)
  print '(2i3)', m, n
end program swap_demo
```

<!-- output: ch18/swap.out -->
```text
  2  1
```

선언은 가인수를 먼저, 지역 변수를 그 다음에 쓰고 둘 사이에 빈 줄을 둔다. 원본이 상수, common 블록, 지역 변수를 나누어 선언하라고 한 것과 같은 뜻이다. common 블록은 모듈로 대체되었으므로 더는 나누지 않는다.

## 이름

원본은 변수 이름을 6자 안으로 쓰라고 했다. Fortran 77의 한계였고 지금은 이름이 63자까지 허용된다. 모범 사례의 권고는 다음과 같다.

- Fortran 키워드를 포함해 모두 소문자로 쓴다. Fortran은 대소문자를 구별하지 않는다.
- 수식에서 쓰는 변수는 수학 표기를 따라 짧게 쓴다.
- 나머지는 한두 단어로 줄이고, 단어가 더 필요하면 밑줄로 구분한다.
- 줄임말은 뜻이 하나로 읽힐 때만 쓴다. `spline_interp`는 괜찮지만 `splineint`는 `int`가 적분인지 정수인지 알 수 없다.

같은 대상은 프로그램 어디에서나 같은 이름으로 부른다.

## 들여쓰기와 end 뒤 이름

구문 안쪽은 일정한 칸 수로 들여 쓴다. 모범 사례는 두 칸, 세 칸, 네 칸을 모두 흔한 선택으로 소개한다. 이 가이드는 두 칸을 쓴다.

`end subroutine swap`처럼 `end` 뒤에 이름을 쓰면 읽는 사람이 어느 프로시저의 끝인지 알 수 있고, 컴파일러도 이름이 맞는지 검사한다.

<!-- file: ch18/end_name.f90 -->
```fortran
program end_name
  implicit none

  call hello()

contains

  subroutine hello()
    print '(a)', 'hello'
  end subroutine helo
end program end_name
```

`end subroutine helo`의 이름이 `hello`와 다르다. gfortran 15.2의 첫 메시지는 다음과 같다.

```text
end_name.f90:10:21:

   10 |   end subroutine helo
      |                     1
Error: Expected label ‘hello’ for END SUBROUTINE statement at (1)
```

## 함수에는 부작용을 두지 않는다

원본은 함수가 입력 인수의 값을 바꾸는 부작용을 갖지 않게 하고, 그런 일에는 서브루틴을 쓰라고 했다. 현대 Fortran에서는 `pure`를 붙여 이 약속을 컴파일러가 검사하게 한다. 표준은 순수 함수에서 포인터가 아닌 가인수가 모두 `intent(in)`이거나 `value` 속성을 가져야 한다고 정한다(제약 C1583, 15.7절). 다음 함수는 가인수를 바꾸려다 컴파일되지 않는다.

<!-- file: ch18/side_effect.f90 -->
```fortran
program side_effect
  implicit none
  real :: x

  x = 3.0
  print '(f6.1)', twice(x)

contains

  pure function twice(v) result(w)
    real, intent(in) :: v
    real :: w

    v = 2.0 * v
    w = v
  end function twice
end program side_effect
```

```text
side_effect.f90:14:5:

   14 |     v = 2.0 * v
      |     1~
Error: Dummy argument ‘v’ with INTENT(IN) in variable definition context (assignment) at (1)
```

결과가 하나이고 인수를 건드리지 않는 계산은 `pure` 함수로, 값을 둘 이상 돌려주거나 인수를 바꿔야 하는 일은 서브루틴으로 쓴다. 앞의 `statistics` 모듈의 `mean`과 `variance`가 순수 함수의 예다.

## 전역 상태를 줄인다

원본은 common 블록을 줄이라고 했다. 모듈 변수가 common 블록의 자리를 이어받았으므로 같은 주의가 필요하다. 모듈의 선언부에 쓴 변수는 `save` 속성을 암시적으로 가져서 프로그램이 끝날 때까지 값이 남는다(Fortran 2018 8.5.16절). 어느 프로시저든 그 값을 읽고 바꿀 수 있으면 프로시저의 결과가 인수만으로 정해지지 않는다. 함수를 따로 시험하기도 어렵다.

모범 사례는 모듈 변수를 이름 붙은 상수(`parameter`)로 제한하거나, 바뀌는 값은 `protected`로 내놓으라고 한다. 이 가이드는 값을 인수로 넘기고, 함께 다니는 값은 파생 타입([17장](/fortran/17-derived-types/))으로 묶는 방법을 권한다. 옛 코드의 common 블록은 [부록 A](/fortran/21-legacy-code/)에서 읽는 법만 다룬다.

## goto 대신 구문

원본은 `while`이 표준이 아니어서 `goto`로 반복을 만들어야 한다고 했다. Fortran 90 이후에는 `do while`, `exit`, `cycle`, `select case`가 있으므로 `goto`가 필요한 곳이 없다. 원본의 2의 거듭제곱 예제와 until 반복은 다음과 같이 쓴다.

<!-- file: ch18/no_goto.f90 -->
```fortran
program no_goto
  implicit none
  integer :: n

  n = 1
  do while (n <= 100)
    print '(i4)', n
    n = 2 * n
  end do

  do
    n = n - 50
    if (n <= 0) exit
  end do
  print '(a, i4)', 'n =', n
end program no_goto
```

<!-- output: ch18/no_goto.out -->
```text
   1
   2
   4
   8
  16
  32
  64
n = -22
```

두 반복문의 문법은 [9장](/fortran/09-loops/)에서 다룬다. `goto`로 만든 반복문을 읽어야 할 때는 [부록 A](/fortran/21-legacy-code/)를 본다.

## 큰 배열은 한곳에서 할당한다

원본은 큰 배열을 주 프로그램에 선언해서 부프로그램에 넘기고, 선행 차원도 함께 넘기라고 했다. 할당 가능 배열과 가정 형상 배열을 쓰면 이 두 지침이 한 번에 해결된다. 배열을 `allocate`로 한 번 만들고, 가정 형상 배열(`a(:, :)`)을 받는 프로시저에 넘기면 배열의 크기가 함께 전달되므로 선행 차원을 따로 넘기지 않는다.

<!-- file: ch18/allocate_once.f90 -->
```fortran
module matrices
  implicit none
contains
  subroutine set_identity(a)
    real, intent(out) :: a(:, :)
    integer :: i

    a = 0.0
    do i = 1, min(size(a, 1), size(a, 2))
      a(i, i) = 1.0
    end do
  end subroutine set_identity
end module matrices

program allocate_once
  use matrices, only: set_identity
  implicit none
  integer, parameter :: n = 1000
  real, allocatable :: a(:, :)

  allocate (a(n, n))
  call set_identity(a)
  print '(a, i0, a, f7.1)', 'elements = ', size(a), ', sum = ', sum(a)
end program allocate_once
```

<!-- output: ch18/allocate_once.out -->
```text
elements = 1000000, sum =  1000.0
```

`set_identity`는 `size(a, 1)`로 크기를 알아낸다. 크기가 상수인 지역 배열은 gfortran이 기본값 65536바이트를 넘으면 스택 대신 정적 메모리에 둔다(`-fmax-stack-var-size`). 큰 배열은 이렇게 한곳에서 할당하면 크기를 프로그램 한 군데에서만 정하게 된다. 선행 차원을 직접 넘겨야 하는 라이브러리 호출은 [20장](/fortran/20-blas-lapack/)에서 다룬다.

## 열 우선 순서에 맞춘 반복 순서

원본은 이중 반복문에서 첫째 첨자를 안쪽 반복에 두라고 했다. Fortran은 배열을 열 우선 순서(column-major order)로 저장하므로 첫째 첨자가 가장 빨리 변하는 순서로 원소가 놓인다(Fortran 2018 9.5.3.2절, 표 9.1). 전체 배열을 출력하면 이 순서로 나온다.

<!-- file: ch18/loop_order.f90 -->
```fortran
program loop_order
  implicit none
  integer, parameter :: n = 2, m = 3
  integer :: a(n, m), b(n, m)
  integer :: i, j

  do j = 1, m
    do i = 1, n
      a(i, j) = 10 * i + j
    end do
  end do

  do i = 1, n
    do j = 1, m
      b(i, j) = 10 * i + j
    end do
  end do

  print '(6i4)', a
  print '(l1)', all(a == b)
end program loop_order
```

<!-- output: ch18/loop_order.out -->
```text
  11  21  12  22  13  23
T
```

`a(i, j) = 10 * i + j`로 채운 배열을 출력하면 `11 21 12 22 13 23`이다. 첫째 첨자 `i`가 먼저 변한다. 첫 번째 반복문은 `i`가 안쪽이어서 메모리를 처음부터 차례대로 쓰고, 두 번째는 `j`가 안쪽이어서 한 번에 `n`칸씩 건너뛴다. 결과는 `all(a == b)`가 참으로 같다. 배열이 작으면 차이가 보이지 않지만 큰 배열에서는 건너뛰는 접근이 느려진다. 모범 사례도 다차원 배열은 연속한 메모리를 차례로 접근하라고 권한다.

## 주석보다 이름

원본은 부프로그램마다 머리말 주석으로 입출력 인수를 설명하라고 했다. 지금은 가인수의 `intent`와 이름, 명시적 인터페이스가 그 정보 대부분을 컴파일러가 검사하는 형태로 전달한다. 주석은 코드가 말하지 못하는 것, 곧 왜 이렇게 했는지와 수식의 출처에만 쓴다. 주석은 코드가 바뀌어도 그대로 남아서 거짓이 되기 쉽다.

```text
x = x + 1    ! x에 1을 더한다
```

이런 주석은 아무것도 더하지 않는다. 대신 `x`를 `count`처럼 알아볼 수 있는 이름으로 바꾼다. 모범 사례는 모듈과 프로시저 머리에 목적을 적는 짧은 주석을 권한다. 이 가이드의 예제에는 주석을 달지 않고 설명을 본문에 썼다.

## 흔한 실수

- `-std=f2018` 없이 컴파일해서 GNU 확장이 섞인 코드가 표준 코드인 줄 안다.
- 모듈 변수에 프로시저 사이의 상태를 저장하고, 호출 순서에 따라 결과가 달라지는 코드를 쓴다.
- 함수에서 가인수를 바꾼다. `pure`와 `intent(in)`을 쓰면 컴파일러가 막는다.
- `end` 뒤의 이름을 복사해서 붙이고 고치지 않는다. 이름이 어긋나면 컴파일 오류가 난다.
- 반복문의 순서를 첨자 순서와 반대로 쓴다. 결과는 같지만 큰 배열에서 느려진다.
