---
title: 디버깅
order: 19
permalink: /fortran/19-debugging/
---

이 장에서는 gfortran 옵션으로 오류를 일찍 찾는 방법과 gdb로 실행 중인 프로그램을 들여다보는 방법을 다룬다. 원본이 쓴 Sun Fortran 77의 옵션(`-ansi`, `-u`, `-C`)은 gfortran에서 다음 옵션에 대응한다.

| 원본(Sun f77) | gfortran | 하는 일 |
|---|---|---|
| `-ansi` | `-std=f2018` | 표준 밖의 확장을 오류로 알린다. |
| `-u` | 소스의 `implicit none`, 또는 `-fimplicit-none` | 선언하지 않은 이름을 오류로 알린다. |
| `-C` | `-fcheck=bounds` | 배열 첨자가 범위를 벗어나면 실행 중에 멈춘다. |

여기에 경고 옵션(`-Wall`, `-Wextra`), 부동소수점 예외를 잡는 `-ffpe-trap`, 초기화하지 않은 변수를 드러내는 `-finit-real`이 더해진다. 개발 중에는 다음처럼 컴파일한다.

```sh
gfortran -std=f2018 -Wall -Wextra -g -fcheck=all -ffpe-trap=invalid,zero,overflow main.f90 -o main
```

## 컴파일 시간에 잡기

### 표준과 암시적 타입 지정

`-std=f2018`은 [18장](/fortran/18-style/)에서 본 것처럼 표준 밖의 문법에 오류를 낸다. 선언하지 않은 변수는 소스에 `implicit none`을 쓰면 오류가 된다. 고치기 어려운 옛 소스에는 `-fimplicit-none`이 모든 프로시저의 맨 앞에 `implicit none`을 넣은 것과 같은 효과를 낸다.

원본이 흔한 오류로 든 `o`와 `0`, `l`과 `1`의 혼동도 `implicit none`이 있으면 컴파일 단계에서 드러난다. 다음 코드는 반복문의 시작값을 `1` 대신 `l`로 잘못 쳤다.

<!-- file: ch19/lookalike.f90 -->
```fortran
program lookalike
  implicit none
  integer :: i, total

  total = 0
  do i = l, 10
    total = total + i
  end do
  print '(i0)', total
end program lookalike
```

`l`은 선언한 적 없는 이름이므로 gfortran 15.2가 멈춘다.

```text
lookalike.f90:6:10:

    6 |   do i = l, 10
      |          1
Error: Symbol ‘l’ at (1) has no IMPLICIT type
```

`implicit none`이 없었다면 `l`은 값이 정해지지 않은 실수형 변수가 되어, 반복문은 엉뚱한 횟수로 돌았을 것이다.

### -Wall과 -Wextra

`-Wall`은 피하기 쉬운 문제를 묶어서 켜는 옵션이다. gfortran 매뉴얼의 목록에는 `-Wconversion`, `-Wunused`, `-Winteger-division`, `-Wline-truncation`, `-Wtabs`, `-Waliasing` 등이 들어 있다. `-Wextra`는 문제가 될 수 있는 용법에 대한 경고를 더하며 `-Wcompare-reals`, `-Wunused-parameter`, `-Wdo-subscript`, `-Wunused-intent-out`, `-Wunused-read`가 포함된다. 다음 프로그램은 이 중 몇 가지를 한꺼번에 일으킨다.

<!-- file: ch19/warn_demo.f90 -->
```fortran
program warn_demo
  implicit none
  real :: x, y
  integer :: unused

  x = 0.1
  y = 1.0d0 / 3.0d0
  if (x == y) print '(a)', 'equal'
  call report(x, y)

contains

  subroutine report(v, w)
    real, intent(in) :: v, w

    print '(f6.2)', v
  end subroutine report
end program warn_demo
```

`-std=f2018 -Wall -Wextra`로 컴파일하면 gfortran 15.2는 네 가지 경고를 낸다.

```text
warn_demo.f90:7:6:

    7 |   y = 1.0d0 / 3.0d0
      |      1
Warning: Change of value in conversion from ‘REAL(8)’ to ‘REAL(4)’ at (1) [-Wconversion]
warn_demo.f90:8:6:

    8 |   if (x == y) print '(a)', 'equal'
      |      1
Warning: Equality comparison for REAL(4) at (1) [-Wcompare-reals]
warn_demo.f90:13:24:

   13 |   subroutine report(v, w)
      |                        1
Warning: Unused dummy argument ‘w’ at (1) [-Wunused-dummy-argument]
warn_demo.f90:4:14:

    4 |   integer :: unused
      |              1~~~~~
Warning: Unused variable ‘unused’ declared at (1) [-Wunused-variable]
```

- `-Wconversion`: `1.0d0 / 3.0d0`은 배정밀도인데 단정밀도 변수에 대입하면 값이 바뀐다.
- `-Wcompare-reals`: 실수를 `==`로 비교한다. 반올림 오차 때문에 같아야 할 값이 같지 않을 수 있다.
- `-Wunused-dummy-argument`: 쓰지 않는 가인수 `w`.
- `-Wunused-variable`: 선언만 하고 쓰지 않은 변수 `unused`.

경고는 오류가 아니므로 컴파일은 끝난다. 경고가 나오면 원인을 고쳐서 0개로 만든다. 경고를 오류로 바꾸려면 `-Werror`를 준다.

### 정수 나눗셈

정수끼리 나누면 소수부가 버려진다([6장](/fortran/06-expressions/)). `7 / 2`는 `3`이고, 실수 변수에 대입해도 `3.0`이다. 상수끼리의 나눗셈은 `-Winteger-division`(`-Wall`에 포함)이 알려 준다.

```text
Warning: Integer division truncated to constant ‘3’ at (1) [-Winteger-division]
```

변수가 섞인 나눗셈은 컴파일러가 알 수 없으므로 `real(n) / 2.0`처럼 의도를 직접 쓴다.

### 인수 목록 불일치

원본은 호출하는 쪽과 호출받는 쪽의 인수 목록이 맞는지 확인하라고 했다. 모듈 프로시저나 인터페이스 블록처럼 명시적 인터페이스가 있으면 컴파일러가 대신 확인한다. 같은 파일 안에 있는 외부 서브루틴도 gfortran은 호출을 대조한다.

<!-- file: ch19/mismatch.f90 -->
```fortran
program mismatch
  implicit none
  integer :: n

  n = 3
  call scale_by_two(n)
  print '(i0)', n
end program mismatch

subroutine scale_by_two(x)
  real, intent(inout) :: x

  x = 2.0 * x
end subroutine scale_by_two
```

정수 `n`을 실수 가인수에 넘겼다. gfortran 15.2의 메시지다.

```text
mismatch.f90:6:22:

    6 |   call scale_by_two(n)
      |                      1
Error: Type mismatch in argument ‘x’ at (1); passed INTEGER(4) to REAL(4)
```

외부 프로시저가 다른 파일에 있으면 컴파일러가 대조할 수 없다. 그러면 호출이 암시적 인터페이스를 쓰게 되고, 타입이 어긋나도 컴파일은 통과하고, 서브루틴은 정수의 비트를 실수로 읽는다. 위 예제의 주 프로그램과 서브루틴을 파일 둘로 나누어 함께 컴파일하면 경고 없이 끝난다. `-Wimplicit-interface`는 명시적 인터페이스 없이 부르는 호출에 경고한다. 이 옵션은 `-Wall`에 들어 있지 않아 따로 켜야 한다. 이 옵션은 인터페이스가 있는지만 확인하고, 인터페이스끼리 서로 맞는지는 확인하지 않는다.

<!-- file: ch19/implicit_iface.f90 -->
```fortran
program implicit_iface
  implicit none
  real :: x

  x = 3.0
  call scale_by_two(x)
  print '(f4.1)', x
end program implicit_iface

subroutine scale_by_two(x)
  real, intent(inout) :: x

  x = 2.0 * x
end subroutine scale_by_two
```

`-Wimplicit-interface`를 주고 컴파일하면 다음 경고가 나온다.

```text
implicit_iface.f90:6:22:

    6 |   call scale_by_two(x)
      |                      1
Warning: Procedure ‘scale_by_two’ called with an implicit interface at (1) [-Wimplicit-interface]
```

해결은 `scale_by_two`를 모듈에 넣어 `use`하는 것이다. 외부 라이브러리를 불러야 한다면 [20장](/fortran/20-blas-lapack/)처럼 인터페이스 블록을 쓴다.

### 줄 길이

원본의 "72열에서 줄이 끝난다"는 고정 형식의 규칙이다. 자유 형식은 한 줄이 132자까지이고, 넘으면 gfortran이 `-Wline-truncation`을 오류로 바꾸어 컴파일을 멈춘다. 문장이 길면 줄 끝에 `&`를 쓰고 다음 줄로 잇는다([3장](/fortran/03-basics/)). 고정 형식에서 72열을 넘은 부분이 말없이 잘리는 문제는 [부록 A](/fortran/21-legacy-code/)에서 본다.

## 실행 중에 잡기

### 배열 첨자: -fcheck=bounds

`-fcheck`는 런타임 검사 코드를 프로그램에 넣는다. 값은 쉼표로 나열한다. gfortran 매뉴얼의 값은 `all`, `array-temps`, `bits`, `bounds`, `do`, `mem`, `pointer`, `recursion`이다. `all`은 전부를 켠다. 원본의 `-C`에 해당하는 것이 `bounds`로, 배열 첨자와 선언된 범위를 검사한다. 일부 검사는 주 프로그램을 컴파일할 때도 켜야 동작한다. 검사 코드가 들어가므로 개발과 시험 중에 켜고, 계산을 오래 돌릴 때는 뺀다.

첨자가 상수이면 컴파일러가 컴파일 단계에서 경고하므로(`Array reference at (1) is out of bounds (6 > 5) in dimension 1`) 런타임 검사의 예제에서는 첨자를 입력으로 받는다.

<!-- file: ch19/bounds.f90 -->
```fortran
program bounds
  implicit none
  integer :: a(5), i, k

  a = [(10 * i, i = 1, 5)]
  read (*, *) k
  print '(a, i0, a, i0)', 'a(', k, ') = ', a(k)
end program bounds
```

`6`을 입력하고 `-fcheck=bounds`로 컴파일하면 프로그램이 멈추고 위치를 알려 준다. 다음은 gfortran 15.2에서 실행한 결과의 앞부분이다.

```text
At line 7 of file bounds.f90
Fortran runtime error: Index '6' of dimension 1 of array 'a' above upper bound of 5

Error termination. Backtrace:
#0  0x7d3565e2a494 in ???
...
```

`-fcheck=bounds` 없이 컴파일한 프로그램은 `a(6)`이 배열 밖의 메모리를 읽고도 멈추지 않는다. 읽은 값은 실행할 때마다 다를 수 있다.

### 부동소수점 예외: -ffpe-trap

0으로 나누거나 음수의 제곱근을 구해도 프로그램은 기본적으로 멈추지 않는다. 결과가 특별한 값이 될 뿐이다.

<!-- file: ch19/inf_nan.f90 -->
```fortran
program inf_nan
  implicit none
  real :: x, y

  read (*, *) x, y
  print '(a, f10.3)', '1 / x    = ', 1.0 / x
  print '(a, f10.3)', 'sqrt(y)  = ', sqrt(y)
end program inf_nan
```

`0.0`과 `-1.0`을 입력하면 다음과 같이 출력한다.

<!-- output: ch19/inf_nan.out -->
```text
1 / x    =   Infinity
sqrt(y)  =        NaN
```

`Infinity`와 `NaN`(숫자가 아님)은 이후의 계산으로 계속 전달되어, 프로그램의 맨 끝에서야 이상한 결과로 보인다. `-ffpe-trap=목록`은 지정한 예외가 일어나는 순간 `SIGFPE` 신호로 프로그램을 멈춘다. 목록에는 `invalid`(`sqrt(-1.0)` 같은 잘못된 연산), `zero`(0으로 나누기), `overflow`, `underflow`, `inexact`, `denormal`을 쓸 수 있다. gfortran 매뉴얼은 앞의 세 가지가 심각한 오류를 가리키는 경우가 많으므로 `invalid,zero,overflow`를 켜 두는 것이 좋다고 설명한다. 기본값은 어느 예외도 막지 않는 것이다.

<!-- file: ch19/fpe_zero.f90 -->
```fortran
program fpe_zero
  implicit none
  real :: x

  read (*, *) x
  print '(f8.3)', inverse(x)

contains

  real function inverse(v)
    real, intent(in) :: v

    inverse = 1.0 / v
  end function inverse
end program fpe_zero
```

`0.0`을 입력하고 `-ffpe-trap=invalid,zero,overflow`로 컴파일하면 `inverse` 안에서 프로그램이 멈춘다.

```text
Program received signal SIGFPE: Floating-point exception - erroneous arithmetic operation.

Backtrace for this error:
#0  0x792b89c2a494 in ???
#1  0x792b89c29085 in ???
...
```

음수의 제곱근도 같은 옵션으로 잡힌다. 다음 프로그램에 `-1.0`을 입력하면 `invalid` 예외로 `SIGFPE`가 일어난다.

<!-- file: ch19/fpe_sqrt.f90 -->
```fortran
program fpe_sqrt
  implicit none
  real :: y

  read (*, *) y
  print '(f8.3)', sqrt(y)
end program fpe_sqrt
```

한 번 켠 예외는 `none`으로 모두 끄는 것 말고는 개별로 끌 수 없다.

### 초기화하지 않은 변수

값을 정하지 않은 지역 변수를 읽으면 그 자리에 남은 값이 쓰인다. 실행할 때마다 결과가 달라지는 버그의 흔한 원인이다. `-finit-real=snan`은 지역 실수 변수를 신호를 내는 NaN(signalling NaN)으로 채우고, `-ffpe-trap=invalid`가 그 값을 읽는 순간 프로그램을 멈춘다. 다음 프로그램은 `total = 0.0`을 빠뜨렸다.

<!-- file: ch19/uninit.f90 -->
```fortran
program uninit
  implicit none
  real :: total, x(3)
  integer :: i

  x = [1.0, 2.0, 3.0]
  do i = 1, 3
    total = total + x(i)
  end do
  print '(f8.3)', total
end program uninit
```

`-finit-real=snan -ffpe-trap=invalid`로 컴파일하고 실행하면 `total + x(i)`에서 멈춘다.

```text
Program received signal SIGFPE: Floating-point exception - erroneous arithmetic operation.
...
```

매뉴얼에 따르면 `-finit-` 옵션을 쓰면 해당 변수에 대한 `-Wuninitialized` 경고가 사라지고, 컴파일 시간 최적화가 신호를 내는 NaN을 조용한 NaN으로 바꿀 수 있어서 트랩을 켜야 한다. 최적화를 켜고 컴파일하면 컴파일러가 직접 경고한다. 다음은 같은 파일을 `-O2 -Wall -Wextra`로 컴파일한 결과다.

```text
uninit.f90:8:24:

    8 |     total = total + x(i)
      |                        ^
Warning: ‘total’ is used uninitialized [-Wuninitialized]
uninit.f90:3:11:

    3 |   real :: total, x(3)
      |           ^~~~~
note: ‘total’ declared here
```

## 역추적과 gdb

### 역추적

gfortran의 런타임 라이브러리는 심각한 오류나 `SIGFPE` 같은 치명적 신호를 만나면 역추적(backtrace)을 출력한다. 매뉴얼의 `-fno-backtrace` 설명이 이것을 기본 동작으로 전제하며, 끄는 옵션이 `-fno-backtrace`다. 옛 자료에 보이는 `-fbacktrace`는 gfortran 15.2도 받아들이지만 기본이 켜져 있으므로 쓸 필요가 없다. 앞의 결과에서 각 줄이 `???`로 나온 것은 디버깅 정보가 없기 때문이다. `-g`를 더하면 프로시저 이름과 줄 번호가 나온다. 주소는 실행마다 다르고, 경로는 줄여서 적었다.

```text
Backtrace for this error:
#0  0x7998e002a494 in ???
#1  0x7998e0029085 in ???
#2  0x7998dfc45caf in ???
	at ./signal/../sysdeps/unix/sysv/linux/x86_64/libc_sigaction.c:0
#3  0x59cdf008b1d5 in inverse
	at .../fpe_zero.f90:13
#4  0x59cdf008b2c3 in fpe_zero
	at .../fpe_zero.f90:6
#5  0x59cdf008b33a in main
	at .../fpe_zero.f90:6
```

`#3`이 `inverse`의 13번째 줄, `#4`가 호출한 쪽의 6번째 줄이다. 역추적만으로도 어느 줄을 볼지 정해진다.

### -O0과 최적화

`-g`는 디버거가 읽을 정보를 실행 파일에 넣는다. 최적화 수준은 `-O0`이 기본이며, 디버깅 결과가 소스와 가장 잘 맞는다. `-O2`처럼 최적화를 켜면 컴파일러가 코드를 재배치하고 변수를 없애므로 디버거에서 소스 줄과 변수가 맞지 않게 보인다. 같은 프로그램을 `-g -O2`로 컴파일해 gdb로 돌리면 `inverse`의 가인수가 `v=<optimized out>`로 나오고, `inverse`가 호출한 쪽에 합쳐져 `x`도 보이지 않는다. GCC 문서는 편집, 컴파일, 디버그를 반복하는 동안에는 `-Og`를 권한다. 반대로 위의 초기화하지 않은 변수 예제는 `-O0`에서는 경고가 없고 `-O2`에서만 경고가 나왔다.

### gdb의 기본 사용

gdb는 프로그램을 한 줄씩 실행하며 변수 값을 보여 주는 디버거다. 원본은 명령행 인터페이스가 어렵다고 했지만, 아래 명령 몇 개면 충분하다. `-g -O0`으로 컴파일한 프로그램을 `gdb ./fpe_zero`로 연다.

```sh
gfortran -g -O0 -ffpe-trap=invalid,zero,overflow fpe_zero.f90 -o fpe_zero
gdb ./fpe_zero
```

| 명령 | 하는 일 |
|---|---|
| `break 이름` | 프로시저의 시작이나 `파일:줄`에 멈춤점을 둔다. |
| `run` | 프로그램을 시작한다. `run < 파일`로 입력을 연결한다. |
| `print 변수` | 변수 값을 출력한다. |
| `next`, `step` | 한 줄 실행한다. `step`은 호출한 프로시저 안으로 들어간다. |
| `continue` | 다음 멈춤점이나 끝까지 실행한다. |
| `backtrace`, `up` | 호출 순서를 보고, 한 단계 호출한 쪽으로 올라간다. |
| `info locals` | 지금 프로시저의 지역 변수를 보여 준다. |
| `quit` | gdb를 끝낸다. |

`inverse`에 멈춤점을 두고 실행하는 세션이다. 일부 줄은 줄였고 주소는 실행마다 다르다.

```text
(gdb) break inverse
Breakpoint 1 at 0x11c5: file fpe_zero.f90, line 13.
(gdb) run < fpe_zero.in
Breakpoint 1, fpe_zero::inverse (v=0) at fpe_zero.f90:13
13	    inverse = 1.0 / v
(gdb) print v
$1 = 0
(gdb) next

Program received signal SIGFPE, Arithmetic exception.
0x00005555555551d5 in fpe_zero::inverse (v=0) at fpe_zero.f90:13
13	    inverse = 1.0 / v
(gdb) backtrace
#0  0x00005555555551d5 in fpe_zero::inverse (v=0) at fpe_zero.f90:13
#1  0x00005555555552c4 in fpe_zero () at fpe_zero.f90:6
(gdb) up
#1  0x00005555555552c4 in fpe_zero () at fpe_zero.f90:6
6	  print '(f8.3)', inverse(x)
(gdb) print x
$2 = 0
(gdb) quit
```

`print v`가 `0`임을 확인하고 `next`를 실행하면 나눗셈에서 `SIGFPE`가 일어난다. 원인은 `inverse`가 아니라 `0.0`을 넘긴 호출한 쪽이다. `write`나 `print`를 여기저기 넣고 다시 컴파일하는 원본의 방법보다 빠르게 같은 정보를 얻는다.

## 흔한 실수

- 경고를 무시한다. 위 예제의 경고는 모두 실제 버그의 징후다. `-Wall -Wextra`로 컴파일해서 경고가 0개가 되게 한다.
- 최적화를 켠 채 `-g`만 믿고 디버깅한다. 변수가 `<optimized out>`로 보이면 `-O0`으로 다시 컴파일한다.
- 주 프로그램을 `-fcheck=bounds` 없이 컴파일한다. 매뉴얼에 따르면 일부 검사는 주 프로그램도 같은 옵션으로 컴파일해야 동작한다.
- 정수 나눗셈과 실수 나눗셈을 혼동한다.
- 상수 첨자로만 시험해서 `-fcheck=bounds` 없이도 컴파일러가 잡아 준다고 믿는다. 첨자가 실행 중에 정해지는 경우는 런타임 검사가 필요하다.
