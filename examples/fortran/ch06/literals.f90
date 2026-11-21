program literals
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  integer :: n
  real :: a
  real(dp) :: b
  complex :: z
  logical :: flag

  n = -100
  a = 2.0e6
  b = 3.333e-1_dp
  z = (2.0, -3.0)
  flag = .true.
  print '(a, i0)', 'integer: ', n
  print '(a, es12.4)', 'real:    ', a
  print '(a, es24.16)', 'real(dp):', b
  print '(a, 2f6.2)', 'complex: ', z
  print '(a, l1)', 'logical: ', flag
end program literals
