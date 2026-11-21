program fmt_label
  implicit none
  integer :: i
  real :: x

  i = 42
  x = 3.14159
  write (*, 900) i, x
900 format (i4, f8.3)
end program fmt_label
