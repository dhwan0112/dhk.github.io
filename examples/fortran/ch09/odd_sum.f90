program odd_sum
  implicit none
  integer :: i, total

  total = 0
  do i = 1, 10
    if (mod(i, 2) == 0) cycle
    total = total + i
  end do
  print '(a, i0)', 'sum of odd numbers = ', total
end program odd_sum
