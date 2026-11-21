program reversion
  implicit none
  integer :: v(7)

  v = [1, 2, 3, 4, 5, 6, 7]
  write (*, '(i3)') v
  print '(a)', '---'
  write (*, '("v:", 2i3)') v
  print '(a)', '---'
  write (*, '("v:", 2(i3))') v
end program reversion
