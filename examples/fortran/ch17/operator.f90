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
