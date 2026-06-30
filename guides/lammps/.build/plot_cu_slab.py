"""Cu(100) slab figure for cu-01 (English labels — matches site convention;
Korean goes in the HTML figcaption).

Reproduces assets/images/cu-slab.png from an actual LAMMPS run. The run inputs
and captured outputs live in cu-demo/ (in.cu_slab + slab_final.dump + zdens.dat),
generated with LAMMPS 22 Jul 2025 (conda-forge, serial) using the EAM Cu
potential of Mishin et al. (Phys. Rev. B 63, 224106, 2001). To re-run the MD:
    lmp -in cu-demo/in.cu_slab        # needs Cu_mishin1.eam.alloy in the run dir
                                      # (lammps.org potentials: Cu_mishin1.eam.alloy)
then point W at the run directory. By default we read the captured cu-demo/ data."""
from pathlib import Path
import numpy as np, matplotlib as mpl
mpl.use("Agg"); import matplotlib.pyplot as plt

BUILD = Path(__file__).resolve().parent
W = BUILD / "cu-demo"
IMG = BUILD.parent / "assets" / "images"
IMG.mkdir(parents=True, exist_ok=True)

lines = open(W/"slab_final.dump").read().splitlines()
i  = next(k for k,l in enumerate(lines) if l.startswith("ITEM: ATOMS"))
bi = next(k for k,l in enumerate(lines) if l.startswith("ITEM: BOX BOUNDS"))
box = [[float(v) for v in lines[bi+k].split()] for k in (1,2,3)]
atoms = np.array([[float(v) for v in l.split()] for l in lines[i+1:] if l.strip()])
x, z = atoms[:,2], atoms[:,4]
zlo, zhi = box[2]

rows = [l for l in open(W/"zdens.dat") if not l.startswith("#") and len(l.split())==4]
prof = np.array([[float(v) for v in r.split()] for r in rows])
zc, dens = prof[:,1], prof[:,3]

mpl.rcParams.update({
 "font.family":"DejaVu Sans","font.size":11,
 "axes.spines.top":False,"axes.spines.right":False,
 "axes.edgecolor":"#4a5568","axes.labelcolor":"#1a202c",
 "xtick.color":"#4a5568","ytick.color":"#4a5568",
 "axes.grid":True,"grid.color":"#e2e8f0","grid.linewidth":0.7})

fig,(axL,axR)=plt.subplots(1,2,figsize=(11.0,4.4),dpi=160,
                           gridspec_kw={"width_ratios":[1.25,1]})

axL.axhspan(z.max()+0.4, zhi, color="#ebf4ff", alpha=0.7)
axL.scatter(x, z, s=16, c="#b87333", edgecolors="#7a4a1e", linewidths=0.3, alpha=0.95)
axL.text((x.min()+x.max())/2, (z.max()+zhi)/2, "vacuum",
         ha="center", va="center", fontsize=12, color="#3b5b8c", style="italic")
axL.set_xlabel("x  (Å)   — periodic boundary (p)")
axL.set_ylabel("z  (Å)   — non-periodic boundary (f)")
axL.set_title("Cu(100) slab, side view  (x–z projection, 300 K)", fontsize=11, pad=8)
axL.set_ylim(zlo-1, zhi+1); axL.grid(False)

axR.plot(dens, zc, color="#2b6cb0", linewidth=1.5)
axR.fill_betweenx(zc, 0, dens, color="#2b6cb0", alpha=0.12)
axR.set_xlabel("number density  (atoms / Å³)")
axR.set_ylabel("z  (Å)")
axR.set_title("Number-density profile along z", fontsize=11, pad=8)
axR.set_ylim(zlo-1, zhi+1)
axR.text(0.96, 0.97, "(100) layer spacing ≈ 1.81 Å\neach peak = one atomic plane",
         transform=axR.transAxes, ha="right", va="top", fontsize=9, color="#4a5568")

fig.suptitle("Cu(100) slab — periodic x·y, vacuum in z   (EAM, Mishin 2001; a = 3.615 Å; standalone run)",
             fontsize=12, y=1.02)
fig.tight_layout()
out = IMG/"cu-slab.png"
fig.savefig(out, bbox_inches="tight", facecolor="white")
nlayers = int(np.sum(dens > dens.max()*0.25))
print(f"wrote {out} ({out.stat().st_size} bytes); natoms={len(atoms)}; "
      f"layers~{nlayers}; slab z=[{z.min():.1f},{z.max():.1f}]; box z=[{zlo:.1f},{zhi:.1f}]")
