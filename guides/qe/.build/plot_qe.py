"""Generate the QE guide figures from actual pw.x runs (Quantum ESPRESSO 7.5,
conda-forge, WSL Ubuntu). English axis labels match the site convention; Korean
explanation goes in the HTML figcaptions.

Reads captured outputs under qe-demo/ and writes PNGs to ../assets/images/:
  qe-si-conv.png       E1  total energy vs ecutwfc and vs k-grid (Si)
  qe-si-bands-dos.png  E2  Si band structure (L-G-X-U-G) + DOS
  qe-al-dos.png        E3  Al metallic DOS with Fermi level
  qe-si-vcrelax.png    E4  energy & pressure vs BFGS step (Si vc-relax)

All data comes from the input decks stored alongside each dataset in qe-demo/.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

BUILD = Path(__file__).resolve().parent
D = BUILD / "qe-demo"
IMG = BUILD.parent / "assets" / "images"
IMG.mkdir(parents=True, exist_ok=True)
RY = 13.605693  # eV per Ry

mpl.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#4a5568", "axes.labelcolor": "#1a202c",
    "xtick.color": "#4a5568", "ytick.color": "#4a5568",
    "axes.grid": True, "grid.color": "#e2e8f0", "grid.linewidth": 0.7,
})
BLUE, GREEN, ORANGE, PURPLE, SLATE = "#2b6cb0", "#2f855a", "#c05621", "#805ad5", "#4a5568"


# ---------------- E1: convergence ----------------
ec = np.loadtxt(D / "e1" / "ecut.dat")   # ecutwfc(Ry), E(Ry)
kc = np.loadtxt(D / "e1" / "kconv.dat")   # n, E(Ry)
dE_ec = (ec[:, 1] - ec[-1, 1]) * RY * 1000 / 2.0   # meV/atom vs finest
dE_k = (kc[:, 1] - kc[-1, 1]) * RY * 1000 / 2.0

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 3.9), dpi=160)
a1.semilogy(ec[:-1, 0], np.abs(dE_ec[:-1]), marker="o", color=BLUE, linewidth=1.6)
a1.axhline(1.0, color=ORANGE, ls="--", lw=1, alpha=0.7, label="1 meV/atom")
a1.set_xlabel("ecutwfc  (Ry)")
a1.set_ylabel("|ΔE| to finest  (meV/atom)")
a1.set_title("Wavefunction cutoff convergence", fontsize=11, pad=8)
a1.legend(frameon=False, fontsize=9)
a2.semilogy(kc[:-1, 0], np.abs(dE_k[:-1]), marker="s", color=GREEN, linewidth=1.6)
a2.axhline(1.0, color=ORANGE, ls="--", lw=1, alpha=0.7, label="1 meV/atom")
a2.set_xlabel("k-grid  n  (n×n×n Monkhorst–Pack)")
a2.set_ylabel("|ΔE| to finest  (meV/atom)")
a2.set_title("k-point convergence", fontsize=11, pad=8)
a2.legend(frameon=False, fontsize=9)
fig.suptitle("Silicon SCF convergence  (QE 7.5, PBE US pseudo)", fontsize=12, y=1.02)
fig.tight_layout()
fig.savefig(IMG / "qe-si-conv.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("wrote qe-si-conv.png")


# ---------------- E2: bands + DOS ----------------
def read_gnu(path):
    bands, cur = [], []
    for line in open(path):
        s = line.split()
        if len(s) == 2:
            cur.append((float(s[0]), float(s[1])))
        elif cur:
            bands.append(np.array(cur)); cur = []
    if cur:
        bands.append(np.array(cur))
    return bands

vbm = float((D / "e2" / "vbm.txt").read_text().split()[0])
bands = read_gnu(D / "e2" / "si.bands.dat.gnu")
ticks = [(float(l.split()[0]), l.split()[1]) for l in open(D / "e2" / "ticks.txt")]
tick_x = [t[0] for t in ticks]
tick_l = [("Γ" if t[1] == "G" else t[1]) for t in ticks]

dos = np.loadtxt(D / "e2" / "si.dos", skiprows=1)  # E, dos, intdos
de, dd = dos[:, 0] - vbm, dos[:, 1]

# indirect gap: lowest band energy above VBM
allE = np.concatenate([b[:, 1] for b in bands]) - vbm
cbm = allE[allE > 0.05].min()

fig = plt.figure(figsize=(10.6, 4.6), dpi=160)
gs = fig.add_gridspec(1, 2, width_ratios=[3.1, 1.0], wspace=0.05)
axb = fig.add_subplot(gs[0]); axd = fig.add_subplot(gs[1], sharey=axb)

for b in bands:
    axb.plot(b[:, 0], b[:, 1] - vbm, color=BLUE, linewidth=1.3)
axb.axhline(0.0, color=SLATE, ls="--", lw=1, alpha=0.7)
axb.axhline(cbm, color=ORANGE, ls=":", lw=1, alpha=0.8)
for x in tick_x:
    axb.axvline(x, color="#cbd5e0", lw=0.8)
axb.set_xticks(tick_x); axb.set_xticklabels(tick_l)
axb.set_xlim(tick_x[0], tick_x[-1]); axb.set_ylim(-13, 8)
axb.set_ylabel("E − E$_{VBM}$  (eV)")
axb.set_title("Si band structure", fontsize=11, pad=8)
axb.grid(False)
axb.text(tick_x[-1] * 0.02, cbm + 0.3, f"indirect gap ≈ {cbm:.2f} eV",
         fontsize=9, color=ORANGE)

axd.plot(dd, de, color=BLUE, linewidth=1.4)
axd.fill_betweenx(de, 0, dd, where=(de <= 0), color=BLUE, alpha=0.13)
axd.axhline(0.0, color=SLATE, ls="--", lw=1, alpha=0.7)
axd.set_xlabel("DOS  (states/eV)")
axd.set_title("DOS", fontsize=11, pad=8)
axd.set_xlim(0, dd.max() * 1.05)
plt.setp(axd.get_yticklabels(), visible=False)
axd.grid(False)
fig.suptitle("Silicon: band structure + density of states  (QE 7.5, PBE)", fontsize=12, y=1.0)
fig.savefig(IMG / "qe-si-bands-dos.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote qe-si-bands-dos.png  (gap {cbm:.2f} eV)")


# ---------------- E3: Al metallic DOS ----------------
hdr = open(D / "e3" / "al.dos").readline()
ef = float(hdr.split("EFermi")[1].split("=")[1].split()[0])
al = np.loadtxt(D / "e3" / "al.dos", skiprows=1)
ae, ad = al[:, 0] - ef, al[:, 1]
dos_ef = np.interp(0.0, ae, ad)

fig, ax = plt.subplots(figsize=(6.6, 4.1), dpi=160)
ax.plot(ae, ad, color=GREEN, linewidth=1.6)
ax.fill_between(ae, 0, ad, where=(ae <= 0), color=GREEN, alpha=0.15)
ax.axvline(0.0, color=ORANGE, ls="--", lw=1.3)
ax.plot([0], [dos_ef], "o", color=ORANGE)
ax.annotate(f"E$_F$: DOS ≈ {dos_ef:.2f} states/eV\n(finite → metallic)",
            xy=(0, dos_ef), xytext=(1.5, dos_ef + 0.15),
            fontsize=9, color=ORANGE,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1))
ax.set_xlabel("E − E$_F$  (eV)")
ax.set_ylabel("DOS  (states/eV)")
ax.set_title("Aluminium DOS — metallic (QE 7.5, PBE, MV smearing)", fontsize=11, pad=8)
ax.set_xlim(ae.min(), ae.max())
ax.set_ylim(0, ad.max() * 1.1)
fig.tight_layout()
fig.savefig(IMG / "qe-al-dos.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote qe-al-dos.png  (DOS(EF)={dos_ef:.2f})")


# ---------------- E4: vc-relax convergence ----------------
tr = np.loadtxt(D / "e4" / "relax.dat")  # step, E(Ry), P(kbar)
step, E, P = tr[:, 0], tr[:, 1], tr[:, 2]
dE = (E - E[-1]) * RY * 1000 / 2.0  # meV/atom

fig, axL = plt.subplots(figsize=(6.8, 4.1), dpi=160)
axL.plot(step, dE, marker="o", color=BLUE, linewidth=1.6, label="ΔE (meV/atom)")
axL.set_xlabel("BFGS step")
axL.set_ylabel("E − E$_{final}$  (meV/atom)", color=BLUE)
axL.tick_params(axis="y", labelcolor=BLUE)
axL.axhline(0, color="#cbd5e0", lw=1)
axR = axL.twinx()
axR.spines.top.set_visible(False)
axR.plot(step, P, marker="s", color=ORANGE, linewidth=1.5, label="pressure (kbar)")
axR.set_ylabel("pressure  (kbar)", color=ORANGE)
axR.tick_params(axis="y", labelcolor=ORANGE)
axR.grid(False)
axL.set_title("Si vc-relax: energy & pressure vs step  (QE 7.5, PBE)", fontsize=11, pad=8)
# final lattice constant from volume (FCC primitive V = a^3/4)
V_ang3 = 40.90421
a0 = (4 * V_ang3) ** (1 / 3)
axL.text(0.97, 0.5, f"converged: a = {a0:.3f} Å\n(V = {V_ang3:.2f} Å³, P → 0)",
         transform=axL.transAxes, ha="right", va="center", fontsize=9, color=SLATE)
fig.tight_layout()
fig.savefig(IMG / "qe-si-vcrelax.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote qe-si-vcrelax.png  (a0={a0:.3f} Ang)")
