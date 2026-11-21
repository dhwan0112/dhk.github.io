---
title: 기본
order: 3
permalink: /fortran/03-basics/
---

이 장에서는 Fortran 프로그램 하나가 어떤 모양인지 본다. 자유 형식 소스 파일의 규칙, `program`과 `end program`, `implicit none`을 다룬다.

## 첫 프로그램

Fortran 프로그램은 정해진 구조를 따르는 텍스트 줄의 나열이다. 다음은 화면에 한 줄을 출력하는 프로그램이다.

<!-- file: ch03/hello.f90 -->
```fortran
program hello
  implicit none

  print *, 'Hello, Fortran!'
end program hello
```

<!-- output: ch03/hello.out -->
```text
 Hello, Fortran!
```

출력 앞의 공백 한 칸은 `print *`가 넣는다. 출력 모양을 정하는 방법은 [13장](/fortran/13-format/)에서 다룬다.

## 프로그램의 구조

주 프로그램(main program)은 다음 순서로 쓴다.

1. `program 이름`
2. `implicit none`
3. 변수 선언
4. 실행문
5. `end program 이름`

선언은 모두 실행문보다 앞에 와야 한다. `end program` 뒤의 이름은 생략할 수 있지만, 쓰면 `program` 문의 이름과 같아야 한다. 프로그램은 `end program`에 이르면 끝나므로 원본에서 권했던 `stop`은 붙이지 않는다.

다음은 원의 반지름을 읽어 넓이를 출력하는 프로그램이다.

<!-- file: ch03/circle.f90 -->
```fortran
program circle
  implicit none
  real :: r, area

  write (*, *) 'Give radius r:'
  read (*, *) r
  area = 3.14159 * r * r
  write (*, *) 'Area = ', area
end program circle
```

`2.0`을 입력하면 다음과 같이 출력한다.

<!-- output: ch03/circle.out -->
```text
 Give radius r:
 Area =    12.5663605
```

`real :: r, area`가 선언이고 `write`, `read`, 대입이 실행문이다. 실행문은 위에서 아래로 차례대로 실행된다.

## implicit none

Fortran은 선언하지 않은 이름에 이름의 첫 글자로 타입을 정해 준다. `i`부터 `n`까지로 시작하면 정수형(`integer`), 나머지는 실수형(`real`)이다. 이 규칙을 암시적 타입 지정이라고 한다. 암시적 타입 지정이 켜져 있으면 변수 이름을 잘못 쳐도 컴파일러가 새 변수로 받아들이고, 프로그램은 틀린 값을 낸 채 끝까지 실행된다.

`implicit none`은 이 규칙을 끈다. 그러면 선언하지 않은 이름은 컴파일 오류가 된다. 모든 주 프로그램과 모듈의 맨 앞에 `implicit none`을 쓴다. 모듈에 쓴 `implicit none`은 그 모듈 안의 프로시저에도 적용된다.

<!-- file: ch03/typo.f90 -->
```fortran
program typo
  implicit none
  real :: radius, area

  radius = 2.0
  area = 3.14159 * raduis**2
  print *, area
end program typo
```

`radius`를 `raduis`로 잘못 쳤으므로 gfortran은 컴파일을 멈춘다. 다음은 gfortran 15.2의 메시지다.

```text
typo.f90:6:25:

    6 |   area = 3.14159 * raduis**2
      |                         1
Error: Symbol ‘raduis’ at (1) has no IMPLICIT type; did you mean ‘radius’?
```

`implicit none`이 없었다면 `raduis`는 값이 정해지지 않은 실수형 변수가 되고, 프로그램은 의미 없는 넓이를 출력한다.

## 자유 형식의 규칙

확장자가 `.f90`인 파일은 자유 형식(free source form)으로 읽힌다. 고정 형식처럼 문장이 시작하는 열이 정해져 있지 않다. 지켜야 할 규칙은 다음과 같다.

- 한 줄은 132자를 넘을 수 없다.
- 느낌표(`!`) 뒤는 줄 끝까지 주석이다. 문자열 안의 `!`는 주석이 아니다.
- 줄 끝에 `&`를 쓰면 다음 줄로 문장이 이어진다. 한 문장은 이어지는 줄을 255개까지 가질 수 있다.
- 세미콜론(`;`)으로 한 줄에 문장 여러 개를 쓸 수 있다.
- 공백이 의미를 가진다. `end do`처럼 키워드 사이에 공백을 넣을 수는 있지만 이름이나 키워드 가운데에 공백을 넣을 수는 없다.
- 대문자와 소문자를 구별하지 않는다. `X`와 `x`는 같은 변수다. 문자열 안의 글자는 구별한다.
- 이름은 영문자로 시작하고 영문자, 숫자, 밑줄(`_`)로 63자까지 쓸 수 있다.

<!-- file: ch03/layout.f90 -->
```fortran
program layout
  implicit none
  real :: total
  integer :: i, j

  ! 느낌표 뒤는 줄 끝까지 주석이다.
  total = 1.0 + 2.0 + 3.0 &
        + 4.0 + 5.0
  i = 1; j = 2
  print *, total, i + j
end program layout
```

<!-- output: ch03/layout.out -->
```text
   15.0000000               3
```

들여쓰기는 문법이 아니다. 그래도 구문 안쪽을 두 칸이나 세 칸 들여 쓰면 구조가 눈에 보인다. 이 가이드는 두 칸을 쓴다.

## 흔한 실수

- `implicit none`을 빠뜨린다. 오타가 컴파일 오류가 아니라 틀린 결과로 나타난다.
- 선언을 실행문 뒤에 쓴다. gfortran은 `Unexpected data declaration statement` 오류를 낸다.
- 고정 형식 코드를 `.f90` 파일에 붙여 넣는다. 6열의 이어쓰기 문자와 1열의 `c` 주석은 자유 형식에서 문법 오류가 된다. 옛 코드는 [부록 A](/fortran/21-legacy-code/)를 참고한다.
