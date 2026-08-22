"""z-number-density profile per atom type from a LAMMPS dump (ASE + pandas).

usage: python zprofile.py dump.lammpstrj [dz]  ->  zprofile.csv
"""
import sys
import numpy as np
import pandas as pd
from ase.io import iread


def z_profile(dumpfile, dz=0.25):
    """Return a DataFrame: index = bin centre z (Å), one column per LAMMPS type,
    values = number density (atoms/Å^3) averaged over all frames in the dump."""
    counts, nframes, edges, area = {}, 0, None, None
    for atoms in iread(dumpfile, format="lammps-dump-text", index=":"):
        lx, ly, lz = atoms.cell.lengths()
        if edges is None:                       # bins fixed by the first frame
            edges = np.arange(0.0, lz + dz, dz)
            area = lx * ly
        z = atoms.positions[:, 2]
        types = atoms.arrays["type"]            # ASE keeps the LAMMPS type here
        for t in np.unique(types):
            h, _ = np.histogram(z[types == t], bins=edges)
            counts[t] = counts.get(t, 0) + h
        nframes += 1
    centres = 0.5 * (edges[:-1] + edges[1:])
    df = pd.DataFrame({f"type{t}": c / (nframes * area * dz) for t, c in counts.items()},
                      index=pd.Index(centres, name="z"))
    df.attrs["nframes"] = nframes
    return df


if __name__ == "__main__":
    dump = sys.argv[1]
    dz = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
    prof = z_profile(dump, dz)
    prof.to_csv("zprofile.csv", float_format="%.6f")
    print(f"{prof.attrs['nframes']} frame(s), {len(prof)} bins of {dz} Å")
    print(prof[prof.sum(axis=1) > 0].head(8))
