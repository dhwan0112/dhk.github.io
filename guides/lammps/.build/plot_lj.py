"""Plot the LJ-fluid thermo trace from chapter 01 — temperature equilibration
and total-energy conservation under NVE. Data captured from an actual run of
the guide's in.lj script (LAMMPS 22 Jul 2025, conda-forge serial)."""

from __future__ import annotations
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl

steps  = [   0,    50,   100,   150,   200,   250]
temp   = [1.4400, 0.7437, 0.7572, 0.7518, 0.7514, 0.7595]
e_pair = [-6.7733681, -5.7370606, -5.7581426, -5.7510464, -5.7500924, -5.7621762]
toteng = [-4.6139081, -4.6218173, -4.6226965, -4.6235610, -4.6232753, -4.6231440]

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#4a5568",
    "axes.labelcolor": "#1a202c",
    "xtick.color": "#4a5568",
    "ytick.color": "#4a5568",
    "axes.grid": True,
    "grid.color": "#e2e8f0",
    "grid.linewidth": 0.7,
    "grid.linestyle": "-",
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.6), dpi=160)

ax1.plot(steps, temp, marker="o", linewidth=2, color="#2b6cb0", markersize=6)
ax1.set_xlabel("step")
ax1.set_ylabel("Temperature  (LJ units)")
ax1.set_title("Temperature: 1.44 -> ~0.75 (equilibration)", fontsize=11, pad=10)
ax1.axhline(y=0.75, color="#c05621", linestyle="--", linewidth=1, alpha=0.6, label="approx. eq.")
ax1.legend(loc="upper right", frameon=False, fontsize=9)

ax2.plot(steps, toteng, marker="s", linewidth=2, color="#2f855a", markersize=6, label="Total (E_pair + E_kin)")
ax2.plot(steps, e_pair, marker="^", linewidth=1.5, color="#805ad5", markersize=5, alpha=0.7, label="E_pair")
ax2.set_xlabel("step")
ax2.set_ylabel("Energy  (LJ units / atom)")
ax2.set_title("Total energy stays ~constant (NVE conservation)", fontsize=11, pad=10)
ax2.legend(loc="center right", frameon=False, fontsize=9)

ax2.set_ylim(-7.0, -4.2)

fig.suptitle("LJ fluid, NVE 250 steps  (lattice fcc 0.8442, 4000 atoms, LAMMPS 22 Jul 2025)",
             fontsize=12, y=1.02, color="#1a202c")
fig.tight_layout()

out = Path(__file__).resolve().parent.parent / "assets" / "images" / "lj-thermo.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, bbox_inches="tight", facecolor="white")
print(f"wrote {out}  ({out.stat().st_size} bytes)")
