---
title: 부프로그램
order: 11
permalink: /fortran/11-subprograms/
---

이 장에서는 프로그램을 함수와 서브루틴으로 나누는 방법을 다룬다. 모듈 안에 프로시저를 두어 명시적 인터페이스를 얻는 방식을 기본으로 삼고, `intent`, 인수 결합, 내부 프로시저, 재귀를 설명한다.

## 부프로그램

몇백 줄이 넘는 프로그램은 읽기 어렵다. 풀어야 할 문제를 작은 부분 문제로 나누고, 각 부분 문제를 부프로그램(subprogram) 하나가 맡게 한다. 같은 부분 문제를 서로 다른 데이터로 여러 번 풀어야 할 때도 코드를 복사하지 않고 부프로그램을 여러 번 부른다.

부프로그램은 두 종류다. 함수(function)는 값 하나를 돌려주고 식 안에서 쓴다. 서브루틴(subroutine)은 값을 돌려주지 않거나 여러 개를 돌려주고 `call` 문으로 부른다. 함수와 서브루틴을 통틀어 프로시저(procedure)라고 부른다.

## 내장 함수

Fortran에는 내장 함수(intrinsic function)가 많이 들어 있다. 자주 쓰는 것은 다음과 같다.

| 이름 | 뜻 |
|---|---|
| `abs(x)` | 절댓값 |
| `min(a, b, ...)`, `max(a, b, ...)` | 최솟값, 최댓값 |
| `sqrt(x)` | 제곱근 |
| `sin(x)`, `cos(x)`, `tan(x)` | 삼각함수 (라디안) |
| `atan(x)`, `atan2(y, x)` | 아크탄젠트, 점 (x, y)의 각도 |
| `exp(x)`, `log(x)` | 지수 함수, 자연로그 |

원본은 `cos(pi/3.0)` 예에서 Fortran 77에는 내장 상수가 없어 `pi`를 직접 정의해야 한다고 했다. Fortran 2018 표준에도 `pi` 같은 내장 상수는 없다. 필요하면 `acos(-1.0)`이나 `4.0 * atan(1.0)`으로 얻는다.

이 함수들은 인수의 타입과 kind에 따라 알맞은 버전이 자동으로 선택된다. 이를 일반(generic) 함수라고 한다. `sqrt` 하나로 단정밀도와 배정밀도를 모두 받으므로 kind마다 다른 이름을 쓸 필요가 없다. `dsqrt` 같은 특정 이름은 폐기 예정 기능(obsolescent feature)이다(부속서 B.3.12). 결과의 kind는 인수의 kind와 같다.

<!-- file: ch11/intrinsics.f90 -->
```fortran
program intrinsics
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  real :: x
  real(dp) :: y

  x = 2.0
  y = 2.0_dp
  print '(a, f10.7)', 'sqrt single: ', sqrt(x)
  print '(a, f18.15)', 'sqrt double: ', sqrt(y)
  print '(a, f10.7)', 'atan2(1, 1): ', atan2(1.0, 1.0)
  print '(a, 3i4)', 'abs min max: ', abs(-3), min(4, 2, 7), max(4, 2, 7)
end program intrinsics
```

<!-- output: ch11/intrinsics.out -->
```text
sqrt single:  1.4142135
sqrt double:  1.414213562373095
atan2(1, 1):  0.7853982
abs min max:    3   2   7
```

`2.0_dp`의 `_dp`는 상수의 kind 매개변수(kind type parameter)이고 `dp`는 `iso_fortran_env` 모듈의 `real64`에 붙인 새 이름이다. kind는 [5장](../05-variables/)에서, `use`의 `=>`는 [16장](../16-modules/)에서 설명한다. 단정밀도 `sqrt(2.0)`은 일곱 자리 남짓, 배정밀도는 열다섯 자리 남짓까지 맞는다.

`atan2(y, x)`는 복소수 (x, y)의 편각을 라디안으로 돌려주며 범위는 -π에서 π까지다. `atan(y/x)`와 달리 두 인수의 부호로 사분면을 정하고 `x`가 0이어도 쓸 수 있다. 둘 다 0이면 안 된다(Fortran 2018 16.9.18).

## 함수 만들기

원본의 예제는 강수량 모델이다. 월 `m`과 지역 매개변수 `t`로 그 달의 강수량 `r(m, t)`를 구하고, 1월부터 12월까지 더해 연 강수량을 얻는다. 식은 다음과 같다.

```text
r(m, t) = t/10 * (m**2 + 14*m + 46)   (이 값이 양수일 때)
r(m, t) = 0                           (그 밖의 경우)
```

현대 Fortran에서는 함수를 모듈 안의 `contains` 뒤에 둔다. 이렇게 만든 모듈 프로시저(module procedure)는 `use`로 불러 쓰며, 컴파일러가 가인수의 타입과 개수를 호출마다 검사한다. 이 정보를 명시적 인터페이스(explicit interface)라고 한다.

<!-- file: ch11/rain.f90 -->
```fortran
module rain_model
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
contains
  function monthly_rain(m, t) result(r)
    integer, intent(in) :: m
    real(dp), intent(in) :: t
    real(dp) :: r

    r = 0.1_dp * t * (m**2 + 14*m + 46)
    if (r < 0.0_dp) r = 0.0_dp
  end function monthly_rain
end module rain_model

program rain
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use rain_model, only: monthly_rain
  implicit none
  real(dp) :: t, total
  integer :: m

  read (*, *) t
  total = 0.0_dp
  do m = 1, 12
    total = total + monthly_rain(m, t)
  end do
  print '(a, f9.2, a)', 'Annual rainfall is ', total, ' inches'
end program rain
```

`1.5`를 입력하면 다음과 같이 출력한다.

<!-- output: ch11/rain.out -->
```text
Annual rainfall is    344.10 inches
```

함수의 모양은 다음과 같다.

- `function 이름(가인수 목록) result(결과 변수)`로 시작하고 `end function 이름`으로 끝난다.
- 결과는 `result` 절에 적은 변수에 대입해 돌려준다. 이 예제의 `r`이다. 결과 변수는 함수 안에서 읽을 수도 있어서 `if (r < 0.0_dp)`처럼 쓸 수 있다.
- 결과 변수의 타입은 함수 본문에서 선언한다. `real(dp) :: r`이다.
- `return`은 필요 없다. 함수 중간에서 빠져나갈 때만 쓴다.

원본은 호출하는 쪽에서도 `real r`처럼 함수의 타입을 선언해야 하고, 선언하지 않으면 암시적 타입 지정으로 틀린 타입이 되기 쉽다고 했다. 모듈 프로시저는 `use`만 하면 타입 정보가 따라오므로 이 문제가 없다.

모듈은 `program`보다 앞에 둔다. 모듈 안의 `implicit none`은 그 모듈의 프로시저에도 적용된다. `use rain_model, only: monthly_rain`의 `only:`는 가져올 이름을 한정한다.

## 서브루틴

함수는 값 하나만 돌려준다. 값을 여러 개 돌려주거나 아무것도 돌려주지 않는 일은 서브루틴이 맡는다. 서브루틴은 타입이 없고, `call 이름(실인수 목록)`으로 부른다. 원본의 `iswap`은 두 정수의 값을 맞바꾼다.

<!-- file: ch11/iswap.f90 -->
```fortran
module swap_mod
  implicit none
contains
  subroutine iswap(a, b)
    integer, intent(inout) :: a, b
    integer :: tmp

    tmp = a
    a = b
    b = tmp
  end subroutine iswap
end module swap_mod

program callex
  use swap_mod, only: iswap
  implicit none
  integer :: m, n

  m = 1
  n = 2
  call iswap(m, n)
  print '(2i3)', m, n
end program callex
```

<!-- output: ch11/iswap.out -->
```text
  2  1
```

`a`와 `b`는 `iswap`이 받는 가인수(dummy argument)이고, 호출하는 `call iswap(m, n)`의 `m`과 `n`은 실인수(actual argument)다. `tmp`는 서브루틴 안에서만 쓰는 지역 변수다. 다른 프로시저에 같은 이름의 변수가 있어도 서로 다른 변수다.

## intent

가인수가 데이터를 받는지, 돌려주는지, 둘 다인지를 `intent` 속성으로 적는다.

| 속성 | 뜻 |
|---|---|
| `intent(in)` | 입력만 받는다. 프로시저 안에서 값을 바꿀 수 없다. |
| `intent(out)` | 결과를 돌려준다. 호출될 때 값이 정해지지 않은 상태가 된다. |
| `intent(inout)` | 값을 받아 바꾼 뒤 돌려준다. |

원본은 입력용 가인수를 지역 변수처럼 쓰다가 호출한 쪽의 값이 뜻하지 않게 바뀌는 일을 조심하라고 했다. `intent(in)`은 이를 컴파일러가 막게 한다.

<!-- file: ch11/polar.f90 -->
```fortran
module convert
  implicit none
contains
  subroutine to_polar(x, y, r, theta)
    real, intent(in) :: x, y
    real, intent(out) :: r, theta

    r = sqrt(x**2 + y**2)
    theta = atan2(y, x)
  end subroutine to_polar
end module convert

program polar
  use convert, only: to_polar
  implicit none
  real :: r, theta

  call to_polar(1.0, 1.0, r, theta)
  print '(a, f7.4)', 'r     = ', r
  print '(a, f7.4)', 'theta = ', theta
end program polar
```

<!-- output: ch11/polar.out -->
```text
r     =  1.4142
theta =  0.7854
```

`intent(in)` 가인수에 대입하면 컴파일 오류다.

<!-- file: ch11/intent_error.f90 -->
```fortran
module bad_mod
  implicit none
contains
  subroutine double_it(a)
    integer, intent(in) :: a

    a = 2 * a
  end subroutine double_it
end module bad_mod
```

gfortran 15.2는 다음 메시지를 낸다.

```text
intent_error.f90:7:5:

    7 |     a = 2 * a
      |     1~
Error: Dummy argument ‘a’ with INTENT(IN) in variable definition context (assignment) at (1)
```

실인수도 검사한다. `intent(out)`이나 `intent(inout)` 가인수에는 값을 바꿀 수 있는 변수만 줄 수 있다. `iswap`의 첫째 실인수에 상수를 주면 컴파일 오류다. `iswap`을 정의한 모듈은 앞의 예제와 같다.

<!-- file: ch11/literal_error.f90 -->
```fortran
module swap_mod
  implicit none
contains
  subroutine iswap(a, b)
    integer, intent(inout) :: a, b
    integer :: tmp

    tmp = a
    a = b
    b = tmp
  end subroutine iswap
end module swap_mod

program literal_error
  use swap_mod, only: iswap
  implicit none
  integer :: n

  n = 2
  call iswap(1, n)
end program literal_error
```

```text
literal_error.f90:20:13:

   20 |   call iswap(1, n)
      |             1
Error: Non-variable expression in variable definition context (actual argument to INTENT = OUT/INOUT) at (1)
```

표준은 `intent(in)` 가인수가 변수 정의 문맥에 나타나면 안 된다고 정한다(Fortran 2018 8.5.10 C844). 컴파일러는 이를 어기는 문장을 오류로 알려 준다. 모든 가인수에 `intent`를 쓰는 습관을 들인다.

## 인수 결합

원본은 Fortran이 call-by-reference라서 주소가 넘어간다고 설명했다. Fortran 표준은 그런 전달 방식을 정하지 않는다. 표준은 가인수와 실인수의 결합(argument association)으로 정의한다. 프로시저를 실행하는 동안 가인수는 실인수와 결합하며, 결합한 실인수가 있는 변수라면 가인수를 바꾸는 것은 곧 그 변수를 바꾸는 것이다(15.5.2.3). 표준은 이를 "보통 call by reference나 call by value-result와 비슷하다"고 설명하되 실제 방법은 컴파일러가 정한다고 덧붙인다(15.5.2.3 NOTE 2). 그래서 이 가이드는 "주소가 넘어간다"고 쓰지 않고, 가인수가 실인수와 결합해 같은 값을 가리킨다고 쓴다.

실용적으로 이렇게 이해하면 된다.

- 가인수에 대입하면 호출한 쪽의 변수가 바뀔 수 있다. `iswap`이 그런 경우다.
- 가인수와 결합한 변수는 프로시저가 실행되는 동안 그 가인수를 통해서만 바꿀 수 있다. 같은 변수를 다른 경로(예를 들어 모듈 변수)로 바꾸면 표준을 어기며 결과는 정해져 있지 않다(15.5.2.13).

값만 필요하고 호출한 쪽의 변수는 건드리지 않을 가인수에는 `value` 속성을 쓸 수 있다. 가인수는 실인수의 값을 복사한 임시 변수와 결합한 것처럼 동작한다(8.5.18, 15.5.2.3). 입력만 받는 가인수에는 보통 `intent(in)`을 쓴다. `value`는 가인수를 지역 변수처럼 바꿔 쓰고 싶을 때 쓴다.

<!-- file: ch11/by_value.f90 -->
```fortran
module value_mod
  implicit none
contains
  subroutine bump(a, b)
    integer, intent(inout) :: a
    integer, value :: b

    a = a + 1
    b = b + 1
  end subroutine bump
end module value_mod

program by_value
  use value_mod, only: bump
  implicit none
  integer :: i, j

  i = 10
  j = 20
  call bump(i, j)
  print '(2i4)', i, j
end program by_value
```

<!-- output: ch11/by_value.out -->
```text
  11  20
```

`b`는 `value` 가인수라 `bump` 안에서 바꿔도 `j`는 `20`으로 남는다.

## 명시적 인터페이스

프로시저를 부르는 쪽이 가인수의 타입, 차원 수, 속성을 알아야 검사할 수 있다. 이 정보가 보이는 것이 명시적 인터페이스이고, 보이지 않으면 암시적 인터페이스(implicit interface)다. 부르는 쪽에서 가인수 선언을 알 수 없으면 컴파일러가 호출을 검사하지 못하므로 인수 개수나 타입을 잘못 줘도 그대로 컴파일되어 틀린 결과로 이어질 수 있다.

다음 프로시저는 반드시 명시적 인터페이스가 있어야 한다(15.4.2.2).

- 가정 형상 배열, `allocatable`, `optional`, `pointer`, `target`, `value` 가인수가 있는 프로시저
- 결과가 배열이거나 `allocatable`인 함수
- `elemental` 프로시저
- 인수 키워드(`call f(x=1.0)`)로 부르는 프로시저
- `pure`여야 하는 문맥에서 쓰는 프로시저

모듈 프로시저와 내부 프로시저는 정의 자체가 명시적 인터페이스다. 그래서 이 가이드는 프로시저를 항상 모듈 안에 둔다.

## 내부 프로시저와 호스트 연관

주 프로그램이나 다른 프로시저 안의 `contains` 뒤에도 프로시저를 둘 수 있다. 이를 내부 프로시저(internal procedure)라고 한다. 내부 프로시저는 바깥 프로그램 단위의 변수를 그대로 볼 수 있다. 이것이 호스트 연관(host association)이다.

<!-- file: ch11/internal.f90 -->
```fortran
program internal
  implicit none
  real :: radius

  radius = 2.0
  print '(a, f8.3)', 'area:          ', area()
  radius = 3.0
  print '(a, f8.3)', 'area:          ', area()
  print '(a, f8.3)', 'circumference: ', circumference(radius)

contains

  function area() result(a)
    real :: a

    a = 3.14159 * radius**2
  end function area

  function circumference(r) result(c)
    real, intent(in) :: r
    real :: c

    c = 2.0 * 3.14159 * r
  end function circumference
end program internal
```

<!-- output: ch11/internal.out -->
```text
area:            12.566
area:            28.274
circumference:   18.850
```

`area`는 가인수가 없고 호스트의 `radius`를 읽는다. `radius`를 바꾼 뒤 다시 부르면 다른 값을 낸다. `circumference`는 같은 계산을 가인수로 받는다. 짧은 보조 계산을 한곳에 묶을 때는 내부 프로시저가 편하다. 하지만 호스트의 변수를 읽는 프로시저는 이름만 봐서는 무엇에 의존하는지 보이지 않으므로, 여러 곳에서 쓰는 프로시저는 모듈에 두고 필요한 값을 인수로 받게 한다.

## 재귀

프로시저가 자기 자신을 부르는 것을 재귀(recursion)라고 한다. Fortran 2018부터는 프로시저가 기본적으로 재귀 가능하다. 이전 표준에서는 `recursive` 접두어를 붙여야 했고, 2018에서 `recursive`가 기본이 되면서 반대로 재귀가 아님을 알리는 `non_recursive`가 새로 생겼다(WG5 N2161 5.26).

<!-- file: ch11/factorial.f90 -->
```fortran
module factorial_mod
  implicit none
contains
  recursive function factorial(n) result(f)
    integer, intent(in) :: n
    integer :: f

    if (n <= 1) then
      f = 1
    else
      f = n * factorial(n - 1)
    end if
  end function factorial
end module factorial_mod

program factorial_demo
  use factorial_mod, only: factorial
  implicit none
  integer :: n

  do n = 1, 6
    print '(i2, a, i4)', n, '! = ', factorial(n)
  end do
end program factorial_demo
```

<!-- output: ch11/factorial.out -->
```text
 1! =    1
 2! =    2
 3! =    6
 4! =   24
 5! =  120
 6! =  720
```

이 가이드는 재귀 프로시저에 `recursive`를 계속 쓴다. 2018 이전 표준만 지원하는 컴파일러에서도 컴파일되고, 읽는 사람에게 의도를 알려 준다. gfortran 매뉴얼은 `recursive`가 붙지 않은 프로시저의 큰 지역 배열은 정적 메모리에 둘 수 있다고 하고(`-fmax-stack-var-size`), `recursive`가 없는 프로시저를 재귀로 부르려면 `-frecursive`를 쓰라고 안내한다. `recursive`를 붙이면 이런 옵션을 따로 신경 쓸 필요가 없다. 원본이 Fortran 77에서 재귀를 허용하지 않는다고 한 것은 이전 표준의 상황이다.

## pure와 elemental

`pure` 프로시저는 부작용이 없음을 컴파일러가 확인해 주는 프로시저다. `pure` 함수의 가인수는 모두 `intent(in)`(또는 `value`)이어야 하고, 호스트나 모듈의 변수를 바꾸거나 `print`나 장치 번호를 쓰는 `read`와 `write`를 쓸 수 없으며, 안에서 부르는 프로시저도 `pure`여야 한다(15.7). `elemental` 프로시저는 스칼라 가인수만 받지만 배열 실인수로 부를 수 있고, 배열의 각 원소에 적용된다. `impure`를 붙이지 않은 `elemental` 프로시저는 `pure`이기도 하다(15.7, 15.8.1).

<!-- file: ch11/pure_elemental.f90 -->
```fortran
module shapes
  implicit none
contains
  pure function hypotenuse(a, b) result(c)
    real, intent(in) :: a, b
    real :: c

    c = sqrt(a**2 + b**2)
  end function hypotenuse

  elemental function clamp(x, lo, hi) result(y)
    real, intent(in) :: x, lo, hi
    real :: y

    y = min(max(x, lo), hi)
  end function clamp
end module shapes

program pure_elemental
  use shapes, only: hypotenuse, clamp
  implicit none
  real :: v(5)

  v = [-2.0, 0.5, 1.0, 3.5, 7.0]
  print '(a, f6.2)', 'hypotenuse: ', hypotenuse(3.0, 4.0)
  print '(5f6.1)', clamp(v, 0.0, 4.0)
end program pure_elemental
```

<!-- output: ch11/pure_elemental.out -->
```text
hypotenuse:   5.00
   0.0   0.5   1.0   3.5   4.0
```

`clamp(v, 0.0, 4.0)`은 `v`의 원소마다 `clamp`를 부르고 같은 형상의 결과를 만든다. 스칼라 `lo`와 `hi`는 모든 원소에 같이 쓰인다.

`pure` 함수 안에 `print`를 넣으면 컴파일 오류다.

<!-- file: ch11/pure_error.f90 -->
```fortran
module noisy
  implicit none
contains
  pure function square(x) result(y)
    real, intent(in) :: x
    real :: y

    y = x * x
    print *, 'squaring', x
  end function square
end module noisy
```

```text
pure_error.f90:9:26:

    9 |     print *, 'squaring', x
      |                          1
Error: PRINT statement at (1) not allowed within PURE procedure
```

위는 gfortran 15.2의 메시지다.

## 함수의 부작용

함수는 식 안에서 부르므로 호출 순서와 횟수를 프로그래머가 정하지 못한다. 표준은 값을 다른 방법으로 알 수 있으면 식의 피연산자를 모두 평가하지 않아도 된다고 허용한다. `x > y .or. g(z)`에서 `x > y`이면 `g(z)`는 불리지 않을 수 있고, 그때 `g`가 바꿀 수 있었던 변수는 정해지지 않은 값이 된다(10.1.7). 함수가 인수나 모듈 변수를 바꾸거나 화면에 출력하면 결과가 컴파일러와 최적화에 따라 달라질 수 있다. 값을 계산해 돌려주는 일만 하는 함수는 `pure`로 만들고, 인수를 바꾸거나 값을 여러 개 돌려줘야 하는 일은 서브루틴으로 쓴다.

## 외부 프로시저와 인터페이스 블록

모듈이나 `contains` 밖에 따로 선언된 프로시저를 외부 프로시저(external procedure)라고 한다. 옛 코드와 다른 언어로 만든 라이브러리가 이 형태다. 부르는 쪽에는 정의가 보이지 않으므로 기본적으로 암시적 인터페이스가 된다. 명시적 인터페이스를 주려면 호출하는 쪽에 인터페이스 블록(interface block)으로 가인수를 다시 적는다.

<!-- file: ch11/external.f90 -->
```fortran
program external_demo
  implicit none
  interface
    function cube(x) result(y)
      real, intent(in) :: x
      real :: y
    end function cube
  end interface

  print '(f6.1)', cube(3.0)
end program external_demo

function cube(x) result(y)
  implicit none
  real, intent(in) :: x
  real :: y

  y = x**3
end function cube
```

<!-- output: ch11/external.out -->
```text
  27.0
```

인터페이스 블록의 내용이 실제 프로시저와 어긋나도 컴파일러는 알지 못한다. 그래서 새 코드는 외부 프로시저 대신 모듈 프로시저를 쓰고, 인터페이스 블록은 이미 컴파일된 외부 라이브러리를 부를 때 쓴다. [20장](../20-blas-lapack/)에서 BLAS와 LAPACK을 부를 때 다시 나온다.

## 흔한 실수

- `intent`를 빼먹는다. 입력용 가인수를 실수로 바꿔도 컴파일러가 알려 주지 않는다.
- 함수를 `call`로 부르거나 서브루틴을 식 안에서 부른다. 함수는 식 안에서, 서브루틴은 `call`로 부른다.
- 모듈 밖에 프로시저를 두고 인터페이스 없이 부른다. 인수 개수나 타입이 틀려도 컴파일되고 실행 중에 엉뚱한 값이 나온다.
- 같은 변수를 두 번째 가인수와 모듈 변수로 동시에 바꾼다. 15.5.2.13의 제한을 어기는 코드다.
- 결과 변수에 값을 대입하지 않고 함수를 끝낸다. `if`의 한쪽 가지에서만 대입하면 컴파일러가 알려 주지 않는 채 결과가 정해지지 않은 값이 된다.
