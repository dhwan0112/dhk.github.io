program short_forms
  implicit none
  real :: a, b

  read *, a, b
  if (a > b) then
    print *, 'a is larger'
  else
    print *, 'b is larger or equal'
  end if
end program short_forms
