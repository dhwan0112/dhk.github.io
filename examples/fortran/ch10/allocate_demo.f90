program allocate_demo
  implicit none
  integer :: i, n, ios
  integer, allocatable :: a(:)

  n = 4
  print '(a, l1)', 'allocated before: ', allocated(a)
  allocate (a(n))
  a = [(i, i = 1, n)]
  print '(a, l1, a, i0)', 'allocated now: ', allocated(a), ', size ', size(a)

  allocate (a(n), stat=ios)
  if (ios /= 0) print '(a)', 'second allocate failed'

  a = [10, 20, 30, 40, 50, 60]
  print '(a, i0)', 'size after assignment: ', size(a)

  deallocate (a)
  print '(a, l1)', 'allocated after: ', allocated(a)
end program allocate_demo
