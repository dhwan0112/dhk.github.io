program abs_value
  implicit none
  real :: x

  x = -2.5
  if (x < 0.0) x = -x
  print '(a, f3.1)', 'abs(x) = ', x
end program abs_value
