program repeat_count
  implicit none
  integer :: v(4)

  v = [1, 2, 3, 4]
  write (*, '(2x, i3, 2x, i3, 2x, i3, 2x, i3)') v
  write (*, '(4(2x, i3))') v
end program repeat_count
