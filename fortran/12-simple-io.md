---
title: 간단한 입출력
order: 12
permalink: /fortran/12-simple-io/
---

이 장에서는 `read`, `write`, `print`로 키보드와 화면을 다루는 기본 입출력을 배운다. 값의 모양을 컴파일러에 맡기는 목록 지시 입출력의 규칙과 잘못된 입력을 처리하는 `iostat`를 다룬다. 모양을 직접 정하는 방법은 [13장](/fortran/13-format/), 파일은 [14장](/fortran/14-file-io/)에서 다룬다.

## read와 write

`read (장치 번호, 형식) 변수 목록`은 입력을, `write (장치 번호, 형식) 값 목록`은 출력을 한다. 장치 번호(unit)와 형식 자리에 `*`를 쓰면 표준 입력과 표준 출력, 그리고 컴파일러가 정하는 기본 모양(목록 지시 입출력, list-directed input/output)을 뜻한다. 표준은 `read`의 `*`를 표준 입력에, `write`의 `*`를 표준 출력에 연결된 장치 번호라고 정한다(Fortran 2018, 12.5.1).

`read`는 표준 입력에서 값을 읽어 변수에 대입하고, `write`는 값을 표준 출력에 쓴다. 장치 번호와 형식을 생략한 짧은 꼴도 있다.

<!-- file: ch12/short_forms.f90 -->
```fortran
program short_forms
  implicit none
  real :: a, b

  read *, a, b
  if (a > b) then
    print *, 'a is larger'
  else
    print *, 'b is larger or equal'
  end if
end program short_forms
```

`read *, 목록`은 `read (*, *) 목록`과 같고 `print *, 목록`은 `write (*, *) 목록`과 같다. `3.5 1.5`를 입력하면 `a is larger`를 출력한다.

<!-- output: ch12/short_forms.out -->
```text
 a is larger
```

## 목록 지시 입력의 규칙

목록 지시 입력은 값을 공백이나 쉼표로 구분한다. 값 사이에 공백이 여러 개 있어도 하나로 본다(13.10.2). 정수 변수에는 정수를, 실수 변수에는 `-1.0`이나 `1e+2`처럼 실수로 읽을 수 있는 값을 쓴다.

한 `read` 문은 항상 새 레코드(record), 곧 새 줄에서 읽기 시작한다. 읽기를 마치면 그 줄에 남은 값은 버리고 다음 줄의 앞에 파일 위치를 둔다(12.3.4.2). 변수 목록에 비해 줄에 값이 모자라면 다음 줄에서 이어 읽는다. 다음 세 예제가 이 규칙을 보여 준다.

먼저 줄마다 `read` 문 하나씩이 대응하는 보통의 경우다. 값을 구분하는 공백과 쉼표를 섞어 썼다.

<!-- file: ch12/read_records.f90 -->
```fortran
program read_records
  implicit none
  integer :: m, n
  real :: x, y, z(4)

  read (*, *) m, n
  read (*, *) x, y
  read (*, *) z
  print '(2i5)', m, n
  print '(2f7.1)', x, y
  print '(4f5.1)', z
end program read_records
```

입력 파일은 다음과 같다.

```text
   -1  100
  -1.0 1e+2
  1.0, 2.0, 3.0 4.0
```

<!-- output: ch12/read_records.out -->
```text
   -1  100
   -1.0  100.0
  1.0  2.0  3.0  4.0
```

다음은 첫 줄에 값이 네 개 들어 있는 경우다. 첫째 `read`는 `m`과 `n`만 읽고 그 줄의 나머지 `-1.0, 1e+2`를 버린다. 둘째 `read`는 다음 줄에서 읽는다.

<!-- file: ch12/read_extra.f90 -->
```fortran
program read_extra
  implicit none
  integer :: m, n
  real :: x, y

  read (*, *) m, n
  read (*, *) x, y
  print '(2i5)', m, n
  print '(2f7.1)', x, y
end program read_extra
```

입력 파일은 다음과 같다.

```text
-1, 100, -1.0, 1e+2
1.0, 2.0, 3.0, 4.0
```

<!-- output: ch12/read_extra.out -->
```text
   -1  100
    1.0    2.0
```

`x`와 `y`는 첫 줄의 값이 아니라 둘째 줄의 `1.0, 2.0`이 되고 뒤의 `3.0, 4.0`도 버려진다.

반대로 줄에 값이 모자라면 다음 줄로 넘어가서 읽는다. 한 `read` 문이 변수 넷을 읽는데 값이 줄마다 하나씩 있어도 된다.

<!-- file: ch12/read_short.f90 -->
```fortran
program read_short
  implicit none
  integer :: m, n
  real :: x, y

  read (*, *) m, n, x, y
  print '(2i5)', m, n
  print '(2f7.1)', x, y
end program read_short
```

입력 파일은 다음과 같다.

```text
-1
100
-1.0
1e+2
```

<!-- output: ch12/read_short.out -->
```text
   -1  100
   -1.0  100.0
```

이 밖에 알아 둘 규칙이 둘 있다. 값 자리에 아무것도 쓰지 않고 쉼표를 연달아 쓰면(`10,,30`) 그 변수는 바뀌지 않는다(13.10.3.2). `3*1.5`는 `1.5`를 세 번 쓴 것과 같다(13.10.2). 슬래시(`/`)를 만나면 그 `read`는 거기서 끝나고 남은 변수는 바뀌지 않는다.

## 표준 장치

`*`는 간편하지만 표준 출력과 표준 오류를 따로 쓰려면 이름이 필요하다. `iso_fortran_env` 모듈이 `input_unit`, `output_unit`, `error_unit`을 제공한다. `input_unit`과 `output_unit`은 `*`가 가리키는 표준 입력과 표준 출력이고, `error_unit`은 오류 메시지를 위한 장치다(12.5.1).

<!-- file: ch12/std_units.f90 -->
```fortran
program std_units
  use, intrinsic :: iso_fortran_env, only: input_unit, output_unit, error_unit
  implicit none
  real :: r

  write (output_unit, *) 'Give radius r:'
  read (input_unit, *) r
  if (r < 0.0) then
    write (error_unit, *) 'radius must not be negative'
  else
    write (output_unit, '(a, f8.3)') 'Area = ', 3.14159 * r * r
  end if
end program std_units
```

`2.0`을 입력하면 다음과 같이 출력한다.

<!-- output: ch12/std_units.out -->
```text
 Give radius r:
Area =   12.566
```

`-1.0`을 입력하면 `radius must not be negative`가 `error_unit`으로 나간다. 터미널에서는 두 출력이 섞여 보이지만 `> out.txt`로 표준 출력만 파일로 돌리면 오류 메시지는 화면에 남는다. 오류 메시지는 `error_unit`으로 쓰는 것이 관례다.

## 문자열 읽기

문자 변수에 읽을 때는 따옴표가 없으면 첫 공백, 쉼표, 슬래시에서 값이 끝난다(13.10.3.1). 공백이 들어 있는 문자열을 목록 지시 입력으로 읽으려면 값을 작은따옴표나 큰따옴표로 감싸야 한다.

<!-- file: ch12/read_string.f90 -->
```fortran
program read_string
  implicit none
  character(len=20) :: first, second

  read (*, *) first
  read (*, *) second
  print '(a, a, a)', '[', first, ']'
  print '(a, a, a)', '[', second, ']'
end program read_string
```

입력 파일은 다음과 같다.

```text
Hong Gildong
'Hong Gildong'
```

<!-- output: ch12/read_string.out -->
```text
[Hong                ]
[Hong Gildong        ]
```

첫 줄은 `Hong`만 읽힌다. 변수 길이 20에 못 미치는 문자열은 뒤를 공백으로 채우므로 대괄호로 끝을 표시했다. 줄 전체를 공백째 읽으려면 `read (*, '(a)') line`처럼 형식을 지정한다. 형식은 [13장](/fortran/13-format/)에서 다룬다.

## iostat로 잘못된 입력 처리

입력이 잘못되면 `read`는 기본적으로 프로그램을 오류로 끝낸다. `iostat=` 변수를 주면 프로그램은 멈추지 않고 그 변수에 결과가 담긴다. 0이면 성공, 양수이면 오류, 음수이면 파일 끝이다(12.11.5). 구체적인 값은 컴파일러가 정하므로 값 자체를 쓰지 않고 `ios /= 0`이나 `is_iostat_end(ios)`로 검사한다.

<!-- file: ch12/read_iostat.f90 -->
```fortran
program read_iostat
  implicit none
  integer :: n, ios

  do
    read (*, *, iostat=ios) n
    if (is_iostat_end(ios)) exit
    if (ios /= 0) then
      print '(a)', 'not an integer, skipped'
    else
      print '(a, i0)', 'n = ', n
    end if
  end do
  print '(a)', 'end of input'
end program read_iostat
```

입력 파일은 다음과 같다.

```text
12
abc
7
```

<!-- output: ch12/read_iostat.out -->
```text
n = 12
not an integer, skipped
n = 7
end of input
```

둘째 줄의 `abc`는 정수가 아니라서 오류이고 프로그램은 그 줄을 건너뛰고 계속한다. 오류가 난 뒤 파일 위치는 표준이 정하지 않는다. gfortran 15.2는 오류가 난 줄 다음으로 간다. 파일 끝에서는 `is_iostat_end`가 참이 되어 반복이 끝난다.

## 목록 지시 출력의 모양

`print *`와 `write (*, *)`가 값을 쓰는 모양은 컴파일러가 정한다. 표준은 값 사이에 공백이나 쉼표를 두고 필요하면 새 줄을 시작할 수 있다고만 하며, 실수의 자릿수와 너비도 프로세서가 정하는 적당한 값을 쓴다고 한다(13.10.4). 따라서 같은 프로그램이 컴파일러에 따라 다르게 출력할 수 있다.

<!-- file: ch12/list_output.f90 -->
```fortran
program list_output
  implicit none
  integer :: n
  real :: x
  double precision :: d
  logical :: flag
  character(len=5) :: word

  n = 42
  x = 3.14159
  d = 1.0d0 / 3.0d0
  flag = .true.
  word = 'abc'
  print *, n
  print *, x
  print *, d
  print *, flag
  print *, word
  print *, n, x, flag
end program list_output
```

gfortran 15.2에서는 다음과 같이 출력한다.

<!-- output: ch12/list_output.out -->
```text
          42
   3.14159012    
  0.33333333333333331     
 T
 abc  
          42   3.14159012     T
```

줄 앞의 공백 한 칸과 정수의 넓은 너비, 단정밀도 실수의 아홉 자리와 배정밀도 실수의 열일곱 자리가 gfortran의 선택이다. 다른 컴파일러는 다르게 쓸 수 있다. 출력을 다른 프로그램이 읽거나 모양이 중요하면 [13장](/fortran/13-format/)의 형식 지정을 쓴다.

## 흔한 실수

- 한 줄에 값을 더 많이 넣으면 모두 읽힌다고 생각한다. 한 `read` 문은 남은 값을 버리고 다음 `read`는 다음 줄에서 시작한다.
- 공백이 들어 있는 문자열을 따옴표 없이 입력하고 첫 단어만 읽힌다고 놀란다.
- `iostat=` 없이 읽으면서 잘못된 입력에 프로그램이 멈추는 것을 막지 않는다. 사용자가 입력하는 값은 `iostat=`로 검사한다.
- `print *`의 출력 모양에 의존해 결과를 다른 도구로 처리한다.
