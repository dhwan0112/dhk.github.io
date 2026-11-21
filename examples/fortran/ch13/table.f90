program table
  implicit none
  integer :: i, j, a(3, 5)

  do j = 1, 5
    do i = 1, 3
      a(i, j) = i * j
    end do
  end do

  print '(a)', '  i     sqrt(i)    i**2'
  do i = 1, 3
    write (*, '(i3, f12.4, i8)') i, sqrt(real(i)), i**2
  end do

  print '(a)', 'rows of a:'
  do i = 1, 3
    write (*, '(5i4)') (a(i, j), j = 1, 5)
  end do

  print '(a)', 'all at once, row by row:'
  write (*, '(5i4)') ((a(i, j), j = 1, 5), i = 1, 3)
end program table
