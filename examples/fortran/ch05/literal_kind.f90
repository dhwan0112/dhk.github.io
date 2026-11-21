program literal_kind
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp) :: a, b

  a = 0.1
  b = 0.1_dp
  print '(a, es24.16)', 'a = 0.1     : ', a
  print '(a, es24.16)', 'b = 0.1_dp  : ', b
  print '(a, es24.16)', '1.0e-3_dp   : ', 1.0e-3_dp
end program literal_kind
