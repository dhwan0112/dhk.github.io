program points
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  integer, parameter :: n = 5
  real(dp) :: x(n), y(n), z(n)
  real(dp), allocatable :: px(:), py(:), pz(:)
  integer :: u, ios, i, np
  character(len=100) :: msg

  x = [(0.5_dp * i, i = 1, n)]
  y = x**2
  z = 1.0_dp - x
  open (newunit=u, file='points.dat', status='replace', action='write', iostat=ios, iomsg=msg)
  if (ios /= 0) error stop msg
  write (u, '(i0)') n
  write (u, '(3f10.4)') (x(i), y(i), z(i), i = 1, n)
  close (u)

  open (newunit=u, file='points.dat', status='old', action='read', iostat=ios, iomsg=msg)
  if (ios /= 0) error stop msg
  read (u, *) np
  allocate (px(np), py(np), pz(np))
  do i = 1, np
    read (u, '(3f10.4)') px(i), py(i), pz(i)
  end do
  close (u)

  print '(a, i0, a)', 'read ', np, ' points'
  print '(a, 3f9.4)', 'center: ', sum(px) / np, sum(py) / np, sum(pz) / np
end program points
