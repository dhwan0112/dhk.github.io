module norms
  implicit none
contains
  function norm_assumed(v) result(s)
    real, intent(in) :: v(:)
    real :: s

    s = sqrt(sum(v**2))
  end function norm_assumed

  function norm_explicit(n, v) result(s)
    integer, intent(in) :: n
    real, intent(in) :: v(n)
    real :: s

    s = sqrt(sum(v**2))
  end function norm_explicit
end module norms

program sections
  use norms, only: norm_assumed, norm_explicit
  implicit none
  real :: a(3, 4)
  integer :: i

  a = reshape([(real(i), i = 1, 12)], [3, 4])
  print '(f8.4)', norm_assumed(a(:, 2))
  print '(f8.4)', norm_assumed(a(2, :))
  print '(f8.4)', norm_explicit(4, a(2, :))
end program sections
