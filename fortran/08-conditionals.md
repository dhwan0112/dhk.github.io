---
title: 조건문
order: 8
permalink: /fortran/08-conditionals/
---

이 장에서는 조건에 따라 실행할 문을 고르는 방법을 배운다. 한 줄 `if`, `if` 구문, `select case` 구문을 다루고, 둘 중 무엇을 쓸지 정하는 기준도 본다.

## 한 줄 if

조건이 참일 때 문 하나만 실행하면 되면 한 줄 `if`를 쓴다. 형태는 `if (논리식) 문`이다. 다음은 `x`의 절댓값을 구한다.

<!-- file: ch08/abs_value.f90 -->
```fortran
program abs_value
  implicit none
  real :: x

  x = -2.5
  if (x < 0.0) x = -x
  print '(a, f3.1)', 'abs(x) = ', x
end program abs_value
```

<!-- output: ch08/abs_value.out -->
```text
abs(x) = 2.5
```

조건에는 [7장](../07-logical/)에서 본 논리식을 쓴다. 한 줄 `if`가 실행하는 문은 `if` 문이 아니어야 한다. 그래서 `if (a) if (b) ...`처럼 겹쳐 쓸 수 없다. 여러 조건을 함께 따지려면 `.and.`로 묶거나 아래의 `if` 구문을 쓴다.

## if 구문

참일 때 실행할 문이 여럿이거나 거짓일 때 할 일이 따로 있으면 `if` 구문(construct)을 쓴다. `then`으로 시작해 `end if`로 끝나고, 가운데에 `else if`와 `else`를 둘 수 있다.

<!-- file: ch08/sign_class.f90 -->
```fortran
program sign_class
  implicit none
  integer :: n

  read (*, *) n
  if (n > 0) then
    print *, 'positive'
  else if (n < 0) then
    print *, 'negative'
  else
    print *, 'zero'
  end if
end program sign_class
```

`0`을 입력하면 다음과 같이 출력한다.

<!-- output: ch08/sign_class.out -->
```text
 zero
```

조건은 위에서 아래로 차례대로 평가하고, 처음 참이 나오면 그 블록만 실행한 뒤 `end if` 다음으로 넘어간다. 나머지 `else if`의 조건은 평가하지 않는다. `else`가 있으면 블록 하나는 반드시 실행되고, 없으면 조건이 모두 거짓일 때 아무것도 실행하지 않는다. `else if`와 `else`는 여러 번 쓰거나 생략할 수 있다.

`end if`, `else if`는 `endif`, `elseif`로 붙여 써도 된다. 이 가이드는 띄어 쓴다.

## 중첩과 들여쓰기

`if` 구문 안에 `if` 구문을 넣을 수 있다. 블록마다 두 칸씩 들여 쓰면 어느 `else`가 어느 `if`에 속하는지 눈으로 알 수 있다.

<!-- file: ch08/nested_if.f90 -->
```fortran
program nested_if
  implicit none
  real :: x, y

  x = 3.0
  y = 5.0
  if (x > 0.0) then
    if (x >= y) then
      print *, 'x is positive and x >= y'
    else
      print *, 'x is positive but x < y'
    end if
  else
    print *, 'x is not positive'
  end if
end program nested_if
```

<!-- output: ch08/nested_if.out -->
```text
 x is positive but x < y
```

중첩이 서너 겹을 넘으면 읽기 어려워진다. 조건을 `.and.`로 합치거나 [11장](../11-subprograms/)의 부프로그램으로 나누는 편이 낫다.

### 이름 붙은 구문

`if` 구문에는 이름을 붙일 수 있다. 이름은 `if` 앞에 `이름:`으로 쓰고, `end if` 뒤에 같은 이름을 쓴다. 이름을 붙였다면 `end if`에도 반드시 같은 이름이 있어야 하고, 이름을 붙이지 않았다면 `end if`에도 쓸 수 없다. `else if`와 `else` 뒤의 이름은 생략해도 되지만 쓴다면 같은 이름이어야 한다.

<!-- file: ch08/named_if.f90 -->
```fortran
program named_if
  implicit none
  real :: x, y

  x = 3.0
  y = 5.0
  sign_check: if (x > 0.0) then
    order_check: if (x >= y) then
      print *, 'x is positive and x >= y'
    else order_check
      print *, 'x is positive but x < y'
    end if order_check
  else sign_check
    print *, 'x is not positive'
  end if sign_check
end program named_if
```

<!-- output: ch08/named_if.out -->
```text
 x is positive but x < y
```

이름은 중첩이 깊거나 구문이 한 화면을 넘을 때 짝을 찾기 쉽게 해 준다. 이름 붙은 구문은 [9장](../09-loops/)의 `exit`, `cycle`에서도 쓴다.

## select case

같은 식의 값에 따라 갈래가 여럿일 때는 `select case` 구문이 `if`와 `else if`의 나열보다 읽기 쉽다. `select case (식)` 뒤에 `case (값)` 블록을 늘어놓는다. 식은 정수, 문자, 논리 타입이어야 하고, `case`에 쓰는 값은 상수여야 한다.

`case`에는 값 하나, 쉼표로 나눈 값 여러 개, `low:high` 꼴의 범위를 쓸 수 있다. 어디에도 해당하지 않을 때는 `case default` 블록이 실행된다.

<!-- file: ch08/grade_case.f90 -->
```fortran
program grade_case
  implicit none
  integer :: score

  read (*, *) score
  select case (score)
  case (90:100)
    print *, 'A'
  case (80:89)
    print *, 'B'
  case (60:79)
    print *, 'C'
  case (0:59)
    print *, 'F'
  case default
    print *, 'score out of range'
  end select
end program grade_case
```

`85`를 입력하면 다음과 같이 출력한다.

<!-- output: ch08/grade_case.out -->
```text
 B
```

`case`의 값과 범위는 서로 겹칠 수 없다. 한 값이 두 `case`에 걸리면 컴파일 오류이므로 `case`의 순서는 결과에 영향을 주지 않는다. 일치하는 `case`가 없고 `case default`도 없으면 아무것도 실행하지 않는다.

범위의 한쪽을 비워 두면 그쪽이 끝없는 범위가 된다. `case (:-1)`은 `-1` 이하, `case (1:)`은 `1` 이상이다.

<!-- file: ch08/sign_case.f90 -->
```fortran
program sign_case
  implicit none
  integer :: n

  read (*, *) n
  select case (n)
  case (:-1)
    print *, 'negative'
  case (0)
    print *, 'zero'
  case (1:)
    print *, 'positive'
  end select
end program sign_case
```

`-7`을 입력하면 `negative`를 출력한다.

### 문자열 case

문자열도 `select case`로 가를 수 있다. 길이가 다른 문자열은 짧은 쪽 뒤를 공백으로 채워 비교하므로, 길이 8인 `answer`에 `'yes'`를 넣어도 `case ('y', 'yes')`에 일치한다.

<!-- file: ch08/char_case.f90 -->
```fortran
program char_case
  implicit none
  character(len=8) :: answer

  answer = 'yes'
  select case (answer)
  case ('y', 'yes')
    print *, 'accepted'
  case ('n', 'no')
    print *, 'rejected'
  case default
    print *, 'unknown answer'
  end select
end program char_case
```

<!-- output: ch08/char_case.out -->
```text
 accepted
```

## if와 select case 중 고르기

- 한 정수나 문자열 식의 값에 따라 갈래를 나누고 갈래마다 조건이 상수나 상수 범위이면 `select case`를 쓴다.
- 서로 다른 변수를 비교하거나 `.and.`, `.or.`로 조건을 합쳐야 하면 `if` 구문을 쓴다.
- 실수 값에 따라 가를 때도 `if` 구문을 쓴다. `select case`의 식에는 실수를 쓸 수 없다.
- 조건이 하나이고 문도 하나면 한 줄 `if`가 가장 짧다.

옛 코드에서는 산술 `if`(`if (식) 10, 20, 30`)와 계산된 `goto`로 갈래를 나눈 것을 볼 수 있다. 새 코드에는 쓰지 않으며, 읽는 법은 [부록 A](../21-legacy-code/)에서 다룬다.

## 흔한 실수

한 줄 `if` 안에 `if`를 쓴다. 다음 코드는 컴파일되지 않는다.

<!-- file: ch08/if_if.f90 -->
```fortran
program if_if
  implicit none
  integer :: n

  n = 3
  if (n > 0) if (n < 10) print *, 'small positive'
end program if_if
```

gfortran 15.2는 `Error: Syntax error in IF-clause after (1)`을 낸다. `.and.`로 조건을 합치면 된다.

`case` 범위를 겹치게 쓴다. 다음 코드에서 `5`는 두 범위에 모두 속한다.

<!-- file: ch08/case_overlap.f90 -->
```fortran
program case_overlap
  implicit none
  integer :: n

  n = 5
  select case (n)
  case (1:5)
    print *, 'low'
  case (5:9)
    print *, 'high'
  end select
end program case_overlap
```

gfortran 15.2는 `Error: CASE label at (1) overlaps with CASE label at (2)`를 낸다.

`select case`에 `case default`를 빠뜨려서 처리하지 못한 값이 조용히 지나간다. 값의 범위가 모든 경우를 덮지 않는다면 `case default`를 두고 오류를 알린다.
