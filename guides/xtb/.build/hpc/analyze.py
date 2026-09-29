"""Turn the xtb/CREST/ORCA runs into figures, GIFs and summary.json.

Run from the bundle directory after run_xtb.pbs and run_orca.pbs:
    python analyze.py
Every figure is wrapped separately, so a failed run only drops its own figures.
"""
import glob
import json
import os
import re
import traceback

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle

OUT = "fig"
os.makedirs(OUT, exist_ok=True)
BB = json.load(open("backbone.json"))
HARTREE_KCAL = 627.509474

RADIUS = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66}
DRAW_R = {"H": 0.22, "C": 0.38, "N": 0.36, "O": 0.35}
COLOR = {"H": "#f2f2f2", "C": "#4a4a4a", "N": "#3b5bdb", "O": "#e03131"}
BG = "#fafaf8"
REGIONS = {"C7eq": (-83, 73), "C5": (-155, 160), "αR": (-70, -40),
           "αL": (60, 45), "C7ax": (75, -65)}

summary = {}


# ---------------------------------------------------------------- parsing
def read_xyz(path):
    frames, lines = [], open(path).read().splitlines()
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        n = int(lines[i].split()[0])
        comment = lines[i + 1]
        block = [l.split() for l in lines[i + 2:i + 2 + n]]
        if len(block) < n:
            break
        syms = [b[0].capitalize() for b in block]
        xyz = np.array([[float(v) for v in b[1:4]] for b in block])
        frames.append((syms, xyz, comment))
        i += 2 + n
    return frames


def first_float(s):
    m = re.search(r"-?\d+\.\d+", s)
    return float(m.group()) if m else None


def grep_last(path, pattern, group=1):
    val = None
    if not os.path.exists(path):
        return None
    for line in open(path, errors="replace"):
        m = re.search(pattern, line)
        if m:
            val = m.group(group)
    return val


def timings():
    t = {}
    if os.path.exists("timings.txt"):
        for line in open("timings.txt"):
            m = re.match(r"(\S+) exit=(\d+) wall_s=([\d.]+)", line)
            if m:
                t[m.group(1)] = {"exit": int(m.group(2)), "wall_s": float(m.group(3))}
    return t


def xtb_md_log(path):
    """(time_ps, T_K, Etot_Eh) rows from the xtb MD progress table."""
    rows, on = [], False
    for line in open(path, errors="replace"):
        if "time (ps)" in line:
            on = True
            continue
        if on:
            tok = line.split()
            try:
                vals = [float(x) for x in tok[:7]]
            except ValueError:
                continue
            if len(vals) == 7:
                rows.append((vals[1], vals[5], vals[6]))
    return np.array(rows)


def find_traj(d):
    cands = [p for p in glob.glob(f"{d}/*.xyz") + glob.glob(f"{d}/*.trj")]
    cands = [p for p in cands if not p.endswith((".inp", "_trj_start.xyz"))]
    best, nbest = None, 1
    for p in cands:
        try:
            n = len(read_xyz(p))
        except Exception:
            continue
        if n > nbest:
            best, nbest = p, n
    return best


# ---------------------------------------------------------------- geometry
def dihedral(x, idx):
    p0, p1, p2, p3 = x[idx]
    b0, b1, b2 = p0 - p1, p2 - p1, p3 - p2
    b1 /= np.linalg.norm(b1)
    v = b0 - np.dot(b0, b1) * b1
    w = b2 - np.dot(b2, b1) * b1
    return np.degrees(np.arctan2(np.dot(np.cross(b1, v), w), np.dot(v, w)))


def phipsi(xyz):
    return dihedral(xyz, BB["phi"]), dihedral(xyz, BB["psi"])


def kabsch_onto(ref, x, mask):
    rc, xc = ref[mask].mean(0), x[mask].mean(0)
    h = (x[mask] - xc).T @ (ref[mask] - rc)
    u, _, vt = np.linalg.svd(h)
    d = np.sign(np.linalg.det(vt.T @ u.T))
    r = vt.T @ np.diag([1, 1, d]) @ u.T
    return (x - xc) @ r.T + rc


def bonds_of(syms, x):
    out = []
    for i in range(len(syms)):
        for j in range(i + 1, len(syms)):
            if np.linalg.norm(x[i] - x[j]) < 1.15 * (RADIUS[syms[i]] + RADIUS[syms[j]]):
                out.append((i, j))
    return out


def prepare(frames):
    """Align every frame on the heavy atoms and rotate into the principal-axis view."""
    syms, ref = frames[0][0], frames[0][1].copy()
    heavy = np.array([s != "H" for s in syms])
    c = ref[heavy].mean(0)
    _, _, vt = np.linalg.svd(ref[heavy] - c)
    rot = vt.T
    if np.linalg.det(rot) < 0:  # an improper axis set would draw the mirror image
        rot[:, 2] *= -1
    ref = (ref - c) @ rot
    out = [ref]
    for _, x, _ in frames[1:]:
        out.append(kabsch_onto(ref, x, heavy))
    return syms, np.array(out), bonds_of(syms, frames[0][1])


# ---------------------------------------------------------------- drawing
def draw_molecule(ax, syms, x, bonds, lim):
    ax.clear()
    ax.set_facecolor(BG)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axis("off")
    z = x[:, 2]
    zn = (z - z.min()) / (np.ptp(z) + 1e-9)
    for i, j in bonds:
        mid = (x[i] + x[j]) / 2
        for a, m in ((i, mid), (j, mid)):
            ax.plot([x[a, 0], m[0]], [x[a, 1], m[1]], color=COLOR[syms[a]],
                    lw=5, solid_capstyle="round", zorder=2 + 10 * (x[a, 2] + m[2]) / 2 - 0.5)
            ax.plot([x[a, 0], m[0]], [x[a, 1], m[1]], color="#222", lw=6.5,
                    solid_capstyle="round", zorder=2 + 10 * (x[a, 2] + m[2]) / 2 - 0.6)
    for k, s in enumerate(syms):
        zo = 2 + 10 * z[k]
        r = DRAW_R[s] * (0.9 + 0.2 * zn[k])
        ax.add_patch(Circle(x[k, :2], r, fc=COLOR[s], ec="#222", lw=1.0, zorder=zo))
        ax.add_patch(Circle(x[k, :2] + np.array([-0.3, 0.3]) * r, 0.35 * r,
                            fc="white", ec="none", alpha=0.35, zorder=zo + 0.01))


def setup_rama(ax, title=None):
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_xticks(range(-180, 181, 90))
    ax.set_yticks(range(-180, 181, 90))
    ax.set_xlabel("φ (°)")
    ax.set_ylabel("ψ (°)")
    ax.grid(alpha=0.3)
    ax.set_aspect("equal")
    for name, (p, q) in REGIONS.items():
        ax.text(p, q + 16, name, ha="center", va="bottom", fontsize=8, color="#555", zorder=5,
                bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
    if title:
        ax.set_title(title, fontsize=10)


def md_gif(frames, times_ps, path, title, stride=1, trail=40, fps=20):
    syms, xs, bonds = prepare(frames)
    xs, times_ps = xs[::stride], np.asarray(times_ps)[::stride]
    ang = np.array([phipsi(x) for x in xs])
    lim = np.abs(xs[..., :2]).max() + 0.8
    fig, (am, ar) = plt.subplots(1, 2, figsize=(8, 4), dpi=80,
                                 gridspec_kw={"width_ratios": [1, 1]})
    fig.patch.set_facecolor(BG)

    def update(k):
        draw_molecule(am, syms, xs[k], bonds, lim)
        am.text(0.02, 0.02, f"t = {times_ps[k]:6.2f} ps", transform=am.transAxes,
                family="monospace", fontsize=10)
        ar.clear()
        ar.set_facecolor("white")
        setup_rama(ar, title)
        lo = max(0, k - trail)
        ar.plot(ang[:k + 1, 0], ang[:k + 1, 1], ".", ms=2, color="#bbb")
        seg = ang[lo:k + 1]
        ar.scatter(seg[:, 0], seg[:, 1], s=8, c=np.linspace(0.2, 1, len(seg)),
                   cmap="Blues", vmin=0, vmax=1)
        ar.plot(*ang[k], "o", ms=7, color="#e8590c", mec="k")

    update(0)
    fig.tight_layout()
    anim = FuncAnimation(fig, update, frames=len(xs))
    anim.save(path, writer=PillowWriter(fps=fps))
    plt.close(fig)


def conformer_gif(frames, rel, path, n=8, hold=12):
    frames = frames[:n]
    syms, xs, bonds = prepare(frames)
    lim = np.abs(xs[..., :2]).max() + 0.8
    fig, am = plt.subplots(figsize=(4.5, 4.5), dpi=80)
    fig.patch.set_facecolor(BG)
    order = [k for k in range(len(xs)) for _ in range(hold)]

    def update(f):
        k = order[f]
        draw_molecule(am, syms, xs[k], bonds, lim)
        p, q = phipsi(xs[k])
        am.set_title(f"#{k + 1}   ΔE = {rel[k]:.2f} kcal/mol   φ/ψ = {p:.0f}/{q:.0f}°",
                     fontsize=10)

    anim = FuncAnimation(fig, update, frames=len(order))
    anim.save(path, writer=PillowWriter(fps=6))
    plt.close(fig)


RUN = __name__ == "__main__"


def step(name):
    def deco(fn):
        if not RUN:
            return
        try:
            fn()
            print("ok  ", name)
        except Exception:
            print("FAIL", name)
            traceback.print_exc()
    return deco


# ---------------------------------------------------------------- figures
if RUN:
    summary["timings"] = timings()


@step("xtb single molecule results")
def _():
    r = {}
    for key, path in [("gas_opt", "x01-opt/opt.out"), ("alpb_opt", "x03-alpb/alpb.out"),
                      ("ohess", "x02-ohess/ohess.out")]:
        r[key] = {
            "total_energy_Eh": grep_last(path, r"TOTAL ENERGY\s+(-?\d+\.\d+)"),
            "gap_eV": grep_last(path, r"HOMO-LUMO GAP\s+(-?\d+\.\d+)"),
            "free_energy_Eh": grep_last(path, r"TOTAL FREE ENERGY\s+(-?\d+\.\d+)"),
        }
    for key, path in [("gas_opt", "x01-opt/xtbopt.xyz"), ("alpb_opt", "x03-alpb/xtbopt.xyz")]:
        if os.path.exists(path):
            r[key]["phi_psi"] = [round(v, 1) for v in phipsi(read_xyz(path)[0][1])]
    freqs = []
    if os.path.exists("x02-ohess/vibspectrum"):
        for line in open("x02-ohess/vibspectrum"):
            tok = line.split()
            if len(tok) >= 4 and tok[0].isdigit():
                try:
                    freqs.append(float(tok[-3]))
                except ValueError:
                    pass
    r["lowest_freqs_cm1"] = sorted(f for f in freqs if abs(f) > 1e-3)[:6]
    summary["xtb"] = r


@step("xtb MD energy/temperature plot")
def _():
    log = xtb_md_log("x04-md/md.out")
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.5, 4.2), sharex=True, dpi=110)
    a1.plot(log[:, 0], log[:, 1], lw=0.8, color="#e8590c")
    a1.axhline(300, color="k", lw=0.6, ls="--")
    a1.set_ylabel("T (K)")
    a2.plot(log[:, 0], (log[:, 2] - log[0, 2]) * HARTREE_KCAL, lw=0.8, color="#1c7ed6")
    a2.set_ylabel("E$_{tot}$ − E$_{tot}$(0)\n(kcal/mol)")
    a2.set_xlabel("time (ps)")
    fig.tight_layout()
    fig.savefig(f"{OUT}/xtb-md-thermo.png")
    plt.close(fig)
    summary["xtb_md"] = {"T_mean": float(log[len(log) // 5:, 1].mean()),
                         "T_std": float(log[len(log) // 5:, 1].std()),
                         "n_rows": len(log)}


@step("xtb MD GIFs")
def _():
    fr = read_xyz("x04-md/xtb.trj")
    dump_ps = 0.020
    t = np.arange(len(fr)) * dump_ps
    md_gif(fr[:100], t[:100], f"{OUT}/xtb-md-vibration.gif", "GFN2-xTB MD, first 2 ps")
    md_gif(fr, t, f"{OUT}/xtb-md-100ps.gif", "GFN2-xTB MD, 100 ps",
           stride=max(1, len(fr) // 200), trail=25)
    summary.setdefault("xtb_md", {})["n_frames"] = len(fr)


@step("MD vs metadynamics Ramachandran")
def _():
    fig, axes = plt.subplots(1, 2, figsize=(8, 4), dpi=110)
    res = {}
    for ax, (label, path) in zip(axes, [("MD, 100 ps", "x04-md/xtb.trj"),
                                        ("Metadynamics, 100 ps", "x05-metad/xtb.trj")]):
        ang = np.array([phipsi(x) for _, x, _ in read_xyz(path)])
        setup_rama(ax, label)
        ax.scatter(ang[:, 0], ang[:, 1], s=3, c=np.arange(len(ang)), cmap="viridis")
        hist, _, _ = np.histogram2d(ang[:, 0], ang[:, 1], bins=12, range=[[-180, 180]] * 2)
        res[label] = {"frames": len(ang), "occupied_bins_of_144": int((hist > 0).sum())}
    fig.tight_layout()
    fig.savefig(f"{OUT}/xtb-md-vs-metad-rama.png")
    plt.close(fig)
    summary["rama_coverage"] = res


@step("CREST conformers")
def _():
    fr = read_xyz("x06-crest/crest_conformers.xyz")
    e = np.array([first_float(c) for _, _, c in fr])
    rel = (e - e.min()) * HARTREE_KCAL
    ang = np.array([phipsi(x) for _, x, _ in fr])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.5, 4), dpi=110)
    a1.bar(np.arange(1, len(rel) + 1), rel, color="#1c7ed6")
    a1.axhline(3.0, color="k", lw=0.6, ls="--")
    a1.set_xticks(np.arange(1, len(rel) + 1))
    a1.set_xlim(0.4, len(rel) + 0.6)
    a1.text(1, 0.03, "ref", ha="center", va="bottom", fontsize=7, color="#555")
    a1.set_xlabel("conformer")
    a1.set_ylabel("ΔE (kcal/mol)")
    setup_rama(a2, "CREST conformers")
    sc = a2.scatter(ang[:, 0], ang[:, 1], c=rel, cmap="viridis_r", s=40, ec="k")
    fig.colorbar(sc, ax=a2, label="ΔE (kcal/mol)")
    fig.tight_layout()
    fig.savefig(f"{OUT}/crest-conformers.png")
    plt.close(fig)
    conformer_gif(fr, rel, f"{OUT}/crest-conformers.gif")
    summary["crest"] = {"n_conformers": len(fr),
                        "rel_kcal": [round(float(v), 2) for v in rel[:10]],
                        "phi_psi": [[round(float(p)), round(float(q))] for p, q in ang[:10]],
                        "runtime_line": grep_last("x06-crest/crest.out",
                                                  r"(CREST runtime.*)")}


@step("ORCA results")
def _():
    r = {}
    for name in ["o01-xtb-opt-freq", "o02-r2scan-opt-freq", "o03-xtb-md", "o04-r2scan-md"]:
        out = f"{name}/{name}.out"
        r[name] = {
            "normal": grep_last(out, r"(ORCA TERMINATED NORMALLY)") is not None,
            "final_energy_Eh": grep_last(out, r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)"),
            "gibbs_Eh": grep_last(out, r"Final Gibbs free energy\s+\.+\s+(-?\d+\.\d+)"),
            "run_time": grep_last(out, r"TOTAL RUN TIME:\s*(.*)"),
        }
        xyz = f"{name}/{name}.xyz"
        if os.path.exists(xyz) and "opt" in name:
            r[name]["phi_psi"] = [round(v, 1) for v in phipsi(read_xyz(xyz)[-1][1])]
    summary["orca"] = r


@step("ORCA MD GIF and dihedral trace")
def _():
    tr = find_traj("o03-xtb-md")
    fr = read_xyz(tr)
    dt_ps = 0.5e-3 * 20
    t = np.arange(len(fr)) * dt_ps
    md_gif(fr, t, f"{OUT}/orca-xtb-md.gif", "ORCA, XTB2 MD, 10 ps",
           stride=max(1, len(fr) // 200), trail=25)
    ang = np.array([phipsi(x) for _, x, _ in fr])
    fig, ax = plt.subplots(figsize=(6.5, 3), dpi=110)
    ax.plot(t, ang[:, 0], lw=0.8, label="φ")
    ax.plot(t, ang[:, 1], lw=0.8, label="ψ")
    ax.set_xlabel("time (ps)")
    ax.set_ylabel("angle (°)")
    ax.set_ylim(-180, 180)
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(f"{OUT}/orca-xtb-md-dihedrals.png")
    plt.close(fig)
    summary["orca_md"] = {"trajectory": tr, "n_frames": len(fr)}


@step("ORCA cost per MD step")
def _():
    t = summary["timings"]
    per = {}
    for name, steps in [("o03-xtb-md", 20000), ("o04-r2scan-md", 200)]:
        if name in t:
            per[name] = t[name]["wall_s"] / steps
    summary["orca_md"] = {**summary.get("orca_md", {}), "sec_per_step": per}


if RUN:
    json.dump(summary, open("summary.json", "w"), indent=1, ensure_ascii=False, default=str)
    print(json.dumps(summary, indent=1, ensure_ascii=False, default=str))
