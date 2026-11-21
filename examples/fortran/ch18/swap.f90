module swapping
  implicit none
contains
  subroutine swap(a, b)
    integer, intent(inout) :: a, b
    integer :: tmp

    tmp = a
    a = b
    b = tmp
  end subroutine swap
end module swapping

program swap_demo
  use swapping, only: swap
  implicit none
  integer :: m, n

  m = 1
  n = 2
  call swap(m, n)
  print '(2i3)', m, n
end program swap_demo
