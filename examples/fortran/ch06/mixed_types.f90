program mixed_types
  implicit none
  integer :: i, j, n
  real :: x

  i = 1
  j = 4
  n = 3
  x = 0.5
  print '(a, f6.3)', 'n * x = ', n * x
  print '(a, f6.3)', 'n + 1.5 = ', n + 1.5
  print '(a, f6.3)', 'i / j * x = ', i / j * x
  print '(a, f6.3)', 'real(i) / j * x = ', real(i) / j * x
  x = n
  print '(a, f6.3)', 'x = n gives ', x
  n = int(2.7 * x)
  print '(a, i0)', 'n = int(2.7 * x) gives ', n
end program mixed_types
