module old_style
  implicit none
contains
  subroutine scale(n, alpha, x)
    integer, intent(in) :: n
    real, intent(in) :: alpha
    real, intent(inout) :: x(*)
    integer :: i

    do i = 1, n
      x(i) = alpha * x(i)
    end do
  end subroutine scale

  subroutine mscale(m, n, alpha, a, lda)
    integer, intent(in) :: m, n, lda
    real, intent(in) :: alpha
    real, intent(inout) :: a(lda, *)
    integer :: j

    do j = 1, n
      call scale(m, alpha, a(1, j))
    end do
  end subroutine mscale
end module old_style

program legacy_style
  use old_style, only: mscale
  implicit none
  real :: a(4, 3)

  a = 1.0
  call mscale(3, 2, 5.0, a, 4)
  print '(3f5.1)', transpose(a)
end program legacy_style
