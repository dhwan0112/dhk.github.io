#!/bin/bash
# E12: tightly converged scf first, then the hp.x linear-response run.
# The result file lists U per atom plus the full chi0/chi matrices.
set -e
pw.x -in feo_hp_scf.in > feo_hp_scf.out   # ~3 min on 8 ranks (measured)
hp.x -in feo.hp.in     > feo.hp.out       # ~2 h on 8 ranks, 4 irreducible q (measured)
echo "--- computed Hubbard parameters ---"
cat FeO.Hubbard_parameters.dat
