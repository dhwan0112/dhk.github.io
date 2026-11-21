program no_goto
  implicit none
  integer :: n

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
end program no_goto
