program select_kind
  implicit none
  integer, parameter :: sp = selected_real_kind(6, 37)
  integer, parameter :: dp = selected_real_kind(15, 307)
  integer, parameter :: i8 = selected_int_kind(9)
  integer, parameter :: i18 = selected_int_kind(18)

  print '(a, i0)', 'sp  = ', sp
  print '(a, i0)', 'dp  = ', dp
  print '(a, i0)', 'i8  = ', i8
  print '(a, i0)', 'i18 = ', i18
  print '(a, i0)', 'selected_real_kind(40) = ', selected_real_kind(40)
end program select_kind
