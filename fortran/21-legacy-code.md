---
title: 레거시 코드 읽는 법
order: 21
permalink: /fortran/21-legacy-code/
---

이 부록은 Fortran 77 시대의 코드를 읽을 때 만나는 문법을 설명한다. 이 장의 문법은 옛 코드를 이해하고 현대 문법으로 옮기기 위한 것이고, 새 코드에는 쓰지 않는다. 새 코드는 본문의 자유 형식, 모듈, 구문으로 쓴다.

예제는 모두 `-std=f2018 -Wall -Wextra`로 컴파일한다. gfortran은 이 옵션에서 폐기 예정 기능에 경고를 내고 삭제된 기능에는 오류를 낸다. 이 장의 예제는 그 경고를 일부러 남겨 두었고, 각 경고가 어떤 문법을 가리키는지 읽는 것이 목적이다.

## 고정 형식

고정 형식(fixed source form)은 문장의 각 부분이 놓이는 열이 정해진 소스 형식이다. gfortran은 확장자가 `.f`인 파일을 고정 형식으로 읽는다.

| 열 | 내용 |
|---|---|
| 1 | 비어 있거나 `c`, `C`, `*`이면 그 줄 전체가 주석이다. |
| 1-5 | 문번호(선택) |
| 6 | 비어 있거나 `0`이면 새 문장이고, 그 밖의 문자이면 앞 줄에서 이어지는 줄이다. |
| 7-72 | 문장 |
| 73-80 | 일련번호(선택). 컴파일러가 읽지 않는다. |

열 1의 `c`와 `*`, 열 1-5의 문번호, 열 6의 이어쓰기 문자, 7-72열의 문장, `!`로 시작하는 주석은 Fortran 2018 표준의 6.3.3절이 정한 규칙이다. 다음은 3장의 `circle` 프로그램을 고정 형식으로 쓴 것이다.

<!-- file: ch21/columns.f -->
```fortran
c Area of a circle: the layout of a fixed form source file.
      program columns
      real r, area
      r = 2.0
      area = 3.14159265358979
     +       * r * r
      write (*,'(a,f8.4)') 'Area = ', area
      end
```

<!-- output: ch21/columns.out -->
```text
Area =  12.5664
```

첫 줄의 `c`가 주석 표시이고, `area` 대입문은 6열의 `+`로 다음 줄에 이어진다. 이어쓰기 문자는 공백과 `0`이 아니면 무엇이든 되고, `+`, `&`, 숫자를 많이 썼다. 옛 코드는 대문자로 쓴 것이 많은데, Fortran은 대소문자를 구별하지 않으므로 `PROGRAM`과 `program`은 같다. 고정 형식에서는 공백이 문자열 밖에서 의미가 없다.

### 72열을 넘으면 잘린다

72열 뒤는 컴파일러가 읽지 않는다. 원본이 흔한 오류로 꼽은 문제다. 문장이 72열을 넘으면 넘은 부분이 사라지고, 남은 부분이 문법에 맞으면 오류 없이 다른 값이 된다.

<!-- file: ch21/truncated.f -->
```fortran
      program truncated
      real grand_total
      grand_total = 1.0 + 20.0 + 300.0 + 4000.0 + 50000.0 + 600000.0 + 7000000.0
      write (*,'(f12.1)') grand_total
      end
```

`7000000.0`의 첫 글자가 72열이라서 대입문은 `... + 7`로 읽힌다. gfortran 15.2는 경고를 내지만 컴파일은 끝난다.

```text
truncated.f:3:72:

    3 |       grand_total = 1.0 + 20.0 + 300.0 + 4000.0 + 50000.0 + 600000.0 + 7000000.0
      |                                                                        1
Warning: Line truncated at (1) [-Wline-truncation]
```

<!-- output: ch21/truncated.out -->
```text
    654328.0
```

합이 `7654321.0`이 되어야 하는데 `654328.0`이 나온다. `-Wall`의 `-Wline-truncation`이 이 경고를 낸다. 경고를 무시하지 않는다. 옛 코드가 80열까지 쓴 것이면 `-ffixed-line-length-none`이나 `-ffixed-line-length-80`처럼 줄 길이를 늘려 컴파일한다. 이 옵션으로 `truncated.f`를 컴파일하면 `7654321.0`이 나온다. 자유 형식으로 옮길 때까지만 쓴다.

## 암시적 타입 지정

옛 코드에는 `implicit none`이 없어서 선언하지 않은 이름이 첫 글자로 타입이 정해진다. `i`부터 `n`까지는 `integer`, 나머지는 `real`이다(Fortran 2018 8.7절). `implicit` 문은 이 규칙을 바꾼다. `implicit double precision (a-h, o-z)`는 `a`-`h`와 `o`-`z`로 시작하는 이름을 배정밀도로 만든다. `implicit none`은 규칙을 끈다.

<!-- file: ch21/implicit_rules.f -->
```fortran
      program implicit_rules
      kount = 7
      avg = kount / 2
      ratio = kount / 2.0
      write (*,'(2f6.2)') avg, ratio
      end
```

<!-- output: ch21/implicit_rules.out -->
```text
  3.00  3.50
```

`kount`는 `k`로 시작해서 정수이고 `avg`는 `a`로 시작해서 실수다. `kount / 2`가 정수 나눗셈이므로 `avg`에는 `3.0`이 들어가고, 실수와 나누는 `ratio`는 `3.5`다. 이름 하나를 잘못 쳐도 새 변수가 생기므로 옛 코드를 읽을 때는 선언이 없는 이름의 타입을 첫 글자로 따져 본다. 옛 코드에 `implicit none`을 일일이 넣기 전에 `-fimplicit-none`을 주면 선언이 빠진 이름이 오류로 드러난다.

## 문번호와 do 반복문

문번호는 1-5열에 쓴 정수로, 값에는 의미가 없고 같은 프로그램 단위 안에서 겹치지만 않으면 된다. 문번호를 `do`가 끝나는 문에 붙이면 반복문이 된다. `continue`는 아무것도 하지 않는 문으로, 문번호를 달아 둘 자리로 쓰인다. 문번호를 쓰는 `do`와 `goto`로 만든 반복문은 다음과 같다.

<!-- file: ch21/old_loops.f -->
```fortran
      program old_loops
      integer i, n, total
      total = 0
      do 10 i = 1, 4
         total = total + i
   10 continue
      write (*,'(a,i3)') 'sum =', total
      n = 1
   20 if (n .le. 100) then
         write (*,'(i4)') n
         n = 2*n
         goto 20
      endif
   30 continue
         n = n - 50
      if (n .gt. 0) goto 30
      write (*,'(a,i4)') 'n =', n
      end
```

<!-- output: ch21/old_loops.out -->
```text
sum = 10
   1
   2
   4
   8
  16
  32
  64
n = -22
```

- `do 10 i = 1, 4`는 `10 continue`까지 `i`를 1부터 4까지 반복한다. 오늘의 `do i = 1, 4`와 `end do`에 해당한다.
- `20 if (...) then` 뒤에서 `goto 20`으로 돌아가는 구조가 while 반복이다. 조건이 참인 동안 본문을 실행한다.
- `30 continue`로 시작해서 끝에서 `if (...) goto 30`으로 돌아가는 구조가 until 반복이다. 본문을 한 번 실행한 뒤 조건을 검사하며, 반복을 계속하는 조건이라서 until의 종료 조건을 뒤집은 것이다.

gfortran은 `do 10`에 경고를 낸다.

```text
old_loops.f:4:72:

    4 |       do 10 i = 1, 4
      |                                                                        1
Warning: Fortran 2018 obsolescent feature: Labeled DO statement at (1)
```

문번호를 쓰는 `do`는 Fortran 2018에서 폐기 예정 기능이다. 표준은 이 문번호가 구문 이름과 중복이고 제한 없는 분기를 허락하며, 주된 용도인 반복 건너뛰기는 `cycle`이 더 분명하다고 설명한다(표준 부속서 B.3.10). 현대 문법으로는 `do`, `do while`, `exit`로 쓰고, 세 반복문의 출력이 같다.

<!-- file: ch21/modern_loops.f90 -->
```fortran
program modern_loops
  implicit none
  integer :: i, n, total

  total = 0
  do i = 1, 4
    total = total + i
  end do
  print '(a, i3)', 'sum =', total

  n = 1
  do while (n <= 100)
    print '(i4)', n
    n = 2 * n
  end do

  do
    n = n - 50
    if (n <= 0) exit
  end do
  print '(a, i4)', 'n =', n
end program modern_loops
```

<!-- output: ch21/modern_loops.out -->
```text
sum = 10
   1
   2
   4
   8
  16
  32
  64
n = -22
```

### 삭제된 기능

더 옛날 형태는 Fortran 2018에서 아예 삭제되었다. gfortran은 `-std=f2018`에서 다음 오류를 낸다.

| 옛 문법 | 메시지 |
|---|---|
| 정수가 아닌 `do` 변수 `do 10 x = 1.0, 3.0` | `Deleted feature: Loop variable at (1) must be integer` |
| 비블록 `do`. `do 10 i = 1, 3`이 `10 print *, 'end'`처럼 `continue`나 `end do`가 아닌 문으로 끝난다. | `Fortran 2018 deleted feature: DO termination statement which is not END DO or CONTINUE with label 10` |
| `pause` | `Deleted feature: PAUSE statement` |
| `assign 10 to k`, `goto k` | `Deleted feature: ASSIGN statement`, `Deleted feature: Assigned GOTO statement` |
| 산술 `if` | `Fortran 2018 deleted feature: Arithmetic IF statement` |

정수가 아닌 `do` 변수, `pause`, `assign`, `H` 편집 기술자는 Fortran 90에 있던 기능으로 Fortran 95에서 삭제되었고(표준 부속서 B.1), 산술 `if`와 비블록 `do`는 Fortran 2008에 있던 기능으로 Fortran 2018에서 삭제되었다(표준 부속서 B.2). `5Hhello` 같은 `H` 편집 기술자는 gfortran이 경고(`The H format specifier at (1) is a Fortran 95 deleted feature`)만 낸다.

## goto 문

### 계산된 goto

계산된 goto(computed GO TO)는 `goto (10, 20, 30) k`처럼 정수 식의 값에 따라 목록의 문번호로 분기한다. 값이 1이면 첫 문번호, 2이면 둘째 문번호로 가고, 목록 밖이면 분기하지 않고 다음 문장으로 간다.

<!-- file: ch21/computed_goto.f -->
```fortran
      program computed_goto
      integer k
      do k = 1, 4
         goto (10, 20, 30) k
         write (*,'(i2,a)') k, ' other'
         goto 50
   10    write (*,'(i2,a)') k, ' first'
         goto 50
   20    write (*,'(i2,a)') k, ' second'
         goto 50
   30    write (*,'(i2,a)') k, ' third'
   50    continue
      end do
      end
```

<!-- output: ch21/computed_goto.out -->
```text
 1 first
 2 second
 3 third
 4 other
```

`k = 4`는 목록 밖이므로 `other`가 나온다. gfortran 15.2의 경고는 다음과 같다.

```text
computed_goto.f:4:72:

    4 |          goto (10, 20, 30) k
      |                                                                        1
Warning: Obsolescent feature: Computed GOTO at (1)
```

계산된 goto는 `select case`로 대체되었다(표준 부속서 B.3.3). 현대 문법으로는 `case default`가 목록 밖의 값을 맡는다.

<!-- file: ch21/modern_select.f90 -->
```fortran
program modern_select
  implicit none
  integer :: k

  do k = 1, 4
    select case (k)
    case (1)
      print '(i2, a)', k, ' first'
    case (2)
      print '(i2, a)', k, ' second'
    case (3)
      print '(i2, a)', k, ' third'
    case default
      print '(i2, a)', k, ' other'
    end select
  end do
end program modern_select
```

<!-- output: ch21/modern_select.out -->
```text
 1 first
 2 second
 3 third
 4 other
```

### 산술 if

산술 `if (n) 10, 20, 30`은 `n`이 음수, 0, 양수일 때 각각 다른 문번호로 간다. Fortran 2018에서 삭제되었으므로 `-std=f2018`에서는 컴파일되지 않는다.

<!-- file: ch21/arith_if.f -->
```fortran
      program arith_if
      integer n
      n = -2
      if (n) 10, 20, 30
   10 write (*,*) 'negative'
      goto 40
   20 write (*,*) 'zero'
      goto 40
   30 write (*,*) 'positive'
   40 continue
      end
```

```text
arith_if.f:4:72:

    4 |       if (n) 10, 20, 30
      |                                                                        1
Error: Fortran 2018 deleted feature: Arithmetic IF statement at (1)
```

`if (n < 0) then ... else if (n == 0) then ... else ... end if`로 쓴다([8장](/fortran/08-conditionals/)). 옛 코드를 그대로 빌드해야 하면 `-std=legacy`를 쓴다(아래).

### 대체 복귀

`call subr (x, y, z, *100, *200)`처럼 인수 목록에 `*100`을 쓰는 대체 복귀(alternate return)도 폐기 예정 기능이다. 표준은 반환 코드를 인수로 돌려받아 `select case`로 분기하라고 설명한다(표준 부속서 B.3.2).

## common 블록

common 블록은 여러 프로그램 단위가 변수를 공유하게 하는 옛 방법이다. 블록에 이름을 붙이고 변수 목록을 쓰면, 같은 이름의 블록을 선언한 모든 곳에서 같은 기억 장소를 본다. 블록 안의 변수는 이름이 아니라 위치로 짝지어진다. 표준은 같은 이름의 common 블록이 모두 같은 첫 기억 단위에서 시작한다고 정한다(8.10.2.4절).

<!-- file: ch21/common_swap.f -->
```fortran
      program common_swap
      real alpha, beta
      common /coeff/ alpha, beta
      alpha = 1.0
      beta = 2.0
      call sub4
      end

      subroutine sub4
      real alpha, beta
      common /coeff/ beta, alpha
      write (*,'(a,f4.1,a,f4.1)') 'alpha = ', alpha, ', beta = ', beta
      end
```

<!-- output: ch21/common_swap.out -->
```text
alpha =  2.0, beta =  1.0
```

주 프로그램은 `alpha = 1.0`, `beta = 2.0`을 대입했다. `sub4`는 같은 블록을 `beta, alpha` 순서로 선언했으므로 `alpha`가 주 프로그램의 `beta`를 읽는다. 둘 다 `real`이어서 컴파일러도 막지 않고, 값만 바뀐 채 실행된다. 원본이 지적한 위험이다. 비슷한 선언을 보았는데 순서가 다르면 오타일 가능성이 크다.

다음은 gfortran 15.2의 경고다.

```text
common_swap.f:3:20:

    3 |       common /coeff/ alpha, beta
      |                    1
Warning: Fortran 2018 obsolescent feature: COMMON block at (1)
```

common 블록에 배열을 넣으면 크기도 모든 곳에서 같아야 하므로 `parameter`로 정한 상수 `nmax`를 모든 프로그램 단위에 똑같이 적어야 한다. 원본은 그래서 common 블록 대신 배열을 선행 차원과 함께 인수로 넘기라고 했다. 표준은 common 블록이 모듈로 대체되었고 오류가 잦다고 설명한다(표준 부속서 B.3.11). 현대 문법에서는 값을 인수로 넘기거나 모듈에 둔다.

<!-- file: ch21/modern_common.f90 -->
```fortran
module coefficients
  implicit none
contains
  subroutine show(alpha, beta)
    real, intent(in) :: alpha, beta

    print '(a, f4.1, a, f4.1)', 'alpha = ', alpha, ', beta = ', beta
  end subroutine show
end module coefficients

program modern_common
  use coefficients, only: show
  implicit none
  real :: alpha, beta

  alpha = 1.0
  beta = 2.0
  call show(alpha, beta)
end program modern_common
```

<!-- output: ch21/modern_common.out -->
```text
alpha =  1.0, beta =  2.0
```

모듈 프로시저는 가인수의 타입과 `intent`를 컴파일러가 알고 있으므로 인수 순서가 틀려 타입이 어긋나면 오류가 난다. 같은 타입이면 호출문에서 순서를 눈으로 확인할 수 있다. 공유할 상수는 모듈의 `parameter`로, 바뀌는 상태는 파생 타입으로 둔다([16장](/fortran/16-modules/), [17장](/fortran/17-derived-types/)).

## data 문과 block data

`data` 문은 실행 전에 변수의 초기값을 정한다. `data m/10/, x/2.5/`처럼 변수 목록 뒤에 값을 `/` 사이에 쓰고, `3*100.0`은 `100.0`을 세 번 반복한다. 표준은 `data`로 초기화한 이름 붙은 변수(common 블록의 변수 제외)가 `save` 속성을 가진다고 정한다(8.6.7절). 현대 코드는 선언에서 초기화한다([5장](/fortran/05-variables/)). 실행문 사이에 `data` 문을 두는 것도 폐기 예정 기능이다(표준 부속서 B.3.5).

`data` 문으로는 common 블록의 변수를 초기화할 수 없다. 표준은 이 일을 하는 프로그램 단위로 `block data`를 두었다(14.3절). `block data` 밖에서 `data`로 common 블록의 변수를 초기화하면 gfortran은 `-std=f2018`에서 `GNU Extension: initialization of common block variable` 오류를 낸다.

<!-- file: ch21/block_data.f -->
```fortran
      block data init
      real v(3), alpha
      common /vector/ v, alpha
      data v /3*100.0/, alpha /3.14/
      end

      program use_block_data
      real v(3), alpha
      common /vector/ v, alpha
      write (*,'(4f8.2)') v, alpha
      end
```

<!-- output: ch21/block_data.out -->
```text
  100.00  100.00  100.00    3.14
```

`block data init`은 `/vector/` 블록의 `v`와 `alpha`를 정한다. 주 프로그램은 이 블록을 선언만 하고 값은 `block data`가 이미 넣어 두었다. gfortran은 `block data`와 `common`에 각각 경고를 낸다.

```text
block_data.f:1:16:

    1 |       block data init
      |                1
Warning: Fortran 2018 obsolescent feature: BLOCK DATA construct at (1)
```

표준은 `block data`가 common 블록을 위해서만 존재하므로 common이 모듈로 대체되면 필요 없다고 설명한다(표준 부속서 B.3.11).

## equivalence

`equivalence`는 서로 다른 이름이 같은 기억 장소를 가리키게 한다. 메모리를 아끼거나 한 배열을 다른 이름으로 읽을 때 썼다.

<!-- file: ch21/equiv_overlay.f -->
```fortran
      program equiv_overlay
      real a(4), x, y
      equivalence (a(1), x), (a(2), y)
      a(1) = 1.5
      a(2) = 2.5
      write (*,'(2f6.1)') x, y
      end
```

<!-- output: ch21/equiv_overlay.out -->
```text
   1.5   2.5
```

`x`와 `y`는 `a(1)`과 `a(2)`와 같은 기억 장소다. 이름 하나를 바꾸면 다른 이름의 값도 바뀌므로 읽기 어렵고, 표준은 오류가 잦고 성능을 해칠 수 있다고 설명한다(표준 부속서 B.3.11). 옛 코드를 옮길 때는 별개의 변수나 배열 원소로 바꾼다.

## 옛 타입 선언

`double precision`은 표준에 있는 타입이고 폐기 예정도 아니다. 상수는 `1.0d0`처럼 지수를 `d`로 쓴다. 현대 코드는 kind 매개변수로 정밀도를 정한다([5장](/fortran/05-variables/), [18장](/fortran/18-style/)).

`real*8`처럼 타입 뒤에 바이트 수를 붙이는 형태는 표준이 아니다.

<!-- file: ch21/real8.f -->
```fortran
      program real8
      real*8 x
      x = 1.0d0 / 3.0d0
      write (*,'(f12.9)') x
      end
```

`-std=f2018`에서는 컴파일되지 않는다.

```text
real8.f:2:13:

    2 |       real*8 x
      |             1
Error: GNU Extension: Nonstandard type declaration REAL*8 at (1)
```

`character*8 name`처럼 문자열 길이를 `*` 뒤에 쓰는 형태는 표준에 있지만 폐기 예정이다(표준 부속서 B.3.8). `character(len=8)`과 같은 뜻이다.

<!-- file: ch21/char_star.f -->
```fortran
      program char_star
      character*8 name
      double precision x
      name = 'Fortran'
      x = 1.0d0 / 3.0d0
      write (*,'(a,f12.9)') name, x
      end
```

<!-- output: ch21/char_star.out -->
```text
Fortran  0.333333333
```

`name`에는 길이 8에 맞추어 `'Fortran'` 뒤에 공백 한 칸이 붙으므로 출력에서 `Fortran`과 숫자 사이에 공백이 두 칸 보인다. 경고는 다음과 같다.

```text
char_star.f:2:18:

    2 |       character*8 name
      |                  1
Warning: Obsolescent feature: Old-style character length at (1)
```

## 가정 크기 배열

옛 코드의 부프로그램은 배열 크기를 모르는 채로 받아서 크기를 따로 인수로 넘겼다. 마지막 차원을 `*`로 쓴 가정 크기 배열(assumed-size array)이 이 일을 한다. 다음 `total`은 `v(*)`와 `n`을 받고, `old_total`은 `v(1)`을 쓴다.

<!-- file: ch21/assumed_size.f -->
```fortran
      program assumed_size
      real x(5), total, old_total
      integer i
      do i = 1, 5
         x(i) = i
      end do
      write (*,'(2f6.1)') total(x, 5), old_total(x, 5)
      end

      real function total(v, n)
      integer n, i
      real v(*)
      total = 0.0
      do i = 1, n
         total = total + v(i)
      end do
      end

      real function old_total(v, n)
      integer n, i
      real v(1)
      old_total = 0.0
      do i = 1, n
         old_total = old_total + v(i)
      end do
      end
```

<!-- output: ch21/assumed_size.out -->
```text
  15.0  15.0
```

`v(1)`처럼 크기를 `1`로 선언하는 것은 "크기를 신경 쓰지 않는다"는 옛 관례다. 결과는 같아 보이지만 `-fcheck=bounds`를 주면 실행이 멈춘다.

```text
At line 24 of file assumed_size.f
Fortran runtime error: Index '2' of dimension 1 of array 'v' above upper bound of 1
```

`v(*)`는 첨자가 범위를 벗어나는지 컴파일러가 알 수 없으므로 검사하지 못한다. 현대 코드는 크기를 함께 전달하는 가정 형상 배열 `v(:)`를 모듈 프로시저에 쓴다([15장](/fortran/15-arrays-in-subprograms/)).

## 문 함수와 entry

문 함수(statement function)는 한 줄로 쓰는 함수다. `f(x) = a*x + 1.0`은 함수 정의처럼 보이지만 대입문과 같은 모양이어서 혼동하기 쉽다. 표준은 폐기 예정이며 내부 프로시저가 완전히 대체한다고 설명한다(표준 부속서 B.3.4).

<!-- file: ch21/stmt_function.f -->
```fortran
      program stmt_function
      real a, f, x
      f(x) = a*x + 1.0
      a = 2.0
      write (*,'(f6.1)') f(3.0)
      end
```

<!-- output: ch21/stmt_function.out -->
```text
   7.0
```

```text
stmt_function.f:3:72:

    3 |       f(x) = a*x + 1.0
      |                                                                        1
Warning: Obsolescent feature: Statement function at (1)
```

`entry`는 한 부프로그램에 진입점을 여럿 두는 문이다. 다음에서 `counter_reset`과 `counter_next`는 지역 변수 `n`을 공유한다.

<!-- file: ch21/entry_point.f -->
```fortran
      subroutine counter_reset
      integer n, k
      save n
      n = 0
      return
      entry counter_next(k)
      n = n + 1
      k = n
      end

      program entry_point
      integer k
      call counter_reset
      call counter_next(k)
      call counter_next(k)
      write (*,'(i3)') k
      end
```

<!-- output: ch21/entry_point.out -->
```text
  2
```

```text
entry_point.f:6:25:

    6 |       entry counter_next(k)
      |                         1
Warning: Fortran 2008 obsolescent feature: ENTRY statement at (1)
```

표준은 `entry`를 모듈 프로시저로 바꾸라고 설명한다. 공유하는 데이터를 모듈의 `private` 변수로 두고 진입점마다 모듈 프로시저를 만든다(표준 부속서 B.3.9).

## -std=legacy로 옛 코드 빌드하기

`-std=f2018`은 폐기 예정 기능에 경고를 내고 비표준 확장에 오류를 내므로 옛 코드를 처음 빌드할 때는 걸리적거린다. gfortran 매뉴얼에 따르면 기본값 `-std=gnu`는 GNU 확장을 받아들이되 권하지 않는 옛 확장에는 경고를 내고, `-std=legacy`는 그 경고마저 내지 않는 모드로 옛 비표준 프로그램에 쓰기 좋다. `real8.f`는 `-std=legacy`에서 컴파일되고 `0.333333333`을 출력한다.

```sh
gfortran -std=legacy real8.f -o real8
```

`-std=legacy`는 `-fallow-argument-mismatch`를 함께 켠다. 이 옵션은 호출과 프로시저 정의의 인수가 어긋난 코드의 오류를 경고로 낮추며 매뉴얼은 쓰지 말라고 강하게 권한다. 이 모드는 옛 코드를 빌드해서 현재 동작을 기록하는 용도로만 쓴다. 새로 쓰는 코드와 고친 코드는 `-std=f2018 -Wall -Wextra`로 컴파일한다.

## 현대 문법으로 옮기는 순서

한 번에 고치지 않고 단계마다 결과를 비교한다.

1. `-std=legacy -O0 -g`로 빌드해서 대표 입력에 대한 출력을 저장한다. 이후 모든 단계에서 같은 입력의 출력을 비교한다.
2. 파일 하나씩 자유 형식으로 옮기고 확장자를 `.f90`으로 바꾼다. `c` 주석은 `!`로, 6열의 이어쓰기는 줄 끝의 `&`로 바꾼다.
3. `implicit none`을 넣고 선언을 채운다. `-fimplicit-none`이 빠진 선언을 찾아 준다.
4. 문번호 `do`, `goto`로 만든 반복문, 산술 `if`, 계산된 goto를 `do`, `do while`, `exit`, `if`, `select case`로 바꾼다.
5. common 블록, `block data`, `equivalence`를 모듈과 인수로 바꾸고 `data` 문은 선언의 초기화로 바꾼다.
6. `real*8`, `character*n`을 kind 매개변수와 `character(len=n)`으로 바꾼다.
7. 외부 프로시저를 모듈로 옮기고 `intent`를 쓴다. `v(*)`와 `v(1)`은 `v(:)`로 바꾼다. 문 함수와 `entry`는 내부 프로시저와 모듈 프로시저로 바꾼다.
8. `-std=f2018 -Wall -Wextra -fcheck=all`로 컴파일해서 경고를 0개로 만든다.

## 흔한 실수

- 옛 코드의 문법을 새 코드에 흉내 낸다. 이 장의 모든 기능은 대체 문법이 있다.
- 72열을 넘은 줄의 경고를 무시한다. 값이 말없이 바뀐다.
- common 블록의 변수 순서가 어긋난 것을 놓친다. 같은 이름 블록은 모든 곳에서 같은 순서와 타입이어야 한다.
- 한 번에 모두 고치고 결과를 비교하지 않는다. 어느 단계에서 값이 바뀌었는지 알 수 없다.
- 고정 형식 코드를 `.f90` 파일에 붙여 넣는다. 6열의 이어쓰기와 1열의 `c` 주석은 자유 형식에서 문법 오류가 된다.
