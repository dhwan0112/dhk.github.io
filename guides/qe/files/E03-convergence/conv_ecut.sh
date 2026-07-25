#!/bin/bash
# ecutwfc convergence scan; ecutrho follows at 8x (PAW/US convention).
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
