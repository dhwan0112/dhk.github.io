module geometry
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp), parameter :: pi = 3.14159265358979324_dp

contains

  function circle_area(r) result(area)
    real(dp), intent(in) :: r
    real(dp) :: area

    area = pi * r**2
  end function circle_area
end module geometry
