      program equiv_overlay
      real a(4), x, y
      equivalence (a(1), x), (a(2), y)
      a(1) = 1.5
      a(2) = 2.5
      write (*,'(2f6.1)') x, y
      end
