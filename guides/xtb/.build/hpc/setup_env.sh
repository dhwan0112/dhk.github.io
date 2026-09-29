#!/bin/bash
# One-time setup on the cluster login node: a conda env with xtb, crest and the
# analysis stack, then the starting geometry.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v conda >/dev/null 2>&1 && ! command -v mamba >/dev/null 2>&1; then
    if [ ! -x "$HOME/miniforge3/bin/conda" ]; then
        wget -q https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O /tmp/mf.sh
        bash /tmp/mf.sh -b -p "$HOME/miniforge3"
    fi
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
fi
CONDA=$(command -v mamba || command -v conda)

if ! $CONDA env list | grep -q '^guide-xtb '; then
    $CONDA create -y -n guide-xtb -c conda-forge xtb crest rdkit numpy matplotlib pillow
fi

source "$($CONDA info --base)/etc/profile.d/conda.sh"
conda activate guide-xtb
xtb --version | head -5
crest --version | head -5 || true
python make_start.py
