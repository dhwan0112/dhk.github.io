module counter
  implicit none
  private
  public :: calls, record_call, last_call
  integer, protected :: calls = 0
  integer :: last_value = -1
contains
  subroutine record_call(value)
    integer, intent(in) :: value

    calls = calls + 1
    last_value = value
  end subroutine record_call

  function last_call() result(v)
    integer :: v

    v = last_value
  end function last_call
end module counter

program counter_demo
  use counter, only: calls, record_call, last_call
  implicit none

  call record_call(10)
  call record_call(20)
  call record_call(30)
  print '(a, i0, a, i0)', 'calls: ', calls, '  last: ', last_call()
end program counter_demo
