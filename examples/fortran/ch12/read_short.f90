program read_short
  implicit none
  integer :: m, n
  real :: x, y

  read (*, *) m, n, x, y
  print '(2i5)', m, n
  print '(2f7.1)', x, y
end program read_short
