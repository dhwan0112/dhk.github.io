program implicit_iface
  implicit none
  real :: x

  x = 3.0
  call scale_by_two(x)
  print '(f4.1)', x
end program implicit_iface

subroutine scale_by_two(x)
  real, intent(inout) :: x

  x = 2.0 * x
end subroutine scale_by_two
