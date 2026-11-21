program bad_kind
  implicit none
  integer, parameter :: qp = selected_real_kind(40)
  real(qp) :: x

  print '(i0)', qp
end program bad_kind
