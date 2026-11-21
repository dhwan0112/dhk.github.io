program exists
  implicit none
  character(len=*), parameter :: name = 'scratch.txt'
  logical :: found
  integer :: u, ios

  inquire (file=name, exist=found)
  print '(a, l2)', 'before: ', found
  open (newunit=u, file=name, status='old', action='read', iostat=ios)
  print '(a, l2)', 'open failed: ', ios /= 0

  open (newunit=u, file=name, status='new', action='write')
  write (u, '(a)') 'hello'
  close (u)
  inquire (file=name, exist=found)
  print '(a, l2)', 'after write: ', found

  open (newunit=u, file=name, status='old')
  close (u, status='delete')
  inquire (file=name, exist=found)
  print '(a, l2)', 'after delete: ', found
end program exists
