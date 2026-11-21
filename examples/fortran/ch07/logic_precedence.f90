program logic_precedence
  implicit none
  logical :: a, b, c
  integer :: n, m

  a = .true.
  b = .false.
  c = .false.
  n = 3
  m = 5
  print '(a, l1)', 'a .and. n < m / 2     : ', a .and. n < m / 2
  print '(a, l1)', '.not. a .and. b       : ', .not. a .and. b
  print '(a, l1)', '.not. (a .and. b)     : ', .not. (a .and. b)
  print '(a, l1)', 'a .or. b .and. c      : ', a .or. b .and. c
  print '(a, l1)', '(a .or. b) .and. c    : ', (a .or. b) .and. c
  print '(a, l1)', 'a .or. b .eqv. c      : ', a .or. b .eqv. c
  print '(a, l1)', 'a .or. (b .eqv. c)    : ', a .or. (b .eqv. c)
  print '(a, l1)', 'a .neqv. b            : ', a .neqv. b
end program logic_precedence
