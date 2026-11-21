program out_of_bounds
  implicit none
  integer :: i, n
  integer :: a(5)

  read (*, *) n
  do i = 1, n
    a(i) = i
  end do
  print '(a, i0)', 'filled ', n
end program out_of_bounds
