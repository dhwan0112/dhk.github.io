program init_save
  implicit none
  integer :: k

  do k = 1, 3
    call count_calls()
  end do
contains
  subroutine count_calls()
    integer :: n = 0

    n = n + 1
    print '(a, i0)', 'call number ', n
  end subroutine count_calls
end program init_save
