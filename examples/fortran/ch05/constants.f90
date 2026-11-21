program constants
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp), parameter :: pi = 4.0_dp * atan(1.0_dp)
  real(dp), parameter :: two_pi = 2.0_dp * pi
  integer, parameter :: n = 5
  real(dp) :: r, area

  r = 1.5_dp
  area = pi * r**2
  print '(a, f18.15)', 'pi     = ', pi
  print '(a, f18.15)', 'two_pi = ', two_pi
  print '(a, f8.4)', 'area   = ', area
  print '(a, i0)', 'n      = ', n
end program constants
