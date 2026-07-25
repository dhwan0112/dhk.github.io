#!/bin/bash
# ecutwfc convergence scan; ecutrho follows at 8x (the PAW/US convention).
#
# For each cutoff E:
#   1. sed derives a scan input from si.scf.in, rewriting the two cutoff lines
#   2. pw.x runs it
#   3. grep '^!' picks the line "!    total energy = ..." (the converged value;
#      unmarked "total energy" lines are intermediate SCF iterations)
# Finally awk converts to meV/atom relative to the densest point:
#   dE [meV/atom] = (E - E_ref) * 13605.7 / nat     (1 Ry = 13605.7 meV)

NAT=2
printf "# ecutwfc(Ry)  E_total(Ry)   dE_vs_last(meV/atom)\n" > conv_ecut.dat
LAST=""
for E in 20 25 30 35 40 45 50 60 70 80; do
  sed -e "s/ecutwfc *=.*/ecutwfc      = $E/" \
      -e "s/ecutrho *=.*/ecutrho      = $((E*8))/" si.scf.in > tmp_e$E.in
  pw.x -in tmp_e$E.in > tmp_e$E.out
  EN=$(grep '^!' tmp_e$E.out | tail -1 | awk '{print $5}')
  echo "$E  $EN" >> conv_ecut.dat
  LAST=$EN
done
awk -v nat=$NAT -v ref="$LAST" '!/^#/{printf "%6s  %16s  %10.3f\n",$1,$2,($2-ref)*13605.7/nat}' conv_ecut.dat
