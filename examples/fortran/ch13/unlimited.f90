program unlimited
  implicit none
  integer :: v(7)

  v = [1, 2, 3, 4, 5, 6, 7]
  write (*, '(a, *(i0, :, ", "))') 'values: ', v
  write (*, '(*(i3))') v
end program unlimited
