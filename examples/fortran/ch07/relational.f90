program relational
  implicit none
  integer :: a, b
  logical :: same, bigger

  a = 3
  b = 5
  same = a == b
  bigger = a < b
  print '(a, l1)', 'a == b : ', same
  print '(a, l1)', 'a /= b : ', a /= b
  print '(a, l1)', 'a <  b : ', bigger
  print '(a, l1)', 'a <= b : ', a <= b
  print '(a, l1)', 'a >  b : ', a > b
  print '(a, l1)', 'a >= b : ', a >= b
  print '(a, l1)', 'a .lt. b : ', a .lt. b
  print '(a, l1)', 'a .eq. b : ', a .eq. b
end program relational
