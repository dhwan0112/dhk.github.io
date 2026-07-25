#!/bin/bash
set -e
pw.x -in feo_hp_scf.in > feo_hp_scf.out
hp.x -in feo.hp.in     > feo.hp.out
echo "--- computed Hubbard parameters ---"
cat FeO.Hubbard_parameters.dat
