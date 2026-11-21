program declarations
  implicit none
  integer :: count
  real :: height
  complex :: z
  logical :: done
  character(len=12) :: label

  count = 3
  height = 1.75
  z = (1.0, 2.0)
  done = .false.
  label = 'sample'
  print '(a, i0)', 'count  = ', count
  print '(a, f5.2)', 'height = ', height
  print '(a, 2f5.1)', 'z      = ', z
  print '(a, l1)', 'done   = ', done
  print '(a, a, a)', 'label  = [', label, ']'
end program declarations
