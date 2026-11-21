program column_major
  implicit none
  integer :: i, j, pos
  integer :: m(3, 4), flat(12)

  do j = 1, 4
    do i = 1, 3
      m(i, j) = 10 * i + j
    end do
  end do
  do i = 1, 3
    print '(4i4)', m(i, :)
  end do

  flat = reshape(m, [12])
  print '(12i4)', flat

  i = 2
  j = 3
  pos = 1 + (i - 1) + (j - 1) * 3
  print '(a, i0, a, i0)', 'm(2, 3) = ', m(i, j), ', position ', pos
  print '(a, i0)', 'flat(pos) = ', flat(pos)
end program column_major
