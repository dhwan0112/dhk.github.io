"""GIFs for the note on the epsilon-delta definition of a limit.

usage: python make_gifs.py   ->  images/blog/epsilon-delta-limit-definition/*.gif
Needs matplotlib + Pillow and the 'IBM Plex Sans KR' font.
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "images" / "blog" / "epsilon-delta-limit-definition"

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


def style_axes(ax, xlim, ylim, xticks, yticks):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
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


A, L = 3.0, 9.0
xs = np.linspace(0.8, 5.2, 600)


# (a) the epsilon band shrinks; delta = min(1, eps/7) answers each time
def gif_game():
    fig, ax = plt.subplots(figsize=(7.2, 5.0), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.08, top=0.82)
    style_axes(ax, (0.8, 5.2), (0, 26), range(1, 6), range(0, 27, 5))
    ax.plot(xs, xs**2, color=INK, lw=2.2, zorder=3)
    ax.scatter([A], [L], s=46, facecolor="white", edgecolor=INK, lw=1.6, zorder=6)

    eps_band = ax.add_patch(Rectangle((0.8, L - 1), 4.4, 2, color=ACCENT2, alpha=0.12, zorder=1, lw=0))
    del_band = ax.add_patch(Rectangle((A - 0.1, 0), 0.2, 26, color=ACCENT, alpha=0.12, zorder=1, lw=0))
    eps_lines = [ax.axhline(0, color=ACCENT2, lw=1.0, ls="--", zorder=2) for _ in range(2)]
    del_lines = [ax.axvline(0, color=ACCENT, lw=1.0, ls="--", zorder=2) for _ in range(2)]
    inside, = ax.plot([], [], color=ACCENT, lw=4.0, alpha=0.85, zorder=4)
    eps_txt = ax.text(4.95, 0, "", color=ACCENT2, fontsize=11, ha="right", va="bottom")
    del_txt = ax.text(0, 0.6, "", color=ACCENT, fontsize=11, ha="center")
    title = fig.text(0.08, 0.93, r"$\lim_{x\to 3} x^2 = 9$:  상대가 $\varepsilon$을 내면 $\delta=\min(1,\varepsilon/7)$로 답한다",
                     fontsize=13, color=INK, va="center")
    sub = fig.text(0.08, 0.865, "", fontsize=11.5, color="#555555", va="center")

    eps_path = [6.0, 3.0, 1.5, 0.6]
    segs = [("hold0", 14)]
    for i in range(1, len(eps_path)):
        segs += [(f"move{i}", 22), (f"hold{i}", 14)]
    segs += [("end", HOLD_END)]
    frames = timeline(*segs)

    def eps_at(name, t):
        if name.startswith("move"):
            i = int(name[4:])
            return eps_path[i - 1] + (eps_path[i] - eps_path[i - 1]) * ease(t)
        if name.startswith("hold"):
            return eps_path[int(name[4:])]
        return eps_path[-1]

    def update(fr):
        name, t = fr
        e = eps_at(name, t)
        d = min(1.0, e / 7)
        eps_band.set_y(L - e)
        eps_band.set_height(2 * e)
        del_band.set_x(A - d)
        del_band.set_width(2 * d)
        for ln, y in zip(eps_lines, (L - e, L + e)):
            ln.set_ydata([y, y])
        for ln, x in zip(del_lines, (A - d, A + d)):
            ln.set_xdata([x, x])
        xi = np.linspace(A - d, A + d, 200)
        inside.set_data(xi, xi**2)
        eps_txt.set_text(f"9 ± {e:.2f}")
        eps_txt.set_position((5.15, L + e + 0.3))
        del_txt.set_text(f"3 ± {d:.3f}")
        del_txt.set_position((A, 0.7))
        worst = max((A + d) ** 2 - L, L - (A - d) ** 2)
        sub.set_text(f"ε = {e:.2f},  δ = {d:.3f}:  구간 안 최대 오차 {worst:.2f} < ε")
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "epsilon-delta-game.gif", len(frames))


# (b) eps = 10: delta = eps/7 lets x = 4.4 escape, delta = min(1, eps/7) does not
def gif_counterexample():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.6), dpi=100, sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.09, top=0.80, wspace=0.08)
    e = 10.0
    deltas = [e / 7, min(1.0, e / 7)]
    labels = [r"$\delta=\varepsilon/7\approx1.43$", r"$\delta=\min(1,\varepsilon/7)=1$"]
    dots, vals = [], []
    for ax, d, lab in zip(axes, deltas, labels):
        style_axes(ax, (1.2, 4.9), (0, 25), range(2, 5), range(0, 26, 5))
        ax.axhspan(L - e, L + e, color=ACCENT2, alpha=0.12, zorder=1)
        ax.axhline(L + e, color=ACCENT2, lw=1.0, ls="--", zorder=2)
        ax.axvspan(A - d, A + d, color=ACCENT, alpha=0.12, zorder=1)
        ax.plot(xs, xs**2, color=INK, lw=2.2, zorder=3)
        ax.set_title(lab, fontsize=12.5, color=INK, pad=8)
        ax.text(1.3, L + e + 0.5, "9 + ε = 19", color=ACCENT2, fontsize=10.5)
        dots.append(ax.scatter([], [], s=50, zorder=6))
        vals.append(ax.text(0.03, 0.04, "", transform=ax.transAxes, fontsize=11, va="bottom"))
    title = fig.text(0.08, 0.93, r"상대가 $\varepsilon=10$을 낸다. $x$를 구간 오른쪽 끝으로 밀어 본다",
                     fontsize=13, color=INK, va="center")

    frames = timeline(("sweep", 46), ("end", HOLD_END))

    def update(fr):
        name, t = fr
        s = ease(t) if name == "sweep" else 1.0
        for i, (d, dot, v) in enumerate(zip(deltas, dots, vals)):
            x = A + s * (d * 0.98)
            if i == 0 and name == "end":
                x = 4.4
            y = x * x
            bad = y > L + e
            dot.set_offsets([[x, y]])
            dot.set_color(ACCENT if bad else ACCENT2)
            v.set_text(f"x = {x:.2f},  x² = {y:.2f}" + ("  > 19" if bad else "  < 19"))
            v.set_color(ACCENT if bad else ACCENT2)
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "min-counterexample.gif", len(frames))


if __name__ == "__main__":
    gif_game()
    gif_counterexample()
