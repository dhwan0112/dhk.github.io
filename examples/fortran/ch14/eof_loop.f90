program eof_loop
  use, intrinsic :: iso_fortran_env, only: iostat_end
  implicit none
  integer :: u, ios, count
  real :: v, total

  open (newunit=u, file='numbers.dat', status='replace', action='readwrite')
  write (u, '(f6.2)') [1.5, 2.25, 3.0, 4.75]
  rewind (u)

  count = 0
  total = 0.0
  do
    read (u, *, iostat=ios) v
    if (ios == iostat_end) exit
    if (ios /= 0) error stop 'read error'
    count = count + 1
    total = total + v
  end do
  close (u, status='delete')

  print '(a, i0, a, f6.2)', 'values: ', count, '  sum: ', total
end program eof_loop
