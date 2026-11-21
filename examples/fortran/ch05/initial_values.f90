program initial_values
  implicit none
  real :: a(3) = 0.0
  integer :: v(3) = [10, 20, 30]
  integer :: m(2, 2) = reshape([1, 2, 3, 4], [2, 2])
  character(len=8) :: tag = 'run'

  print '(3f5.1)', a
  print '(3i4)', v
  print '(2i4)', m(1, :)
  print '(2i4)', m(2, :)
  print '(a, a, a)', '[', tag, ']'
end program initial_values
