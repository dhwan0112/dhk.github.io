"""GIFs for the note on evaluating a real integral with the residue theorem.

usage: python make_gifs.py   ->  images/blog/residue-theorem-real-integral-semicircle/*.gif
Needs matplotlib + Pillow + numpy and the 'IBM Plex Sans KR' font.
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "images" / "blog" / "residue-theorem-real-integral-semicircle"

FPS = 14
HOLD_END = 28
INK, GREY, LIGHT = "#222222", "#8a8a8a", "#c8c8c8"
ACCENT, ACCENT2 = "#c8553d", "#2f6690"

plt.rcParams.update({
    "font.family": ["IBM Plex Sans KR", "DejaVu Sans"],
    "mathtext.fontset": "dejavusans",
    "axes.unicode_minus": False,
    "font.size": 12,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return 0.5 - 0.5 * np.cos(np.pi * t)


def timeline(*segments):
    frames = []
    for name, n in segments:
        for i in range(n):
            frames.append((name, i / (n - 1) if n > 1 else 1.0))
    return frames


def plain(ax):
    ax.grid(True, color="#eeeeee", lw=0.8, zorder=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors="#555555", length=0, labelsize=10)


def save(anim, fig, name, nframes):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    anim.save(path, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    print(f"{name}: {nframes} frames, {path.stat().st_size / 1024:.0f} KB")


# (a) the semicircle grows: segment -> pi, arc -> 0, ML bound above the arc
def gif_contour():
    R0, R1 = 1.25, 10.0
    Rs = np.linspace(R0, R1, 400)
    seg = 2 * np.arctan(Rs)
    arc = 2 * np.arctan(1 / Rs)
    ml = np.pi * Rs / (Rs**2 - 1)

    fig, (axc, axv) = plt.subplots(1, 2, figsize=(7.6, 4.4), dpi=100,
                                   gridspec_kw=dict(width_ratios=[1, 1.15]))
    fig.subplots_adjust(left=0.04, right=0.98, bottom=0.12, top=0.80, wspace=0.18)
    axc.set_aspect("equal")
    axc.set_xticks([]); axc.set_yticks([])
    for s in axc.spines.values():
        s.set_visible(False)
    plain(axv)
    axv.set_xlim(R0 - 0.1, R1 + 0.2)
    axv.set_ylim(0, 3.6)
    axv.set_xlabel("R", color="#555555")
    axv.axhline(np.pi, color=GREY, lw=1.0, ls="--")
    axv.text(R1 + 0.1, np.pi + 0.08, "π", color=GREY, ha="right", fontsize=11)

    hx = axc.axhline(0, color=GREY, lw=0.9)
    vx = axc.axvline(0, color=GREY, lw=0.9)
    seg_line, = axc.plot([], [], color=ACCENT2, lw=2.4)
    arc_line, = axc.plot([], [], color=ACCENT, lw=2.4)
    pole_in = axc.scatter([0], [1], s=60, marker="x", color=INK, lw=2, zorder=5)
    pole_out = axc.scatter([0], [-1], s=60, marker="x", color=LIGHT, lw=2, zorder=5)
    lab_i = axc.text(0, 0, "i", fontsize=11, color=INK)
    lab_mi = axc.text(0, 0, "−i", fontsize=11, color=GREY)
    lab_R = axc.text(0, 0, "", fontsize=11, color=ACCENT, ha="center")

    l_seg, = axv.plot([], [], color=ACCENT2, lw=2.0, label="선분 적분 2arctan R")
    l_arc, = axv.plot([], [], color=ACCENT, lw=2.0, label="호 적분 2arctan(1/R)")
    l_ml, = axv.plot([], [], color=ACCENT, lw=1.4, ls=":", label="ML 상한 πR/(R²−1)")
    axv.legend(loc="center right", fontsize=9.5, frameon=False)
    dots = axv.scatter([R0] * 3, [0] * 3, s=24, color=[ACCENT2, ACCENT, ACCENT], zorder=5)

    fig.text(0.04, 0.93, r"$\oint_{C}\,\frac{dz}{z^2+1} = \pi$ 는 R 과 무관. 선분은 $\pi$ 로, 호는 0 으로 간다",
             fontsize=13, color=INK, va="center")
    sub = fig.text(0.04, 0.855, "", fontsize=11.5, color="#555555", va="center")

    frames = timeline(("grow", 100), ("end", HOLD_END))

    def update(fr):
        name, t = fr
        s = ease(t) if name == "grow" else 1.0
        R = R0 + (R1 - R0) * s
        n = max(2, int(np.searchsorted(Rs, R)))
        lim = 1.2 * R
        axc.set_xlim(-lim, lim)
        axc.set_ylim(-0.45 * lim, 1.1 * lim)
        th = np.linspace(0, np.pi, 200)
        seg_line.set_data([-R, R], [0, 0])
        arc_line.set_data(R * np.cos(th), R * np.sin(th))
        lab_i.set_position((0.04 * lim, 1 + 0.03 * lim))
        lab_mi.set_position((0.04 * lim, -1 - 0.12 * lim))
        lab_R.set_text(f"R = {R:.1f}")
        lab_R.set_position((0, 1.02 * R + 0.03 * lim))

        l_seg.set_data(Rs[:n], seg[:n])
        l_arc.set_data(Rs[:n], arc[:n])
        l_ml.set_data(Rs[:n], np.minimum(ml[:n], 3.6))
        a, b, c = 2 * np.arctan(R), 2 * np.arctan(1 / R), np.pi * R / (R * R - 1)
        dots.set_offsets(np.c_[[R, R, R], [a, b, min(c, 3.6)]])
        sub.set_text(f"선분 {a:.4f} + 호 {b:.4f} = {a + b:.4f},   ML 상한 {c:.4f}")
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "contour-growing.gif", len(frames))


def seg_cos(R, n=40001):
    x = np.linspace(-R, R, n)
    y = np.cos(x) / (x * x + 1)
    return np.trapezoid(y, x) if hasattr(np, "trapezoid") else np.trapz(y, x)


# (b) e^{iz}/(z^2+1): closing upward the arc dies, closing downward it tends to 2 pi sinh 1
def gif_jordan():
    R0, R1 = 1.5, 20.0
    Rs = np.linspace(R0, R1, 300)
    segs = np.array([seg_cos(R) for R in Rs])
    up = np.pi / np.e - segs          # upper closed contour = pi/e
    down = np.pi * np.e - segs        # lower closed contour = pi e (clockwise)

    fig, (axm, axv) = plt.subplots(1, 2, figsize=(7.6, 4.4), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.13, top=0.78, wspace=0.28)
    plain(axm); plain(axv)
    th = np.linspace(0, np.pi, 300)
    axm.set_yscale("log")
    axm.set_xlim(0, 180)
    axm.set_ylim(1e-9, 1e9)
    axm.set_xticks([0, 90, 180])
    axm.set_xlabel("호 위치 θ (도)", color="#555555")
    axm.set_title(r"호 위의 $|e^{iz}|$", fontsize=12, color=INK)
    m_up, = axm.plot([], [], color=ACCENT2, lw=2.0, label="위 반원  e^(−R sin θ)")
    m_dn, = axm.plot([], [], color=ACCENT, lw=2.0, label="아래 반원  e^(+R sin θ)")
    axm.axhline(1, color=GREY, lw=0.9)
    axm.legend(loc="upper left", fontsize=9, frameon=False)

    axv.set_xlim(R0, R1 + 0.3)
    axv.set_ylim(-1.0, 9.0)
    axv.set_xlabel("R", color="#555555")
    axv.set_title("호 적분 값", fontsize=12, color=INK)
    target = 2 * np.pi * np.sinh(1)
    axv.axhline(target, color=ACCENT, lw=0.9, ls="--")
    axv.axhline(0, color=ACCENT2, lw=0.9, ls="--")
    axv.text(R1 + 0.2, target + 0.25, "2π sinh 1 ≈ 7.384", color=ACCENT, fontsize=10, ha="right")
    v_up, = axv.plot([], [], color=ACCENT2, lw=2.0)
    v_dn, = axv.plot([], [], color=ACCENT, lw=2.0)

    fig.text(0.04, 0.93, r"$\int \frac{e^{ix}}{x^2+1}dx$: 위로 닫으면 호가 사라지고, 아래로 닫으면 남는다",
             fontsize=13, color=INK, va="center")
    sub = fig.text(0.04, 0.855, "", fontsize=11.5, color="#555555", va="center")

    frames = timeline(("grow", 96), ("end", HOLD_END))

    def update(fr):
        name, t = fr
        s = ease(t) if name == "grow" else 1.0
        R = R0 + (R1 - R0) * s
        n = max(2, int(np.searchsorted(Rs, R)))
        m_up.set_data(np.degrees(th), np.exp(-R * np.sin(th)))
        m_dn.set_data(np.degrees(th), np.exp(R * np.sin(th)))
        v_up.set_data(Rs[:n], up[:n])
        v_dn.set_data(Rs[:n], down[:n])
        k = n - 1
        sub.set_text(f"R = {Rs[k]:.1f}:  위쪽 호 {up[k]:+.4f},  아래쪽 호 {down[k]:.4f}"
                     .replace("-", "−"))
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "jordan-upper-vs-lower.gif", len(frames))


if __name__ == "__main__":
    gif_contour()
    gif_jordan()
