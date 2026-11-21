program tolerance
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp), parameter :: tol = 1.0e-12_dp
  real(dp) :: a, b, c, d

  a = 0.1_dp + 0.2_dp
  b = 0.3_dp
  c = 1.0e-20_dp
  d = 0.0_dp
  print '(a, es10.2)', 'a - b = ', a - b
  print '(a, l1)', 'a, b absolute: ', abs(a - b) <= tol
  print '(a, l1)', 'a, b relative: ', abs(a - b) <= tol * max(abs(a), abs(b))
  print '(a, l1)', 'c, d absolute: ', abs(c - d) <= tol
  print '(a, l1)', 'c, d relative: ', abs(c - d) <= tol * max(abs(c), abs(d))
end program tolerance
