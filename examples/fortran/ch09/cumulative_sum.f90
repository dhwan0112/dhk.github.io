program cumulative_sum
  implicit none
  integer :: i, n, total

  n = 5
  total = 0
  do i = 1, n
    total = total + i
    print '(a, i0, a, i0)', 'i = ', i, ', sum = ', total
  end do
end program cumulative_sum
