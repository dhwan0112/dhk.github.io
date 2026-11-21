program modern_loops
  implicit none
  integer :: i, n, total

  total = 0
  do i = 1, 4
    total = total + i
  end do
  print '(a, i3)', 'sum =', total

  n = 1
  do while (n <= 100)
    print '(i4)', n
    n = 2 * n
  end do

  do
    n = n - 50
    if (n <= 0) exit
  end do
  print '(a, i4)', 'n =', n
end program modern_loops
