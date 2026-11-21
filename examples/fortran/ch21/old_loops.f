      program old_loops
      integer i, n, total
      total = 0
      do 10 i = 1, 4
         total = total + i
   10 continue
      write (*,'(a,i3)') 'sum =', total
      n = 1
   20 if (n .le. 100) then
         write (*,'(i4)') n
         n = 2*n
         goto 20
      endif
   30 continue
         n = n - 50
      if (n .gt. 0) goto 30
      write (*,'(a,i4)') 'n =', n
      end
