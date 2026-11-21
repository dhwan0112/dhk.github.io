module blas_like
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
contains
  subroutine saxpy(alpha, x, y)
    real(dp), intent(in) :: alpha, x(:)
    real(dp), intent(inout) :: y(:)

    if (size(x) /= size(y)) error stop 'saxpy: size mismatch'
    y = alpha * x + y
  end subroutine saxpy

  subroutine matvec(a, x, y)
    real(dp), intent(in) :: a(:, :), x(:)
    real(dp), intent(out) :: y(:)
    integer :: j

    y = 0.0_dp
    do j = 1, size(a, 2)
      call saxpy(x(j), a(:, j), y)
    end do
  end subroutine matvec
end module blas_like

program matvec_demo
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use blas_like, only: matvec
  implicit none
  real(dp) :: a(3, 2), x(2), y(3)

  a = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [3, 2])
  x = [10.0_dp, 100.0_dp]
  call matvec(a, x, y)
  print '(3f8.1)', y
  print '(a, f4.1)', 'difference from matmul: ', maxval(abs(y - matmul(a, x)))
end program matvec_demo
