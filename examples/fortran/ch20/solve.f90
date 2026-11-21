program solve
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  interface
    subroutine dgesv(n, nrhs, a, lda, ipiv, b, ldb, info)
      import :: dp
      integer, intent(in) :: n, nrhs, lda, ldb
      real(dp), intent(inout) :: a(lda, *), b(ldb, *)
      integer, intent(out) :: ipiv(*), info
    end subroutine dgesv
  end interface

  real(dp) :: a(3, 3), b(3), s(2, 2), t(2)
  integer :: ipiv(3), info

  a = reshape([2.0_dp, 1.0_dp, -1.0_dp, &
              -3.0_dp, -1.0_dp, 2.0_dp, &
              -2.0_dp, 1.0_dp, 2.0_dp], [3, 3], order=[2, 1])
  b = [8.0_dp, -11.0_dp, -3.0_dp]
  call dgesv(3, 1, a, 3, ipiv, b, 3, info)
  print '(a, i0)', 'info = ', info
  print '(a, 3f8.3)', 'x = ', b

  s = reshape([1.0_dp, 2.0_dp, 2.0_dp, 4.0_dp], [2, 2], order=[2, 1])
  t = [1.0_dp, 2.0_dp]
  call dgesv(2, 1, s, 2, ipiv, t, 2, info)
  print '(a, i0)', 'info = ', info
end program solve
