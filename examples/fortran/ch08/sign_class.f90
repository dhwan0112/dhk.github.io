program sign_class
  implicit none
  integer :: n

  read (*, *) n
  if (n > 0) then
    print *, 'positive'
  else if (n < 0) then
    print *, 'negative'
  else
    print *, 'zero'
  end if
end program sign_class
