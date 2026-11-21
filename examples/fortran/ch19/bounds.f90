program bounds
  implicit none
  integer :: a(5), i, k

  a = [(10 * i, i = 1, 5)]
  read (*, *) k
  print '(a, i0, a, i0)', 'a(', k, ') = ', a(k)
end program bounds
