program strings
  implicit none
  character(len=20) :: s
  character(len=5) :: t

  s = 'It''s a nice day'
  print '(a)', s
  print '(a)', "She said ""hello"""
  print '(a)', "It's fine too"
  t = 'ab'
  print '(a, a, a)', '[', t, ']'
  print '(a, i0)', 'len(t)      = ', len(t)
  print '(a, i0)', 'len_trim(t) = ', len_trim(t)
  s = 'Fortran'
  print '(a)', s(1:3)
  print '(a)', s(4:7)
  print '(a)', trim(s) // ' 2018'
  s(1:1) = 'f'
  print '(a)', s
end program strings
