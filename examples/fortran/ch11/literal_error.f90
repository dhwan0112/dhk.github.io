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

program literal_error
  use swap_mod, only: iswap
  implicit none
  integer :: n

  n = 2
  call iswap(1, n)
end program literal_error
