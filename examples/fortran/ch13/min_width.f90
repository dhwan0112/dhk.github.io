program min_width
  implicit none
  real :: x

  x = 0.025
  write (*, '(i0, 1x, i0, 1x, i0)') 7, 12345, -42
  write (*, '(f0.2, 1x, f0.2, 1x, f0.2)') 3.14159, 100.0, 0.5
  write (*, '(a, f3.3)') 'f3.3: ', x
  write (*, '(a, f5.2)') 'f5.2: ', 123.456
  write (*, '(a, i3)') 'i3:   ', 12345
end program min_width
