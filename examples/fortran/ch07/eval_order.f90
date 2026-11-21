program eval_order
  implicit none
  logical :: r

  r = check(1) .or. check(2)
  print '(a, l1)', 'or:  ', r
  r = .not. check(1) .and. check(3)
  print '(a, l1)', 'and: ', r
contains
  logical function check(k)
    integer, intent(in) :: k

    print '(a, i0)', 'check called with ', k
    check = k == 1
  end function check
end program eval_order
