      program assumed_size
      real x(5), total, old_total
      integer i
      do i = 1, 5
         x(i) = i
      end do
      write (*,'(2f6.1)') total(x, 5), old_total(x, 5)
      end

      real function total(v, n)
      integer n, i
      real v(*)
      total = 0.0
      do i = 1, n
         total = total + v(i)
      end do
      end

      real function old_total(v, n)
      integer n, i
      real v(1)
      old_total = 0.0
      do i = 1, n
         old_total = old_total + v(i)
      end do
      end
