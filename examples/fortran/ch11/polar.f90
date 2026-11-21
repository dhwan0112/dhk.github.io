module convert
  implicit none
contains
  subroutine to_polar(x, y, r, theta)
    real, intent(in) :: x, y
    real, intent(out) :: r, theta

    r = sqrt(x**2 + y**2)
    theta = atan2(y, x)
  end subroutine to_polar
end module convert

program polar
  use convert, only: to_polar
  implicit none
  real :: r, theta

  call to_polar(1.0, 1.0, r, theta)
  print '(a, f7.4)', 'r     = ', r
  print '(a, f7.4)', 'theta = ', theta
end program polar
