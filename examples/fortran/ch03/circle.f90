program circle
  implicit none
  real :: r, area

  write (*, *) 'Give radius r:'
  read (*, *) r
  area = 3.14159 * r * r
  write (*, *) 'Area = ', area
end program circle
