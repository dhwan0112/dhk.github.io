program safe_index
  implicit none
  integer, parameter :: n = 5
  real :: a(n)
  integer :: i
  logical :: found

  a = [1.0, -2.0, 3.0, -4.0, 5.0]
  i = n + 1
  found = .false.
  if (i <= n) then
    found = a(i) > 0.0
  end if
  print '(a, l1)', 'found = ', found
end program safe_index
