      program arith_if
      integer n
      n = -2
      if (n) 10, 20, 30
   10 write (*,*) 'negative'
      goto 40
   20 write (*,*) 'zero'
      goto 40
   30 write (*,*) 'positive'
   40 continue
      end
