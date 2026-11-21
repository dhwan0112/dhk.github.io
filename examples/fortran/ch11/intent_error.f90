module bad_mod
  implicit none
contains
  subroutine double_it(a)
    integer, intent(in) :: a

    a = 2 * a
  end subroutine double_it
end module bad_mod
