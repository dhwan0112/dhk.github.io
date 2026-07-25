#!/bin/bash
# Force-based convergence scan (the criterion that matters for ML training
# data). On a perfectly symmetric structure every force is zero, so first
# break the symmetry: move the second Si from 0.25 to 0.26 along x.
sed 's/  Si  0.25  0.25  0.25/  Si  0.26  0.25  0.25/' si.scf.in > si_disp.in
for E in 30 40 50 60 70 80 90; do
  sed -e "s/ecutwfc *=.*/ecutwfc      = $E/" \
      -e "s/ecutrho *=.*/ecutrho      = $((E*8))/" si_disp.in > tmp_f$E.in
  pw.x -in tmp_f$E.in > tmp_f$E.out
  # The FIRST "atom 1 ... force" match after 'Forces acting on atoms' is the
  # total force. Later matches are the contribution breakdown (the last one
  # is the ~1e-6 SCF correction), so head -1 here, never tail -1.
  F=$(grep 'atom    1 type  1   force' tmp_f$E.out | head -1 | awk '{print $7}')
  echo "$E  $F"   # Ry/bohr -> eV/A: multiply by 25.7110
done
