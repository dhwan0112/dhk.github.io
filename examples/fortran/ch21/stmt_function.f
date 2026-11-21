      program stmt_function
      real a, f, x
      f(x) = a*x + 1.0
      a = 2.0
      write (*,'(f6.1)') f(3.0)
      end
