program stream
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  real(dp) :: a(4), b(4)
  integer :: u, nbytes

  a = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp]
  open (newunit=u, file='values.bin', access='stream', form='unformatted', &
        status='replace', action='readwrite')
  write (u) a
  inquire (unit=u, size=nbytes)
  read (u, pos=1) b
  close (u, status='delete')
  print '(a, i0, a, f5.1)', 'stream file: ', nbytes, ' bytes, sum ', sum(b)

  open (newunit=u, file='values.dat', form='unformatted', status='replace', action='readwrite')
  write (u) a
  inquire (unit=u, size=nbytes)
  close (u, status='delete')
  print '(a, i0, a)', 'sequential file: ', nbytes, ' bytes'
end program stream
