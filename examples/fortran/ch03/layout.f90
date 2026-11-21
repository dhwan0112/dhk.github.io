program layout
  implicit none
  real :: total
  integer :: i, j

  ! 느낌표 뒤는 줄 끝까지 주석이다.
  total = 1.0 + 2.0 + 3.0 &
        + 4.0 + 5.0
  i = 1; j = 2
  print *, total, i + j
end program layout
