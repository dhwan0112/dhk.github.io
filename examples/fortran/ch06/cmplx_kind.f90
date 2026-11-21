program cmplx_kind
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  complex(dp) :: a, b

  a = cmplx(0.1_dp, 0.2_dp)
  b = cmplx(0.1_dp, 0.2_dp, kind=dp)
  print '(2es24.16)', a
  print '(2es24.16)', b
end program cmplx_kind
