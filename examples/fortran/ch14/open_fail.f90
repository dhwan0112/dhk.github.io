program open_fail
  implicit none
  integer :: u

  open (newunit=u, file='no_such_file.dat', status='old')
  print *, 'opened'
end program open_fail
