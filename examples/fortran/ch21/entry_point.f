      subroutine counter_reset
      integer n, k
      save n
      n = 0
      return
      entry counter_next(k)
      n = n + 1
      k = n
      end

      program entry_point
      integer k
      call counter_reset
      call counter_next(k)
      call counter_next(k)
      write (*,'(i3)') k
      end
