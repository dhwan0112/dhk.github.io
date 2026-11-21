program new_style
  implicit none
  real :: a(4, 3)
  integer :: m, n

  a = 1.0
  m = 3
  n = 2
  a(1:m, 1:n) = 5.0 * a(1:m, 1:n)
  print '(3f5.1)', transpose(a)
end program new_style
