module coefficients
  implicit none
contains
  subroutine show(alpha, beta)
    real, intent(in) :: alpha, beta

    print '(a, f4.1, a, f4.1)', 'alpha = ', alpha, ', beta = ', beta
  end subroutine show
end module coefficients

program modern_common
  use coefficients, only: show
  implicit none
  real :: alpha, beta

  alpha = 1.0
  beta = 2.0
  call show(alpha, beta)
end program modern_common
