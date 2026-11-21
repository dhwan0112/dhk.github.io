program float_equal
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp) :: a, b

  a = 0.1_dp + 0.2_dp
  b = 0.3_dp
  print '(a, l1)', 'a == b: ', a == b
end program float_equal
