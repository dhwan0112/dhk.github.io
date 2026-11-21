program dot_axpy
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    function ddot(n, x, incx, y, incy)
      import :: dp
      real(dp) :: ddot
      integer, intent(in) :: n, incx, incy
      real(dp), intent(in) :: x(*), y(*)
    end function ddot

    subroutine daxpy(n, a, x, incx, y, incy)
      import :: dp
      integer, intent(in) :: n, incx, incy
      real(dp), intent(in) :: a, x(*)
      real(dp), intent(inout) :: y(*)
    end subroutine daxpy
  end interface

  real(dp) :: x(4), y(4)

  x = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp]
  y = [4.0_dp, 3.0_dp, 2.0_dp, 1.0_dp]
  print '(a, f6.1)', 'ddot:        ', ddot(4, x, 1, y, 1)
  print '(a, f6.1)', 'dot_product: ', dot_product(x, y)
  print '(a, f6.1)', 'stride 2:    ', ddot(2, x, 2, y, 1)
  call daxpy(4, 2.0_dp, x, 1, y, 1)
  print '(a, 4f6.1)', 'daxpy:       ', y
end program dot_axpy
