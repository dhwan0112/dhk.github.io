"""Generate the QE guide figures from actual pw.x runs (Quantum ESPRESSO 7.5,
conda-forge, WSL Ubuntu). All labels and captions are English.

Reads captured outputs under qe-demo/ and writes PNGs to ../assets/images/:
  qe-e03-convergence.png   E3  dE vs ecutwfc / dE vs k-grid / force convergence
  qe-e05-smearing.png      E5  Al energy vs degauss per smearing type
  qe-e06-vcrelax.png       E6  Si vc-relax energy & pressure per BFGS step
  qe-e07-dos-pdos.png      E7  Si total DOS + s/p PDOS
  qe-e08-bands.png         E8  Si band structure L-G-X-W-K-G
  qe-e09-fe-dos.png        E9  bcc Fe spin-resolved DOS
  qe-e10-e11-feo-dos.png   E10/E11  FeO DOS: GGA (metal) vs GGA+U (gap)
  qe-e13-workfunction.png  E13 planar-averaged potential (if data present)
  qe-e13-md.png            E13 BOMD temperature & conserved energy (if present)

Derived numbers (gaps, lattice constants) are printed so the page text can
quote them.
"""
from __future__ import annotations
from pathlib import Path
import re
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

BUILD = Path(__file__).resolve().parent
D = BUILD / "qe-demo"
IMG = BUILD.parent / "assets" / "images"
IMG.mkdir(parents=True, exist_ok=True)
RY = 13.605693          # eV per Ry
RYB = 25.71104          # (Ry/bohr -> eV/A)

mpl.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#4a5568", "axes.labelcolor": "#1a202c",
    "xtick.color": "#4a5568", "ytick.color": "#4a5568",
    "axes.grid": True, "grid.color": "#e2e8f0", "grid.linewidth": 0.7,
})
BLUE, GREEN, ORANGE, RED, SLATE = "#2b6cb0", "#2f855a", "#c05621", "#9b2c2c", "#4a5568"


# ---------------- E3: convergence ----------------
ec = np.loadtxt(D / "e03" / "conv_ecut.dat")
kc = np.loadtxt(D / "e03" / "conv_kpts.dat")
fc = np.loadtxt(D / "e03" / "conv_force_fixed.dat")
dE_ec = np.abs(ec[:, 1] - ec[-1, 1]) * RY * 1000 / 2.0
dE_k = np.abs(kc[:, 1] - kc[-1, 1]) * RY * 1000 / 2.0
dF = np.abs(fc[:, 1] - fc[-1, 1]) * RYB * 1000  # meV/A

fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(12.6, 3.8), dpi=160)
a1.semilogy(ec[:-1, 0], dE_ec[:-1], marker="o", color=BLUE, lw=1.6)
a1.axhline(1.0, color=ORANGE, ls="--", lw=1, alpha=0.7, label="1 meV/atom")
a1.set_xlabel("ecutwfc  (Ry)")
a1.set_ylabel("|ΔE| to 80 Ry  (meV/atom)")
a1.set_title("Cutoff convergence", fontsize=11, pad=8)
a1.legend(frameon=False, fontsize=9)
a2.semilogy(kc[:-1, 0], dE_k[:-1], marker="s", color=GREEN, lw=1.6)
a2.axhline(1.0, color=ORANGE, ls="--", lw=1, alpha=0.7, label="1 meV/atom")
a2.set_xlabel("k-grid  n  (n×n×n)")
a2.set_ylabel("|ΔE| to 16³  (meV/atom)")
a2.set_title("k-point convergence", fontsize=11, pad=8)
a2.legend(frameon=False, fontsize=9)
a3.semilogy(fc[:-1, 0], np.clip(dF[:-1], 1e-3, None), marker="^", color=RED, lw=1.6)
a3.axhline(1.0, color=ORANGE, ls="--", lw=1, alpha=0.7, label="1 meV/Å")
a3.set_xlabel("ecutwfc  (Ry)")
a3.set_ylabel("|ΔF| to 90 Ry  (meV/Å)")
a3.set_title("Force convergence (displaced)", fontsize=11, pad=8)
a3.legend(frameon=False, fontsize=9)
fig.suptitle("Silicon convergence tests  (QE 7.5, PAW, ecutrho = 8×ecutwfc)", fontsize=12, y=1.03)
fig.tight_layout()
fig.savefig(IMG / "qe-e03-convergence.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("wrote qe-e03-convergence.png")


# ---------------- E5: smearing scan ----------------
rows = []
for line in (D / "e05" / "smear_scan.dat").read_text().splitlines()[1:]:
    p = line.split()
    if len(p) == 4:
        rows.append((p[0], float(p[1]), float(p[2]), float(p[3])))
types = {"gauss": ("gaussian", BLUE, "o"), "mv": ("mv (cold)", GREEN, "s"),
         "fd": ("fermi-dirac", ORANGE, "^")}
eref = [r[2] for r in rows if r[0] == "mv" and r[1] == 0.01][0]

fig, ax = plt.subplots(figsize=(6.8, 4.2), dpi=160)
for key, (label, color, mk) in types.items():
    xs = [r[1] for r in rows if r[0] == key]
    ys = [(r[2] - eref) * 1000 for r in rows if r[0] == key]  # mRy
    ax.plot(xs, ys, marker=mk, color=color, lw=1.6, label=label)
ax.axhline(0, color="#cbd5e0", lw=1)
ax.set_xlabel("degauss  (Ry)")
ax.set_ylabel("E − E(mv, 0.01 Ry)  (mRy)")
ax.set_title("fcc Al: smearing type vs degauss  (QE 7.5, 12³ k)", fontsize=11, pad=8)
ax.legend(frameon=False, fontsize=9)
ax.annotate("mv @ 0.005 fails:\n'charge is wrong'\n(k-grid too coarse)",
            xy=(0.005, -0.5), xytext=(0.008, -13), fontsize=8.5, color=SLATE,
            arrowprops=dict(arrowstyle="->", color=SLATE, lw=0.9))
fig.tight_layout()
fig.savefig(IMG / "qe-e05-smearing.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("wrote qe-e05-smearing.png")


# ---------------- E6: vc-relax trajectory ----------------
text = (D / "e06" / "si.vcrelax.out").read_text()
energies = [float(m) for m in re.findall(r"^!\s+total energy\s+=\s+(-?\d+\.\d+)", text, re.M)]
pressures = [float(m) for m in re.findall(r"P=\s+(-?\d+\.\d+)", text)]
vols = re.findall(r"new unit-cell volume\s+=\s+\d+\.\d+ a\.u\.\^3 \(\s*(\d+\.\d+) Ang\^3", text)
a0 = (4 * float(vols[-1])) ** (1 / 3)
n = min(len(energies), len(pressures))
step = np.arange(1, n + 1)
dE = (np.array(energies[:n]) - energies[n - 1]) * RY * 1000 / 2.0

fig, axL = plt.subplots(figsize=(6.8, 4.1), dpi=160)
axL.plot(step, dE, marker="o", color=BLUE, lw=1.6)
axL.set_xlabel("BFGS step")
axL.set_ylabel("E − E$_{final}$  (meV/atom)", color=BLUE)
axL.tick_params(axis="y", labelcolor=BLUE)
axL.axhline(0, color="#cbd5e0", lw=1)
axR = axL.twinx()
axR.spines.top.set_visible(False)
axR.plot(step, pressures[:n], marker="s", color=ORANGE, lw=1.5)
axR.set_ylabel("pressure  (kbar)", color=ORANGE)
axR.tick_params(axis="y", labelcolor=ORANGE)
axR.grid(False)
axL.set_title("Si vc-relax: energy & pressure per step  (QE 7.5, PBE)", fontsize=11, pad=8)
axL.text(0.97, 0.55, f"converged: a = {a0:.3f} Å\n(exp. 5.431 Å, +{(a0/5.431-1)*100:.2f}%)",
         transform=axL.transAxes, ha="right", va="center", fontsize=9, color=SLATE)
fig.tight_layout()
fig.savefig(IMG / "qe-e06-vcrelax.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote qe-e06-vcrelax.png  (a0={a0:.4f} A, P0={pressures[0]:.1f} kbar, steps={n})")


# ---------------- E7: DOS + PDOS ----------------
VBM = 6.2124
dos = np.loadtxt(D / "e07" / "si.dos", skiprows=1)
pd_s = np.loadtxt(D / "e07" / "si.pdos_atm1_s.dat", skiprows=1)
pd_p = np.loadtxt(D / "e07" / "si.pdos_atm1_p.dat", skiprows=1)

fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=160)
ax.plot(dos[:, 0] - VBM, dos[:, 1], color=SLATE, lw=1.5, label="total DOS")
ax.fill_between(dos[:, 0] - VBM, 0, dos[:, 1], color=SLATE, alpha=0.10)
ax.plot(pd_s[:, 0] - VBM, 2 * pd_s[:, 1], color=BLUE, lw=1.3, label="Si s (×2 atoms)")
ax.plot(pd_p[:, 0] - VBM, 2 * pd_p[:, 1], color=GREEN, lw=1.3, label="Si p (×2 atoms)")
ax.axvline(0, color=ORANGE, ls="--", lw=1.1)
ax.text(0.12, 1.95, "VBM", color=ORANGE, fontsize=9)
ax.set_xlim(-13, 6)
ax.set_ylim(bottom=0)
ax.set_xlabel("E − E$_{VBM}$  (eV)")
ax.set_ylabel("DOS  (states/eV)")
ax.set_title("Si DOS + projected DOS  (QE 7.5, nscf 16³, tetrahedra)", fontsize=11, pad=8)
ax.legend(frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(IMG / "qe-e07-dos-pdos.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("wrote qe-e07-dos-pdos.png")


# ---------------- E8: band structure ----------------
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

bands = read_gnu(D / "e08" / "si.bands.dat.gnu")
tick_x = [float(l.split()[0]) for l in open(D / "e08" / "ticks_x.txt")]
tick_l = ["L", "Γ", "X", "W", "K", "Γ"]

# 4 valence bands (8 electrons): VBM = max of 4th band, CBM = min of 5th
per_x = {}
for b in bands:
    for x, e in b:
        per_x.setdefault(round(x, 4), []).append(e)
vbm_v, cbm_v, cbm_x = -1e9, 1e9, None
for x, es in per_x.items():
    es = sorted(es)
    if len(es) >= 5:
        vbm_v = max(vbm_v, es[3])
        if es[4] < cbm_v:
            cbm_v, cbm_x = es[4], x
gap = cbm_v - vbm_v
# direct gap at Gamma
gx = min(per_x.keys(), key=lambda x: abs(x - tick_x[1]))
esg = sorted(per_x[gx])
dgap = esg[4] - esg[3]

fig, ax = plt.subplots(figsize=(7.0, 4.6), dpi=160)
for b in bands:
    ax.plot(b[:, 0], b[:, 1] - vbm_v, color=BLUE, lw=1.3)
ax.axhline(0, color=SLATE, ls="--", lw=1, alpha=0.7)
ax.axhline(gap, color=ORANGE, ls=":", lw=1, alpha=0.8)
for x in tick_x:
    ax.axvline(x, color="#cbd5e0", lw=0.8)
ax.set_xticks(tick_x); ax.set_xticklabels(tick_l)
ax.set_xlim(tick_x[0], tick_x[-1]); ax.set_ylim(-13, 7)
ax.set_ylabel("E − E$_{VBM}$  (eV)")
ax.set_title("Si band structure  (QE 7.5, PBE)", fontsize=11, pad=8)
ax.grid(False)
frac = (cbm_x - tick_x[1]) / (tick_x[2] - tick_x[1])
ax.text(tick_x[1] + 0.06, gap + 0.25,
        f"indirect gap ≈ {gap:.2f} eV  (Γ → {frac:.2f}·ΓX)",
        fontsize=9, color=ORANGE)
fig.tight_layout()
fig.savefig(IMG / "qe-e08-bands.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote qe-e08-bands.png  (indirect gap {gap:.3f} eV, direct at Gamma {dgap:.3f} eV, VBM {vbm_v:.4f})")


# ---------------- E9: Fe spin DOS ----------------
hdr = open(D / "e09" / "fe.dos").readline()
ef = float(hdr.split("EFermi =")[1].split()[0])
fd = np.loadtxt(D / "e09" / "fe.dos", skiprows=1)
fe_e, up, dw = fd[:, 0] - ef, fd[:, 1], fd[:, 2]

fig, ax = plt.subplots(figsize=(7.0, 4.2), dpi=160)
ax.plot(fe_e, up, color=BLUE, lw=1.4, label="spin up")
ax.plot(fe_e, -dw, color=RED, lw=1.4, label="spin down")
ax.fill_between(fe_e, 0, up, where=(fe_e <= 0), color=BLUE, alpha=0.13)
ax.fill_between(fe_e, 0, -dw, where=(fe_e <= 0), color=RED, alpha=0.13)
ax.axvline(0, color=ORANGE, ls="--", lw=1.2)
ax.axhline(0, color=SLATE, lw=0.8)
ax.set_xlim(-9, 4)
ax.set_xlabel("E − E$_F$  (eV)")
ax.set_ylabel("DOS  (states/eV)   up / −down")
ax.set_title("bcc Fe spin-resolved DOS  (QE 7.5, PBE, m = 2.19 μB)", fontsize=11, pad=8)
ax.legend(frameon=False, fontsize=9, loc="upper left")
fig.tight_layout()
fig.savefig(IMG / "qe-e09-fe-dos.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("wrote qe-e09-fe-dos.png")


# ---------------- E10/E11: FeO GGA vs +U ----------------
def spin_dos(path):
    hdr = open(path).readline()
    ef = float(hdr.split("EFermi =")[1].split()[0])
    d = np.loadtxt(path, skiprows=1)
    return d[:, 0] - ef, d[:, 1], d[:, 2], ef

def gap_at_ef(e, tot, thr=1e-3):
    below = e[(e < 0) & (tot > thr)]
    above = e[(e > 0) & (tot > thr)]
    dos_ef = np.interp(0.0, e, tot)
    if dos_ef > thr or below.size == 0 or above.size == 0:
        return 0.0, dos_ef
    return above.min() - below.max(), dos_ef

eg, upg, dwg, efg = spin_dos(D / "e10" / "feo_gga.dos")
eu, upu, dwu, efu = spin_dos(D / "e11" / "feo_u.dos")
gap_g, dosef_g = gap_at_ef(eg, upg + dwg)
gap_u, dosef_u = gap_at_ef(eu, upu + dwu)

fig, (ag, au) = plt.subplots(1, 2, figsize=(11.4, 4.3), dpi=160, sharey=True)
for ax, (e, up, dw), ttl in (
        (ag, (eg, upg, dwg), "GGA (PBE): metallic"),
        (au, (eu, upu, dwu), "GGA+U (U = 4.6 eV): Hubbard splitting")):
    ax.plot(e, up, color=BLUE, lw=1.2, label="spin up")
    ax.plot(e, -dw, color=RED, lw=1.2, label="spin down")
    ax.axvline(0, color=ORANGE, ls="--", lw=1.2)
    ax.axhline(0, color=SLATE, lw=0.8)
    ax.set_xlim(-9, 5)
    ax.set_xlabel("E − E$_F$  (eV)")
    ax.set_title(ttl, fontsize=11, pad=8)
ag.set_ylabel("DOS  (states/eV)   up / −down")
ag.legend(frameon=False, fontsize=9, loc="upper left")
ag.annotate(f"DOS(E$_F$) ≈ {dosef_g:.1f} → metal", xy=(0, 2.0), xytext=(1.2, 9.5),
            fontsize=9, color=ORANGE,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1))
au.annotate("narrow minority-t2g band\npinned at E$_F$ (ideal cubic cell)",
            xy=(0.1, 2.5), xytext=(1.1, 9.0), fontsize=8.5, color=ORANGE,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1))
au.annotate("Hubbard gap", xy=(-1.2, 0.25), xytext=(-4.2, 6.0),
            fontsize=8.5, color=SLATE,
            arrowprops=dict(arrowstyle="->", color=SLATE, lw=0.9))
au.annotate("Hubbard gap", xy=(1.4, 0.25), xytext=(2.4, 6.0),
            fontsize=8.5, color=SLATE,
            arrowprops=dict(arrowstyle="->", color=SLATE, lw=0.9))
fig.suptitle("FeO (rocksalt, AFM-II) spin-resolved DOS  (QE 7.5)", fontsize=12, y=1.02)
fig.tight_layout()
fig.savefig(IMG / "qe-e10-e11-feo-dos.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote qe-e10-e11-feo-dos.png  (GGA DOS(EF)={dosef_g:.2f}, +U gap={gap_u:.2f} eV)")


# ---------------- E13: workfunction + MD (guarded) ----------------
wf_file = D / "e13" / "avg_pot.dat"
if wf_file.exists():
    z, v = np.loadtxt(wf_file, unpack=True)  # z (A), V (eV)
    ef13 = float((D / "e13" / "fermi.txt").read_text().split()[0])
    vvac = float((D / "e13" / "vacuum.txt").read_text().split()[0])
    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=160)
    ax.plot(z, v, color=BLUE, lw=1.5)
    ax.axhline(ef13, color=ORANGE, ls="--", lw=1.2, label=f"E$_F$ = {ef13:.2f} eV")
    ax.axhline(vvac, color=GREEN, ls=":", lw=1.2, label=f"V$_{{vac}}$ = {vvac:.2f} eV")
    ax.annotate(f"Φ = {vvac - ef13:.2f} eV",
                xy=(z[-1] * 0.75, (vvac + ef13) / 2), fontsize=10, color=SLATE)
    ax.set_xlabel("z  (Å)")
    ax.set_ylabel("planar-avg  V$_{bare}$+V$_H$  (eV)")
    ax.set_title("FeO(100) slab: planar-averaged potential  (QE 7.5)", fontsize=11, pad=8)
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    fig.tight_layout()
    fig.savefig(IMG / "qe-e13-workfunction.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote qe-e13-workfunction.png  (WF={vvac - ef13:.2f} eV)")

md_file = D / "e13" / "md_trace.dat"
if md_file.exists():
    t, temp, econs = np.loadtxt(md_file, unpack=True)  # step, K, Ry
    fig, axL = plt.subplots(figsize=(7.2, 4.0), dpi=160)
    axL.plot(t * 0.968 / 1000, temp, color=ORANGE, lw=1.2)
    axL.axhline(300, color=SLATE, ls="--", lw=1, alpha=0.7)
    axL.set_xlabel("time  (ps)")
    axL.set_ylabel("temperature  (K)", color=ORANGE)
    axL.tick_params(axis="y", labelcolor=ORANGE)
    axR = axL.twinx()
    axR.spines.top.set_visible(False)
    axR.plot(t * 0.968 / 1000, (econs - econs[0]) * RY, color=BLUE, lw=1.2)
    axR.set_ylabel("(E$_{kin}$+E$_{tot}$) − initial  (eV)", color=BLUE)
    axR.tick_params(axis="y", labelcolor=BLUE)
    axR.grid(False)
    axL.set_title("FeO(+U) BOMD from ideal lattice, SVR 300 K  (QE 7.5)", fontsize=11, pad=8)
    fig.tight_layout()
    fig.savefig(IMG / "qe-e13-md.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote qe-e13-md.png")

print("done.")
