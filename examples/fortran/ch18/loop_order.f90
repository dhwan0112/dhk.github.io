program loop_order
  implicit none
  integer, parameter :: n = 2, m = 3
  integer :: a(n, m), b(n, m)
  integer :: i, j

  do j = 1, m
    do i = 1, n
      a(i, j) = 10 * i + j
    end do
  end do

  do i = 1, n
    do j = 1, m
      b(i, j) = 10 * i + j
    end do
  end do

  print '(6i4)', a
  print '(l1)', all(a == b)
end program loop_order
