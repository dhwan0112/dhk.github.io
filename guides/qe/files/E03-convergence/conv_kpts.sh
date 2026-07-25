#!/bin/bash
# k-point convergence scan
NAT=2
for K in 2 4 6 8 10 12 14 16; do
  sed "s/^ *[0-9]* [0-9]* [0-9]*  0 0 0/  $K $K $K  0 0 0/" si.scf.in > tmp_k$K.in
  pw.x -in tmp_k$K.in > tmp_k$K.out
  EN=$(grep '^!' tmp_k$K.out | tail -1 | awk '{print $5}')
  echo "$K  $EN"
done
