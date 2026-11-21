program modern_select
  implicit none
  integer :: k

  do k = 1, 4
    select case (k)
    case (1)
      print '(i2, a)', k, ' first'
    case (2)
      print '(i2, a)', k, ' second'
    case (3)
      print '(i2, a)', k, ' third'
    case default
      print '(i2, a)', k, ' other'
    end select
  end do
end program modern_select
