#!/bin/bash
set -e
pw.x       -in si.scf.in     > si.scf.out
pw.x       -in si.nscf.in    > si.nscf.out
dos.x      -in si.dos.in     > si.dos.out
projwfc.x  -in si.projwfc.in > si.projwfc.out
grep -A20 'Lowdin Charges' si.projwfc.out
