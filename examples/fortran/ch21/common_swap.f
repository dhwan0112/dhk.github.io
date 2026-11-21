      program common_swap
      real alpha, beta
      common /coeff/ alpha, beta
      alpha = 1.0
      beta = 2.0
      call sub4
      end

      subroutine sub4
      real alpha, beta
      common /coeff/ beta, alpha
      write (*,'(a,f4.1,a,f4.1)') 'alpha = ', alpha, ', beta = ', beta
      end
