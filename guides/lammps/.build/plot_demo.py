"""Generate three figures from the LAMMPS demo run (Chapters 6 & 7):
  1. lj-production.png — Temp / Press / Density vs step during NPT production
  2. lj-rdf.png         — radial distribution function g(r)
  3. lj-msd.png         — mean squared displacement vs time + linear fit (self-diffusion)

All data was captured from an actual run of in.demo (LAMMPS 22 Jul 2025,
serial, in a conda-forge env on WSL Ubuntu 24.04). The matplotlib styling
mirrors the existing lj-thermo.png to keep the visual language consistent."""

from __future__ import annotations
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

BUILD = Path(__file__).resolve().parent
DEMO = BUILD / "lammps-demo"
IMG = BUILD.parent / "assets" / "images"
IMG.mkdir(parents=True, exist_ok=True)


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
})


def parse_thermo(out_path: Path):
    """Yield blocks of thermo data (one per `run`). Each block is a list of
    (step, temp, press, peng, keng, etotal, density)."""
    blocks = []
    cur = []
    with open(out_path, encoding="utf-8") as f:
        in_block = False
        for line in f:
            if line.startswith("Per MPI rank memory"):
                if cur:
                    blocks.append(cur)
                    cur = []
                in_block = True
                continue
            if line.startswith("Loop time"):
                if cur:
                    blocks.append(cur)
                    cur = []
                in_block = False
                continue
            if not in_block:
                continue
            parts = line.split()
            if not parts or parts[0] == "Step":
                continue
            try:
                row = [float(p) for p in parts]
                if len(row) == 7:
                    cur.append(row)
            except ValueError:
                continue
    if cur:
        blocks.append(cur)
    return blocks


# ------------- figure 1: NPT production thermo ----------------------
blocks = parse_thermo(DEMO / "out.demo")
# Expected stage order (after the cg minimize block which has only 1-2 rows):
#   block 0: cg minimize (short)
#   block 1: NVT 2000
#   block 2: NPT 3000
#   block 3: production 5000
print(f"thermo blocks found: {len(blocks)}, sizes = {[len(b) for b in blocks]}")
prod = np.array(blocks[-1])

steps = prod[:, 0]
temp  = prod[:, 1]
press = prod[:, 2]
density = prod[:, 6]

fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.6), dpi=160)
axes[0].plot(steps, temp,    color="#2b6cb0", linewidth=1.5)
axes[0].axhline(1.0, color="#c05621", linestyle="--", linewidth=1, alpha=0.6, label="setpoint T = 1.0")
axes[0].set_xlabel("step")
axes[0].set_ylabel("Temperature  (LJ)")
axes[0].set_title("Temperature trace (NPT thermostat)", fontsize=11, pad=8)
axes[0].legend(loc="lower right", frameon=False, fontsize=9)

axes[1].plot(steps, press,   color="#2f855a", linewidth=1.5)
axes[1].axhline(0.5, color="#c05621", linestyle="--", linewidth=1, alpha=0.6, label="setpoint P = 0.5")
axes[1].set_xlabel("step")
axes[1].set_ylabel("Pressure  (LJ)")
axes[1].set_title("Pressure trace (NPT barostat)", fontsize=11, pad=8)
axes[1].legend(loc="lower right", frameon=False, fontsize=9)

axes[2].plot(steps, density, color="#805ad5", linewidth=1.5)
axes[2].set_xlabel("step")
axes[2].set_ylabel("Density  (LJ)")
axes[2].set_title("Density (relaxing under NPT)", fontsize=11, pad=8)

fig.suptitle("LJ liquid, NPT production 5000 steps  (T = 1.0, P = 0.5)",
             fontsize=12, y=1.02)
fig.tight_layout()
out1 = IMG / "lj-production.png"
fig.savefig(out1, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote {out1.name}  ({out1.stat().st_size} bytes)")


# ------------- figure 2: radial distribution function -----------------
# rdf.dat layout: 3 comment lines, then "<TimeStep> <Nrows>", then Nrows of "row r g(r) coord"
rdf_rows = [l for l in open(DEMO / "rdf.dat", encoding="utf-8")
            if not l.startswith("#") and len(l.split()) == 4]
rdf = np.array([[float(x) for x in r.split()] for r in rdf_rows])[:, 1:]
r, gr, coord = rdf[:, 0], rdf[:, 1], rdf[:, 2]


fig, ax1 = plt.subplots(figsize=(6.5, 4.0), dpi=160)
ax1.plot(r, gr, color="#2b6cb0", linewidth=2, label="g(r)")
ax1.axhline(1.0, color="#718096", linestyle=":", linewidth=1)
ax1.set_xlabel("r  (LJ units σ)")
ax1.set_ylabel("g(r)", color="#2b6cb0")
ax1.tick_params(axis="y", labelcolor="#2b6cb0")
ax1.set_xlim(0, r.max())
ax1.set_ylim(0, max(gr) * 1.1)

# annotate first peak
peak_idx = int(np.argmax(gr))
ax1.annotate(f"first peak r ≈ {r[peak_idx]:.2f}σ\ng(r) ≈ {gr[peak_idx]:.2f}",
             xy=(r[peak_idx], gr[peak_idx]),
             xytext=(r[peak_idx] + 0.3, gr[peak_idx] - 0.5),
             fontsize=9,
             arrowprops=dict(arrowstyle="->", color="#4a5568", lw=1))

ax2 = ax1.twinx()
ax2.spines.top.set_visible(False)
ax2.plot(r, coord, color="#c05621", linewidth=1.3, linestyle="--", label="coord N(r)")
ax2.set_ylabel("N(r)  (running coordination)", color="#c05621")
ax2.tick_params(axis="y", labelcolor="#c05621")
ax2.grid(False)

ax1.set_title("LJ liquid g(r) at T = 1.0, ρ ≈ 0.70  (5000-step time-averaged)", fontsize=11, pad=10)
fig.tight_layout()
out2 = IMG / "lj-rdf.png"
fig.savefig(out2, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote {out2.name}  ({out2.stat().st_size} bytes)")


# ------------- figure 3: MSD + diffusion fit --------------------------
msd = np.loadtxt(DEMO / "msd.dat", comments="#")
step = msd[:, 0]
msd_tot = msd[:, 4]      # column "MSD_total"
t = step * 0.005          # dt in LJ units = 0.005 (default)

# linear fit on the late-time portion (drop first 25%)
n = len(t)
i0 = n // 4
slope, intercept = np.polyfit(t[i0:], msd_tot[i0:], 1)
D = slope / 6.0          # Einstein: MSD = 6 D t  in 3D

fig, ax = plt.subplots(figsize=(6.5, 4.0), dpi=160)
ax.plot(t, msd_tot, color="#2f855a", linewidth=2, label="MSD total")
ax.plot(t, msd[:, 1], color="#805ad5", linewidth=1, alpha=0.6, label="MSD_x")
ax.plot(t, msd[:, 2], color="#c05621", linewidth=1, alpha=0.6, label="MSD_y")
ax.plot(t, msd[:, 3], color="#9b2c2c", linewidth=1, alpha=0.6, label="MSD_z")
fit_x = np.array([t[i0], t[-1]])
ax.plot(fit_x, slope * fit_x + intercept, color="#1a202c", linestyle="--", linewidth=1,
        label=f"linear fit:  D ≈ {D:.3f}")
ax.set_xlabel("time t  (LJ units τ)")
ax.set_ylabel("⟨ Δr²(t) ⟩")
ax.set_title("Mean squared displacement, LJ liquid (Einstein relation: MSD = 6Dt)",
             fontsize=11, pad=10)
ax.legend(loc="upper left", frameon=False, fontsize=9)

fig.tight_layout()
out3 = IMG / "lj-msd.png"
fig.savefig(out3, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote {out3.name}  ({out3.stat().st_size} bytes)")
print(f"\nfitted self-diffusion coefficient D = {D:.4f}  (LJ units)")
