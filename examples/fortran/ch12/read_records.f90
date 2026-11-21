program read_records
  implicit none
  integer :: m, n
  real :: x, y, z(4)

  read (*, *) m, n
  read (*, *) x, y
  read (*, *) z
  print '(2i5)', m, n
  print '(2f7.1)', x, y
  print '(4f5.1)', z
end program read_records
