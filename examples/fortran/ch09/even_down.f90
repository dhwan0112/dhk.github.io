program even_down
  implicit none
  integer :: i

  do i = 10, 1, -2
    print '(a, i0)', 'i = ', i
  end do
end program even_down
