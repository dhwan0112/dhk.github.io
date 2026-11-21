program list_output
  implicit none
  integer :: n
  real :: x
  double precision :: d
  logical :: flag
  character(len=5) :: word

  n = 42
  x = 3.14159
  d = 1.0d0 / 3.0d0
  flag = .true.
  word = 'abc'
  print *, n
  print *, x
  print *, d
  print *, flag
  print *, word
  print *, n, x, flag
end program list_output
