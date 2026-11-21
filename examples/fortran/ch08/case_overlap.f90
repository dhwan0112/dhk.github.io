program case_overlap
  implicit none
  integer :: n

  n = 5
  select case (n)
  case (1:5)
    print *, 'low'
  case (5:9)
    print *, 'high'
  end select
end program case_overlap
