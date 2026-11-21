program inf_nan
  implicit none
  real :: x, y

  read (*, *) x, y
  print '(a, f10.3)', '1 / x    = ', 1.0 / x
  print '(a, f10.3)', 'sqrt(y)  = ', sqrt(y)
end program inf_nan
