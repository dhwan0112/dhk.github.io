module matrices
  implicit none
contains
  subroutine set_identity(a)
    real, intent(out) :: a(:, :)
    integer :: i

    a = 0.0
    do i = 1, min(size(a, 1), size(a, 2))
      a(i, i) = 1.0
    end do
  end subroutine set_identity
end module matrices

program allocate_once
  use matrices, only: set_identity
  implicit none
  integer, parameter :: n = 1000
  real, allocatable :: a(:, :)

  allocate (a(n, n))
  call set_identity(a)
  print '(a, i0, a, f7.1)', 'elements = ', size(a), ', sum = ', sum(a)
end program allocate_once
