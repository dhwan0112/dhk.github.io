program read_string
  implicit none
  character(len=20) :: first, second

  read (*, *) first
  read (*, *) second
  print '(a, a, a)', '[', first, ']'
  print '(a, a, a)', '[', second, ']'
end program read_string
