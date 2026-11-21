program sections
  implicit none
  integer :: i
  integer :: a(8), m(3, 4)

  a = [(10 * i, i = 1, 8)]
  m = reshape([(i, i = 1, 12)], [3, 4])

  print '(a, 4i4)', 'a(2:5)   =', a(2:5)
  print '(a, 3i4)', 'a(:3)    =', a(:3)
  print '(a, 3i4)', 'a(6:)    =', a(6:)
  print '(a, 4i4)', 'a(::2)   =', a(::2)
  print '(a, 4i4)', 'a(8:5:-1)=', a(8:5:-1)
  print '(a, 3i4)', 'm(:, 2)  =', m(:, 2)
  print '(a, 4i4)', 'm(2, :)  =', m(2, :)
  print '(a, 4i4)', 'm(1:2, 3:4) =', m(1:2, 3:4)

  a(2:4) = 0
  print '(a, 8i4)', 'a =', a
end program sections
