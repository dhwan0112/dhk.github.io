program precedence
  implicit none
  integer :: a, b

  a = 2
  b = 3
  print '(a, i0)', '-a**2     = ', -a**2
  print '(a, i0)', '(-a)**2   = ', (-a)**2
  print '(a, i0)', 'a**b**2   = ', a**b**2
  print '(a, i0)', '(a**b)**2 = ', (a**b)**2
  print '(a, i0)', '2 + 3 * 4 = ', 2 + 3 * 4
  print '(a, i0)', '10 - 4 - 3 = ', 10 - 4 - 3
  print '(a, i0)', '8 / 2 * 3 = ', 8 / 2 * 3
end program precedence
