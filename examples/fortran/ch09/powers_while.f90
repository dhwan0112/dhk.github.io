program powers_while
  implicit none
  integer :: n

  n = 1
  do while (n <= 100)
    print '(i0)', n
    n = 2 * n
  end do
end program powers_while
