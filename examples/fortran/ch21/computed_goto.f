      program computed_goto
      integer k
      do k = 1, 4
         goto (10, 20, 30) k
         write (*,'(i2,a)') k, ' other'
         goto 50
   10    write (*,'(i2,a)') k, ' first'
         goto 50
   20    write (*,'(i2,a)') k, ' second'
         goto 50
   30    write (*,'(i2,a)') k, ' third'
   50    continue
      end do
      end
