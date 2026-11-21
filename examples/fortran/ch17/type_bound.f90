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
