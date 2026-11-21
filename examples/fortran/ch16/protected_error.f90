module counter
  implicit none
  integer, protected :: calls = 0
end module counter

program protected_error
  use counter, only: calls
  implicit none

  calls = 0
end program protected_error
