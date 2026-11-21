program warn_demo
  implicit none
  real :: x, y
  integer :: unused

  x = 0.1
  y = 1.0d0 / 3.0d0
  if (x == y) print '(a)', 'equal'
  call report(x, y)

contains

  subroutine report(v, w)
    real, intent(in) :: v, w

    print '(f6.2)', v
  end subroutine report
end program warn_demo
