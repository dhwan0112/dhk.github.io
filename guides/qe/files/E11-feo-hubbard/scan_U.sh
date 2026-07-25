#!/bin/bash
# U 스캔: 밴드갭과 Fe 국소 모멘트의 U 의존성을 본다
for U in 0.001 2.0 4.0 4.6 6.0 8.0; do
  sed -e "s/^U Fe1-3d .*/U Fe1-3d $U/" -e "s/^U Fe2-3d .*/U Fe2-3d $U/" \
      -e "s/prefix      = 'FeO_U'/prefix      = 'FeO_U$U'/" feo_u.scf.in > tmp_U$U.in
  pw.x -in tmp_U$U.in > tmp_U$U.out
  GAP=$(grep 'highest occupied, lowest unoccupied' tmp_U$U.out | tail -1)
  MAG=$(grep 'total magnetization' tmp_U$U.out | tail -1)
  ABS=$(grep 'absolute magnetization' tmp_U$U.out | tail -1)
  echo "U=$U | $GAP | $MAG | $ABS"
done
