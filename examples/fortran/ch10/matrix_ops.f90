program matrix_ops
  implicit none
  integer :: i
  integer :: a(2, 3), b(3, 2), c(2, 2), v(3), w(3)

  a = reshape([1, 2, 3, 4, 5, 6], [2, 3])
  b = transpose(a)
  c = matmul(a, b)
  v = [1, 2, 3]
  w = [4, 5, 6]

  do i = 1, 2
    print '(a, 3i3)', 'a row:', a(i, :)
  end do
  do i = 1, 3
    print '(a, 2i3)', 'b row:', b(i, :)
  end do
  do i = 1, 2
    print '(a, 2i4)', 'c row:', c(i, :)
  end do
  print '(a, i0)', 'dot_product(v, w) = ', dot_product(v, w)
end program matrix_ops
