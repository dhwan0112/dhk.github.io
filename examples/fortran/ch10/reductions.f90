program reductions
  implicit none
  integer :: x(8)

  x = [3, 1, 4, 1, 5, 9, 2, 6]
  print '(a, i0)', 'sum     = ', sum(x)
  print '(a, i0)', 'product = ', product(x)
  print '(a, i0)', 'maxval  = ', maxval(x)
  print '(a, i0)', 'minval  = ', minval(x)
  print '(a, i0)', 'maxloc  = ', maxloc(x, dim=1)
  print '(a, l1)', 'any(x > 8)  = ', any(x > 8)
  print '(a, l1)', 'all(x > 0)  = ', all(x > 0)
  print '(a, i0)', 'count(x > 2) = ', count(x > 2)
end program reductions
