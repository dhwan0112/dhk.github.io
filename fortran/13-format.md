---
title: 형식문
order: 13
permalink: /fortran/13-format/
---

이 장에서는 입출력의 모양을 직접 정하는 형식 지정을 배운다. 형식 지정을 쓰는 방법 두 가지, 편집 기술자, 되풀이 규칙, 암시적 do로 표를 출력하는 방법을 다룬다.

## 형식 지정 쓰기

[12장](/fortran/12-simple-io/)의 `print *`는 값의 모양을 컴파일러에 맡긴다. 형식 지정(format specification)은 `read`와 `write`의 두 번째 자리에 `*` 대신 쓰는 `(편집 기술자, ...)` 꼴의 문자열이다. 편집 기술자(edit descriptor)는 값 하나를 어떤 모양으로 읽고 쓸지를 정한다.

<!-- file: ch13/fmt_string.f90 -->
```fortran
program fmt_string
  implicit none
  integer :: i
  real :: x

  i = 42
  x = 3.14159
  write (*, '(i4, f8.3)') i, x
end program fmt_string
```

`i4`는 정수를 너비 4칸에, `f8.3`은 실수를 너비 8칸에 소수점 아래 3자리로 쓴다. 출력은 다음과 같다.

<!-- output: ch13/fmt_string.out -->
```text
  42   3.142
```

`print`에도 같은 문자열을 쓸 수 있다. `print '(a, f8.3)', 'x = ', x`처럼 `print` 뒤에 형식을 놓는다.

### 형식문

형식 지정은 문번호(statement label)를 붙인 `format` 문으로 따로 적을 수도 있다. 이때 `read`와 `write`의 두 번째 자리에는 문번호를 쓴다. 두 방법은 뜻이 같다.

<!-- file: ch13/fmt_label.f90 -->
```fortran
program fmt_label
  implicit none
  integer :: i
  real :: x

  i = 42
  x = 3.14159
  write (*, 900) i, x
900 format (i4, f8.3)
end program fmt_label
```

출력은 `fmt_string`과 같다. 형식문(format statement)은 지금도 표준이며 옛 코드에서 자주 보인다. 형식문에는 반드시 문번호가 있어야 하고(C1301), 실행되는 문이 아니라서 선언부나 실행부 어디에든 둘 수 있다. 모듈의 선언부에는 둘 수 없다(C1403). 같은 형식을 여러 `write` 문에서 쓸 수 있다는 것이 장점이지만, 읽는 사람이 문번호를 따라 위아래로 오가야 한다. 이 가이드는 형식 지정을 문자열로 입출력 문 안에 적는다.

## 편집 기술자

자주 쓰는 편집 기술자는 다음과 같다. `w`는 너비, `d`는 소수점 아래 자릿수, `m`은 최소 숫자 개수, `n`은 칸이나 위치의 수다.

| 기술자 | 쓰임 |
|---|---|
| `Iw`, `Iw.m` | 정수. `m`이 있으면 `m`자리가 되도록 앞을 0으로 채운다 |
| `Fw.d` | 고정 소수점 실수 |
| `Ew.d` | 지수 꼴 실수. `0.1235E+05`처럼 0.1 이상 1 미만의 가수 |
| `ESw.d` | 과학 표기. `1.2346E+04`처럼 1 이상 10 미만의 가수 |
| `ENw.d` | 공학 표기. 지수가 3의 배수 |
| `Gw.d` | 값의 크기에 따라 `F`나 `E` 꼴을 고른다 |
| `Aw`, `A` | 문자열. 너비를 생략하면 문자열 길이만큼 |
| `Lw` | 논리값 `T` 또는 `F` |
| `nX` | `n`칸 건너뛰기 |
| `/` | 새 줄(레코드)로 넘어가기 |
| `Tn` | `n`번째 칸으로 이동 |

실수의 `w`와 `d`는 `F`, `E`, `ES`, `EN`에서 모두 있어야 한다. `A`만 너비를 생략할 수 있다(R1307). 출력은 항상 필드의 오른쪽에 맞추고 남는 앞칸은 공백으로 채운다(13.7.2.1).

<!-- file: ch13/descriptors.f90 -->
```fortran
program descriptors
  implicit none
  write (*, '(a, i6, i6.4)') 'I:  ', 42, 42
  write (*, '(a, f10.3)') 'F:  ', 1234.5678
  write (*, '(a, e12.4)') 'E:  ', 12345.678
  write (*, '(a, es12.4)') 'ES: ', 12345.678
  write (*, '(a, en12.4)') 'EN: ', 12345.678
  write (*, '(a, g12.4, g12.4)') 'G:  ', 1234.5678, 0.01234
  write (*, '(a, a6, a)') 'A:  ', 'abc', '|'
  write (*, '(a, l5)') 'L:  ', .true.
  write (*, '(a, 3x, a)') 'X:', 'after 3 blanks'
  write (*, '(a, /, a)') 'slash:', 'next record'
  write (*, '(a, t12, a)') 'T:', 'column 12'
end program descriptors
```

<!-- output: ch13/descriptors.out -->
```text
I:      42  0042
F:    1234.568
E:    0.1235E+05
ES:   1.2346E+04
EN:  12.3457E+03
G:     1235.      0.1234E-01
A:     abc|
L:      T
X:   after 3 blanks
slash:
next record
T:         column 12
```

`G12.4`는 `1234.5678`에는 `F` 꼴을, `0.01234`에는 `E` 꼴을 골랐다(13.7.5.2). `T12`는 12번째 칸에서 쓰기 시작하게 한다.

`I`, `F`, `E` 같은 숫자 기술자는 입력에도 쓴다. 입력에서는 필드 안에 소수점이 있으면 `d`와 상관없이 그 소수점을 쓰고, 소수점이 없으면 필드의 오른쪽 `d`자리를 소수 부분으로 읽는다(13.7.2.3.2). 문자열 한 줄을 통째로 읽을 때는 `'(a)'`를 쓴다.

<!-- file: ch13/read_fixed.f90 -->
```fortran
program read_fixed
  implicit none
  integer :: i
  real :: x
  character(len=20) :: line

  read (*, '(i4, f5.2)') i, x
  read (*, '(a)') line
  print '(i0, 1x, f0.2)', i, x
  print '(a, a, a)', '[', line, ']'
end program read_fixed
```

입력 파일은 다음과 같다.

```text
  42 2500
Hong Gildong
```

<!-- output: ch13/read_fixed.out -->
```text
42 25.00
[Hong Gildong        ]
```

`2500`을 `f5.2`로 읽었으므로 소수점이 없는 필드의 오른쪽 두 자리가 소수 부분이 되어 `25.00`이다. 둘째 줄은 `(a)`로 읽어서 공백이 들어 있어도 한 줄이 통째로 `line`에 들어간다.

## 원본의 x = 0.025 예제

원본은 `x = 0.025`를 `F`, `F5.3`, `E`, `E8.1`로 출력했다. 이 가운데 너비가 없는 `F`와 `E`는 표준이 아니다. `F`와 `E`는 너비와 소수점 아래 자릿수가 있어야 한다. gfortran은 컴파일 때 오류로 알려 준다.

<!-- file: ch13/no_width.f90 -->
```fortran
program no_width
  implicit none
  real :: x

  x = 0.025
  write (*, '(a, f)') 'x=', x
end program no_width
```

gfortran 15.2의 메시지는 다음과 같다. 옵션 없이 컴파일해도 같은 오류가 난다. `E`를 너비 없이 `format` 문에 쓰면 `Error: Period required in format specifier E at (1)`이다.

```text
no_width.f90:6:17:

    6 |   write (*, '(a, f)') 'x=', x
      |                 1
Error: Nonnegative width required in format string at (1)
```

너비를 정해서 다시 쓰면 다음과 같다.

<!-- file: ch13/x_example.f90 -->
```fortran
program x_example
  implicit none
  real :: x

  x = 0.025
  write (*, '(a, f8.3)') 'x=', x
  write (*, '(a, f5.3)') 'x=', x
  write (*, '(a, e12.5)') 'x=', x
  write (*, '(a, e8.1)') 'x=', x
end program x_example
```

<!-- output: ch13/x_example.out -->
```text
x=   0.025
x=0.025
x= 0.25000E-01
x= 0.3E-01
```

`f8.3`은 너비 8칸에 맞추려고 앞에 공백을 채운다. `f5.3`은 `0.025`가 정확히 5칸이다. `e12.5`는 `0.25000E-01`, `e8.1`은 `0.3E-01`로 `0.025`를 소수점 아래 한 자리로 반올림한다.

### 너비가 모자랄 때

출력할 글자가 너비를 넘으면 필드 전체를 `*`로 채운다(13.7.2.1). 예외가 하나 있다. 1보다 작은 값의 소수점 앞 `0`은 선택적이라서 자리가 모자라면 빼 버린다(13.7.2.3.2). 그래서 `0.025`를 `f4.3`으로 쓰면 `.025`가 된다.

너비를 0으로 쓰면 컴파일러가 필요한 최소 너비를 고른다(13.7.2.1). `i0`, `f0.2`가 대표적이다. 앞에 공백이 붙지 않아 문장 사이에 숫자를 끼워 넣을 때 편하다. 다만 `f0.2`로 `0.5`를 쓰면 gfortran 15.2는 `.50`으로 쓴다. 앞의 `0`을 빼는 것은 표준이 허용하는 동작이므로, 모양이 중요하면 `f4.2`처럼 너비를 정한다.

<!-- file: ch13/min_width.f90 -->
```fortran
program min_width
  implicit none
  real :: x

  x = 0.025
  write (*, '(i0, 1x, i0, 1x, i0)') 7, 12345, -42
  write (*, '(f0.2, 1x, f0.2, 1x, f0.2)') 3.14159, 100.0, 0.5
  write (*, '(a, f3.3)') 'f3.3: ', x
  write (*, '(a, f5.2)') 'f5.2: ', 123.456
  write (*, '(a, i3)') 'i3:   ', 12345
end program min_width
```

<!-- output: ch13/min_width.out -->
```text
7 12345 -42
3.14 100.00 .50
f3.3: ***
f5.2: *****
i3:   ***
```

## 되풀이

같은 기술자를 여러 번 쓸 때는 앞에 반복 횟수를 쓴다. `2x, i3, 2x, i3, 2x, i3, 2x, i3`는 `4(2x, i3)`로 쓴다. `3f8.2`는 `f8.2, f8.2, f8.2`와 같다.

<!-- file: ch13/repeat_count.f90 -->
```fortran
program repeat_count
  implicit none
  integer :: v(4)

  v = [1, 2, 3, 4]
  write (*, '(2x, i3, 2x, i3, 2x, i3, 2x, i3)') v
  write (*, '(4(2x, i3))') v
end program repeat_count
```

<!-- output: ch13/repeat_count.out -->
```text
    1    2    3    4
    1    2    3    4
```

### 무제한 반복

`*( ... )`는 괄호 안의 목록을 출력할 값이 남아 있는 동안 반복한다. 값의 개수를 미리 몰라도 된다. Fortran 2008에 추가된 문법이고 괄호 안에 데이터 편집 기술자가 하나 이상 있어야 한다(R1305, C1303). 쉼표 구분 목록을 만들 때 `:`를 쓴다. `:`는 남은 값이 없으면 그 자리에서 형식 처리를 끝낸다(13.4).

<!-- file: ch13/unlimited.f90 -->
```fortran
program unlimited
  implicit none
  integer :: v(7)

  v = [1, 2, 3, 4, 5, 6, 7]
  write (*, '(a, *(i0, :, ", "))') 'values: ', v
  write (*, '(*(i3))') v
end program unlimited
```

<!-- output: ch13/unlimited.out -->
```text
values: 1, 2, 3, 4, 5, 6, 7
  1  2  3  4  5  6  7
```

### 형식 되풀이

출력할 값이 형식보다 많으면 형식을 처음부터 다시 쓰고, 그때마다 새 줄(레코드)로 넘어간다. 이를 형식 되풀이(format reversion)라고 한다. 되풀이는 형식 전체가 아니라 마지막 오른쪽 괄호가 닫는 항목에서 시작한다. 마지막 괄호가 없으면 형식 맨 앞으로 간다. 반복 횟수가 붙은 괄호로 돌아가면 그 반복 횟수도 다시 쓴다(13.4).

<!-- file: ch13/reversion.f90 -->
```fortran
program reversion
  implicit none
  integer :: v(7)

  v = [1, 2, 3, 4, 5, 6, 7]
  write (*, '(i3)') v
  print '(a)', '---'
  write (*, '("v:", 2i3)') v
  print '(a)', '---'
  write (*, '("v:", 2(i3))') v
end program reversion
```

<!-- output: ch13/reversion.out -->
```text
  1
  2
  3
  4
  5
  6
  7
---
v:  1  2
v:  3  4
v:  5  6
v:  7
---
v:  1  2
  3  4
  5  6
  7
```

`i3`만 있는 형식은 값 하나마다 한 줄을 쓴다. `"v:", 2i3`에는 오른쪽 괄호가 없으므로 `v:`부터 다시 시작한다. `"v:", 2(i3)`에는 `2(i3)`의 괄호가 있어서 그 항목으로 돌아가므로 `v:`는 첫 줄에만 나온다. 값이 모자라면 마지막 줄은 짧다.

## 암시적 do와 표 출력

`write` 문의 값 목록 자리에 `(값, 변수 = 시작, 끝)`을 쓰면 값을 반복해서 만들어 낸다. [10장](/fortran/10-arrays/)의 배열 생성자에서 본 암시적 do와 같다. 형식 되풀이와 함께 쓰면 표가 된다. 다음은 원본의 5 x 10 부분 행렬 출력과 같은 일을 3 x 5 배열로 한다.

<!-- file: ch13/table.f90 -->
```fortran
program table
  implicit none
  integer :: i, j, a(3, 5)

  do j = 1, 5
    do i = 1, 3
      a(i, j) = i * j
    end do
  end do

  print '(a)', '  i     sqrt(i)    i**2'
  do i = 1, 3
    write (*, '(i3, f12.4, i8)') i, sqrt(real(i)), i**2
  end do

  print '(a)', 'rows of a:'
  do i = 1, 3
    write (*, '(5i4)') (a(i, j), j = 1, 5)
  end do

  print '(a)', 'all at once, row by row:'
  write (*, '(5i4)') ((a(i, j), j = 1, 5), i = 1, 3)
end program table
```

<!-- output: ch13/table.out -->
```text
  i     sqrt(i)    i**2
  1      1.0000       1
  2      1.4142       4
  3      1.7321       9
rows of a:
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
all at once, row by row:
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
```

`write (*, '(5i4)') (a(i, j), j = 1, 5)`는 한 행을 한 줄로 쓴다. 이중 암시적 do `((a(i, j), j = 1, 5), i = 1, 3)`은 행 단위로 값을 내므로, 형식이 `5i4`이면 한 줄에 5개씩 묶인다. 암시적 do를 너무 복잡하게 중첩하면 읽기 어려우니 `do` 문으로 풀어 쓰는 편이 낫다.

## 반올림

`F`, `E` 같은 기술자가 값을 `d`자리로 줄일 때 어느 방향으로 반올림할지는 입출력 반올림 모드가 정한다. 모드를 정하지 않았을 때 기본은 컴파일러가 정하는 모드다(12.5.6.16). 원본은 0부터 4는 내리고 5부터 9는 올린다고 했지만 기본 모드가 그렇다고 표준이 정한 것은 아니다. gfortran 15.2에서 `0.125`를 `f6.2`로 쓰면 `0.12`이고, 정확히 중간인 값은 짝수 쪽으로 간다. `rc`, `ru`, `rd`, `rz`, `rn` 편집 기술자로 방식을 정한다.

<!-- file: ch13/rounding.f90 -->
```fortran
program rounding
  implicit none
  real :: x

  x = 0.125
  write (*, '(a, f6.2)') 'default: ', x
  write (*, '(a, rn, f6.2)') 'rn:      ', x
  write (*, '(a, rc, f6.2)') 'rc:      ', x
  write (*, '(a, ru, f6.2)') 'ru:      ', x
  write (*, '(a, rd, f6.2)') 'rd:      ', x
  write (*, '(a, rz, f6.2)') 'rz:      ', x
  write (*, '(a, f4.0, 1x, f4.0, 1x, f4.0)') 'f4.0:    ', 0.5, 1.5, 2.5
end program rounding
```

<!-- output: ch13/rounding.out -->
```text
default:   0.12
rn:        0.12
rc:        0.13
ru:        0.13
rd:        0.12
rz:        0.12
f4.0:      0.   2.   2.
```

`rc`(compatible)는 중간 값을 0에서 먼 쪽으로, `ru`는 위로, `rd`는 아래로, `rz`는 0 쪽으로, `rn`은 가장 가까운 값으로 반올림하며, IEEE 반올림을 지원하는 컴파일러에서는 정확히 중간인 값을 짝수 쪽으로 보낸다(13.7.2.3.8). 대부분의 값은 이진수로 정확히 중간이 되지 않으므로 이 차이는 `0.125`나 `2.5`처럼 정확히 표현되는 값에서 드러난다.

## 형식을 문자 변수에 담기

형식 지정은 문자열이므로 문자 변수에 담아 쓸 수 있다. 변수 `fmt`를 `write`의 두 번째 자리에 놓는다. 문자 변수의 길이가 형식보다 길어도 된다. 표준은 형식 지정의 마지막 오른쪽 괄호 뒤의 문자를 무시한다(13.2.2). 내부 파일에 `write`를 하면 실행 중에 형식을 만들 수 있다. 다음은 열의 개수 `n`으로 형식을 만든다.

<!-- file: ch13/fmt_var.f90 -->
```fortran
program fmt_var
  implicit none
  character(len=20) :: fmt
  integer :: n
  real :: row(4)

  row = [1.0, 2.5, 3.25, 4.0]
  fmt = '(4f8.2)'
  write (*, fmt) row

  n = 4
  write (fmt, '(a, i0, a)') '(', n, 'f8.2)'
  print '(a, a)', 'fmt = ', trim(fmt)
  write (*, fmt) row
end program fmt_var
```

<!-- output: ch13/fmt_var.out -->
```text
    1.00    2.50    3.25    4.00
fmt = (4f8.2)
    1.00    2.50    3.25    4.00
```

## 흔한 실수

- `F`나 `E`를 너비 없이 쓴다. 옛 컴파일러는 받아 주었지만 표준이 아니고 gfortran은 오류를 낸다.
- 너비를 빠듯하게 잡아 `***`가 나온다. 음수 부호와 소수점도 너비에 들어간다. 모양이 중요하지 않으면 `i0`이나 `f0.d`로 컴파일러가 너비를 정하게 한다.
- `f0.d`로 쓴 0.5가 `.50`으로 나오는 것을 모르고 숫자를 정렬하려 한다.
- 소수점 없이 입력된 필드를 `Fw.d`로 읽어 값이 100배, 1000배로 달라진다. 입력에 소수점을 쓰거나 목록 지시 입력을 쓴다.
- 값이 형식보다 많은데 되풀이 규칙을 몰라 줄이 이상하게 나뉜다. 한 줄에 몇 개를 쓸지 반복 횟수로 정한다.
- 기술자가 값의 타입과 맞지 않는다. 정수에 `f`를, 실수에 `i`를 쓰면 실행 중에 오류가 난다. gfortran 15.2는 `Fortran runtime error: Expected REAL for item 1 in formatted transfer, got INTEGER`를 낸다.
