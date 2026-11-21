program derived_io
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  type :: sample
    integer :: id = 0
    real(dp) :: value = 0.0_dp
  end type sample

  type(sample) :: s(2)

  s(1) = sample(1, 0.25_dp)
  s(2) = sample(2, 1.75_dp)
  print '(i3, f7.2)', s
  print '(a, i0, a, f5.2)', 'second: id=', s(2)%id, ' value=', s(2)%value
end program derived_io
