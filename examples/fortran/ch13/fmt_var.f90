program fmt_var
  implicit none
  character(len=20) :: fmt
  integer :: n
  real :: row(4)

  row = [1.0, 2.5, 3.25, 4.0]
  fmt = '(4f8.2)'
  write (*, fmt) row

  n = 4
  write (fmt, '(a, i0, a)') '(', n, 'f8.2)'
  print '(a, a)', 'fmt = ', trim(fmt)
  write (*, fmt) row
end program fmt_var
