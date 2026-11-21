module coefficients
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  real(dp) :: alpha = 1.0_dp
  real(dp) :: beta = 0.0_dp
end module coefficients

module models
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use coefficients, only: alpha, beta
  implicit none
contains
  function line(x) result(y)
    real(dp), intent(in) :: x
    real(dp) :: y

    y = alpha * x + beta
  end function line

  function parabola(x) result(y)
    real(dp), intent(in) :: x
    real(dp) :: y

    y = alpha * x**2 + beta * x
  end function parabola
end module models

program coeff
  use coefficients, only: alpha, beta
  use models, only: line, parabola
  implicit none

  alpha = 2.0d0
  beta = 1.0d0
  print '(2f8.2)', line(3.0d0), parabola(3.0d0)
  beta = -1.0d0
  print '(2f8.2)', line(3.0d0), parabola(3.0d0)
end program coeff
