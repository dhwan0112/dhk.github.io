program find_pair
  implicit none
  integer :: i, j

  outer: do i = 1, 5
    inner: do j = 1, 5
      if (i * j == 12) then
        print '(a, i0, a, i0)', 'i = ', i, ', j = ', j
        exit outer
      end if
    end do inner
  end do outer
  print '(a, i0, a, i0)', 'stopped at i = ', i, ', j = ', j
end program find_pair
