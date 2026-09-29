"""Stage 1: split the lowest CREST conformers into ORCA r2SCAN-3c inputs (rerank/confNN/).
Stage 2 (--collect): gather DFT energies, write fig/rerank.png and summary_rerank.json.
"""
import json
import os
import re
import sys

import numpy as np

HARTREE_KCAL = 627.509474
BB = json.load(open("backbone.json"))
REGIONS = {"C7eq": (-83, 73), "C5": (-155, 160), "αR": (-70, -40),
           "αL": (60, 45), "C7ax": (75, -65)}


def read_xyz(path):
    frames, lines, i = [], open(path).read().splitlines(), 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        n = int(lines[i].split()[0])
        block = [l.split() for l in lines[i + 2:i + 2 + n]]
        if len(block) < n:
            break
        frames.append(([b[0].capitalize() for b in block],
                       np.array([[float(v) for v in b[1:4]] for b in block]), lines[i + 1]))
        i += 2 + n
    return frames


def first_float(s):
    m = re.search(r"-?\d+\.\d+", s)
    return float(m.group()) if m else None


def dihedral(x, idx):
    p0, p1, p2, p3 = x[idx]
    b0, b1, b2 = p0 - p1, p2 - p1, p3 - p2
    b1 = b1 / np.linalg.norm(b1)
    v = b0 - np.dot(b0, b1) * b1
    w = b2 - np.dot(b2, b1) * b1
    return float(np.degrees(np.arctan2(np.dot(np.cross(b1, v), w), np.dot(v, w))))


def phipsi(x):
    return dihedral(x, BB["phi"]), dihedral(x, BB["psi"])


def setup_rama(ax, title):
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_xticks(range(-180, 181, 90))
    ax.set_yticks(range(-180, 181, 90))
    ax.set_xlabel("φ (°)")
    ax.set_ylabel("ψ (°)")
    ax.grid(alpha=0.3)
    ax.set_aspect("equal")
    for name, (p, q) in REGIONS.items():
        ax.text(p, q + 16, name, ha="center", va="bottom", fontsize=8, color="#888", zorder=0)
    ax.set_title(title, fontsize=10)


NCONF = 8
INP = """! r2SCAN-3c Opt CPCM(water)
%pal nprocs 8 end
%maxcore 1500
* xyzfile 0 1 {name}_xtb.xyz
"""


def split():
    fr = read_xyz("x06-crest/crest_conformers.xyz")[:NCONF]
    os.makedirs("rerank", exist_ok=True)
    for k, (syms, xyz, comment) in enumerate(fr, 1):
        name = f"conf{k:02d}"
        d = f"rerank/{name}"
        os.makedirs(d, exist_ok=True)
        with open(f"{d}/{name}_xtb.xyz", "w") as f:
            f.write(f"{len(syms)}\n{comment.strip()}\n")
            for s, (x, y, z) in zip(syms, xyz):
                f.write(f"{s:2s} {x:12.6f} {y:12.6f} {z:12.6f}\n")
        open(f"{d}/{name}.inp", "w").write(INP.format(name=name))
    print("wrote", len(fr), "inputs under rerank/")


def final_energy(out):
    e = None
    for line in open(out, errors="replace"):
        if "FINAL SINGLE POINT ENERGY" in line:
            e = float(line.split()[-1])
    return e


def collect():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fr = read_xyz("x06-crest/crest_conformers.xyz")[:NCONF]
    e_xtb = np.array([first_float(c) for _, _, c in fr])
    rows = []
    for k in range(1, len(fr) + 1):
        name = f"conf{k:02d}"
        out = f"rerank/{name}/{name}.out"
        opt = f"rerank/{name}/{name}.xyz"
        e = final_energy(out) if os.path.exists(out) else None
        ang_dft = None
        if e is not None and os.path.exists(opt):
            ang_dft = phipsi(read_xyz(opt)[-1][1])
        rows.append({"crest_rank": k, "E_xtb": e_xtb[k - 1], "E_dft": e,
                     "phipsi_xtb": [round(v) for v in phipsi(fr[k - 1][1])],
                     "phipsi_dft": [round(v) for v in ang_dft] if ang_dft else None})
    ok = [r for r in rows if r["E_dft"] is not None]
    e0x = min(r["E_xtb"] for r in ok)
    e0d = min(r["E_dft"] for r in ok)
    for r in ok:
        r["dE_xtb"] = round((r["E_xtb"] - e0x) * HARTREE_KCAL, 2)
        r["dE_dft"] = round((r["E_dft"] - e0d) * HARTREE_KCAL, 2)
    for rank, r in enumerate(sorted(ok, key=lambda r: r["E_dft"]), 1):
        r["dft_rank"] = rank
    json.dump(rows, open("summary_rerank.json", "w"), indent=1)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.5, 4), dpi=110)
    x = [r["dE_xtb"] for r in ok]
    y = [r["dE_dft"] for r in ok]
    a1.scatter(x, y, s=40, color="#1c7ed6", ec="k", zorder=3)
    for r in ok:
        a1.annotate(str(r["crest_rank"]), (r["dE_xtb"], r["dE_dft"]),
                    xytext=(4, 4), textcoords="offset points", fontsize=8)
    lim = max(max(x), max(y)) + 0.5
    a1.plot([0, lim], [0, lim], "k--", lw=0.6)
    a1.set_xlim(-0.3, lim)
    a1.set_ylim(-0.3, lim)
    a1.set_xlabel("ΔE GFN2-xTB (kcal/mol)")
    a1.set_ylabel("ΔE r2SCAN-3c (kcal/mol)")
    setup_rama(a2, "xTB → r2SCAN-3c geometry")
    for r in ok:
        if r["phipsi_dft"]:
            (p0, q0), (p1, q1) = r["phipsi_xtb"], r["phipsi_dft"]
            a2.annotate("", (p1, q1), (p0, q0), arrowprops=dict(arrowstyle="->", lw=0.8))
            a2.plot(p0, q0, "o", ms=5, color="#adb5bd")
            a2.plot(p1, q1, "o", ms=6, color="#e8590c", mec="k")
    fig.tight_layout()
    os.makedirs("fig", exist_ok=True)
    fig.savefig("fig/rerank.png")
    print(json.dumps(rows, indent=1))


if __name__ == "__main__":
    collect() if "--collect" in sys.argv else split()
