#!/bin/bash
# The whole E07 pipeline in order. Everything is glued together by the
# same prefix ('si') and outdir ('./tmp/'); break either and the chain dies.
set -e
pw.x       -in si.scf.in     > si.scf.out      # 1. converge the density
pw.x       -in si.nscf.in    > si.nscf.out     # 2. dense-grid eigenvalues
dos.x      -in si.dos.in     > si.dos.out      # 3. total DOS -> si.dos
projwfc.x  -in si.projwfc.in > si.projwfc.out  # 4. PDOS + Lowdin charges
grep -A20 'Lowdin Charges' si.projwfc.out      # show the per-orbital occupations
