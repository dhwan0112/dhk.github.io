---
title: 파일 입출력
order: 14
permalink: /fortran/14-file-io/
---

이 장에서는 파일을 열고 읽고 쓰고 닫는 방법을 다룬다. `open`의 `newunit`, 오류와 파일 끝 처리, 파일의 존재 확인, 서식 없는 입출력을 설명한다.

## 장치 번호와 파일

Fortran에서 파일은 장치 번호(unit)와 연결해서 쓴다. 화면 출력과 키보드 입력도 장치이고, [12장](/fortran/12-simple-io/)의 `print *`와 `read (*, *)`가 쓰는 `*`가 그 표준 장치를 가리킨다. 파일을 읽고 쓰려면 `open`으로 파일을 장치 번호에 연결하고, 다 쓰면 `close`로 연결을 끊는다.

원본은 1부터 99 사이 번호를 프로그래머가 골라 쓰고 겹치지 않도록 책임지라고 했다. 새 코드는 `open`의 `newunit=`에 정수 변수를 주어 번호를 컴파일러가 고르게 한다. 표준은 `newunit` 값이 음수이고, 표준 입출력 장치나 이미 연결된 다른 파일의 번호와 같지 않다고 정한다(Fortran 2018 12.5.6.12). 번호를 직접 고르면 다른 모듈이나 라이브러리가 쓰는 번호와 겹쳐 파일 내용이 섞일 수 있고, 이 오류는 찾기 어렵다.

## open과 close

`open`의 자주 쓰는 지정자는 다음과 같다.

| 지정자 | 뜻 |
|---|---|
| `newunit=u` | 장치 번호를 정수 변수 `u`에 받는다. `file=`이 있어야 한다(`status='scratch'`일 때는 예외). |
| `file='이름'` | 파일 이름 |
| `status=` | `'old'`는 있는 파일만 열고, `'new'`는 없는 파일만 만들고, `'replace'`는 있으면 지우고 새로 만든다. 생략하면 `'unknown'`이다. |
| `action=` | `'read'`, `'write'`, `'readwrite'`. 생략했을 때의 값은 컴파일러마다 다르다. |
| `iostat=ios` | 성공하면 0, 실패하면 0이 아닌 값을 `ios`에 받는다. |
| `iomsg=msg` | 실패했을 때의 설명 문자열을 `msg`에 받는다. |

`status`와 `action`은 항상 쓰는 편이 좋다. 읽기만 할 파일에 `status='old'`, `action='read'`를 주면 파일이 없을 때 `open`이 실패하고, `action='read'`로 연 파일에 `write`하는 일은 표준이 허용하지 않는다(12.5.6.4). 원본은 `status`에 `'old'`, `'new'`, `'scratch'`를 소개했다. 현대 코드에서는 새 파일을 만들 때 `'replace'`가 편하다. `'scratch'`는 이름 없는 임시 파일이고 `close` 때 지워진다.

`close(u)`는 연결을 끊는다. `close(u, status='delete')`는 파일도 지우고, `status='keep'`이 기본이다. 쓴 파일을 다시 읽으려면 `close`한 뒤 다시 열거나 `rewind`로 처음 위치로 돌아가야 한다.

장치 번호는 `read`와 `write`의 첫째 위치에 쓴다.

<!-- excerpt: ch14/points.f90 -->
```fortran
  write (u, '(i0)') n
  write (u, '(3f10.4)') (x(i), y(i), z(i), i = 1, n)
```

첫째 위치가 장치, 둘째가 형식이다. `read (u, *) np`처럼 형식 자리에 `*`를 쓰면 목록 지시 입출력(list-directed input/output)이다. 형식 지정은 [13장](/fortran/13-format/)에서 다룬다.

## 점 파일 읽기

원본의 예제는 `points.dat`에서 점 좌표를 읽는다. 첫 줄에 점의 수 `n`이 있고, 이어서 줄마다 `F10.4` 형식으로 x, y, z가 있다. 아래 예제는 읽기 전에 같은 모양의 파일을 먼저 쓰므로 어디서든 같은 결과가 나온다.

<!-- file: ch14/points.f90 -->
```fortran
program points
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  integer, parameter :: n = 5
  real(dp) :: x(n), y(n), z(n)
  real(dp), allocatable :: px(:), py(:), pz(:)
  integer :: u, ios, i, np
  character(len=100) :: msg

  x = [(0.5_dp * i, i = 1, n)]
  y = x**2
  z = 1.0_dp - x
  open (newunit=u, file='points.dat', status='replace', action='write', iostat=ios, iomsg=msg)
  if (ios /= 0) error stop msg
  write (u, '(i0)') n
  write (u, '(3f10.4)') (x(i), y(i), z(i), i = 1, n)
  close (u)

  open (newunit=u, file='points.dat', status='old', action='read', iostat=ios, iomsg=msg)
  if (ios /= 0) error stop msg
  read (u, *) np
  allocate (px(np), py(np), pz(np))
  do i = 1, np
    read (u, '(3f10.4)') px(i), py(i), pz(i)
  end do
  close (u)

  print '(a, i0, a)', 'read ', np, ' points'
  print '(a, 3f9.4)', 'center: ', sum(px) / np, sum(py) / np, sum(pz) / np
end program points
```

<!-- output: ch14/points.out -->
```text
read 5 points
center:    1.5000   2.7500  -0.5000
```

실행하고 나면 `points.dat`이 남는다. 내용은 다음과 같다.

```text
5
    0.5000    0.2500    0.5000
    1.0000    1.0000    0.0000
    1.5000    2.2500   -0.5000
    2.0000    4.0000   -1.0000
    2.5000    6.2500   -1.5000
```

원본과 다른 점을 짚으면 다음과 같다.

- 원본은 배열을 `nmax=1000`으로 고정하고 `n > nmax`인지 검사했다. 여기서는 `n`을 읽은 뒤 `allocate`로 필요한 크기만 만든다.
- 원본의 `format (3(F10.4))`와 `read(u,100)`은 번호 붙은 형식문이다. 여기서는 형식 지정을 문자열로 바로 준다.
- `write (u, '(3f10.4)') (x(i), y(i), z(i), i = 1, n)`은 값 열다섯 개를 쓰며, 형식을 다 쓰면 다음 레코드(record)로 넘어간다. 그래서 점마다 한 줄이 된다.
- `open`이 실패하면 `iostat`와 `iomsg`로 이유를 받아 `error stop`으로 끝낸다. `error stop`은 오류 종료를 시작하며, 문자열 stop code는 오류 장치에 출력하도록 표준이 권장한다(11.4).

`iostat`나 `err=`를 주지 않고 `open`이 실패하면 프로그램이 오류로 끝난다. 다음은 없는 파일을 `status='old'`로 여는 프로그램이다.

<!-- file: ch14/open_fail.f90 -->
```fortran
program open_fail
  implicit none
  integer :: u

  open (newunit=u, file='no_such_file.dat', status='old')
  print *, 'opened'
end program open_fail
```

gfortran 15.2로 실행하면 다음과 같이 끝난다(역추적 줄은 생략했다).

```text
At line 5 of file open_fail.f90
Fortran runtime error: Cannot open file 'no_such_file.dat': No such file or directory

Error termination. Backtrace:
```

`iostat=ios`를 주면 오류 대신 `ios`에 0이 아닌 값(gfortran 15.2에서는 `2`)이 들어가고, `iomsg=msg`에는 위와 같은 설명이 들어간다. 표준은 `iostat` 값이 오류일 때 양수라고 정하지만 구체적인 숫자는 컴파일러마다 다르다(12.11.5). 그러므로 `ios /= 0`으로만 검사한다.

옛 코드에서는 `iostat` 대신 `err=100`처럼 문번호로 분기하는 `err=`, `end=` 지정자가 보인다. 옛 코드를 읽을 때 필요한 설명은 [부록 A](/fortran/21-legacy-code/)에 있다. 새 코드에서는 `iostat`로 검사한다.

## 파일 끝 처리

몇 줄인지 모르는 파일은 끝까지 읽어야 한다. `read`가 파일 끝(end of file)을 만나면 `iostat` 변수에 음수 값 `iostat_end`가 들어간다. `iostat_end`는 `iso_fortran_env` 모듈이 주는 이름 붙은 상수이며 값은 컴파일러가 정한다. 값이 얼마인지 알 필요 없이 `ios == iostat_end`로 비교한다(12.11.5).

<!-- file: ch14/eof_loop.f90 -->
```fortran
program eof_loop
  use, intrinsic :: iso_fortran_env, only: iostat_end
  implicit none
  integer :: u, ios, count
  real :: v, total

  open (newunit=u, file='numbers.dat', status='replace', action='readwrite')
  write (u, '(f6.2)') [1.5, 2.25, 3.0, 4.75]
  rewind (u)

  count = 0
  total = 0.0
  do
    read (u, *, iostat=ios) v
    if (ios == iostat_end) exit
    if (ios /= 0) error stop 'read error'
    count = count + 1
    total = total + v
  end do
  close (u, status='delete')

  print '(a, i0, a, f6.2)', 'values: ', count, '  sum: ', total
end program eof_loop
```

<!-- output: ch14/eof_loop.out -->
```text
values: 4  sum:  11.50
```

파일 끝이 아닌 오류(예를 들어 숫자 자리에 글자가 있을 때)는 `ios`가 양수이므로 따로 처리한다. 이 예제는 `error stop`으로 끝낸다. `is_iostat_end(ios)` 내장 함수도 같은 검사를 한다. 이 예제에서는 파일을 `readwrite`로 열어 쓴 뒤 `rewind(u)`로 처음 위치로 돌아가 읽는다. `close(u, status='delete')`는 끝난 파일을 지운다.

## 파일이 있는지 확인

`inquire`는 파일의 상태를 묻는다. `file=`로 이름을 주고 `exist=`에 논리 변수를 받으면 파일이 있는지 알 수 있다. `status='old'`로 열 때와 같은 질문이지만, `open`을 시도하기 전에 확인해서 사용자에게 알맞은 메시지를 보여 줄 때 쓴다.

<!-- file: ch14/exists.f90 -->
```fortran
program exists
  implicit none
  character(len=*), parameter :: name = 'scratch.txt'
  logical :: found
  integer :: u, ios

  inquire (file=name, exist=found)
  print '(a, l2)', 'before: ', found
  open (newunit=u, file=name, status='old', action='read', iostat=ios)
  print '(a, l2)', 'open failed: ', ios /= 0

  open (newunit=u, file=name, status='new', action='write')
  write (u, '(a)') 'hello'
  close (u)
  inquire (file=name, exist=found)
  print '(a, l2)', 'after write: ', found

  open (newunit=u, file=name, status='old')
  close (u, status='delete')
  inquire (file=name, exist=found)
  print '(a, l2)', 'after delete: ', found
end program exists
```

<!-- output: ch14/exists.out -->
```text
before:  F
open failed:  T
after write:  T
after delete:  F
```

`ios /= 0`은 논리식이고 `print`가 `T`나 `F`로 출력한다. 존재를 확인한 직후 다른 프로그램이 파일을 지울 수도 있으므로 `inquire`의 결과만 믿지 말고 `open`의 `iostat`도 검사한다.

## 서식 없는 입출력

지금까지 쓴 입출력은 사람이 읽을 수 있는 글자로 바꾸는 서식 있는(formatted) 입출력이다. 서식 없는(unformatted) 입출력은 값을 글자로 바꾸지 않고 컴퓨터 안의 이진 표현으로 파일에 쓴다. 글자로 바꾸고 되돌리는 과정이 없어 값이 그대로 보존되고 파일이 작다. 대신 텍스트 편집기로 볼 수 없고, 다른 컴파일러나 다른 컴퓨터에서는 읽지 못할 수도 있다.

서식 없는 파일은 `form='unformatted'`로 연다. 기본 접근 방식인 순차 접근(`access='sequential'`)에서는 `write` 한 번이 레코드 하나를 만들고, 레코드를 파일에 담는 방식은 컴파일러가 정한다. `access='stream'`으로 열면 레코드가 없고 바이트가 이어진 파일로 다룬다. 스트림 접근에서는 `form`을 생략하면 `unformatted`가 기본이고(12.5.6.11), `read (u, pos=1)`처럼 `pos=`로 바이트 위치를 지정할 수 있다. 파일의 바이트 배치를 프로그래머가 알 수 있으므로 다른 프로그램이 읽을 파일에는 스트림이 쓰기 쉽다.

<!-- file: ch14/stream.f90 -->
```fortran
program stream
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  real(dp) :: a(4), b(4)
  integer :: u, nbytes

  a = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp]
  open (newunit=u, file='values.bin', access='stream', form='unformatted', &
        status='replace', action='readwrite')
  write (u) a
  inquire (unit=u, size=nbytes)
  read (u, pos=1) b
  close (u, status='delete')
  print '(a, i0, a, f5.1)', 'stream file: ', nbytes, ' bytes, sum ', sum(b)

  open (newunit=u, file='values.dat', form='unformatted', status='replace', action='readwrite')
  write (u) a
  inquire (unit=u, size=nbytes)
  close (u, status='delete')
  print '(a, i0, a)', 'sequential file: ', nbytes, ' bytes'
end program stream
```

<!-- output: ch14/stream.out -->
```text
stream file: 32 bytes, sum  10.0
sequential file: 40 bytes
```

배정밀도 실수 네 개는 8바이트씩 32바이트다. 같은 값을 순차 접근으로 쓴 파일은 gfortran 15.2에서 8바이트 더 큰 40바이트다. 레코드의 구조를 파일에 담는 방식은 컴파일러가 정하므로 이 크기는 다른 컴파일러에서 다를 수 있다.

## 흔한 실수

- 장치 번호를 직접 고른다(`open (unit=10, ...)`). 다른 곳이 쓰는 번호와 겹칠 수 있으므로 `newunit=`를 쓴다.
- `iostat`를 주고도 검사하지 않는다. 오류를 받고도 프로그램이 계속 돌아가 틀린 값을 쓴다.
- 쓴 파일을 닫거나 `rewind`하지 않고 바로 읽는다. 연결 위치가 파일 끝이라 읽을 것이 없다.
- 쓴 파일의 형식과 읽는 형식이 다르다. `f10.4`로 쓴 파일을 `f8.3`으로 읽으면 열이 어긋난다.
- 서식 없는 파일을 서식 있는 파일처럼 열거나 반대로 연다. `form=`을 파일을 쓴 방식과 맞춘다.
