program internal
  implicit none
  real :: radius

  radius = 2.0
  print '(a, f8.3)', 'area:          ', area()
  radius = 3.0
  print '(a, f8.3)', 'area:          ', area()
  print '(a, f8.3)', 'circumference: ', circumference(radius)

contains

  function area() result(a)
    real :: a

    a = 3.14159 * radius**2
  end function area

  function circumference(r) result(c)
    real, intent(in) :: r
    real :: c

    c = 2.0 * 3.14159 * r
  end function circumference
end program internal
