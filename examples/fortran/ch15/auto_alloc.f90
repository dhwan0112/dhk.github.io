module work_mod
  implicit none
contains
  subroutine smooth(x, y)
    real, intent(in) :: x(:)
    real, intent(out) :: y(size(x))
    real :: tmp(size(x))
    integer :: n

    n = size(x)
    tmp = x
    tmp(2:n-1) = (x(1:n-2) + x(2:n-1) + x(3:n)) / 3.0
    y = tmp
  end subroutine smooth

  subroutine make_ramp(n, v)
    integer, intent(in) :: n
    real, allocatable, intent(out) :: v(:)
    integer :: i

    allocate (v(n))
    v = [(real(i * i), i = 1, n)]
  end subroutine make_ramp
end module work_mod

program auto_alloc
  use work_mod, only: smooth, make_ramp
  implicit none
  real, allocatable :: v(:), s(:)

  call make_ramp(6, v)
  allocate (s(size(v)))
  call smooth(v, s)
  print '(6f7.2)', v
  print '(6f7.2)', s
end program auto_alloc
