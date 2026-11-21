program bound_once
  implicit none
  integer :: i, j

  read (*, *) j
  do i = 1, j
    j = j + 1
  end do
  print '(a, i0)', 'j = ', j
end program bound_once
