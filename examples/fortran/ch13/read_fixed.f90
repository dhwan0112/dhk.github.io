program read_fixed
  implicit none
  integer :: i
  real :: x
  character(len=20) :: line

  read (*, '(i4, f5.2)') i, x
  read (*, '(a)') line
  print '(i0, 1x, f0.2)', i, x
  print '(a, a, a)', '[', line, ']'
end program read_fixed
