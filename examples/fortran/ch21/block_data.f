      block data init
      real v(3), alpha
      common /vector/ v, alpha
      data v /3*100.0/, alpha /3.14/
      end

      program use_block_data
      real v(3), alpha
      common /vector/ v, alpha
      write (*,'(4f8.2)') v, alpha
      end
