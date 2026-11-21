program uninit
  implicit none
  real :: total, x(3)
  integer :: i

  x = [1.0, 2.0, 3.0]
  do i = 1, 3
    total = total + x(i)
  end do
  print '(f8.3)', total
end program uninit
