import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DT_FRAME = 1.0e-3   # ns per frame: timestep 0.5 fs x dump every 2000 steps
NBLOCKS, RUNNING = 10, 50   # running mean in frames (50 ps)
FIRST_LAYER = 6.4

def cu_top(path="opls.data"):
    lines = open(path).read().split("\n")
    i = next(k for k, l in enumerate(lines) if l.strip().startswith("Atoms")) + 2
    z = []
    for l in lines[i:]:
        s = l.split()
        if not s: break
        if s[2] == "12": z.append(float(s[6]))
    return max(z)

zcu = cu_top()
C = {"benzene": "#2b6cb0", "ethanol": "#c0782f", "pppm": "#2b6cb0", "msm": "#c0782f"}
fig, (a, b) = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"width_ratios": [1.15, 1]})

for combo, ls, lab in [("pppm", "-", "PPPM + slab"), ("msm", "--", "MSM")]:
    d = pd.read_csv(f"zprofile_{combo}.csv")
    for s in ("benzene", "ethanol"):
        a.plot(d.z - zcu, d[f"rho_{s}"], ls, color=C[s], lw=2, label=f"{s}, {lab}")
a.axvspan(-2, 0, color="#e2e8f0"); a.text(-1.6, 0.95, "Cu", color="#4a5568")
a.axvline(FIRST_LAYER, color="#718096", ls=":", lw=1)
a.text(FIRST_LAYER + 0.4, 0.86, "first-layer cutoff\n(6.4 Å, first minimum)", color="#4a5568", fontsize=9)
a.set(xlim=(-2, 33), ylim=(0, 1), xlabel="z − z(Cu top)  (Å)", ylabel="mass density  (g / cm³)",
      title="OPLS-AA benzene/ethanol on Cu, 2 ns production, 0.25 Å bins")
a.legend(frameon=False, fontsize=9)

for combo, lab in [("pppm", "PPPM + slab"), ("msm", "MSM")]:
    x = pd.read_csv(f"first_layer_{combo}.csv").x_bz_first.values
    n = len(x) // NBLOCKS * NBLOCKS
    t = np.arange(len(x)) * DT_FRAME
    run = pd.Series(x).rolling(RUNNING, center=True, min_periods=1).mean()
    blocks = np.nanmean(x[:n].reshape(NBLOCKS, -1), axis=1)
    tb = (np.arange(NBLOCKS) + 0.5) * n / NBLOCKS * DT_FRAME
    se = blocks.std(ddof=1) / np.sqrt(NBLOCKS)
    b.plot(t, run, color=C[combo], alpha=0.35, lw=1)
    b.axhline(np.nanmean(x), color=C[combo], ls=":", lw=1)
    b.plot(tb, blocks, "o", color=C[combo], ms=8, label=f"{lab}: {np.nanmean(x):.2f} ± {se:.2f}")
b.set(xlim=(0, len(x) * DT_FRAME), ylim=(0.3, 1), xlabel="production time  (ns)",
      ylabel="benzene mole fraction, first layer",
      title=f"Dots = {n // NBLOCKS * DT_FRAME * 1000:.0f} ps block means; faint = {RUNNING * DT_FRAME * 1000:.0f} ps running mean")
b.legend(title="mean ± SE (10 blocks)", fontsize=9, loc="lower left", facecolor="white", edgecolor="none", framealpha=0.9)

for ax in (a, b):
    ax.grid(alpha=0.3); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("../../../images/blog/pppm-vs-msm.png", dpi=110)
