program powers_exit
  implicit none
  integer :: n

  n = 1
  do
    if (n > 100) exit
    print '(i0)', n
    n = 2 * n
  end do
end program powers_exit
