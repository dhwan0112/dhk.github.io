program intrinsics
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  real :: x
  real(dp) :: y

  x = 2.0
  y = 2.0_dp
  print '(a, f10.7)', 'sqrt single: ', sqrt(x)
  print '(a, f18.15)', 'sqrt double: ', sqrt(y)
  print '(a, f10.7)', 'atan2(1, 1): ', atan2(1.0, 1.0)
  print '(a, 3i4)', 'abs min max: ', abs(-3), min(4, 2, 7), max(4, 2, 7)
end program intrinsics
