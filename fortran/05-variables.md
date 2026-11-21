---
title: 변수, 선언, 타입
order: 5
permalink: /fortran/05-variables/
---

이 장에서는 변수의 이름 규칙과 내장 타입을 보고, 선언하는 방법을 익힌다. 이어서 kind 매개변수로 정밀도를 정하는 법, 이름 붙은 상수, 선언과 함께 하는 초기화를 다룬다.

## 이름 규칙

변수 이름은 영문자로 시작하고, 영문자, 숫자, 밑줄(`_`)로 이어 쓰며, 63자를 넘을 수 없다(Fortran 2018 표준 6.2.2). 대문자와 소문자는 구별하지 않는다. `total_count`처럼 뜻이 드러나는 영어 소문자 이름을 쓴다.

Fortran에는 예약어가 없다. 문의 키워드와 같은 철자의 이름을 변수에 써도 문법 오류가 아니다. `integer :: real`도 컴파일된다. 읽기 어려운 코드가 되므로 `real`, `program`, `end` 같은 이름은 쓰지 않는다.

## 내장 타입과 선언

Fortran의 내장 타입(intrinsic type)은 다섯 가지다.

| 타입 | 용도 | 예 |
|---|---|---|
| `integer` | 정수 | `3`, `-100` |
| `real` | 실수 | `1.75`, `2.0e6` |
| `complex` | 복소수 | `(1.0, 2.0)` |
| `logical` | 참과 거짓 | `.true.`, `.false.` |
| `character` | 문자열 | `'sample'` |

변수는 사용하기 전에 선언(declaration)한다. 선언은 `타입 :: 이름 목록` 꼴이다. 같은 타입의 변수는 쉼표로 이어 한 문에 쓸 수 있다. `implicit none`을 쓰면([3장](/fortran/03-basics/)) 선언하지 않은 이름은 오류가 되므로, 모든 변수를 선언해야 한다.

<!-- file: ch05/declarations.f90 -->
```fortran
program declarations
  implicit none
  integer :: count
  real :: height
  complex :: z
  logical :: done
  character(len=12) :: label

  count = 3
  height = 1.75
  z = (1.0, 2.0)
  done = .false.
  label = 'sample'
  print '(a, i0)', 'count  = ', count
  print '(a, f5.2)', 'height = ', height
  print '(a, 2f5.1)', 'z      = ', z
  print '(a, l1)', 'done   = ', done
  print '(a, a, a)', 'label  = [', label, ']'
end program declarations
```

<!-- output: ch05/declarations.out -->
```text
count  = 3
height =  1.75
z      =   1.0  2.0
done   = F
label  = [sample      ]
```

`character(len=12)`는 길이가 12인 문자열 변수다. `'sample'`은 6글자이므로 나머지 6칸이 공백으로 채워진다. 출력에서 `]` 앞에 공백이 보이는 것이 그 공백이다. 문자열은 [6장](/fortran/06-expressions/)에서 더 다룬다.

`::`는 `integer, parameter :: n = 5`처럼 속성(attribute)을 붙이거나 초기화를 쓸 때 필요하다. 속성이 없는 선언에서는 `integer count`처럼 `::`를 생략할 수도 있다. 옛 코드에서 자주 보이는 이 꼴 대신 이 가이드는 항상 `::`를 쓴다.

## kind 매개변수와 정밀도

`integer`와 `real`은 여러 종류가 있고, 종류는 kind 매개변수(kind type parameter)가 정한다. 선언에서는 `integer(int64)`, `real(dp)`처럼 타입 뒤 괄호에 kind를 적는다. kind 값은 컴파일러마다 다르다. 8바이트 실수를 `real(8)`로 쓴 코드는 `8`이 다른 뜻인 컴파일러에서 틀린 타입이 된다.

`iso_fortran_env` 모듈은 kind 값에 이름을 붙여 둔다. `int8`, `int16`, `int32`, `int64`는 저장 크기가 8, 16, 32, 64비트인 정수의 kind이고, `real32`, `real64`, `real128`은 저장 크기가 32, 64, 128비트인 실수의 kind다. 컴파일러가 해당 kind를 지원하지 않으면 이 값은 음수다.

프로그램에서는 쓸 kind를 이름 붙은 상수(named constant)로 한 번 정해 두고 그 이름을 쓴다. 아래 `dp`가 그 예다. 나중에 정밀도를 바꿀 때 한 줄만 고치면 된다.

<!-- file: ch05/kinds.f90 -->
```fortran
program kinds
  use, intrinsic :: iso_fortran_env, only: int32, int64, real32, real64
  implicit none
  integer, parameter :: dp = real64
  integer(int64) :: big
  real(dp) :: x

  big = 2_int64**40
  x = 1.0_dp / 3.0_dp
  print '(a, i0, a, i0)', 'int32 = ', int32, ', int64 = ', int64
  print '(a, i0, a, i0)', 'real32 = ', real32, ', real64 = ', real64
  print '(a, i0)', 'kind(big) = ', kind(big)
  print '(a, i0)', 'kind(x) = ', kind(x)
  print '(a, i0)', 'big = ', big
  print '(a, f20.17)', 'x = ', x
end program kinds
```

<!-- output: ch05/kinds.out -->
```text
int32 = 4, int64 = 8
real32 = 4, real64 = 8
kind(big) = 8
kind(x) = 8
big = 1099511627776
x =  0.33333333333333331
```

gfortran에서 이 kind 값은 4, 8처럼 바이트 수와 같지만 표준이 그렇게 정한 것은 아니다. `kind(big)`는 변수의 kind 값을 돌려주는 내장 함수다. `2_int64**40`은 `2**40`이 32비트 정수를 넘기 때문에 쓴 것이다. `int64` 변수는 `int32`로 나타낼 수 없는 큰 정수를 담는다. `1.0_dp`처럼 상수 뒤에 `_dp`를 붙이는 표기는 다음 절에서 설명한다.

작은 프로그램 하나에서는 `dp`를 프로그램 안에서 선언하면 된다. 여러 프로그램 단위가 같은 `dp`를 써야 하면 모듈 한 곳에 두고 가져다 쓴다([16장](/fortran/16-modules/)).

### 정밀도로 kind 고르기

`iso_fortran_env`는 저장 크기로 kind를 고른다. 필요한 정밀도로 고르려면 `selected_real_kind`와 `selected_int_kind`를 쓴다. `selected_real_kind(p, r)`은 10진 유효숫자가 적어도 `p`자리이고 10진 지수 범위가 적어도 `r`인 실수 kind를 돌려준다. `selected_int_kind(r)`은 `-10**r`보다 크고 `10**r`보다 작은 정수를 모두 나타내는 정수 kind를 돌려준다. 조건을 만족하는 kind가 없으면 음수를 돌려준다.

<!-- file: ch05/select_kind.f90 -->
```fortran
program select_kind
  implicit none
  integer, parameter :: sp = selected_real_kind(6, 37)
  integer, parameter :: dp = selected_real_kind(15, 307)
  integer, parameter :: i8 = selected_int_kind(9)
  integer, parameter :: i18 = selected_int_kind(18)

  print '(a, i0)', 'sp  = ', sp
  print '(a, i0)', 'dp  = ', dp
  print '(a, i0)', 'i8  = ', i8
  print '(a, i0)', 'i18 = ', i18
  print '(a, i0)', 'selected_real_kind(40) = ', selected_real_kind(40)
end program select_kind
```

<!-- output: ch05/select_kind.out -->
```text
sp  = 4
dp  = 8
i8  = 4
i18 = 8
selected_real_kind(40) = -1
```

조건에 맞는 kind가 여러 개이면 정수는 범위가 가장 작은 것을, 실수는 정밀도가 가장 낮은 것을 돌려준다. 위의 마지막 줄은 40자리 정밀도를 가진 실수가 gfortran에 없다는 뜻이다. 이 가이드는 `iso_fortran_env`의 `real64`를 `dp`로 쓴다.

돌려받은 음수를 그대로 kind로 쓰면 컴파일 오류가 난다.

<!-- file: ch05/bad_kind.f90 -->
```fortran
program bad_kind
  implicit none
  integer, parameter :: qp = selected_real_kind(40)
  real(qp) :: x

  print '(i0)', qp
end program bad_kind
```

```text
bad_kind.f90:4:10:

    4 |   real(qp) :: x
      |          1
Error: Kind -1 not supported for type REAL at (1)
```

## 상수에 kind 붙이기

상수에는 kind가 있다. 실수 상수 `0.1`은 아무것도 붙이지 않으면 기본 kind의 실수다. 다른 kind로 쓰려면 `_`와 kind 이름을 상수 뒤에 붙인다. `1.0_dp`, `2_int64`가 그 예다. 지수가 있는 상수는 `1.0e-3_dp`처럼 지수 뒤에 붙인다.

<!-- file: ch05/literal_kind.f90 -->
```fortran
program literal_kind
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp) :: a, b

  a = 0.1
  b = 0.1_dp
  print '(a, es24.16)', 'a = 0.1     : ', a
  print '(a, es24.16)', 'b = 0.1_dp  : ', b
  print '(a, es24.16)', '1.0e-3_dp   : ', 1.0e-3_dp
end program literal_kind
```

<!-- output: ch05/literal_kind.out -->
```text
a = 0.1     :   1.0000000149011612E-01
b = 0.1_dp  :   1.0000000000000001E-01
1.0e-3_dp   :   1.0000000000000000E-03
```

`a`는 `real(dp)` 변수인데도 `0.1`이 기본 kind 실수로 먼저 만들어진 뒤 `dp`로 변환되므로, 앞 8자리쯤만 맞고 그 뒤는 틀린 값이 된다. gfortran 15.2는 `-std=f2018 -Wall -Wextra`에서 이 대입에 경고를 내지 않는다. 정밀도를 `dp`로 정했다면 상수에도 `_dp`를 붙인다.

## 조사 함수

변수의 kind가 가진 성질은 내장 함수로 알아낸다. 이 함수들은 인수의 값이 아니라 타입과 kind만 본다. 표준은 인수의 값이 정의되지 않아도 된다고 정한다.

| 함수 | 돌려주는 값 |
|---|---|
| `huge(x)` | `x`의 타입과 kind가 나타낼 수 있는 가장 큰 값 |
| `tiny(x)` | 표준의 모형에서 가장 작은 양의 실수 |
| `epsilon(x)` | 1에 비해 작은 값(표준 정의로 `b**(1-p)`) |
| `precision(x)` | 10진 유효숫자 자릿수 |
| `range(x)` | 10진 지수 범위 |
| `kind(x)` | kind 값 |

<!-- file: ch05/inquiry.f90 -->
```fortran
program inquiry
  use, intrinsic :: iso_fortran_env, only: int32, real32, real64
  implicit none

  print '(a, i0)', 'huge(1_int32)         = ', huge(1_int32)
  print '(a, es11.4)', 'huge(1.0_real32)      = ', huge(1.0_real32)
  print '(a, es12.4e3)', 'huge(1.0_real64)      = ', huge(1.0_real64)
  print '(a, es12.4e3)', 'tiny(1.0_real64)      = ', tiny(1.0_real64)
  print '(a, es11.4)', 'epsilon(1.0_real32)   = ', epsilon(1.0_real32)
  print '(a, es11.4)', 'epsilon(1.0_real64)   = ', epsilon(1.0_real64)
  print '(a, i0)', 'precision(1.0_real32) = ', precision(1.0_real32)
  print '(a, i0)', 'precision(1.0_real64) = ', precision(1.0_real64)
  print '(a, i0)', 'range(1.0_real64)     = ', range(1.0_real64)
end program inquiry
```

<!-- output: ch05/inquiry.out -->
```text
huge(1_int32)         = 2147483647
huge(1.0_real32)      =  3.4028E+38
huge(1.0_real64)      =  1.7977E+308
tiny(1.0_real64)      =  2.2251E-308
epsilon(1.0_real32)   =  1.1921E-07
epsilon(1.0_real64)   =  2.2204E-16
precision(1.0_real32) = 6
precision(1.0_real64) = 15
range(1.0_real64)     = 307
```

`real32`는 10진으로 6자리, `real64`는 15자리 정도를 믿을 수 있다. `epsilon`은 정밀도의 크기를 가늠하는 값이어서, 실수를 비교할 때 허용 오차를 정하는 데 쓴다([7장](/fortran/07-logical/)).

## 이름 붙은 상수

`parameter` 속성을 붙이면 값이 바뀌지 않는 이름 붙은 상수가 된다. 선언에서 값을 함께 정하며, 나중에 대입할 수 없다. 값은 상수식이어야 하는데, 상수와 다른 이름 붙은 상수, 일부 내장 함수(`atan` 등)로 만든 식이 상수식이다.

<!-- file: ch05/constants.f90 -->
```fortran
program constants
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp), parameter :: pi = 4.0_dp * atan(1.0_dp)
  real(dp), parameter :: two_pi = 2.0_dp * pi
  integer, parameter :: n = 5
  real(dp) :: r, area

  r = 1.5_dp
  area = pi * r**2
  print '(a, f18.15)', 'pi     = ', pi
  print '(a, f18.15)', 'two_pi = ', two_pi
  print '(a, f8.4)', 'area   = ', area
  print '(a, i0)', 'n      = ', n
end program constants
```

<!-- output: ch05/constants.out -->
```text
pi     =  3.141592653589793
two_pi =  6.283185307179586
area   =   7.0686
n      = 5
```

`dp`도 `n`도 `parameter`이므로 이름 붙은 상수다. 상수를 쓰면 같은 값을 여러 곳에 적다가 오타를 내는 일이 줄고, 값을 바꿀 때 한 곳만 고치면 된다. 이름 붙은 상수에 대입하면 컴파일 오류가 난다.

<!-- file: ch05/assign_constant.f90 -->
```fortran
program assign_constant
  implicit none
  real, parameter :: pi = 3.14159

  pi = 3.0
  print *, pi
end program assign_constant
```

다음은 gfortran 15.2의 메시지다.

```text
assign_constant.f90:5:3:

    5 |   pi = 3.0
      |   1~~
Error: Named constant ‘pi’ in variable definition context (assignment) at (1)
```

옛 코드에서는 `parameter (pi = 3.14159)` 문으로 선언하는 꼴이 보인다. 읽는 법은 [부록 A](/fortran/21-legacy-code/)에서 다룬다.

## 선언과 함께 초기화하기

변수는 선언에서 `= 값`으로 초기값을 정할 수 있다. 배열에는 값 하나로 모든 원소를 채우거나 배열 값 전체를 줄 수 있다.

<!-- file: ch05/initial_values.f90 -->
```fortran
program initial_values
  implicit none
  real :: a(3) = 0.0
  integer :: v(3) = [10, 20, 30]
  integer :: m(2, 2) = reshape([1, 2, 3, 4], [2, 2])
  character(len=8) :: tag = 'run'

  print '(3f5.1)', a
  print '(3i4)', v
  print '(2i4)', m(1, :)
  print '(2i4)', m(2, :)
  print '(a, a, a)', '[', tag, ']'
end program initial_values
```

<!-- output: ch05/initial_values.out -->
```text
  0.0  0.0  0.0
  10  20  30
   1   3
   2   4
[run     ]
```

초기화하지 않은 변수는 값이 정의되지 않은 채 시작한다(Fortran 2018 표준 19.6.4). 값을 대입한 뒤에 쓴다. 옛 코드에서 변수를 미리 채우던 `data` 문은 [부록 A](/fortran/21-legacy-code/)에서 설명한다.

### 초기화는 save 속성을 준다

선언에서 초기화한 변수는 `save` 속성을 가진다. 표준은 `common` 블록에 들지 않은 변수를 명시적으로 초기화하면 `save` 속성이 암시된다고 정한다(Fortran 2018 표준 8.4). `save` 변수는 프로시저가 끝나도 값을 잃지 않는다. 이는 초기화가 프로시저를 부를 때마다 일어나는 대입이 아니라 프로그램을 시작할 때 한 번만 일어난다는 뜻이다.

<!-- file: ch05/init_save.f90 -->
```fortran
program init_save
  implicit none
  integer :: k

  do k = 1, 3
    call count_calls()
  end do
contains
  subroutine count_calls()
    integer :: n = 0

    n = n + 1
    print '(a, i0)', 'call number ', n
  end subroutine count_calls
end program init_save
```

<!-- output: ch05/init_save.out -->
```text
call number 1
call number 2
call number 3
```

부프로그램은 [11장](/fortran/11-subprograms/)에서 다룬다. 서브루틴을 부를 때마다 `n`이 0에서 시작할 것 같지만 값이 이어진다. 호출할 때마다 0에서 시작하게 하려면 선언에서 초기화하지 말고 실행문에서 대입한다.

<!-- file: ch05/init_assign.f90 -->
```fortran
program init_assign
  implicit none
  integer :: k

  do k = 1, 3
    call count_calls()
  end do
contains
  subroutine count_calls()
    integer :: n

    n = 0
    n = n + 1
    print '(a, i0)', 'call number ', n
  end subroutine count_calls
end program init_assign
```

<!-- output: ch05/init_assign.out -->
```text
call number 1
call number 1
call number 1
```

## double precision

옛 코드에서는 배정밀도(double precision) 실수를 `double precision`으로 선언하고 `1.0d0`, `2.5d-3`처럼 지수 문자 `d`로 상수를 쓴다. 표준은 `double precision`을 기본 실수보다 정밀도가 높은 실수 kind의 다른 이름이라고 정하고, `d` 지수를 쓴 상수는 그 kind라고 정한다. 지수 문자 `d`는 `_dp` 같은 kind 접미사와 함께 쓸 수 없다.

<!-- file: ch05/old_double.f90 -->
```fortran
program old_double
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  double precision :: a
  real(real64) :: b

  a = 1.0d0 / 3.0d0
  b = 1.0_real64 / 3.0_real64
  print '(es24.16)', a
  print '(es24.16)', b
  print '(l1)', kind(a) == real64
end program old_double
```

<!-- output: ch05/old_double.out -->
```text
  3.3333333333333331E-01
  3.3333333333333331E-01
T
```

gfortran에서는 두 kind가 같다. 그러나 표준은 `double precision`이 `real64`와 같다고 정하지 않는다. 새 코드에서는 `real64`나 `selected_real_kind`로 정밀도를 직접 정하는 방법을 쓴다. `real*8`은 표준이 아닌 확장이므로 쓰지 않는다([2장](/fortran/02-what-is-fortran/)).

## 흔한 실수

- 변수를 `real(dp)`로 선언하고 상수는 `0.1`처럼 kind 없이 쓴다. 값이 `dp`의 정밀도로 만들어지지 않고 기본 kind의 정밀도로 만들어진다.
- `real(8)`처럼 kind 값을 숫자로 쓴다. 컴파일러가 바뀌면 다른 kind가 된다.
- 프로시저 안의 `integer :: n = 0`이 호출할 때마다 `n`을 0으로 만든다고 생각한다. 이 초기화는 한 번만 일어나고 `n`은 값이 이어진다.
- `selected_real_kind`가 돌려준 음수 kind로 변수를 선언한다. 조건에 맞는 kind가 없다는 뜻이고, gfortran 15.2는 `Kind -1 not supported for type REAL` 오류를 낸다.
- 이름 붙은 상수에 값을 대입한다. 컴파일러가 막아 주지만, 값이 바뀌어야 하는 것이면 `parameter`를 빼고 일반 변수로 선언한다.
