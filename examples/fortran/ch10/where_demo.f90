program where_demo
  implicit none
  real :: a(6), b(6)

  a = [-2.0, 3.0, 0.0, -1.0, 5.0, 4.0]
  where (a < 0.0) a = 0.0
  print '(6f6.1)', a

  where (a > 0.0)
    b = 1.0 / a
  elsewhere
    b = -1.0
  end where
  print '(6f6.2)', b
end program where_demo
