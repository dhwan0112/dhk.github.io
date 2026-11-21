program kinds
  use, intrinsic :: iso_fortran_env, only: int32, int64, real32, real64
  implicit none
  integer, parameter :: dp = real64
  integer(int64) :: big
  real(dp) :: x

  big = 2_int64**40
  x = 1.0_dp / 3.0_dp
  print '(a, i0, a, i0)', 'int32 = ', int32, ', int64 = ', int64
  print '(a, i0, a, i0)', 'real32 = ', real32, ', real64 = ', real64
  print '(a, i0)', 'kind(big) = ', kind(big)
  print '(a, i0)', 'kind(x) = ', kind(x)
  print '(a, i0)', 'big = ', big
  print '(a, f20.17)', 'x = ', x
end program kinds
