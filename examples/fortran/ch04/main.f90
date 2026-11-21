program main
  use geometry, only: dp, circle_area
  implicit none
  real(dp) :: r

  r = 2.0_dp
  print '(a, f10.5)', 'area = ', circle_area(r)
end program main
