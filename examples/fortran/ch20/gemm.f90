program gemm
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    function ddot(n, x, incx, y, incy)
      import :: dp
      real(dp) :: ddot
      integer, intent(in) :: n, incx, incy
      real(dp), intent(in) :: x(*), y(*)
    end function ddot

    subroutine dgemm(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc)
      import :: dp
      character(len=1), intent(in) :: transa, transb
      integer, intent(in) :: m, n, k, lda, ldb, ldc
      real(dp), intent(in) :: alpha, beta, a(lda, *), b(ldb, *)
      real(dp), intent(inout) :: c(ldc, *)
    end subroutine dgemm
  end interface

  real(dp) :: a(2, 3), b(3, 2), c(2, 2)
  integer :: i

  a = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [2, 3], order=[2, 1])
  b = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [3, 2], order=[2, 1])
  call dgemm('N', 'N', 2, 2, 3, 1.0_dp, a, 2, b, 3, 0.0_dp, c, 2)
  do i = 1, 2
    print '(2f7.1)', c(i, :)
  end do
  print '(f4.1)', maxval(abs(c - matmul(a, b)))
  print '(f7.1)', ddot(3, a(1, 1), 2, b(1, 2), 1)
end program gemm
