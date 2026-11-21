program dimension_stmt
  implicit none
  real :: x
  real :: m
  dimension x(50), m(10, 20)

  x(1) = 1.0
  m(1, 1) = 2.0
  print '(a, i0, a, i0)', 'sizes: ', size(x), ' and ', size(m)
end program dimension_stmt
