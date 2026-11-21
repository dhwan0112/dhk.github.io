---
title: 모듈로 데이터 공유하기
order: 16
permalink: /fortran/16-modules/
---

이 장에서는 여러 프로시저가 같은 데이터를 쓰게 하는 방법으로 모듈 변수를 다룬다. `use`와 `only`, 이름 바꾸기, `private`, `public`, `protected`, 그리고 모듈의 컴파일 순서를 설명한다.

## 모듈 변수

원본은 `alpha`와 `beta`를 여러 서브루틴이 함께 쓰는 예를 보이며 `common` 블록으로 해결했다. 현대 Fortran에서는 모듈의 선언부에 변수를 선언하고, 그 값을 쓰려는 프로그램 단위가 `use`로 가져온다. 이것이 use 연관(use association)이다.

<!-- file: ch16/coeff.f90 -->
```fortran
module coefficients
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  real(dp) :: alpha = 1.0_dp
  real(dp) :: beta = 0.0_dp
end module coefficients

module models
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use coefficients, only: alpha, beta
  implicit none
contains
  function line(x) result(y)
    real(dp), intent(in) :: x
    real(dp) :: y

    y = alpha * x + beta
  end function line

  function parabola(x) result(y)
    real(dp), intent(in) :: x
    real(dp) :: y

    y = alpha * x**2 + beta * x
  end function parabola
end module models

program coeff
  use coefficients, only: alpha, beta
  use models, only: line, parabola
  implicit none

  alpha = 2.0d0
  beta = 1.0d0
  print '(2f8.2)', line(3.0d0), parabola(3.0d0)
  beta = -1.0d0
  print '(2f8.2)', line(3.0d0), parabola(3.0d0)
end program coeff
```

<!-- output: ch16/coeff.out -->
```text
    7.00   21.00
    5.00   15.00
```

`coefficients` 모듈이 `alpha`와 `beta`를 가지고, `models` 모듈의 함수 `line`과 `parabola`와 주 프로그램이 이를 `use`한다. 주 프로그램이 `alpha`와 `beta`를 바꾸면 두 함수가 바뀐 값을 쓴다. 두 프로그램 단위가 같은 변수를 공유하므로 `call`에 인수로 넘기지 않아도 된다.

선언에 초기값(`= 1.0_dp`)을 줄 수 있고, 값이 바뀌지 않는 값은 `parameter` 속성으로 이름 붙은 상수(named constant)를 만든다. 모듈 변수는 프로그램이 실행되는 동안 값을 유지한다. 표준은 모듈에서 선언한 변수가 암시적으로 `save` 속성을 가진다고 정한다(Fortran 2018 8.5.16). 이 규칙은 Fortran 2008에서 들어왔다(WG5 N1891 10.1). 표준은 명시한 `save`가 이 속성을 확인하는 것이라고 설명하므로, 옛 코드에서 모듈 변수에 `save`가 붙어 있으면 같은 뜻으로 읽으면 된다. 새 코드에서는 `save`를 쓰지 않아도 된다.

## use와 only

`use 모듈`만 쓰면 그 모듈의 공개된 이름을 모두 가져온다(14.2.2). `use 모듈, only: 이름 목록`은 목록의 이름만 가져온다. 이 가이드는 `only`를 항상 쓴다. 이름이 어디서 왔는지 `use` 문에서 바로 보이고, 모듈에 이름이 새로 생겨도 내 프로그램의 이름과 부딪치지 않는다.

두 모듈이 같은 이름을 내보낼 때는 `이름 => 원래 이름`으로 새 이름을 붙인다. 같은 이름이 서로 다른 개체를 가리키는 채로 쓰면 오류다(14.2.2).

<!-- file: ch16/rename.f90 -->
```fortran
module fluid_props
  implicit none
  real, parameter :: density = 1000.0
  real, parameter :: viscosity = 1.0e-3
end module fluid_props

module solid_props
  implicit none
  real, parameter :: density = 7800.0
end module solid_props

program rename
  use fluid_props, only: water_density => density
  use solid_props, only: steel_density => density
  implicit none

  print '(a, f7.1)', 'water: ', water_density
  print '(a, f7.1)', 'steel: ', steel_density
  print '(a, f5.2)', 'ratio: ', steel_density / water_density
end program rename
```

<!-- output: ch16/rename.out -->
```text
water:  1000.0
steel:  7800.0
ratio:  7.80
```

`water_density`와 `steel_density`는 각각 `fluid_props`와 `solid_props`의 `density`다. `fluid_props`의 `viscosity`는 가져오지 않았다. 새 이름은 `use`를 쓴 프로그램 단위 안에서만 유효하다. 이름 바꾸기는 [11장](../11-subprograms/)의 `dp => real64`에서도 썼다.

## 공개 범위와 보호

모듈의 이름은 기본적으로 모두 공개(public)이고, `private` 문 하나로 이 기본을 비공개(private)로 바꿀 수 있다(8.5.2). 그런 다음 밖에 내보낼 이름만 `public ::`으로 적는다. 모듈 밖에서 보이지 않아야 하는 보조 변수와 프로시저를 감추는 방법이다. 모듈의 내용을 바꿔도 `public` 목록의 이름만 지키면 쓰는 쪽 코드가 깨지지 않는다.

`protected` 속성은 변수를 읽기만 하도록 내보낸다. 모듈 밖에서 `use`로 가져온 `protected` 변수는 값을 바꿀 수 없고, 바꿀 수 있는 곳은 모듈 안뿐이다(8.5.15).

<!-- file: ch16/counter.f90 -->
```fortran
module counter
  implicit none
  private
  public :: calls, record_call, last_call
  integer, protected :: calls = 0
  integer :: last_value = -1
contains
  subroutine record_call(value)
    integer, intent(in) :: value

    calls = calls + 1
    last_value = value
  end subroutine record_call

  function last_call() result(v)
    integer :: v

    v = last_value
  end function last_call
end module counter

program counter_demo
  use counter, only: calls, record_call, last_call
  implicit none

  call record_call(10)
  call record_call(20)
  call record_call(30)
  print '(a, i0, a, i0)', 'calls: ', calls, '  last: ', last_call()
end program counter_demo
```

<!-- output: ch16/counter.out -->
```text
calls: 3  last: 30
```

`calls`는 `protected`이므로 `counter_demo`는 값을 읽을 수만 있고, `record_call`을 불러야 `calls`가 늘어난다. `last_value`는 `private` 문 때문에 비공개이고 `last_call` 함수로만 읽는다. `calls`는 세 번의 `call`에 걸쳐 값이 유지된다. 모듈 변수가 `save` 속성을 가지기 때문이다.

`protected` 변수에 밖에서 대입하면 컴파일 오류다.

<!-- file: ch16/protected_error.f90 -->
```fortran
module counter
  implicit none
  integer, protected :: calls = 0
end module counter

program protected_error
  use counter, only: calls
  implicit none

  calls = 0
end program protected_error
```

gfortran 15.2의 메시지는 다음과 같다.

```text
protected_error.f90:10:3:

   10 |   calls = 0
      |   1~~~~~
Error: Variable ‘calls’ is PROTECTED and cannot appear in a variable definition context (assignment) at (1)
```

비공개 이름을 밖에서 쓰려는 경우도 오류다. 다음은 `use counter`로 가져오려 했지만 `last_value`가 비공개라서 보이지 않는다.

<!-- file: ch16/private_error.f90 -->
```fortran
module counter
  implicit none
  private
  public :: calls
  integer :: calls = 0
  integer :: last_value = -1
end module counter

program private_error
  use counter
  implicit none

  print *, last_value
end program private_error
```

```text
private_error.f90:13:21:

   13 |   print *, last_value
      |                     1
Error: Symbol ‘last_value’ at (1) has no IMPLICIT type
```

`last_value`가 보이지 않으므로 컴파일러는 이를 선언 없는 이름으로 취급한다. 위는 gfortran 15.2의 메시지다.

## 공유 상태를 줄이기

원본은 `common` 블록의 예를 보인 뒤, 이 예의 `alpha`와 `beta`는 인수로 넘길 수도 있으며 `common` 블록은 가능하면 피하라고 했다. 모듈 변수에도 같은 말이 맞다. 모듈 변수는 `common`보다 안전하지만 여러 프로시저가 읽고 쓰는 공유 상태라는 점은 같다.

- 프로시저를 부르는 식만 봐서는 어떤 값에 의존하는지 보이지 않는다. `line(3.0d0)`의 결과가 `alpha`와 `beta`를 누가 마지막에 바꿨는지에 달려 있다.
- 같은 함수를 서로 다른 매개변수로 한 식에서 부르려면 부르기 전에 모듈 변수를 매번 바꿔 줘야 한다.
- 프로시저를 따로 시험하기 어렵다. 시험하려면 먼저 모듈 변수를 정해 줘야 한다.
- 가인수는 `intent`로 읽기와 쓰기를 알린다. 모듈 변수는 그런 표시가 없다.

`line`을 인수로 받게 바꾸면 위의 문제가 없다.

<!-- file: ch16/no_shared.f90 -->
```fortran
module models
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
contains
  pure function line(x, alpha, beta) result(y)
    real(dp), intent(in) :: x, alpha, beta
    real(dp) :: y

    y = alpha * x + beta
  end function line
end module models

program no_shared
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use models, only: line
  implicit none

  print '(2f8.2)', line(3.0_dp, 2.0_dp, 1.0_dp), line(3.0_dp, -1.0_dp, 0.0_dp)
end program no_shared
```

<!-- output: ch16/no_shared.out -->
```text
    7.00   -3.00
```

한 식에서 두 가지 매개변수로 `line`을 불렀다. `pure`를 붙이면 부작용이 없다는 것도 컴파일러가 확인한다([11장](../11-subprograms/)).

모듈 변수가 알맞은 경우도 있다. 물리 상수나 변환 계수처럼 프로그램이 도는 동안 바뀌지 않는 값은 `parameter`로 모듈에 두고 `use`로 가져다 쓴다. 입력 파일에서 한 번 읽어 전체가 같이 쓰는 설정값도 모듈에 둘 수 있다. 값이 계산 중에 바뀌며 여러 프로시저가 같이 쓴다면 인수로 넘기거나 [17장](../17-derived-types/)의 파생 타입으로 묶어서 넘기는 편이 낫다.

## 모듈과 컴파일 순서

gfortran은 모듈을 컴파일할 때 `.o` 파일 말고도 모듈 이름과 같은 `.mod` 파일을 만든다. 이 파일에 모듈의 선언 정보가 들어 있으며, `use`하는 파일을 컴파일할 때 컴파일러가 읽는다. 따라서 모듈을 쓰는 파일보다 모듈이 있는 파일을 먼저 컴파일해야 한다. `.mod` 파일은 표준이 정한 것이 아니라 컴파일러의 구현이므로 컴파일러마다 모양이 다르다.

위의 `coeff.f90`를 모듈마다 파일로 나눈다고 하자. `coefficients.f90`는 `coefficients` 모듈, `models.f90`는 `models` 모듈, `main.f90`는 주 프로그램이다. 모듈을 쓰는 파일을 먼저 컴파일하면 다음과 같이 실패한다.

```sh
gfortran -c main.f90
```

```text
main.f90:2:7:

    2 |   use coefficients, only: alpha, beta
      |       1
Fatal Error: Cannot open module file ‘coefficients.mod’ for reading at (1): No such file or directory
compilation terminated.
```

의존하는 순서대로 컴파일하면 `.mod` 파일이 생기고 링크까지 된다.

```sh
gfortran -c coefficients.f90
gfortran -c models.f90
gfortran -c main.f90
gfortran coefficients.o models.o main.o -o app
```

`coefficients.f90`를 컴파일하면 `coefficients.o`와 `coefficients.mod`가 생긴다. `models.f90`는 `coefficients`를 쓰므로 그다음에 컴파일한다. 소스 파일을 모두 한 명령에 적을 때도 같은 순서로 적는다(`gfortran coefficients.f90 models.f90 main.f90 -o app`). 한 파일에 모듈 여럿을 둘 때도 `use`되는 모듈이 앞에 와야 한다. 파일이 많아지면 이 순서를 직접 관리하기 번거롭다. 빌드 도구를 쓰는 이유 중 하나다.

큰 모듈의 구현을 다른 파일로 나누는 submodule이라는 기능도 있다(14.2.3). 이 가이드는 다루지 않는다.

## common 블록

옛 코드에서는 `common` 블록이 모듈 변수가 하는 일을 맡았다. 변수를 이름이 아니라 선언한 순서로 맞춘다. 원본이 보인 것처럼 한 서브루틴에서 `alpha`와 `beta`의 순서를 바꿔 선언해도 그대로 컴파일된다. Fortran 2018 표준은 `common` 블록을 폐기 예정 기능(obsolescent feature)으로 분류하고, 오류가 나기 쉬워 모듈로 대체되었다고 설명한다(부속서 B.3.11). gfortran도 `-std=f2018`로 컴파일하면 경고한다. 새 코드에는 쓰지 않는다. 옛 코드를 읽는 데 필요한 `common` 문법은 [부록 A](../21-legacy-code/)에서 설명한다.

## 흔한 실수

- `use`하는 파일을 모듈보다 먼저 컴파일한다. `.mod` 파일이 없다는 오류가 난다.
- `only` 없이 `use`해서 같은 이름이 두 모듈에서 오거나 내 변수와 겹친다.
- 모듈 변수를 인수로도 넘기고 프로시저 안에서 모듈 변수로 직접 바꾼다. 표준이 금지한 방식이다([11장](../11-subprograms/)의 인수 결합).
- `protected` 변수를 밖에서 바꾸려 한다. 바꾸는 프로시저를 모듈에 두고 `call`로 부른다.
- 모듈 변수가 저절로 초기화될 것이라 기대한다. 초기값을 주지 않은 모듈 변수는 값이 정해지지 않았다.
