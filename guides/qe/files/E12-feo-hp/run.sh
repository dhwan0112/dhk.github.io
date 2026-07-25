#!/bin/bash
set -e
pw.x -in feo_hp_scf.in > feo_hp_scf.out
hp.x -in feo.hp.in     > feo.hp.out
echo "--- 계산된 Hubbard 파라미터 ---"
cat FeO.Hubbard_parameters.dat
