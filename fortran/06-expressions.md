---
title: 식과 대입
order: 6
permalink: /fortran/06-expressions/
---

이 장에서는 식(expression)을 이루는 상수와 연산자, 연산자의 우선순위, 정수 나눗셈, 타입 변환, 문자열 연산을 본다. 마지막으로 식의 값을 변수에 넣는 대입(assignment)을 다룬다.

## 상수

식에서 가장 단순한 것은 상수다. 내장 타입마다 쓰는 법이 다르다.

- 정수 상수는 `1`, `0`, `-100`, `+15`처럼 쓴다.
- 실수 상수는 소수점이 있거나 지수가 있다. `1.0`, `-0.25`, `2.0e6`, `3.333e-1`이 그 예다. `e` 뒤의 수는 10의 거듭제곱이다. `2.0e6`은 200만이다. `1e6`처럼 소수점 없이 지수만 써도 실수다.
- 복소수 상수는 실수부와 허수부를 쉼표로 구분해 괄호로 묶는다. `(2.0, -3.0)`이다.
- 논리 상수는 `.true.`와 `.false.` 두 개뿐이다. 양쪽의 점이 필요하다.
- 문자열 상수는 작은따옴표나 큰따옴표로 묶는다. `'ABC'`, `"Hello"`이다.

실수와 복소수 상수에는 [5장](/fortran/05-variables/)에서 본 kind 접미사를 붙일 수 있다. `3.333e-1_dp`, `(1.0_dp, 2.0_dp)`가 그 예다. 지수 문자가 `d`인 `2.0d-1`은 옛 코드의 배정밀도(double precision) 상수다.

<!-- file: ch06/literals.f90 -->
```fortran
program literals
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  integer :: n
  real :: a
  real(dp) :: b
  complex :: z
  logical :: flag

  n = -100
  a = 2.0e6
  b = 3.333e-1_dp
  z = (2.0, -3.0)
  flag = .true.
  print '(a, i0)', 'integer: ', n
  print '(a, es12.4)', 'real:    ', a
  print '(a, es24.16)', 'real(dp):', b
  print '(a, 2f6.2)', 'complex: ', z
  print '(a, l1)', 'logical: ', flag
end program literals
```

<!-- output: ch06/literals.out -->
```text
integer: -100
real:      2.0000E+06
real(dp):  3.3329999999999999E-01
complex:   2.00 -3.00
logical: T
```

`3.333e-1_dp`는 0.3333이지만 이진수로 정확히 나타낼 수 없어서, 자리를 많이 출력하면 끝자리가 `3.3329999999999999E-01`처럼 보인다.

문자열 상수 안에서 따옴표 문자를 쓰려면 두 가지 방법이 있다. 바깥을 다른 종류의 따옴표로 묶거나, 같은 따옴표를 두 번 쓴다. 두 번 쓴 따옴표는 문자 하나다. `'It''s a nice day'`는 `It's a nice day`이고 `"She said ""hello"""`는 `She said "hello"`이다.

## 연산자와 우선순위

산술 연산자는 `**`(거듭제곱), `*`, `/`, `+`, `-`이다. 표준(Fortran 2018 표준 10.1.3)이 정한 우선순위는 높은 쪽부터 `**`, `*`와 `/`, 단항 `+`와 `-`, 이항 `+`와 `-` 순서다. 우선순위가 같은 연산자는 왼쪽에서 오른쪽으로 계산한다. 예외가 `**`다. `**`가 연이어 나오면 오른쪽부터 계산한다.

<!-- file: ch06/precedence.f90 -->
```fortran
program precedence
  implicit none
  integer :: a, b

  a = 2
  b = 3
  print '(a, i0)', '-a**2     = ', -a**2
  print '(a, i0)', '(-a)**2   = ', (-a)**2
  print '(a, i0)', 'a**b**2   = ', a**b**2
  print '(a, i0)', '(a**b)**2 = ', (a**b)**2
  print '(a, i0)', '2 + 3 * 4 = ', 2 + 3 * 4
  print '(a, i0)', '10 - 4 - 3 = ', 10 - 4 - 3
  print '(a, i0)', '8 / 2 * 3 = ', 8 / 2 * 3
end program precedence
```

<!-- output: ch06/precedence.out -->
```text
-a**2     = -4
(-a)**2   = 4
a**b**2   = 512
(a**b)**2 = 64
2 + 3 * 4 = 14
10 - 4 - 3 = 3
8 / 2 * 3 = 12
```

`-a**2`는 `-(a**2)`이므로 `-4`다. 단항 `-`는 `**`보다 우선순위가 낮다. `a**b**2`는 `a**(b**2)`이므로 `2**9`, 즉 512다. 헷갈리는 식에는 괄호를 쓴다.

연산자 두 개를 이어 쓰는 `a * -2`는 표준이 아니다. 단항 `-`는 다른 연산자 바로 뒤에 올 수 없고 `a * (-2)`처럼 괄호가 필요하다. gfortran은 `-std=f2018`에서 이를 오류로 처리한다.

<!-- file: ch06/unary_after_op.f90 -->
```fortran
program unary_after_op
  implicit none
  integer :: a

  a = 3
  print '(i0)', a * -2
end program unary_after_op
```

다음은 gfortran 15.2의 메시지다.

```text
unary_after_op.f90:6:22:

    6 |   print '(i0)', a * -2
      |                      1
Error: Extension: Unary operator following arithmetic operator (use parentheses) at (1)
```

## 정수 나눗셈

두 피연산자가 모두 정수이면 `/`는 정수 나눗셈(integer division)이다. 결과는 0과 실제 몫 사이에서 0에 가장 가까운 정수다. 소수 부분을 버리므로 `7/2`는 `3`이고, `(-7)/2`는 `-4`가 아니라 `-3`이다. 정수 `a`의 음수 거듭제곱 `a**(-1)`도 `1/a`를 정수 나눗셈으로 계산하므로 `a`가 2 이상이면 0이다.

<!-- file: ch06/integer_division.f90 -->
```fortran
program integer_division
  implicit none
  integer :: a, b
  real :: x

  a = 7
  b = 2
  x = a / b
  print '(a, i0)', 'a / b = ', a / b
  print '(a, f4.1)', 'x = a / b -> ', x
  x = real(a) / b
  print '(a, f4.1)', 'x = real(a) / b -> ', x
  print '(a, i0)', '(-a) / b = ', (-a) / b
  print '(a, i0)', 'mod(a, b) = ', mod(a, b)
end program integer_division
```

<!-- output: ch06/integer_division.out -->
```text
a / b = 3
x = a / b ->  3.0
x = real(a) / b ->  3.5
(-a) / b = -3
mod(a, b) = 1
```

`x = a / b`는 `x`가 실수여도 오른쪽을 정수 나눗셈으로 먼저 계산한다. 결과 `3`이 `3.0`으로 바뀌어 `x`에 들어간다. 실수 나눗셈을 하려면 피연산자 하나를 `real(a)`처럼 실수로 바꾼다. `mod(a, b)`는 나머지다.

상수끼리 정수 나눗셈을 쓰는 것은 대개 실수다. `-Wall`에 포함된 `-Winteger-division`이 이를 경고한다.

<!-- file: ch06/constant_division.f90 -->
```fortran
program constant_division
  implicit none

  print '(i0)', 3 / 2
end program constant_division
```

gfortran 15.2는 다음 경고를 낸다.

```text
constant_division.f90:4:17:

    4 |   print '(i0)', 3 / 2
      |                 1
Warning: Integer division truncated to constant ‘1’ at (1) [-Winteger-division]
```

## 혼합 연산과 타입 변환

피연산자의 타입이 다르면 정수가 실수나 복소수로 바뀐 뒤 계산한다. 결과의 kind는 실수나 복소수 피연산자의 kind다. 두 피연산자가 kind가 다른 실수이면 정밀도가 높은 쪽의 kind를 따른다.

<!-- file: ch06/mixed_types.f90 -->
```fortran
program mixed_types
  implicit none
  integer :: i, j, n
  real :: x

  i = 1
  j = 4
  n = 3
  x = 0.5
  print '(a, f6.3)', 'n * x = ', n * x
  print '(a, f6.3)', 'n + 1.5 = ', n + 1.5
  print '(a, f6.3)', 'i / j * x = ', i / j * x
  print '(a, f6.3)', 'real(i) / j * x = ', real(i) / j * x
  x = n
  print '(a, f6.3)', 'x = n gives ', x
  n = int(2.7 * x)
  print '(a, i0)', 'n = int(2.7 * x) gives ', n
end program mixed_types
```

<!-- output: ch06/mixed_types.out -->
```text
n * x =  1.500
n + 1.5 =  4.500
i / j * x =  0.000
real(i) / j * x =  0.125
x = n gives  3.000
n = int(2.7 * x) gives 8
```

`i / j * x`는 왼쪽부터 계산하므로 `i / j`가 먼저 정수 나눗셈이 되어 0이다. 변환은 대입에서도 일어난다. 오른쪽 식의 값은 왼쪽 변수의 타입으로 바뀐다. 실수를 정수 변수에 넣으면 소수 부분이 버려진다. 값이 달라지므로 gfortran은 `-Wall`의 `-Wconversion`으로 경고한다.

<!-- file: ch06/real_to_integer.f90 -->
```fortran
program real_to_integer
  implicit none
  integer :: n
  real :: y

  y = 2.7
  n = y
  print '(i0)', n
end program real_to_integer
```

```text
real_to_integer.f90:7:6:

    7 |   n = y
      |      1
Warning: Possible change of value in conversion from REAL(4) to INTEGER(4) at (1) [-Wconversion]
```

값이 바뀌는 변환은 코드에서 드러나게 쓰는 것이 좋다. 변환 함수는 다음과 같다.

| 함수 | 하는 일 |
|---|---|
| `int(x)` | 0 쪽으로 소수 부분을 버려 정수로 만든다 |
| `nint(x)` | 가장 가까운 정수로 반올림한다 |
| `floor(x)` | `x`보다 크지 않은 가장 큰 정수 |
| `ceiling(x)` | `x`보다 작지 않은 가장 작은 정수 |
| `real(x, kind)` | 실수로 바꾸고 kind를 정한다 |
| `cmplx(x, y, kind)` | 복소수로 만든다 |

<!-- file: ch06/conversions.f90 -->
```fortran
program conversions
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp) :: x
  complex(dp) :: z

  x = 2.7_dp
  print '(a, i0)', 'int(2.7)     = ', int(x)
  print '(a, i0)', 'int(-2.7)    = ', int(-x)
  print '(a, i0)', 'nint(2.7)    = ', nint(x)
  print '(a, i0)', 'nint(-2.7)   = ', nint(-x)
  print '(a, i0)', 'floor(2.7)   = ', floor(x)
  print '(a, i0)', 'floor(-2.7)  = ', floor(-x)
  print '(a, i0)', 'ceiling(2.7) = ', ceiling(x)
  print '(a, f4.1)', 'real(3, dp)  = ', real(3, dp)
  z = cmplx(1.0_dp, -2.0_dp, kind=dp)
  print '(a, 2f6.2)', 'z            =', z
  print '(a, f6.2)', 'z%re         =', z%re
  print '(a, f6.2)', 'aimag(z)     =', aimag(z)
end program conversions
```

<!-- output: ch06/conversions.out -->
```text
int(2.7)     = 2
int(-2.7)    = -2
nint(2.7)    = 3
nint(-2.7)   = -3
floor(2.7)   = 2
floor(-2.7)  = -3
ceiling(2.7) = 3
real(3, dp)  =  3.0
z            =  1.00 -2.00
z%re         =  1.00
aimag(z)     = -2.00
```

`int`는 0 쪽으로, `floor`는 아래쪽으로 자르므로 음수에서 값이 다르다. 복소수의 실수부는 `z%re`나 `real(z)`로, 허수부는 `z%im`이나 `aimag(z)`로 꺼낸다.

### kind를 정하는 변환

`real(x, dp)`는 `x`를 `dp` kind의 실수로 바꾼다. 어디서 바꾸는지가 결과를 가른다. `x`와 `y`가 기본 kind 실수일 때, 각각을 먼저 `dp`로 바꾼 뒤 곱하는 것과 기본 kind로 곱한 뒤 `dp`로 바꾸는 것은 다르다.

<!-- file: ch06/product_kind.f90 -->
```fortran
program product_kind
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real :: x, y
  real(dp) :: w1, w2

  x = 0.1
  y = 0.3
  w1 = real(x, dp) * real(y, dp)
  w2 = real(x * y, dp)
  print '(a, f22.18)', 'real(x, dp) * real(y, dp) = ', w1
  print '(a, f22.18)', 'real(x * y, dp)           = ', w2
  print '(a, es10.2)', 'difference = ', w1 - w2
end program product_kind
```

<!-- output: ch06/product_kind.out -->
```text
real(x, dp) * real(y, dp) =   0.030000001639127749
real(x * y, dp)           =   0.030000001192092896
difference =   4.47E-10
```

`w1`은 곱셈을 `dp`로 했고 `w2`는 기본 kind로 한 곱셈의 결과를 변환했을 뿐이다. 두 값은 7자리쯤부터 달라진다. 옛 코드는 `w = dble(x) * dble(y)`와 `w = dble(x * y)`로 같은 차이를 쓴다. 표준은 `dble(a)`를 `real(a, kind(0.0d0))`와 같은 값으로 정의한다. 새 코드에서는 `dble` 대신 `real(a, dp)`를 쓴다.

`cmplx`는 kind를 빼먹기 쉽다. `cmplx(x, y)`는 `kind` 인수가 없으면 인수의 kind와 무관하게 기본 kind 복소수를 돌려준다. `dp` 인수를 주어도 정밀도가 줄어든다.

<!-- file: ch06/cmplx_kind.f90 -->
```fortran
program cmplx_kind
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  complex(dp) :: a, b

  a = cmplx(0.1_dp, 0.2_dp)
  b = cmplx(0.1_dp, 0.2_dp, kind=dp)
  print '(2es24.16)', a
  print '(2es24.16)', b
end program cmplx_kind
```

gfortran 15.2는 `a`의 줄에 경고를 낸다.

```text
cmplx_kind.f90:7:12:

    7 |   a = cmplx(0.1_dp, 0.2_dp)
      |            1
Warning: Conversion from REAL(8) to default-kind COMPLEX(4) at (1) might lose precision, consider using the KIND argument [-Wconversion]
```

`a`에는 `0.1000000014901161`처럼 기본 kind 정밀도의 값이 들어가고, `kind=dp`를 준 `b`는 `0.1000000000000000`에 가까운 값이 들어간다.

## 문자열

문자열(character string)은 `//` 연산자로 이어 붙인다. 문자열의 일부는 `s(시작:끝)`으로 꺼낸다. 시작이나 끝을 생략하면 처음이나 끝까지다. 문자열의 글자는 1번부터 센다.

<!-- file: ch06/strings.f90 -->
```fortran
program strings
  implicit none
  character(len=20) :: s
  character(len=5) :: t

  s = 'It''s a nice day'
  print '(a)', s
  print '(a)', "She said ""hello"""
  print '(a)', "It's fine too"
  t = 'ab'
  print '(a, a, a)', '[', t, ']'
  print '(a, i0)', 'len(t)      = ', len(t)
  print '(a, i0)', 'len_trim(t) = ', len_trim(t)
  s = 'Fortran'
  print '(a)', s(1:3)
  print '(a)', s(4:7)
  print '(a)', trim(s) // ' 2018'
  s(1:1) = 'f'
  print '(a)', s
end program strings
```

<!-- output: ch06/strings.out -->
```text
It's a nice day     
She said "hello"
It's fine too
[ab   ]
len(t)      = 5
len_trim(t) = 2
For
tran
Fortran 2018
fortran             
```

문자열 변수의 길이는 선언한 `len`으로 고정된다. 더 짧은 값을 대입하면 오른쪽이 공백으로 채워지고, 더 긴 값을 대입하면 오른쪽이 잘려 나간다(표준 10.2.1.3). `len(t)`는 선언한 길이 5이고 `len_trim(t)`는 끝의 공백을 뺀 길이 2다. `trim(s)`는 끝의 공백을 뺀 문자열을 돌려주므로 `//`로 이을 때 쓴다. `s(1:1) = 'f'`처럼 부분 문자열에 대입하면 나머지 글자는 그대로다.

잘리는 대입은 `character(len=5) :: t`에 `t = 'abcdefgh'`을 넣는 경우다. gfortran 15.2는 `Warning: CHARACTER expression will be truncated in assignment (5/8) at (1) [-Wcharacter-truncation]`을 낸다.

## 대입

대입문은 `변수 = 식` 꼴이다. 오른쪽 식을 먼저 계산하고, 그 값을 왼쪽 변수에 넣는다. 오른쪽에 쓴 변수들은 값이 바뀌지 않는다.

<!-- file: ch06/assignment.f90 -->
```fortran
program assignment
  implicit none
  real, parameter :: pi = 3.14159
  real :: r, area
  integer :: count

  r = 2.0
  area = pi * r**2
  print '(a, f5.2, a, f7.4)', 'r = ', r, ', area = ', area
  count = 0
  count = count + 1
  count = count + 1
  print '(a, i0)', 'count = ', count
end program assignment
```

<!-- output: ch06/assignment.out -->
```text
r =  2.00, area = 12.5664
count = 2
```

`area = pi * r**2`는 `area`만 바꾼다. `pi`와 `r`은 그대로다. `count = count + 1`은 수학의 등식이 아니라 `count + 1`을 계산해 `count`에 다시 넣는다는 뜻이다. `=`는 같다는 뜻이 아니다. 두 값이 같은지 비교하는 연산자는 `==`이고, [7장](/fortran/07-logical/)에서 다룬다.

## 흔한 실수

- 나누는 값이 정수인 줄 모르고 `x = 1 / 3`을 쓴다. 오른쪽은 정수 나눗셈이라 0이다. `1.0 / 3.0`이나 `real(a) / b`로 쓴다.
- 정수로 나눈 뒤 곱하는 순서를 잘못 잡는다. `a * b / c`와 `a * (b / c)`는 정수일 때 다른 값이다.
- `a * -b`처럼 연산자 두 개를 이어 쓴다. `a * (-b)`로 쓴다.
- `cmplx(x, y)`에서 `kind` 인수를 빼먹는다. `dp` 값이 기본 kind로 줄어든다.
- 거듭제곱에 `^`를 쓴다. Fortran의 거듭제곱은 `**`다. gfortran은 `^`에 `Unclassifiable statement` 오류를 낸다.
- 문자열 변수의 길이보다 긴 값을 넣어 뒷부분이 잘린다. `len`을 충분히 크게 선언한다.
