#!/bin/bash
# 힘 기준 수렴 테스트 (ML 퍼텐셜 학습 데이터용). 대칭 위치를 깨고 힘을 측정한다.
sed 's/  Si  0.25  0.25  0.25/  Si  0.26  0.25  0.25/' si.scf.in > si_disp.in
for E in 30 40 50 60 70 80 90; do
  sed -e "s/ecutwfc *=.*/ecutwfc      = $E/" \
      -e "s/ecutrho *=.*/ecutrho      = $((E*8))/" si_disp.in > tmp_f$E.in
  pw.x -in tmp_f$E.in > tmp_f$E.out
  F=$(grep 'atom    1 type  1   force' tmp_f$E.out | head -1 | awk '{print $7}')
  echo "$E  $F"   # Ry/bohr -> eV/A 환산: x 25.7110
done
