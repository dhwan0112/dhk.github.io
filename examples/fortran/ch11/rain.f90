module rain_model
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
contains
  function monthly_rain(m, t) result(r)
    integer, intent(in) :: m
    real(dp), intent(in) :: t
    real(dp) :: r

    r = 0.1_dp * t * (m**2 + 14*m + 46)
    if (r < 0.0_dp) r = 0.0_dp
  end function monthly_rain
end module rain_model

program rain
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use rain_model, only: monthly_rain
  implicit none
  real(dp) :: t, total
  integer :: m

  read (*, *) t
  total = 0.0_dp
  do m = 1, 12
    total = total + monthly_rain(m, t)
  end do
  print '(a, f9.2, a)', 'Annual rainfall is ', total, ' inches'
end program rain
