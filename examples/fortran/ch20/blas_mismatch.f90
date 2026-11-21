program blas_mismatch
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    subroutine daxpy(n, a, x, incx, y, incy)
      import :: dp
      integer, intent(in) :: n, incx, incy
      real(dp), intent(in) :: a, x(*)
      real(dp), intent(inout) :: y(*)
    end subroutine daxpy
  end interface

  real :: x(3), y(3)

  x = 1.0
  y = 0.0
  call daxpy(3, 2.0_dp, x, 1, y, 1)
  print '(3f6.1)', y
end program blas_mismatch
