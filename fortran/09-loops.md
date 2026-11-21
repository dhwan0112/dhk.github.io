---
title: 반복문
order: 9
permalink: /fortran/09-loops/
---

이 장에서는 같은 일을 되풀이하는 반복문을 배운다. 횟수가 정해진 `do`, 조건을 따지는 `do while`, 조건 없는 `do`와 `exit`, 한 번을 건너뛰는 `cycle`을 다룬다.

## 횟수가 정해진 do

`do 변수 = 시작, 끝, 증분`으로 시작해 `end do`로 끝나는 구문은 변수를 시작값부터 끝값까지 증분씩 바꿔 가며 블록을 되풀이한다. 증분을 생략하면 1이다. 다음은 1부터 `n`까지의 누적합을 출력한다.

<!-- file: ch09/cumulative_sum.f90 -->
```fortran
program cumulative_sum
  implicit none
  integer :: i, n, total

  n = 5
  total = 0
  do i = 1, n
    total = total + i
    print '(a, i0, a, i0)', 'i = ', i, ', sum = ', total
  end do
end program cumulative_sum
```

<!-- output: ch09/cumulative_sum.out -->
```text
i = 1, sum = 1
i = 2, sum = 3
i = 3, sum = 6
i = 4, sum = 10
i = 5, sum = 15
```

반복 변수는 정수여야 한다. 증분은 음수일 수 있지만 0일 수는 없다. 다음은 10부터 1까지 2씩 줄이며 출력한다.

<!-- file: ch09/even_down.f90 -->
```fortran
program even_down
  implicit none
  integer :: i

  do i = 10, 1, -2
    print '(a, i0)', 'i = ', i
  end do
end program even_down
```

<!-- output: ch09/even_down.out -->
```text
i = 10
i = 8
i = 6
i = 4
i = 2
```

`i = 10, 1, -2`의 마지막 값은 `2`다. 다음 값 `0`은 끝값 `1`을 지나므로 반복하지 않는다.

### 반복 횟수는 시작 전에 정해진다

`do` 문을 실행할 때 시작, 끝, 증분 식을 한 번만 계산해서 반복 횟수를 정한다. 표준(Fortran 2018, 11.1.7.4.1)은 이 횟수를 `(끝 - 시작 + 증분) / 증분`으로 정하고, 이 값이 음수이면 0으로 한다. 그 뒤에 반복 안에서 끝값이나 증분에 쓰인 변수를 바꿔도 횟수는 달라지지 않는다.

다음 프로그램은 `j`를 읽어 `1`부터 `j`까지 반복하면서 매번 `j`를 1씩 늘린다.

<!-- file: ch09/bound_once.f90 -->
```fortran
program bound_once
  implicit none
  integer :: i, j

  read (*, *) j
  do i = 1, j
    j = j + 1
  end do
  print '(a, i0)', 'j = ', j
end program bound_once
```

`5`를 입력하면 반복은 처음에 정한 대로 5번 돌고 `j`는 10이 된다. `j`가 늘어나는 것을 따라 반복이 끝나지 않는 일은 없다.

<!-- output: ch09/bound_once.out -->
```text
j = 10
```

`-std=f2018 -Wall -Wextra`로 컴파일해도 gfortran 15.2는 이 코드에 경고를 내지 않는다. 컴파일러가 알려 주지 않으므로 끝값에 쓰는 변수를 반복 안에서 바꾸는 코드는 읽는 사람을 헷갈리게 한다. 바꿀 필요가 없으면 바꾸지 않는다.

시작값이 끝값보다 커서 횟수가 0이면 블록은 한 번도 실행되지 않는다. 반복이 끝난 뒤 반복 변수는 마지막으로 대입된 값을 그대로 가진다. 정상적으로 끝난 `do i = 1, 3` 뒤의 `i`는 `4`다.

<!-- file: ch09/zero_trip.f90 -->
```fortran
program zero_trip
  implicit none
  integer :: i, lo, hi

  do i = 1, 3
  end do
  print '(a, i0)', 'after 1..3: i = ', i

  lo = 5
  hi = 1
  do i = lo, hi
    print '(a, i0)', 'never printed: ', i
  end do
  print '(a, i0)', 'after 5..1: i = ', i
end program zero_trip
```

<!-- output: ch09/zero_trip.out -->
```text
after 1..3: i = 4
after 5..1: i = 5
```

### 반복 변수를 바꾸지 않는다

반복 변수는 반복 안에서 대입하거나 읽어 들여 바꾸면 안 된다. 표준이 금지하고 gfortran은 이를 컴파일할 때 잡는다.

<!-- file: ch09/change_index.f90 -->
```fortran
program change_index
  implicit none
  integer :: i

  do i = 1, 3
    i = i + 1
  end do
end program change_index
```

gfortran 15.2의 메시지는 다음과 같다.

```text
change_index.f90:6:13:

    5 |   do i = 1, 3
      |             2
    6 |     i = i + 1
      |             1
Error: Variable ‘i’ at (1) cannot be redefined inside loop beginning at (2)
```

gfortran 15.2는 `intent(inout)` 가인수를 가진 명시적 인터페이스의 프로시저에 반복 변수를 실인수로 넘기는 경우도 오류로 잡는다. 그러나 인터페이스를 알 수 없는 외부 프로시저에 넘겨서 바꾸면 같은 옵션에서 경고 없이 컴파일된다. 어떤 경우에도 반복 변수는 읽기만 한다.

### 실수 반복 변수

Fortran 77에는 `do x = 0.0, 1.0, 0.25`처럼 실수 반복 변수가 있었다. 오차 때문에 예상한 값을 정확히 밟지 못하는 일이 있었고, 표준은 이 기능을 삭제했다(Fortran 2018 부속서 B.1). `-std=f2018`에서 gfortran은 오류를 낸다.

<!-- file: ch09/real_index.f90 -->
```fortran
program real_index
  implicit none
  real :: x

  do x = 0.0, 1.0, 0.25
    print *, x
  end do
end program real_index
```

gfortran 15.2의 메시지는 `Error: Deleted feature: Loop variable at (1) must be integer`다. 같은 효과가 필요하면 정수 변수로 반복하고 실수 값은 안에서 계산한다.

<!-- file: ch09/real_steps.f90 -->
```fortran
program real_steps
  implicit none
  integer :: i
  real :: x

  do i = 0, 4
    x = 0.25 * real(i)
    print '(f5.2)', x
  end do
end program real_steps
```

<!-- output: ch09/real_steps.out -->
```text
 0.00
 0.25
 0.50
 0.75
 1.00
```

## do while

조건이 참인 동안 되풀이하려면 `do while (논리식)`을 쓴다. 블록을 실행하기 전에 매번 조건을 평가하므로 처음부터 거짓이면 블록은 한 번도 실행되지 않는다. 다음은 100 이하인 2의 거듭제곱을 출력한다.

<!-- file: ch09/powers_while.f90 -->
```fortran
program powers_while
  implicit none
  integer :: n

  n = 1
  do while (n <= 100)
    print '(i0)', n
    n = 2 * n
  end do
end program powers_while
```

<!-- output: ch09/powers_while.out -->
```text
1
2
4
8
16
32
64
```

표준은 `do while`을 블록 맨 앞에 `if (.not. (조건)) exit`를 둔 조건 없는 `do`와 같다고 정의한다(11.1.7.4.1).

## 조건 없는 do와 exit

`do` 뒤에 아무것도 쓰지 않으면 끝없이 되풀이하는 반복문이 된다. 안에서 `exit`를 실행하면 반복문을 벗어나 `end do` 다음 문으로 간다. 앞의 거듭제곱 예제는 이렇게도 쓸 수 있다.

<!-- file: ch09/powers_exit.f90 -->
```fortran
program powers_exit
  implicit none
  integer :: n

  n = 1
  do
    if (n > 100) exit
    print '(i0)', n
    n = 2 * n
  end do
end program powers_exit
```

출력은 `do while` 판과 같다. `exit`의 위치가 블록 앞이면 `do while`과 같고, 블록 뒤나 중간이면 조건을 가운데서 시험할 수 있다.

원본이 "until 반복"이라고 부른, 블록을 먼저 실행하고 끝에서 조건을 시험하는 반복문도 같은 방법으로 쓴다. 다음은 양수가 입력될 때까지 계속 읽는다. 입력을 반드시 한 번은 읽어야 하므로 `do while`로는 쓰기 어색하다.

<!-- file: ch09/read_positive.f90 -->
```fortran
program read_positive
  implicit none
  integer :: n

  do
    read (*, *) n
    if (n > 0) exit
    print '(a, i0, a)', 'got ', n, ', need a positive number'
  end do
  print '(a, i0)', 'n = ', n
end program read_positive
```

`-3`, `0`, `4`를 차례로 입력하면 다음과 같이 출력한다.

<!-- output: ch09/read_positive.out -->
```text
got -3, need a positive number
got 0, need a positive number
n = 4
```

### cycle

`cycle`은 이번 반복의 나머지를 건너뛰고 다음 반복으로 간다. 횟수가 정해진 `do`에서는 반복 변수를 증분만큼 바꾼 뒤 다음 반복을 시작한다. 다음은 1부터 10까지 홀수만 더한다.

<!-- file: ch09/odd_sum.f90 -->
```fortran
program odd_sum
  implicit none
  integer :: i, total

  total = 0
  do i = 1, 10
    if (mod(i, 2) == 0) cycle
    total = total + i
  end do
  print '(a, i0)', 'sum of odd numbers = ', total
end program odd_sum
```

<!-- output: ch09/odd_sum.out -->
```text
sum of odd numbers = 25
```

## 이름 붙은 반복문과 바깥 반복 빠져나가기

`exit`와 `cycle`은 기본적으로 가장 안쪽 반복문에 작용한다. 반복문에 이름을 붙이면 `exit 이름`, `cycle 이름`으로 바깥 반복문을 가리킬 수 있다. 이름은 `do` 앞에 `이름:`으로 쓰고 `end do` 뒤에 같은 이름을 쓴다.

다음은 `i * j`가 12가 되는 첫 쌍을 찾아 두 반복문을 한꺼번에 벗어난다.

<!-- file: ch09/find_pair.f90 -->
```fortran
program find_pair
  implicit none
  integer :: i, j

  outer: do i = 1, 5
    inner: do j = 1, 5
      if (i * j == 12) then
        print '(a, i0, a, i0)', 'i = ', i, ', j = ', j
        exit outer
      end if
    end do inner
  end do outer
  print '(a, i0, a, i0)', 'stopped at i = ', i, ', j = ', j
end program find_pair
```

<!-- output: ch09/find_pair.out -->
```text
i = 3, j = 4
stopped at i = 3, j = 4
```

`exit outer`로 반복문 밖에 나왔으므로 `i`와 `j`는 찾은 값을 그대로 가진다. 이름 없이 `exit`만 썼다면 안쪽 반복문만 끝나고 바깥 반복문은 계속된다. 이름은 `if` 구문에도 붙일 수 있다([8장](../08-conditionals/)).

## do concurrent

`do concurrent (i = 1:n)`은 각 반복이 서로 영향을 주지 않으니 어떤 순서로 실행해도 된다고 컴파일러에 알리는 반복문이다. 표준은 반복을 임의의 순서로 실행할 수 있다고 정하고(11.1.7.4.3), 이 구문 안에서 이 구문이나 바깥 구문을 벗어나는 `exit`를 쓰지 못하게 한다(11.1.12). 컴파일러는 이 약속을 바탕으로 반복의 실행 순서를 자유롭게 정할 수 있다. 아래 예제의 배열 `sq`는 [10장](../10-arrays/)에서 다룬다.

<!-- file: ch09/concurrent_squares.f90 -->
```fortran
program concurrent_squares
  implicit none
  integer :: i
  integer :: sq(5)

  do concurrent (i = 1:5)
    sq(i) = i**2
  end do
  print '(5i4)', sq
end program concurrent_squares
```

<!-- output: ch09/concurrent_squares.out -->
```text
   1   4   9  16  25
```

반복이 서로 값을 주고받는 경우에는 쓰지 않는다. 이 가이드는 소개만 하고 더 다루지 않는다.

## 흔한 실수

- 반복 변수를 반복 안에서 바꾼다. 컴파일 오류가 나거나, 컴파일러가 잡지 못하는 경우에는 표준을 어긴 코드가 된다.
- 조건 없는 `do`에 `exit`를 빠뜨려 프로그램이 끝나지 않는다.
- 안쪽 반복문의 `exit`가 바깥 반복문도 벗어난다고 생각한다. 바깥 반복문을 벗어나려면 이름을 붙인다.
- 반복 도중 끝값 변수를 바꾸면 횟수가 달라진다고 생각한다. 횟수는 `do` 문을 실행할 때 한 번만 정해진다.
- 반복 변수를 실수로 선언한다. 정수로 반복하고 실수 값은 안에서 계산한다.
- 옛 코드의 `do 10 i = 1, n`과 `10 continue` 꼴은 문번호로 반복의 끝을 표시한다. 새 코드에는 `end do`를 쓰고, 옛 꼴은 [부록 A](../21-legacy-code/)에서 다룬다.
