program side_effect
  implicit none
  real :: x

  x = 3.0
  print '(f6.1)', twice(x)

contains

  pure function twice(v) result(w)
    real, intent(in) :: v
    real :: w

    v = 2.0 * v
    w = v
  end function twice
end program side_effect
