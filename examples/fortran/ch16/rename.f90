module fluid_props
  implicit none
  real, parameter :: density = 1000.0
  real, parameter :: viscosity = 1.0e-3
end module fluid_props

module solid_props
  implicit none
  real, parameter :: density = 7800.0
end module solid_props

program rename
  use fluid_props, only: water_density => density
  use solid_props, only: steel_density => density
  implicit none

  print '(a, f7.1)', 'water: ', water_density
  print '(a, f7.1)', 'steel: ', steel_density
  print '(a, f5.2)', 'ratio: ', steel_density / water_density
end program rename
