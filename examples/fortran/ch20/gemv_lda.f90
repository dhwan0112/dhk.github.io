program gemv_lda
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    subroutine dgemv(trans, m, n, alpha, a, lda, x, incx, beta, y, incy)
      import :: dp
      character(len=1), intent(in) :: trans
      integer, intent(in) :: m, n, lda, incx, incy
      real(dp), intent(in) :: alpha, beta, a(lda, *), x(*)
      real(dp), intent(inout) :: y(*)
    end subroutine dgemv
  end interface

  real(dp) :: a(4, 3), x(3), y(2)

  a = 0.0_dp
  a(1:2, 1:3) = reshape([1.0_dp, 2.0_dp, 3.0_dp, &
                         4.0_dp, 5.0_dp, 6.0_dp], [2, 3], order=[2, 1])
  x = [1.0_dp, 2.0_dp, 3.0_dp]
  y = 0.0_dp
  call dgemv('N', 2, 3, 1.0_dp, a, 4, x, 1, 0.0_dp, y, 1)
  print '(a, 2f6.1)', 'y = ', y
end program gemv_lda
