program mismatch
  implicit none
  integer :: n

  n = 3
  call scale_by_two(n)
  print '(i0)', n
end program mismatch

subroutine scale_by_two(x)
  real, intent(inout) :: x

  x = 2.0 * x
end subroutine scale_by_two
