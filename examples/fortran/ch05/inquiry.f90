program inquiry
  use, intrinsic :: iso_fortran_env, only: int32, real32, real64
  implicit none

  print '(a, i0)', 'huge(1_int32)         = ', huge(1_int32)
  print '(a, es11.4)', 'huge(1.0_real32)      = ', huge(1.0_real32)
  print '(a, es12.4e3)', 'huge(1.0_real64)      = ', huge(1.0_real64)
  print '(a, es12.4e3)', 'tiny(1.0_real64)      = ', tiny(1.0_real64)
  print '(a, es11.4)', 'epsilon(1.0_real32)   = ', epsilon(1.0_real32)
  print '(a, es11.4)', 'epsilon(1.0_real64)   = ', epsilon(1.0_real64)
  print '(a, i0)', 'precision(1.0_real32) = ', precision(1.0_real32)
  print '(a, i0)', 'precision(1.0_real64) = ', precision(1.0_real64)
  print '(a, i0)', 'range(1.0_real64)     = ', range(1.0_real64)
end program inquiry
