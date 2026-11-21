program nested_if
  implicit none
  real :: x, y

  x = 3.0
  y = 5.0
  if (x > 0.0) then
    if (x >= y) then
      print *, 'x is positive and x >= y'
    else
      print *, 'x is positive but x < y'
    end if
  else
    print *, 'x is not positive'
  end if
end program nested_if
