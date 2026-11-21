program x_example
  implicit none
  real :: x

  x = 0.025
  write (*, '(a, f8.3)') 'x=', x
  write (*, '(a, f5.3)') 'x=', x
  write (*, '(a, e12.5)') 'x=', x
  write (*, '(a, e8.1)') 'x=', x
end program x_example
