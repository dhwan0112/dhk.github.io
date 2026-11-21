program declare_arrays
  implicit none
  real :: a(20), b(0:19), weird(-162:237)
  real :: grid(0:2, -1:1)

  print '(a, i0)', 'size(a) = ', size(a)
  print '(a, i0, a, i0)', 'b runs from ', lbound(b, 1), ' to ', ubound(b, 1)
  print '(a, i0, a, i0, a, i0)', 'weird runs from ', lbound(weird, 1), &
    ' to ', ubound(weird, 1), ', size ', size(weird)
  print '(a, 2i3)', 'shape(grid) = ', shape(grid)
  print '(a, i0)', 'size(grid) = ', size(grid)
end program declare_arrays
