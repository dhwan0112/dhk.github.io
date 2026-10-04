"""GIFs for the note on why L'Hopital's rule works.

usage: python make_gifs.py   ->  images/blog/why-lhopital-rule-works/*.gif
Needs matplotlib + Pillow and the 'IBM Plex Sans KR' font.
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "images" / "blog" / "why-lhopital-rule-works"

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


def style_axes(ax, xlim, ylim, xticks, yticks, equal=False):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal")
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.grid(True, color="#eeeeee", lw=0.8, zorder=0)
    ax.axhline(0, color=GREY, lw=0.9, zorder=1)
    ax.axvline(0, color=GREY, lw=0.9, zorder=1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors="#555555", length=0, labelsize=10)


def save(anim, fig, name, nframes):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    anim.save(path, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    print(f"{name}: {nframes} frames, {path.stat().st_size / 1024:.0f} KB")


# (a) curve (g, f) = (x^2, x^3): secant from the origin, tangent at the point,
#     and the parallel tangent at c = 2x/3 (Cauchy mean value theorem)
def gif_secant_tangent():
    fig, ax = plt.subplots(figsize=(7.2, 5.4), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.07, top=0.83)
    style_axes(ax, (-0.08, 1.45), (-0.08, 1.45), [0, 0.5, 1.0], [0, 0.5, 1.0], equal=True)
    tt = np.linspace(0, 1.2, 300)
    ax.plot(tt**2, tt**3, color=INK, lw=2.2, zorder=3)
    ax.text(0.02, 1.32, r"곡선 $(g(x), f(x)) = (x^2, x^3)$", color=INK, fontsize=11.5, ha="left")
    ax.scatter([0], [0], s=30, color=INK, zorder=5)

    secant, = ax.plot([], [], color=ACCENT2, lw=1.8, zorder=4)
    tangent, = ax.plot([], [], color=ACCENT, lw=1.5, ls="--", zorder=4)
    parallel, = ax.plot([], [], color=ACCENT2, lw=1.5, ls=":", zorder=4)
    P = ax.scatter([], [], s=46, color=INK, zorder=6)
    Q = ax.scatter([], [], s=40, facecolor="white", edgecolor=ACCENT2, lw=1.6, zorder=6)
    title = fig.text(0.08, 0.94, "할선 기울기 f/g 와 접선 기울기 f′/g′", fontsize=13.5, color=INK, va="center")
    l1 = fig.text(0.08, 0.885, "", fontsize=11.5, color=ACCENT2, va="center")
    l2 = fig.text(0.52, 0.885, "", fontsize=11.5, color=ACCENT, va="center")

    frames = timeline(("show", 16), ("move", 70), ("end", HOLD_END))

    def line_through(x0, y0, m, half):
        xs = np.array([x0 - half, x0 + half])
        return xs, y0 + m * (xs - x0)

    def update(fr):
        name, t = fr
        x = 1.1 if name == "show" else (1.1 - 0.85 * ease(t) if name == "move" else 0.25)
        gx, fx = x * x, x ** 3
        secant.set_data([0, gx * 1.15], [0, fx * 1.15])
        tangent.set_data(*line_through(gx, fx, 1.5 * x, 0.35))
        c = 2 * x / 3
        parallel.set_data(*line_through(c * c, c ** 3, x, 0.3))
        P.set_offsets([[gx, fx]])
        Q.set_offsets([[c * c, c ** 3]])
        l1.set_text(f"할선(실선) f/g = x = {x:.2f}")
        l2.set_text(f"접선(파선) f′/g′ = 3x/2 = {1.5 * x:.2f}")
        if name == "end":
            title.set_text("x → 0 이면 두 기울기 모두 0 으로 간다")
        else:
            title.set_text("점선: 할선과 평행한 접선, 접점 c = 2x/3")
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "secant-tangent.gif", len(frames))


# (b) g' = 0 infinitely often: f'/g' -> 0 but f/g = e^{-sin x} keeps oscillating
def gif_gprime_zero():
    X = np.linspace(4.0, 40, 2400)
    f = X + np.sin(X) * np.cos(X)
    g = np.exp(np.sin(X)) * f
    ratio = f / g
    dratio = 2 * np.cos(X) / (np.exp(np.sin(X)) * (X + np.sin(X) * np.cos(X) + 2 * np.cos(X)))

    fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.11, top=0.80)
    style_axes(ax, (3.5, 40.5), (-0.6, 3.0), range(10, 41, 10), [0, 1 / np.e, 1, 2, np.e])
    ax.set_yticklabels(["0", "1/e", "1", "2", "e"])
    for k in range(1, 13):
        xz = np.pi / 2 + k * np.pi
        ax.axvline(xz, color=LIGHT, lw=0.8, zorder=1)
    ax.text(40.3, -0.5, "세로선: g′(x) = 0 인 x = π/2 + kπ", color=GREY, fontsize=10, ha="right")
    l_ratio, = ax.plot([], [], color=ACCENT, lw=2.0, zorder=3)
    l_dratio, = ax.plot([], [], color=ACCENT2, lw=2.0, zorder=3)
    lab1 = ax.text(0, 0, "", color=ACCENT, fontsize=11.5)
    lab2 = ax.text(0, 0, "", color=ACCENT2, fontsize=11.5)
    fig.text(0.08, 0.93, r"$f=x+\sin x\cos x,\ \ g=e^{\sin x}f$", fontsize=13, color=INK, va="center")
    fig.text(0.08, 0.865, "f′/g′ 는 0 으로 수렴하지만 f/g 는 1/e 와 e 사이를 계속 오간다",
             fontsize=11.5, color="#555555", va="center")

    frames = timeline(("draw", 90), ("end", HOLD_END))

    def update(fr):
        name, t = fr
        n = max(2, int(len(X) * (t if name == "draw" else 1.0)))
        l_ratio.set_data(X[:n], ratio[:n])
        l_dratio.set_data(X[:n], dratio[:n])
        xe = X[n - 1]
        lab1.set_text("f/g = e^(−sin x)")
        lab1.set_position((min(xe, 31) + 0.5, 2.78))
        lab2.set_text("f′/g′")
        lab2.set_position((min(xe, 36) + 0.5, 0.12))
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "gprime-zero-counterexample.gif", len(frames))


if __name__ == "__main__":
    gif_secant_tangent()
    gif_gprime_zero()
