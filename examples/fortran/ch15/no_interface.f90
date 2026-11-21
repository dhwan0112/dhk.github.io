program no_interface
  implicit none
  real :: v(3)

  v = [1.0, 2.0, 3.0]
  call show_sum(v)
end program no_interface

subroutine show_sum(x)
  implicit none
  real, intent(in) :: x(:)

  print *, sum(x)
end subroutine show_sum
