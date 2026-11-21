program concurrent_squares
  implicit none
  integer :: i
  integer :: sq(5)

  do concurrent (i = 1:5)
    sq(i) = i**2
  end do
  print '(5i4)', sq
end program concurrent_squares
