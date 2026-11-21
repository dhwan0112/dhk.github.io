program constructors
  implicit none
  integer :: i, j
  integer :: a(5), b(5), c(3, 2)
  real :: r(3)

  a = [1, 2, 3, 4, 5]
  b = [(i * i, i = 1, 5)]
  r = [real :: 1, 2, 3]
  c = reshape([((10 * i + j, i = 1, 3), j = 1, 2)], [3, 2])
  print '(5i4)', a
  print '(5i4)', b
  print '(3f5.1)', r
  print '(a, 6i4)', 'in memory order:', c
  print '(a, 5i4)', 'odd numbers:', [(i, i = 1, 9, 2)]
end program constructors
