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
