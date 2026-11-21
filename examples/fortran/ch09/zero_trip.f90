program zero_trip
  implicit none
  integer :: i, lo, hi

  do i = 1, 3
  end do
  print '(a, i0)', 'after 1..3: i = ', i

  lo = 5
  hi = 1
  do i = lo, hi
    print '(a, i0)', 'never printed: ', i
  end do
  print '(a, i0)', 'after 5..1: i = ', i
end program zero_trip
