program array_sum
  implicit none
  real :: a(4), b(4), c(4)

  a = [1.0, 2.0, 3.0, 4.0]
  b = 10.0
  c = a * 2.0 + b
  print '(4f6.1)', c
  print '(f6.1)', sum(c)
end program array_sum
