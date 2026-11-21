---
title: 논리식
order: 7
permalink: /fortran/07-logical/
---

이 장에서는 참과 거짓을 값으로 가지는 `logical` 타입과, 값을 비교하는 관계 연산자, 논리 연산자를 본다. 논리식(logical expression)의 우선순위와 계산 방식, 실수를 비교할 때 생기는 문제도 다룬다.

## logical 타입

`logical` 타입의 값은 `.true.`와 `.false.` 둘뿐이다. 선언은 다른 타입과 같고, 변수에 상수를 대입하거나 논리식의 값을 대입한다.

<!-- excerpt: ch07/logic_precedence.f90 -->
```fortran
  logical :: a, b, c
```

논리식은 [8장](../08-conditionals/)의 `if` 문과 [9장](../09-loops/)의 반복문에서 조건으로 쓰인다. 값을 변수에 담아 두었다가 나중에 조건으로 쓰는 경우도 많다.

## 관계 연산자

관계 연산자(relational operator)는 두 값을 비교해 `logical` 값을 만든다.

| 연산자 | 뜻 | 옛 표기 |
|---|---|---|
| `==` | 같다 | `.eq.` |
| `/=` | 같지 않다 | `.ne.` |
| `<` | 작다 | `.lt.` |
| `<=` | 작거나 같다 | `.le.` |
| `>` | 크다 | `.gt.` |
| `>=` | 크거나 같다 | `.ge.` |

옛 표기와 기호 표기는 뜻이 같다. 표준은 `<`, `<=`, `>`, `>=`, `==`, `/=`가 항상 `.lt.`, `.le.`, `.gt.`, `.ge.`, `.eq.`, `.ne.`와 같은 뜻을 가진다고 정한다(Fortran 2018 표준 10.1.6.2). 옛 코드에서는 `.lt.` 꼴이 보이고, 새 코드에서는 읽기 쉬운 기호 꼴을 쓴다. 같지 않다를 나타내는 `/=`는 다른 언어의 `!=`가 아니다.

<!-- file: ch07/relational.f90 -->
```fortran
program relational
  implicit none
  integer :: a, b
  logical :: same, bigger

  a = 3
  b = 5
  same = a == b
  bigger = a < b
  print '(a, l1)', 'a == b : ', same
  print '(a, l1)', 'a /= b : ', a /= b
  print '(a, l1)', 'a <  b : ', bigger
  print '(a, l1)', 'a <= b : ', a <= b
  print '(a, l1)', 'a >  b : ', a > b
  print '(a, l1)', 'a >= b : ', a >= b
  print '(a, l1)', 'a .lt. b : ', a .lt. b
  print '(a, l1)', 'a .eq. b : ', a .eq. b
end program relational
```

<!-- output: ch07/relational.out -->
```text
a == b : F
a /= b : T
a <  b : T
a <= b : T
a >  b : F
a >= b : F
a .lt. b : T
a .eq. b : F
```

`same = a == b`에서 첫 `=`는 대입이고 둘째 `==`는 비교다. 출력 형식 `l1`은 `logical` 값을 `T`나 `F` 한 글자로 쓴다.

## 논리 연산자

`logical` 값끼리는 논리 연산자로 결합한다.

| 연산자 | 뜻 |
|---|---|
| `.not. x` | `x`가 거짓이면 참 |
| `x .and. y` | 둘 다 참이면 참 |
| `x .or. y` | 하나라도 참이면 참 |
| `x .eqv. y` | 두 값이 같으면 참 |
| `x .neqv. y` | 두 값이 다르면 참 (배타적 논리합) |

`.eqv.`와 `.neqv.`는 `logical` 값끼리 같은지 다른지를 비교한다. `logical` 값에는 `==`를 쓸 수 없다. 표준에서 관계 연산자의 피연산자는 숫자나 문자 타입이다(Fortran 2018 표준 표 10.2). gfortran은 다음 코드에 오류를 낸다.

<!-- file: ch07/logical_compare.f90 -->
```fortran
program logical_compare
  implicit none
  logical :: p, q

  p = .true.
  q = .false.
  print '(l1)', p == q
end program logical_compare
```

다음은 gfortran 15.2의 메시지다.

```text
logical_compare.f90:7:15:

    7 |   print '(l1)', p == q
      |               1
Error: Logicals at (1) must be compared with .eqv. instead of ==
```

## 우선순위

식 안에 연산자가 여러 개 있을 때 표준(Fortran 2018 표준 10.1.3)이 정한 순서는 높은 쪽부터 다음과 같다.

1. 산술 연산자 (`**`, `*`와 `/`, `+`와 `-`)
2. 문자열의 `//`
3. 관계 연산자
4. `.not.`
5. `.and.`
6. `.or.`
7. `.eqv.`와 `.neqv.`

산술 연산이 먼저 끝나고, 그 값으로 관계 연산을 하고, 그 결과를 논리 연산자로 결합한다. 논리 연산자 사이에서는 `.not.`이 가장 먼저, `.eqv.`와 `.neqv.`가 가장 나중이다. 우선순위가 같은 연산자는 왼쪽에서 오른쪽으로 묶인다.

<!-- file: ch07/logic_precedence.f90 -->
```fortran
program logic_precedence
  implicit none
  logical :: a, b, c
  integer :: n, m

  a = .true.
  b = .false.
  c = .false.
  n = 3
  m = 5
  print '(a, l1)', 'a .and. n < m / 2     : ', a .and. n < m / 2
  print '(a, l1)', '.not. a .and. b       : ', .not. a .and. b
  print '(a, l1)', '.not. (a .and. b)     : ', .not. (a .and. b)
  print '(a, l1)', 'a .or. b .and. c      : ', a .or. b .and. c
  print '(a, l1)', '(a .or. b) .and. c    : ', (a .or. b) .and. c
  print '(a, l1)', 'a .or. b .eqv. c      : ', a .or. b .eqv. c
  print '(a, l1)', 'a .or. (b .eqv. c)    : ', a .or. (b .eqv. c)
  print '(a, l1)', 'a .neqv. b            : ', a .neqv. b
end program logic_precedence
```

<!-- output: ch07/logic_precedence.out -->
```text
a .and. n < m / 2     : F
.not. a .and. b       : F
.not. (a .and. b)     : T
a .or. b .and. c      : T
(a .or. b) .and. c    : F
a .or. b .eqv. c      : F
a .or. (b .eqv. c)    : T
a .neqv. b            : T
```

첫 줄은 `m / 2`가 먼저 `2`가 되고, `n < 2`가 거짓이므로 `a .and. .false.`는 거짓이다. 둘째 줄은 `.not. a`가 먼저 계산되므로 `(.not. a) .and. b`이고, `.not. (a .and. b)`와 값이 다르다. `.or.`보다 `.and.`가 먼저이므로 넷째 줄은 `a .or. (b .and. c)`다. `.eqv.`는 `.or.`보다 나중이므로 여섯째 줄은 `(a .or. b) .eqv. c`다. 이렇게 우선순위가 기억나지 않으면 괄호를 쓴다.

## 단락 평가를 믿지 말 것

`a .and. b`에서 `a`가 거짓이면 `b`를 보지 않아도 결과를 알 수 있다. 어떤 언어는 이때 `b`를 계산하지 않기로 정해 둔다. 이를 단락 평가(short-circuit evaluation)라고 한다. Fortran 표준은 이를 보장하지 않는다. 표준은 식의 값을 다른 방법으로 알 수 있으면 피연산자를 모두 계산하지 않아도 된다고 정할 뿐이다(Fortran 2018 표준 10.1.7). 계산할지 말지는 컴파일러가 정한다.

다음 프로그램은 호출될 때 메시지를 출력하는 함수 `check`를 `.or.`와 `.and.`의 오른쪽에 둔다. 함수는 [11장](../11-subprograms/)에서 다룬다.

<!-- file: ch07/eval_order.f90 -->
```fortran
program eval_order
  implicit none
  logical :: r

  r = check(1) .or. check(2)
  print '(a, l1)', 'or:  ', r
  r = .not. check(1) .and. check(3)
  print '(a, l1)', 'and: ', r
contains
  logical function check(k)
    integer, intent(in) :: k

    print '(a, i0)', 'check called with ', k
    check = k == 1
  end function check
end program eval_order
```

`check(1)`이 참이므로 `.or.`의 결과는 `check(2)`와 상관없이 참이다. `.not. check(1)`은 거짓이므로 `.and.`의 결과도 `check(3)`과 상관없이 거짓이다. 최적화 없이 컴파일하면 gfortran 15.2는 두 번째 호출도 한다.

<!-- output: ch07/eval_order.out -->
```text
check called with 1
check called with 2
or:  T
check called with 1
check called with 3
and: F
```

같은 프로그램을 `-O2`로 컴파일하면 두 번째 호출이 사라진다. 이 가이드의 옵션에 `-O2`를 더해 컴파일한 결과다.

```sh
gfortran -std=f2018 -Wall -Wextra -O2 eval_order.f90 -o eval_order
./eval_order
```

```text
eval_order.f90:5:19:

    5 |   r = check(1) .or. check(2)
      |                   1
Warning: Impure function ‘check’ at (1) might not be evaluated [-Wfunction-elimination]
eval_order.f90:7:26:

    7 |   r = .not. check(1) .and. check(3)
      |                          1
Warning: Impure function ‘check’ at (1) might not be evaluated [-Wfunction-elimination]
check called with 1
or:  T
check called with 1
and: F
```

`-Wextra`가 켜는 `-Wfunction-elimination`은 최적화가 부수 효과가 있는 함수의 호출을 없앴을 때 경고한다. 표준이 허용하는 동작이므로 컴파일러의 잘못이 아니다. 오른쪽 피연산자가 반드시 계산되거나 계산되지 않는다는 가정에 기대는 코드는 컴파일 옵션에 따라 다르게 동작한다.

배열의 범위를 확인하는 조건이 가장 흔한 예다. `if (i <= n .and. a(i) > 0.0) then`은 `i`가 `n`보다 커도 `a(i)`를 읽을 수 있다. 조건을 둘로 나누면 이런 가정이 필요 없다.

<!-- file: ch07/safe_index.f90 -->
```fortran
program safe_index
  implicit none
  integer, parameter :: n = 5
  real :: a(n)
  integer :: i
  logical :: found

  a = [1.0, -2.0, 3.0, -4.0, 5.0]
  i = n + 1
  found = .false.
  if (i <= n) then
    found = a(i) > 0.0
  end if
  print '(a, l1)', 'found = ', found
end program safe_index
```

<!-- output: ch07/safe_index.out -->
```text
found = F
```

`if` 문은 [8장](../08-conditionals/)에서 다룬다. `a(i)`는 `i <= n`이 참일 때만 계산되는 위치에 있다.

## 실수의 비교

gfortran의 실수는 이진 부동소수점이므로 십진수로 쓴 값이 정확히 저장되지 않는 경우가 많다. 계산 결과가 수학적으로 같더라도 `==`로 비교하면 거짓이 되는 경우가 많다.

<!-- file: ch07/float_equal.f90 -->
```fortran
program float_equal
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp) :: a, b

  a = 0.1_dp + 0.2_dp
  b = 0.3_dp
  print '(a, l1)', 'a == b: ', a == b
end program float_equal
```

`0.1_dp + 0.2_dp`와 `0.3_dp`는 서로 다른 `dp` 값이어서 비교 결과가 거짓이다. `-Wextra`의 `-Wcompare-reals`는 실수나 복소수를 `==`나 `/=`로 비교하는 코드를 경고한다. gfortran 15.2의 경고다.

```text
float_equal.f90:9:30:

    9 |   print '(a, l1)', 'a == b: ', a == b
      |                              1
Warning: Equality comparison for REAL(8) at (1) [-Wcompare-reals]
```

실수는 차이가 허용 오차 안에 드는지로 비교한다. 두 가지 방법이 있다. 절대 오차는 `abs(a - b) <= tol`이고, 값의 크기에 비례하는 상대 오차는 `abs(a - b) <= tol * max(abs(a), abs(b))`다.

<!-- file: ch07/tolerance.f90 -->
```fortran
program tolerance
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp), parameter :: tol = 1.0e-12_dp
  real(dp) :: a, b, c, d

  a = 0.1_dp + 0.2_dp
  b = 0.3_dp
  c = 1.0e-20_dp
  d = 0.0_dp
  print '(a, es10.2)', 'a - b = ', a - b
  print '(a, l1)', 'a, b absolute: ', abs(a - b) <= tol
  print '(a, l1)', 'a, b relative: ', abs(a - b) <= tol * max(abs(a), abs(b))
  print '(a, l1)', 'c, d absolute: ', abs(c - d) <= tol
  print '(a, l1)', 'c, d relative: ', abs(c - d) <= tol * max(abs(c), abs(d))
end program tolerance
```

<!-- output: ch07/tolerance.out -->
```text
a - b =   5.55E-17
a, b absolute: T
a, b relative: T
c, d absolute: T
c, d relative: F
```

`a`와 `b`는 어느 방법으로도 같다고 판정된다. 한쪽이 0인 `c`와 `d`는 상대 오차 방법에서 허용 오차가 `tol * 1.0e-20`으로 줄어들어 같지 않다고 판정된다. 값이 0에 가까워질 수 있으면 절대 오차를 함께 쓴다. 허용 오차 `tol`은 문제에 맞게 정한다. `dp`의 `epsilon`([5장](../05-variables/))은 이 kind가 구별할 수 있는 상대 간격의 크기여서, `tol`을 `epsilon`의 몇 배로 잡는 것이 하나의 기준이다.

정수끼리의 `==`는 정확하므로 문제가 없다.

## 흔한 실수

- 실수를 `==`나 `/=`로 비교한다. 허용 오차 비교를 쓴다.
- `logical` 값을 `==`로 비교한다. `.eqv.`와 `.neqv.`를 쓴다.
- `.and.`와 `.or.`의 오른쪽 피연산자가 왼쪽이 거짓이거나 참일 때는 계산되지 않는다고 가정한다. 표준은 이를 보장하지 않는다. 배열 범위 확인이나 0으로 나누기 확인은 `if` 문을 나누어 쓴다.
- `.not. a .and. b`를 `.not. (a .and. b)`로 읽는다. `.not.`이 먼저 묶인다.
- `a .or. b .and. c`를 왼쪽부터 읽는다. `.and.`가 먼저 묶인다.
- `x = a == b`에서 `=`와 `==`를 혼동한다. 첫 번째는 대입이고 두 번째는 비교다.
