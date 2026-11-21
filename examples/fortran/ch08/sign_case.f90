program sign_case
  implicit none
  integer :: n

  read (*, *) n
  select case (n)
  case (:-1)
    print *, 'negative'
  case (0)
    print *, 'zero'
  case (1:)
    print *, 'positive'
  end select
end program sign_case
