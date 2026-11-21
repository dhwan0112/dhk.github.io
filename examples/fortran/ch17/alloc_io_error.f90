program alloc_io_error
  implicit none

  type :: series
    integer :: n = 0
    real, allocatable :: values(:)
  end type series

  type(series) :: s

  s%n = 2
  s%values = [1.0, 2.0]
  print *, s
end program alloc_io_error
