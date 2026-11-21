module noisy
  implicit none
contains
  pure function square(x) result(y)
    real, intent(in) :: x
    real :: y

    y = x * x
    print *, 'squaring', x
  end function square
end module noisy
