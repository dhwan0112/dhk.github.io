program squares
  implicit none
  integer :: i
  integer :: sq(10)

  do i = 1, 10
    sq(i) = i**2
  end do
  print '(10i4)', sq
end program squares
