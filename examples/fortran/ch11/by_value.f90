module value_mod
  implicit none
contains
  subroutine bump(a, b)
    integer, intent(inout) :: a
    integer, value :: b

    a = a + 1
    b = b + 1
  end subroutine bump
end module value_mod

program by_value
  use value_mod, only: bump
  implicit none
  integer :: i, j

  i = 10
  j = 20
  call bump(i, j)
  print '(2i4)', i, j
end program by_value
