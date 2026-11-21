program external_demo
  implicit none
  interface
    function cube(x) result(y)
      real, intent(in) :: x
      real :: y
    end function cube
  end interface

  print '(f6.1)', cube(3.0)
end program external_demo

function cube(x) result(y)
  implicit none
  real, intent(in) :: x
  real :: y

  y = x**3
end function cube
