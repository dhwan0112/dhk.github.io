module factorial_mod
  implicit none
contains
  recursive function factorial(n) result(f)
    integer, intent(in) :: n
    integer :: f

    if (n <= 1) then
      f = 1
    else
      f = n * factorial(n - 1)
    end if
  end function factorial
end module factorial_mod

program factorial_demo
  use factorial_mod, only: factorial
  implicit none
  integer :: n

  do n = 1, 6
    print '(i2, a, i4)', n, '! = ', factorial(n)
  end do
end program factorial_demo
