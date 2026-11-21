---
title: 파생 타입
order: 17
permalink: /fortran/17-derived-types/
---

이 장에서는 여러 값을 하나로 묶는 파생 타입(derived type)을 다룬다. 타입 정의와 성분, 모듈에 타입과 프로시저를 함께 두는 방법, 타입 결합 프로시저, 연산자 오버로딩, 입출력을 설명한다.

## 타입 정의와 성분

점 하나는 좌표 두 개로 이루어진다. `x`와 `y`를 따로 변수로 두면 점이 여러 개일 때 변수 이름이 늘고, 프로시저에 넘길 인수도 늘어난다. 파생 타입은 이런 값들을 하나의 타입으로 묶는다. 묶은 값 하나하나를 성분(component)이라 하고, 객체 뒤에 `%`를 붙여 이름으로 고른다.

<!-- file: ch17/point.f90 -->
```fortran
program point_demo
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  type :: point
    real(dp) :: x = 0.0_dp
    real(dp) :: y = 0.0_dp
  end type point

  type(point) :: p, q, pts(3)

  q = point(1.5_dp, -2.0_dp)
  p = point(y=4.0_dp)
  pts(2) = q
  pts(3)%x = 7.0_dp

  print '(a, 2f6.2)', 'p: ', p%x, p%y
  print '(a, 2f6.2)', 'q: ', q%x, q%y
  print '(a, 3f6.2)', 'pts%x: ', pts%x
  print '(a, 3f6.2)', 'pts%y: ', pts%y
end program point_demo
```

<!-- output: ch17/point.out -->
```text
p:   0.00  4.00
q:   1.50 -2.00
pts%x:   0.00  1.50  7.00
pts%y:   0.00 -2.00  0.00
```

`type :: point`부터 `end type point`까지가 타입 정의다. 정의 안의 성분 선언은 보통의 변수 선언과 같고, `= 0.0_dp`는 기본 초기값이다. 이 타입의 변수를 만들면 성분이 기본 초기값으로 시작한다(Fortran 2018 7.5.4.6). 실행하기 전에 `p`, `q`, `pts`의 성분은 모두 `0.0`이다.

타입 이름과 같은 이름의 구조 생성자(structure constructor)로 값을 만든다. `point(1.5_dp, -2.0_dp)`는 성분을 선언한 순서대로 값을 준다. `point(y=4.0_dp)`처럼 성분 이름을 쓰면 순서와 상관없이 일부만 줄 수 있다. 값을 주지 않은 성분은 기본 초기값이 있어야 한다(7.5.10 C799). 위치로 준 값 뒤에 키워드를 쓸 수 있고, 키워드 뒤에 위치로 준 값을 쓸 수는 없다.

파생 타입의 배열은 보통의 배열처럼 쓴다. `pts(2) = q`는 배열 원소 하나에 점을 대입한다. `pts(3)%x`는 셋째 점의 `x` 성분이다. `pts%x`는 배열 전체에서 `x` 성분만 모은 길이 3의 배열이다. 일반 배열처럼 `sum(pts%x)` 같은 식에 쓸 수 있다.

같은 타입의 변수끼리는 `b = a`처럼 한 번에 대입한다. 성분을 하나씩 복사하는 것과 같다.

## 중첩과 할당 가능 성분

성분의 타입은 다른 파생 타입이어도 되고, `allocatable` 배열이어도 된다. 파생 타입을 쓰는 프로그램은 타입을 `use`로 가져와야 하므로, 아래는 타입을 모듈에 두었다.

<!-- file: ch17/nested.f90 -->
```fortran
module particles
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  type :: vec3
    real(dp) :: x = 0.0_dp, y = 0.0_dp, z = 0.0_dp
  end type vec3

  type :: particle
    real(dp) :: mass = 1.0_dp
    type(vec3) :: pos
    real(dp), allocatable :: history(:)
  end type particle
end module particles

program nested
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use particles, only: particle, vec3
  implicit none
  type(particle) :: a, b

  a%mass = 2.5_dp
  a%pos = vec3(1.0_dp, 2.0_dp, 3.0_dp)
  a%history = [0.5_dp, 1.5_dp]
  b = a
  b%pos%z = -1.0_dp
  b%history(1) = 9.0_dp

  print '(a, 3f6.2)', 'a%pos: ', a%pos%x, a%pos%y, a%pos%z
  print '(a, 3f6.2)', 'b%pos: ', b%pos%x, b%pos%y, b%pos%z
  print '(a, 2f6.2)', 'a%history: ', a%history
  print '(a, 2f6.2)', 'b%history: ', b%history
end program nested
```

<!-- output: ch17/nested.out -->
```text
a%pos:   1.00  2.00  3.00
b%pos:   1.00  2.00 -1.00
a%history:   0.50  1.50
b%history:   9.00  1.50
```

`particle`의 성분 `pos`는 `vec3` 타입이다. `a%pos%z`처럼 `%`를 이어 안쪽 성분을 고른다. 성분 `history`는 할당 가능 배열이며, 할당 가능 성분은 항상 할당되지 않은 상태로 시작한다(7.5.4.6). `a%history = [0.5_dp, 1.5_dp]`는 배열 대입에서 자동으로 할당한다.

`b = a`는 `a`의 모든 성분을 `b`로 복사한다. 표준은 할당 가능 성분이 할당되어 있으면 같은 모양으로 새로 할당해 값을 복사한다고 정한다(10.2.1.3). 그래서 `b%history(1) = 9.0_dp`로 바꿔도 `a%history`는 그대로다. 성분이 포인터이면 복사가 아니라 같은 대상을 가리키게 된다. 이 가이드는 포인터를 다루지 않는다.

## 모듈에 타입과 프로시저 두기

타입을 다루는 프로시저는 타입과 같은 모듈에 둔다. 이 모듈을 `use`하면 타입과 프로시저가 함께 들어오고, 프로시저의 인터페이스는 명시적이다.

<!-- file: ch17/geometry.f90 -->
```fortran
module geometry
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  type :: point
    real(dp) :: x = 0.0_dp
    real(dp) :: y = 0.0_dp
  end type point

contains

  function distance(a, b) result(d)
    type(point), intent(in) :: a, b
    real(dp) :: d

    d = sqrt((a%x - b%x)**2 + (a%y - b%y)**2)
  end function distance
end module geometry

program geometry_demo
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use geometry, only: point, distance
  implicit none
  type(point) :: path(3)
  integer :: i

  path = [point(0.0_dp, 0.0_dp), point(3.0_dp, 4.0_dp), point(3.0_dp, 5.0_dp)]
  do i = 1, size(path) - 1
    print '(a, i0, a, f5.2)', 'segment ', i, ': ', distance(path(i), path(i + 1))
  end do
end program geometry_demo
```

<!-- output: ch17/geometry.out -->
```text
segment 1:  5.00
segment 2:  1.00
```

타입 정의는 한 곳에만 둔다. 서로 다른 곳에 같은 이름과 같은 성분으로 정의하면 컴파일러는 두 타입을 다른 타입으로 취급한다(7.5.2.4). 두 모듈에 같은 `t`를 정의해 `p = q`를 쓰면 gfortran 15.2는 `Cannot convert TYPE(t) to TYPE(t)`라고 알려 준다. 모든 곳이 같은 모듈에서 타입을 가져오면 이 문제가 없다.

## 타입 결합 프로시저

타입 정의 안의 `contains` 뒤에 `procedure` 문으로 프로시저를 이름 붙여 묶을 수 있다. 이를 타입 결합 프로시저(type-bound procedure)라고 한다. 객체 뒤에 `%`와 이름을 붙여 부른다.

<!-- file: ch17/type_bound.f90 -->
```fortran
module vectors
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  private
  public :: vec2

  type :: vec2
    real(dp) :: x = 0.0_dp
    real(dp) :: y = 0.0_dp
  contains
    procedure :: norm
    procedure :: scale
  end type vec2

contains

  function norm(this) result(r)
    class(vec2), intent(in) :: this
    real(dp) :: r

    r = sqrt(this%x**2 + this%y**2)
  end function norm

  subroutine scale(this, factor)
    class(vec2), intent(inout) :: this
    real(dp), intent(in) :: factor

    this%x = factor * this%x
    this%y = factor * this%y
  end subroutine scale
end module vectors

program type_bound
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use vectors, only: vec2
  implicit none
  type(vec2) :: v

  v = vec2(3.0_dp, 4.0_dp)
  print '(a, f6.2)', 'norm:  ', v%norm()
  call v%scale(2.0_dp)
  print '(a, 2f6.2)', 'v:     ', v%x, v%y
  print '(a, f6.2)', 'norm:  ', v%norm()
end program type_bound
```

<!-- output: ch17/type_bound.out -->
```text
norm:    5.00
v:       6.00  8.00
norm:   10.00
```

`v%norm()`은 `v`를 첫째 인수로 하는 `norm(v)` 호출이다. 타입 결합 프로시저의 첫째 가인수를 전달 객체 가인수(passed-object dummy argument)라고 하며, 호출에 쓴 객체가 여기에 결합한다(7.5.4.5). 이 가이드의 예제는 이 가인수를 `this`로 부른다. 이름은 관례일 뿐 표준이 정한 이름이 아니다. 전달 객체 가인수는 `type(vec2)`가 아니라 `class(vec2)`로 선언한다(C760). `class`는 이 타입이나 이 타입을 확장한 타입의 객체를 받는다는 뜻이다. 이 가이드는 타입 확장을 다루지 않으므로 `class(타입이름)`을 선언 방법 그대로 쓴다.

`procedure :: norm`은 같은 이름의 모듈 프로시저 `norm`을 연결한다(7.5.5). 서브루틴도 같은 방식이다. `call v%scale(2.0_dp)`가 `v`를 바꾼다. 가인수가 `intent(inout)`이기 때문이다.

타입 결합 프로시저를 쓰면 타입을 `use`하는 것만으로 프로시저도 따라온다. 모듈에 타입과 프로시저를 따로 두는 방식(`distance(a, b)`)과 기능은 같고, 타입에 속한 동작이라는 점이 코드에 드러난다.

## 연산자 오버로딩

`a + b`를 파생 타입에도 쓰려면 `interface operator(+)`에 함수를 연결한다. 함수는 `intent(in)` 가인수 두 개를 받아 결과를 돌려주는 모양이어야 한다(15.4.3.4.2). 두 피연산자가 순서대로 두 가인수에 대응한다.

<!-- file: ch17/operator.f90 -->
```fortran
module vectors
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  type :: vec2
    real(dp) :: x = 0.0_dp
    real(dp) :: y = 0.0_dp
  end type vec2

  interface operator(+)
    module procedure add_vec2
  end interface operator(+)

contains

  function add_vec2(a, b) result(c)
    type(vec2), intent(in) :: a, b
    type(vec2) :: c

    c = vec2(a%x + b%x, a%y + b%y)
  end function add_vec2
end module vectors

program operator_demo
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use vectors, only: vec2, operator(+)
  implicit none
  type(vec2) :: a, b, c

  a = vec2(1.0_dp, 2.0_dp)
  b = vec2(0.5_dp, -3.0_dp)
  c = a + b
  print '(a, 2f6.2)', 'c: ', c%x, c%y
end program operator_demo
```

<!-- output: ch17/operator.out -->
```text
c:   1.50 -1.00
```

`use vectors, only: vec2, operator(+)`처럼 `only`에도 `operator(+)`를 따로 적어야 연산자를 가져온다. 내장 타입끼리의 `+`는 그대로이고, `vec2` 둘의 `+`에만 새 뜻이 더해진다.

연산자는 코드를 간결하게 하지만 무엇을 뜻하는지 읽는 사람이 짐작할 수 있을 때만 쓴다. 벡터의 `+`처럼 수학의 뜻과 같을 때가 알맞다.

## 입출력

파생 타입 변수를 서식 있는 입출력(`print`, `write`, `read`)의 목록에 쓰면 성분이 선언한 순서대로 하나씩 나열한 것과 같다. 이때 성분이 모두 접근 가능해야 하고 포인터나 할당 가능 성분이 없어야 한다(12.6.3). 배열이면 원소마다 성분이 이어진다.

<!-- file: ch17/derived_io.f90 -->
```fortran
program derived_io
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  type :: sample
    integer :: id = 0
    real(dp) :: value = 0.0_dp
  end type sample

  type(sample) :: s(2)

  s(1) = sample(1, 0.25_dp)
  s(2) = sample(2, 1.75_dp)
  print '(i3, f7.2)', s
  print '(a, i0, a, f5.2)', 'second: id=', s(2)%id, ' value=', s(2)%value
end program derived_io
```

<!-- output: ch17/derived_io.out -->
```text
  1   0.25
  2   1.75
second: id=2 value= 1.75
```

`print '(i3, f7.2)', s`는 두 점을 한 번에 출력한다. `s(1)`의 `id`와 `value`, `s(2)`의 `id`와 `value` 네 값이 나열되고, 형식 `(i3, f7.2)`를 두 번 쓰므로 두 줄이 된다. 형식은 성분의 타입과 순서에 맞춰야 한다. 성분이 많은 타입은 위의 `s(2)%id`처럼 필요한 성분만 골라 출력하는 편이 안전하다.

서식 없는(unformatted) 입출력에서는 파생 타입 객체가 컴파일러가 정한 형태의 값 하나로 취급된다(12.6.3). 파일에 타입째로 쓴 값을 다른 컴파일러에서 읽을 수 있다고 기대하지 않는다.

할당 가능 성분이 있는 타입을 목록 지시 입출력의 목록에 쓰면 컴파일 오류다.

<!-- file: ch17/alloc_io_error.f90 -->
```fortran
program alloc_io_error
  implicit none

  type :: series
    integer :: n = 0
    real, allocatable :: values(:)
  end type series

  type(series) :: s

  s%n = 2
  s%values = [1.0, 2.0]
  print *, s
end program alloc_io_error
```

gfortran 15.2의 메시지는 다음과 같다.

```text
alloc_io_error.f90:13:12:

   13 |   print *, s
      |            1
Error: Data transfer element at (1) cannot have ALLOCATABLE components unless it is processed by a defined input/output procedure
```

이 경우에는 `print *, s%n, s%values`처럼 성분을 직접 나열한다.

## 흔한 실수

- 타입을 정의하는 모듈을 `use`하지 않고 쓴다. gfortran 15.2는 `Derived type ‘point’ at (1) is being used before it is defined` 오류를 낸다.
- 같은 타입을 여러 곳에 복사해 정의한다. 이름이 같아도 서로 다른 타입이다.
- 구조 생성자에 성분 수나 순서를 틀리게 준다. 키워드로 이름을 쓰면 순서 실수를 줄일 수 있다.
- 타입 결합 프로시저의 전달 객체 가인수를 `type(...)`로 선언한다. `class(...)`여야 한다.
- 할당 가능 성분이 있는 객체를 `print`에 그대로 쓴다.
