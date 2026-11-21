program whole_array
  implicit none
  integer :: a(5), b(5), c(5)

  a = [1, 2, 3, 4, 5]
  b = 2 * a
  c = a + b
  print '(5i4)', c
  c = c * c - 1
  print '(5i4)', c
  c = 0
  print '(5i4)', c
end program whole_array
