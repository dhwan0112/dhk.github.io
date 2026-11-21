module shapes
  implicit none
contains
  pure function hypotenuse(a, b) result(c)
    real, intent(in) :: a, b
    real :: c

    c = sqrt(a**2 + b**2)
  end function hypotenuse

  elemental function clamp(x, lo, hi) result(y)
    real, intent(in) :: x, lo, hi
    real :: y

    y = min(max(x, lo), hi)
  end function clamp
end module shapes

program pure_elemental
  use shapes, only: hypotenuse, clamp
  implicit none
  real :: v(5)

  v = [-2.0, 0.5, 1.0, 3.5, 7.0]
  print '(a, f6.2)', 'hypotenuse: ', hypotenuse(3.0, 4.0)
  print '(5f6.1)', clamp(v, 0.0, 4.0)
end program pure_elemental
