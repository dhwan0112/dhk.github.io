program descriptors
  implicit none
  write (*, '(a, i6, i6.4)') 'I:  ', 42, 42
  write (*, '(a, f10.3)') 'F:  ', 1234.5678
  write (*, '(a, e12.4)') 'E:  ', 12345.678
  write (*, '(a, es12.4)') 'ES: ', 12345.678
  write (*, '(a, en12.4)') 'EN: ', 12345.678
  write (*, '(a, g12.4, g12.4)') 'G:  ', 1234.5678, 0.01234
  write (*, '(a, a6, a)') 'A:  ', 'abc', '|'
  write (*, '(a, l5)') 'L:  ', .true.
  write (*, '(a, 3x, a)') 'X:', 'after 3 blanks'
  write (*, '(a, /, a)') 'slash:', 'next record'
  write (*, '(a, t12, a)') 'T:', 'column 12'
end program descriptors
