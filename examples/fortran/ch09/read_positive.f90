program read_positive
  implicit none
  integer :: n

  do
    read (*, *) n
    if (n > 0) exit
    print '(a, i0, a)', 'got ', n, ', need a positive number'
  end do
  print '(a, i0)', 'n = ', n
end program read_positive
