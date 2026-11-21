program real_steps
  implicit none
  integer :: i
  real :: x

  do i = 0, 4
    x = 0.25 * real(i)
    print '(f5.2)', x
  end do
end program real_steps
