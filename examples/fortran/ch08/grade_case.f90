program grade_case
  implicit none
  integer :: score

  read (*, *) score
  select case (score)
  case (90:100)
    print *, 'A'
  case (80:89)
    print *, 'B'
  case (60:79)
    print *, 'C'
  case (0:59)
    print *, 'F'
  case default
    print *, 'score out of range'
  end select
end program grade_case
