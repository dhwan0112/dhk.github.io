module models
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
contains
  pure function line(x, alpha, beta) result(y)
    real(dp), intent(in) :: x, alpha, beta
    real(dp) :: y

    y = alpha * x + beta
  end function line
end module models

program no_shared
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use models, only: line
  implicit none

  print '(2f8.2)', line(3.0_dp, 2.0_dp, 1.0_dp), line(3.0_dp, -1.0_dp, 0.0_dp)
end program no_shared
