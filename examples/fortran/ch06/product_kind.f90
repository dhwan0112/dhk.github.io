program product_kind
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real :: x, y
  real(dp) :: w1, w2

  x = 0.1
  y = 0.3
  w1 = real(x, dp) * real(y, dp)
  w2 = real(x * y, dp)
  print '(a, f22.18)', 'real(x, dp) * real(y, dp) = ', w1
  print '(a, f22.18)', 'real(x * y, dp)           = ', w2
  print '(a, es10.2)', 'difference = ', w1 - w2
end program product_kind
