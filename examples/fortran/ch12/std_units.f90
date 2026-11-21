program std_units
  use, intrinsic :: iso_fortran_env, only: input_unit, output_unit, error_unit
  implicit none
  real :: r

  write (output_unit, *) 'Give radius r:'
  read (input_unit, *) r
  if (r < 0.0) then
    write (error_unit, *) 'radius must not be negative'
  else
    write (output_unit, '(a, f8.3)') 'Area = ', 3.14159 * r * r
  end if
end program std_units
