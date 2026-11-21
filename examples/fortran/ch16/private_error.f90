module counter
  implicit none
  private
  public :: calls
  integer :: calls = 0
  integer :: last_value = -1
end module counter

program private_error
  use counter
  implicit none

  print *, last_value
end program private_error
