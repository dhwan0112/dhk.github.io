program named_if
  implicit none
  real :: x, y

  x = 3.0
  y = 5.0
  sign_check: if (x > 0.0) then
    order_check: if (x >= y) then
      print *, 'x is positive and x >= y'
    else order_check
      print *, 'x is positive but x < y'
    end if order_check
  else sign_check
    print *, 'x is not positive'
  end if sign_check
end program named_if
