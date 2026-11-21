program point_demo
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  type :: point
    real(dp) :: x = 0.0_dp
    real(dp) :: y = 0.0_dp
  end type point

  type(point) :: p, q, pts(3)

  q = point(1.5_dp, -2.0_dp)
  p = point(y=4.0_dp)
  pts(2) = q
  pts(3)%x = 7.0_dp

  print '(a, 2f6.2)', 'p: ', p%x, p%y
  print '(a, 2f6.2)', 'q: ', q%x, q%y
  print '(a, 3f6.2)', 'pts%x: ', pts%x
  print '(a, 3f6.2)', 'pts%y: ', pts%y
end program point_demo
