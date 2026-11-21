program char_case
  implicit none
  character(len=8) :: answer

  answer = 'yes'
  select case (answer)
  case ('y', 'yes')
    print *, 'accepted'
  case ('n', 'no')
    print *, 'rejected'
  case default
    print *, 'unknown answer'
  end select
end program char_case
