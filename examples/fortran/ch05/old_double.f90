program old_double
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  double precision :: a
  real(real64) :: b

  a = 1.0d0 / 3.0d0
  b = 1.0_real64 / 3.0_real64
  print '(es24.16)', a
  print '(es24.16)', b
  print '(l1)', kind(a) == real64
end program old_double
