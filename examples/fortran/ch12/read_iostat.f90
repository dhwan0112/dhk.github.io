program read_iostat
  implicit none
  integer :: n, ios

  do
    read (*, *, iostat=ios) n
    if (is_iostat_end(ios)) exit
    if (ios /= 0) then
      print '(a)', 'not an integer, skipped'
    else
      print '(a, i0)', 'n = ', n
    end if
  end do
  print '(a)', 'end of input'
end program read_iostat
