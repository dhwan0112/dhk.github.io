module particles
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none

  type :: vec3
    real(dp) :: x = 0.0_dp, y = 0.0_dp, z = 0.0_dp
  end type vec3

  type :: particle
    real(dp) :: mass = 1.0_dp
    type(vec3) :: pos
    real(dp), allocatable :: history(:)
  end type particle
end module particles

program nested
  use, intrinsic :: iso_fortran_env, only: dp => real64
  use particles, only: particle, vec3
  implicit none
  type(particle) :: a, b

  a%mass = 2.5_dp
  a%pos = vec3(1.0_dp, 2.0_dp, 3.0_dp)
  a%history = [0.5_dp, 1.5_dp]
  b = a
  b%pos%z = -1.0_dp
  b%history(1) = 9.0_dp

  print '(a, 3f6.2)', 'a%pos: ', a%pos%x, a%pos%y, a%pos%z
  print '(a, 3f6.2)', 'b%pos: ', b%pos%x, b%pos%y, b%pos%z
  print '(a, 2f6.2)', 'a%history: ', a%history
  print '(a, 2f6.2)', 'b%history: ', b%history
end program nested
