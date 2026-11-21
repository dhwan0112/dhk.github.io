program integer_division
  implicit none
  integer :: a, b
  real :: x

  a = 7
  b = 2
  x = a / b
  print '(a, i0)', 'a / b = ', a / b
  print '(a, f4.1)', 'x = a / b -> ', x
  x = real(a) / b
  print '(a, f4.1)', 'x = real(a) / b -> ', x
  print '(a, i0)', '(-a) / b = ', (-a) / b
  print '(a, i0)', 'mod(a, b) = ', mod(a, b)
end program integer_division
