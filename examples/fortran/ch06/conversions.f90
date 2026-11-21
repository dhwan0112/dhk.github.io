program conversions
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp) :: x
  complex(dp) :: z

  x = 2.7_dp
  print '(a, i0)', 'int(2.7)     = ', int(x)
  print '(a, i0)', 'int(-2.7)    = ', int(-x)
  print '(a, i0)', 'nint(2.7)    = ', nint(x)
  print '(a, i0)', 'nint(-2.7)   = ', nint(-x)
  print '(a, i0)', 'floor(2.7)   = ', floor(x)
  print '(a, i0)', 'floor(-2.7)  = ', floor(-x)
  print '(a, i0)', 'ceiling(2.7) = ', ceiling(x)
  print '(a, f4.1)', 'real(3, dp)  = ', real(3, dp)
  z = cmplx(1.0_dp, -2.0_dp, kind=dp)
  print '(a, 2f6.2)', 'z            =', z
  print '(a, f6.2)', 'z%re         =', z%re
  print '(a, f6.2)', 'aimag(z)     =', aimag(z)
end program conversions
