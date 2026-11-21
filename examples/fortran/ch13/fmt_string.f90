program fmt_string
  implicit none
  integer :: i
  real :: x

  i = 42
  x = 3.14159
  write (*, '(i4, f8.3)') i, x
end program fmt_string
