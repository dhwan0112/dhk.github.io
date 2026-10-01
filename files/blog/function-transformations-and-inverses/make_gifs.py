"""GIFs for the post on function transformations and inverse functions.

usage: python make_gifs.py   ->  images/blog/function-transformations-and-inverses/*.gif
Needs matplotlib + Pillow and the 'IBM Plex Sans KR' font.
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "images" / "blog" / "function-transformations-and-inverses"

FPS = 14
HOLD_END = 28          # frames (2.0 s at 14 fps)
INK, GREY, LIGHT = "#222222", "#8a8a8a", "#c8c8c8"
ACCENT, ACCENT2 = "#c8553d", "#2f6690"

plt.rcParams.update({
    "font.family": "IBM Plex Sans KR",
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


def style_axes(ax, xlim, ylim, xticks, yticks):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.grid(True, color="#eeeeee", lw=0.8, zorder=0)
    ax.axhline(0, color=GREY, lw=0.9, zorder=1)
    ax.axvline(0, color=GREY, lw=0.9, zorder=1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors="#555555", length=0, labelsize=10)


def timeline(*segments):
    """segments: (name, nframes). Returns list of (name, local_t in [0,1])."""
    frames = []
    for name, n in segments:
        for i in range(n):
            frames.append((name, i / (n - 1) if n > 1 else 1.0))
    return frames


def save(anim, fig, name, nframes):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    anim.save(path, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    print(f"{name}: {nframes} frames, {path.stat().st_size / 1024:.0f} KB")


# (a) sqrt(x) -> sqrt(2x) -> sqrt(2x+3) = sqrt(2(x+1.5)), vs the wrong sqrt(2x+6)
def gif_shift():
    u = np.linspace(0, 16, 400)            # parent-graph inputs, points (u, sqrt u)
    v = np.sqrt(u)
    feats = [(0.0, "끝점"), (4.0, None)]    # tracked parent inputs

    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=100)
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.08, top=0.80)
    style_axes(ax, (-4.2, 5.2), (-0.9, 3.3), range(-4, 6), range(0, 4))

    ghost, = ax.plot(u, v, color=LIGHT, lw=1.6, zorder=2)
    wrong, = ax.plot([], [], color=GREY, lw=1.6, ls=(0, (4, 3)), zorder=2, alpha=0)
    wrong_pts = ax.scatter([], [], s=28, facecolor="white", edgecolor=GREY, lw=1.3,
                           zorder=4, alpha=0)
    curve, = ax.plot(u, v, color=INK, lw=2.4, zorder=3)
    pts = ax.scatter([0, 4], [0, 2], s=40, color=ACCENT, zorder=5)
    lab = [ax.text(0, 0, "", fontsize=11, color=ACCENT, zorder=6,
                   ha="center", va="bottom") for _ in feats]
    arrow = ax.annotate("", xy=(0, -0.45), xytext=(0, -0.45),
                        arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.6))
    arrow_txt = ax.text(0, -0.78, "", color=ACCENT, fontsize=11, ha="center")
    wrong_txt = ax.text(1.15, 0.78, "", color=GREY, fontsize=11, alpha=0,
                        va="top", linespacing=1.5)
    wrong_lab = ax.text(-3.15, 0.15, "", color=GREY, fontsize=11, alpha=0, ha="right")
    title = fig.text(0.06, 0.92, "", fontsize=15, color=INK, va="center")
    sub = fig.text(0.06, 0.845, "", fontsize=11.5, color="#555555", va="center")

    frames = timeline(("show", 18), ("scale", 24), ("hold1", 16), ("shift", 24),
                      ("hold2", 16), ("wrong", 18), ("end", HOLD_END))

    def fmt(x):
        return f"{x:g}".replace("-", "−")

    def update(fr):
        name, t = fr
        k, s = 1.0, 0.0
        if name == "scale":
            k = 1 - 0.5 * ease(t)
        elif name in ("hold1",):
            k = 0.5
        elif name == "shift":
            k, s = 0.5, -1.5 * ease(t)
        elif name in ("hold2", "wrong", "end"):
            k, s = 0.5, -1.5
        X = k * u + s
        curve.set_data(X, v)
        fx = [k * f + s for f, _ in feats]
        fy = [np.sqrt(f) for f, _ in feats]
        pts.set_offsets(np.c_[fx, fy])
        for L, x, y, (_, tag) in zip(lab, fx, fy, feats):
            txt = f"({fmt(round(x, 2))}, {fmt(round(y, 2))})"
            L.set_text(txt)
            if y == 0:
                L.set_position((x - 0.15, y + 0.15))
                L.set_ha("right")
            else:
                L.set_position((x, y + 0.18))
                L.set_ha("center")

        if name in ("show",):
            title.set_text(r"$y=\sqrt{x}$")
            sub.set_text("기준 그래프. 끝점 (0, 0)과 점 (4, 2)를 따라간다")
        elif name in ("scale", "hold1"):
            title.set_text(r"$y=\sqrt{2x}$")
            sub.set_text("x 자리에 2x: 가로로 1/2배. 점 (4, 2)는 (2, 2)로")
        else:
            title.set_text(r"$y=\sqrt{2x+3}=\sqrt{2(x+1.5)}$")
            sub.set_text("x 자리에 x+1.5: 왼쪽으로 1.5. 3이 아니다")

        if name in ("shift", "hold2", "wrong", "end"):
            arrow.set_visible(True)
            arrow.xy = (s, -0.45)
            arrow.set_position((0.0, -0.45))
            arrow_txt.set_text(f"{fmt(round(s, 2))}")
            arrow_txt.set_position((s / 2, -0.82))
        else:
            arrow.set_visible(False)
            arrow_txt.set_text("")

        a = 0.0
        if name == "wrong":
            a = ease(t)
        elif name == "end":
            a = 1.0
        if a > 0:
            wrong.set_data(0.5 * u - 3, v)
            wrong_pts.set_offsets(np.c_[[-3, -1], [0, 2]])
            wrong_txt.set_text("회색 점선: 가로 1/2배 후 왼쪽으로 3\n"
                               + r"$=\sqrt{2(x+3)}=\sqrt{2x+6}$" + "  (다른 함수)")
            wrong_lab.set_text("(−3, 0)")
        for artist in (wrong, wrong_pts, wrong_txt, wrong_lab):
            artist.set_alpha(a)
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "shift-order-sqrt.gif", len(frames))


# (b) horizontal line test: x^2 on R vs x^2 on x >= 0
def gif_hline():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.5), dpi=100)
    fig.subplots_adjust(left=0.05, right=0.98, bottom=0.07, top=0.80, wspace=0.12)
    xs = np.linspace(-2.3, 2.3, 300)
    titles = [r"$y=x^2$,  모든 실수 $x$", r"$y=x^2$,  $x\geq 0$"]
    lines, dots, counts = [], [], []
    for i, ax in enumerate(axes):
        style_axes(ax, (-2.6, 2.6), (-1.0, 4.8), range(-2, 3), range(0, 5))
        if i == 0:
            ax.plot(xs, xs**2, color=INK, lw=2.4, zorder=3)
        else:
            ax.plot(xs[xs <= 0], xs[xs <= 0]**2, color=LIGHT, lw=1.6, ls=(0, (4, 3)), zorder=2)
            ax.plot(xs[xs >= 0], xs[xs >= 0]**2, color=INK, lw=2.4, zorder=3)
            ax.scatter([0], [0], s=30, color=INK, zorder=4)
        ax.set_title(titles[i], fontsize=13, color=INK, pad=8)
        ln = ax.axhline(0, color=ACCENT2, lw=1.6, zorder=2)
        d = ax.scatter([], [], s=46, color=ACCENT, zorder=5)
        c = ax.text(0.97, 0.04, "", transform=ax.transAxes, fontsize=11.5,
                    color=ACCENT, ha="right", va="bottom")
        lines.append(ln); dots.append(d); counts.append(c)
    head = fig.text(0.05, 0.93, "", fontsize=13, color=INK, va="center")

    frames = timeline(("up", 44), ("pause", 8), ("down", 26), ("end", HOLD_END))
    c_lo, c_hi, c_end = -0.6, 4.4, 2.25

    def update(fr):
        name, t = fr
        if name == "up":
            c = c_lo + (c_hi - c_lo) * ease(t)
        elif name == "pause":
            c = c_hi
        elif name == "down":
            c = c_hi + (c_end - c_hi) * ease(t)
        else:
            c = c_end
        head.set_text(f"수평선 y = {c:.2f}".replace("-", "−"))
        for i in range(2):
            lines[i].set_ydata([c, c])
            if c < 0:
                xi = []
            elif i == 0:
                r = np.sqrt(c)
                xi = [-r, r] if r > 1e-9 else [0.0]
            else:
                xi = [np.sqrt(c)]
            dots[i].set_offsets(np.c_[xi, [c] * len(xi)] if xi else np.empty((0, 2)))
            n = len(xi)
            counts[i].set_text(f"교점 {n}개")
            counts[i].set_color(ACCENT if n >= 2 else ACCENT2)
        if name == "end":
            head.set_text("y = 2.25: 왼쪽은 x = ±1.5 두 점, 오른쪽은 x = 1.5 한 점")
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "horizontal-line-test.gif", len(frames))


# (c) points of y = e^x reflected in y = x become y = ln x
def gif_reflect():
    fig, ax = plt.subplots(figsize=(7.2, 6.6), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.06, top=0.88)
    lim = (-3.2, 4.4)
    style_axes(ax, lim, lim, range(-3, 5), range(-3, 5))
    ax.plot(lim, lim, color=GREY, lw=1.2, ls=(0, (5, 4)), zorder=2)
    ax.text(3.55, 3.95, "y = x", color=GREY, fontsize=11, ha="right")

    a = np.linspace(-3.2, np.log(4.4), 300)
    b = np.exp(a)
    ax.plot(a, b, color=INK, lw=2.4, zorder=3)
    ax.text(1.12, 3.9, r"$y=e^{x}$", color=INK, fontsize=13, ha="right")
    moving, = ax.plot([], [], color=ACCENT, lw=1.4, alpha=0.5, zorder=3)
    final, = ax.plot([], [], color=ACCENT, lw=2.4, zorder=3)
    final_lab = ax.text(0.75, -1.5, "", color=ACCENT, fontsize=13)

    pa = np.array([-2.0, -1.0, 0.0, 0.5, 1.0, 1.3])
    pb = np.exp(pa)
    ax.scatter(pa, pb, s=26, color=INK, zorder=4)
    segs = [ax.plot([], [], color=LIGHT, lw=1.0, ls=":", zorder=2)[0] for _ in pa]
    pts = ax.scatter(pa, pb, s=40, color=ACCENT, zorder=5)
    lab_src = [ax.text(0, 0, "", fontsize=10.5, color=INK, zorder=6) for _ in range(2)]
    lab_dst = [ax.text(0, 0, "", fontsize=10.5, color=ACCENT, zorder=6) for _ in range(2)]
    title = fig.text(0.08, 0.94, "", fontsize=13, color=INK, va="center")

    frames = timeline(("show", 16), ("move", 40), ("trace", 16), ("end", HOLD_END))

    def update(fr):
        name, t = fr
        s = 0.0 if name == "show" else (ease(t) if name == "move" else 1.0)
        X = (1 - s) * pa + s * pb
        Y = (1 - s) * pb + s * pa
        pts.set_offsets(np.c_[X, Y])
        for g, x0, y0, x1, y1 in zip(segs, pa, pb, X, Y):
            g.set_data([x0, x1], [y0, y1])
        moving.set_data((1 - s) * a + s * b, (1 - s) * b + s * a)
        moving.set_visible(name == "move")

        if name == "show":
            title.set_text("점 (a, b)를 y = x에 대해 뒤집으면 (b, a)")
        elif name == "move":
            title.set_text("각 점은 y = x에 수직으로 움직이고, 중점은 y = x 위에 있다")
        else:
            title.set_text("뒤집힌 점들이 이루는 곡선: " + r"$y=\ln x$")

        on = name in ("trace", "end")
        final.set_data(b, a) if on else final.set_data([], [])
        final_lab.set_text(r"$y=\ln x$" if on else "")

        # coordinate labels for (0,1)<->(1,0) and (1,e)<->(e,1)
        e = np.e
        lab_src[0].set_text("(0, 1)"); lab_src[0].set_position((-0.12, 1.12))
        lab_src[1].set_text("(1, 2.72)"); lab_src[1].set_position((0.85, e - 0.05))
        for L in lab_src:
            L.set_ha("right")
        show_dst = name == "end" or (name == "trace")
        lab_dst[0].set_text("(1, 0)" if show_dst else ""); lab_dst[0].set_position((1.1, -0.42))
        lab_dst[1].set_text("(2.72, 1)" if show_dst else ""); lab_dst[1].set_position((e + 0.1, 0.62))
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "inverse-reflection-exp-ln.gif", len(frames))


if __name__ == "__main__":
    gif_shift()
    gif_hline()
    gif_reflect()
