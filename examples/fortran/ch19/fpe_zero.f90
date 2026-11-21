program fpe_zero
  implicit none
  real :: x

  read (*, *) x
  print '(f8.3)', inverse(x)

contains

  real function inverse(v)
    real, intent(in) :: v

    inverse = 1.0 / v
  end function inverse
end program fpe_zero
