program rounding
  implicit none
  real :: x

  x = 0.125
  write (*, '(a, f6.2)') 'default: ', x
  write (*, '(a, rn, f6.2)') 'rn:      ', x
  write (*, '(a, rc, f6.2)') 'rc:      ', x
  write (*, '(a, ru, f6.2)') 'ru:      ', x
  write (*, '(a, rd, f6.2)') 'rd:      ', x
  write (*, '(a, rz, f6.2)') 'rz:      ', x
  write (*, '(a, f4.0, 1x, f4.0, 1x, f4.0)') 'f4.0:    ', 0.5, 1.5, 2.5
end program rounding
