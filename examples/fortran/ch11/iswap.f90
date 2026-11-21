module swap_mod
  implicit none
contains
  subroutine iswap(a, b)
    integer, intent(inout) :: a, b
    integer :: tmp

    tmp = a
    a = b
    b = tmp
  end subroutine iswap
end module swap_mod

program callex
  use swap_mod, only: iswap
  implicit none
  integer :: m, n

  m = 1
  n = 2
  call iswap(m, n)
  print '(2i3)', m, n
end program callex
