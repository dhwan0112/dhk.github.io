program fpe_sqrt
  implicit none
  real :: y

  read (*, *) y
  print '(f8.3)', sqrt(y)
end program fpe_sqrt
