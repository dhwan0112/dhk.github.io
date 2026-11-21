module kinds
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  private
  public :: dp
  integer, parameter :: dp = real64
end module kinds

module statistics
  use kinds, only: dp
  implicit none
  private
  public :: mean, variance

contains

  pure function mean(x) result(m)
    real(dp), intent(in) :: x(:)
    real(dp) :: m

    m = sum(x) / size(x)
  end function mean

  pure function variance(x) result(v)
    real(dp), intent(in) :: x(:)
    real(dp) :: v

    v = sum((x - mean(x))**2) / (size(x) - 1)
  end function variance
end module statistics

program report
  use kinds, only: dp
  use statistics, only: mean, variance
  implicit none
  real(dp) :: samples(5)

  samples = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
  print '(a, f6.2)', 'mean     = ', mean(samples)
  print '(a, f6.2)', 'variance = ', variance(samples)
end program report
