"""Animated GIFs for the post "그래프 그리기 전에 적는 다섯 줄".

usage: python make_gifs.py   ->  images/blog/sketch-graph-five-steps/*.gif

  five_steps.gif     f(x) = (x+1)(x-2)(x-3) / ((x-1)(x+3)(x-3)), built up step by step
  asymptote_to_hole.gif   f_eps(x) = (x-2+eps)(x+1) / ((x-2)(x-3)), eps -> 0
  sign_chart.gif     f(x) = (x+2)(x-1)^2(x-3), sign chart vs. curve
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

OUT = Path(__file__).resolve().parents[3] / "images" / "blog" / "sketch-graph-five-steps"
FPS = 12
HOLD_END = 24                     # 2 s on the last frame

INK, GREY, LIGHT = "#222222", "#8a8a8a", "#e6e6e6"
BLUE, RED = "#1f5fa8", "#c8553d"

plt.rcParams.update({
    "font.family": "IBM Plex Sans KR",
    "mathtext.fontset": "dejavusans",
    "font.size": 11,
    "axes.edgecolor": "#bbbbbb",
    "axes.linewidth": 0.8,
    "xtick.color": GREY, "ytick.color": GREY,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def branch_x(a, b, n=1500, dense=()):
    """Sample the open interval (a, b), refined near both ends and around `dense` points."""
    t = np.logspace(-7, np.log10((b - a) / 2), 300)
    parts = [np.linspace(a, b, n), a + t, b - t]
    for c, w in dense:
        parts.append(np.linspace(c - w, c + w, 600))
    x = np.unique(np.concatenate(parts))
    return x[(x > a) & (x < b)]


def cut(y, ylim):
    """Drop points far outside the window so no vertical line joins the two sides of a pole."""
    y = np.array(y, dtype=float)
    y[np.abs(y) > 3 * ylim] = np.nan
    return y


def base_axes(ax, xlim, ylim, xticks, yticks):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.grid(color="#f0f0f0", lw=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color=INK, lw=0.9, zorder=1)
    ax.axvline(0, color=INK, lw=0.9, zorder=1)
    ax.tick_params(length=2)


def hole(ax, x, y, color=INK, size=7):
    ax.plot([x], [y], "o", ms=size, mfc="white", mec=color, mew=1.6, zorder=6)


def dot(ax, x, y, color=INK, size=5.5):
    ax.plot([x], [y], "o", ms=size, color=color, zorder=5)


def save(frames_fn, name, figsize):
    fig = plt.figure(figsize=figsize, dpi=100)
    writer = PillowWriter(fps=FPS)
    path = OUT / name
    n = 0
    with writer.saving(fig, str(path), dpi=100):
        for state in frames_fn():
            fig.clf()
            state(fig)
            writer.grab_frame()
            n += 1
    plt.close(fig)
    print(f"{name}: {n} frames, {path.stat().st_size / 1024:.0f} KB")


# ---------------------------------------------------------------- 1. five steps
def g1(x):
    """Reduced form of (x+1)(x-2)(x-3) / ((x-1)(x+3)(x-3))."""
    return (x + 1) * (x - 2) / ((x - 1) * (x + 3))


X1, Y1 = (-7, 7), (-6, 6)
BR1 = [branch_x(X1[0], -3), branch_x(-3, 1), branch_x(1, X1[1])]
STEPS = [
    ("1  끝", [r"$x\to\pm\infty$ 에서 $y\to 1$"]),
    ("2  영점", [r"$x=-1,\ 2$  (홑근, 관통)"]),
    ("3  끊김", [r"구멍  $(3,\ 1/3)$",
                r"수직 점근선  $x=-3,\ 1$",
                r"수평 점근선  $y=1$"]),
    ("4  절편", [r"$y$절편  $(0,\ 2/3)$"]),
    ("5  부호", [r"$+\quad-\quad+\quad-\quad+$",
                r"경계:  $-3,\ -1,\ 1,\ 2$"]),
]
SIGNS1 = [(-5.0, "+"), (-2.0, "−"), (-0.5, "+"), (1.5, "−"), (4.6, "+")]
CUTS1 = [X1[0], -3, -1, 1, 2, X1[1]]


def draw_five(fig, step, front=None):
    """step = number of checklist lines shown (0..5); front = x up to which the curve is drawn."""
    ax = fig.add_axes([0.06, 0.08, 0.53, 0.86])
    base_axes(ax, X1, Y1, range(-6, 7, 2), range(-6, 7, 2))
    hi = lambda k: RED if (k == step and front is None) else INK

    if step >= 1:                                   # end stubs with arrows
        for a, b, d in [(-7.0, -5.6, -1), (5.6, 7.0, 1)]:
            xs = np.linspace(a, b, 40)
            ax.plot(xs, g1(xs), color=hi(1), lw=2.2, zorder=4)
            x0 = a if d < 0 else b
            ax.annotate("", xy=(x0, g1(x0)), xytext=(x0 - 0.25 * d, g1(x0 - 0.25 * d)),
                        arrowprops=dict(arrowstyle="-|>", color=hi(1), lw=1.5), zorder=4)
    if step >= 2:                                   # zeros with a short crossing piece
        for r in (-1, 2):
            xs = np.linspace(r - 0.3, r + 0.3, 30)
            ax.plot(xs, g1(xs), color=hi(2), lw=2.2, zorder=4)
            dot(ax, r, 0, hi(2))
        ax.text(-1, -0.55, "−1", ha="center", va="top", fontsize=9, color=hi(2))
        ax.text(2, -0.55, "2", ha="center", va="top", fontsize=9, color=hi(2))
    if step >= 3:
        for a in (-3, 1):
            ax.axvline(a, color=hi(3), lw=1.1, ls=(0, (4, 3)), zorder=2)
        ax.axhline(1, color=hi(3), lw=1.1, ls=(0, (4, 3)), zorder=2)
        ax.text(-3.15, -5.6, "x = −3", ha="right", fontsize=9, color=hi(3))
        ax.text(1.15, 5.5, "x = 1", ha="left", fontsize=9, color=hi(3))
        ax.text(6.9, 1.25, "y = 1", ha="right", fontsize=9, color=hi(3))
    if step >= 4:
        dot(ax, 0, 2 / 3, hi(4))
        ax.text(-0.25, 1.25, "2/3", ha="right", fontsize=9, color=hi(4))
    if step >= 5:
        for (a, b), (xm, s) in zip(zip(CUTS1[:-1], CUTS1[1:]), SIGNS1):
            up = s == "+"
            ax.fill_between([a, b], 0, 6 if up else -6, color=BLUE if up else RED,
                            alpha=0.06, lw=0, zorder=0)
            ax.text(xm, -5.3 if not up else 5.2, s, ha="center", va="center",
                    fontsize=15, color=BLUE if up else RED, zorder=3)
    if front is not None:
        for xs in BR1:
            m = xs <= front
            if m.any():
                ax.plot(xs[m], cut(g1(xs[m]), Y1[1]), color=BLUE, lw=2.2, zorder=4)
    if step >= 3:
        hole(ax, 3, 1 / 3, hi(3))

    fig.text(0.625, 0.90, r"$f(x)=\frac{(x+1)(x-2)(x-3)}{(x-1)(x+3)(x-3)}$",
             fontsize=13, color=INK, va="center")
    y = 0.78
    for k, (head, lines) in enumerate(STEPS, start=1):
        c = (RED if k == step and front is None else INK) if k <= step else "#cccccc"
        fig.text(0.625, y, head, fontsize=12, color=c, weight="semibold", va="top")
        for ln in lines:
            fig.text(0.735, y, ln if k <= step else "", fontsize=10.5, color=c, va="top")
            y -= 0.055
        y -= 0.03
    if front is not None and front >= X1[1]:
        fig.text(0.625, 0.08, "곡선은 다섯 줄을 다 적은 뒤에 잇는다",
                 fontsize=10, color=GREY)


def frames_five():
    for _ in range(10):
        yield lambda f: draw_five(f, 0)
    for s in range(1, 6):
        for _ in range(18):
            yield lambda f, s=s: draw_five(f, s)
    for fr in np.linspace(X1[0], X1[1], 36):
        yield lambda f, fr=fr: draw_five(f, 5, fr)
    for _ in range(HOLD_END):
        yield lambda f: draw_five(f, 5, X1[1])


# ------------------------------------------------------- 2. asymptote -> hole
def fe(x, e):
    return (x - 2 + e) * (x + 1) / ((x - 2) * (x - 3))


X2, Y2 = (-3, 6.5), (-8, 8)


def draw_eps(fig, e):
    ax = fig.add_axes([0.07, 0.08, 0.90, 0.88])
    base_axes(ax, X2, Y2, range(-2, 7), range(-8, 9, 2))
    ax.axvline(3, color=GREY, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.axhline(1, color=GREY, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.text(3.1, -7.6, "x = 3", fontsize=9, color=GREY)
    ax.text(6.4, 1.3, "y = 1", ha="right", fontsize=9, color=GREY)

    if e > 0:
        ax.axvline(2, color=RED, lw=1.2, ls=(0, (4, 3)), zorder=2)
        ax.text(2.1, 7.2, "x = 2", fontsize=9, color=RED)
        dense = [(2 - e, 4 * e)]
        branches = [branch_x(X2[0], 2, dense=dense), branch_x(2, 3), branch_x(3, X2[1])]
        for xs in branches:
            ax.plot(xs, cut(fe(xs, e), Y2[1]), color=BLUE, lw=2.0, zorder=4)
        dot(ax, 2 - e, 0, RED)
        status = [rf"$\varepsilon = {e:.3f}$",
                  rf"영점  $x = 2-\varepsilon = {2 - e:.3f}$",
                  r"수직 점근선  $x = 2$"]
    else:
        for xs in [branch_x(X2[0], 3), branch_x(3, X2[1])]:
            ax.plot(xs, cut((xs + 1) / (xs - 3), Y2[1]), color=BLUE, lw=2.0, zorder=4)
        hole(ax, 2, -3, RED, size=8)
        ax.annotate("구멍 (2, −3)", xy=(2, -3), xytext=(0.3, -5.6), fontsize=10, color=RED,
                    arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
        status = [r"$\varepsilon = 0$",
                  r"$(x-2)$ 가 약분되어 $f=\frac{x+1}{x-3}$",
                  r"$x=2$ 는 구멍"]
    dot(ax, -1, 0, INK)

    ax.text(-2.8, 7.1, r"$f_\varepsilon(x)=\frac{(x-2+\varepsilon)(x+1)}{(x-2)(x-3)}$",
            fontsize=13, color=INK, va="center")
    for i, s in enumerate(status):
        ax.text(-2.8, 5.4 - 1.05 * i, s, fontsize=11 if i else 13,
                color=RED if i == 0 else INK, va="center")


def frames_eps():
    for _ in range(14):
        yield lambda f: draw_eps(f, 1.0)
    for e in 10 ** np.linspace(0, -2, 50):
        yield lambda f, e=e: draw_eps(f, e)
    for _ in range(10):
        yield lambda f: draw_eps(f, 0.01)
    for _ in range(HOLD_END + 6):
        yield lambda f: draw_eps(f, 0.0)


# --------------------------------------------------------------- 3. sign chart
def p3(x):
    return (x + 2) * (x - 1) ** 2 * (x - 3)


X3, Y3 = (-2.9, 3.9), (-22, 22)
CUTS3 = [X3[0], -2, 1, 3, X3[1]]
ROWS = [("x + 2", "−+++"), ("(x − 1)²", "++++"), ("x − 3", "−−−+")]
FROW = "+−−+"


def draw_signs(fig, k, front=None):
    """k = number of intervals already filled (0..4); front = x reached inside interval k."""
    ax = fig.add_axes([0.14, 0.40, 0.83, 0.56])
    base_axes(ax, X3, Y3, range(-2, 4), range(-20, 21, 10))
    tb = fig.add_axes([0.14, 0.05, 0.83, 0.28], sharex=ax)
    tb.set_ylim(-0.6, 3.6)
    tb.set_yticks([3, 2, 1, 0])
    tb.set_yticklabels([r[0] for r in ROWS] + ["f(x)"], fontsize=10.5, color=INK)
    tb.tick_params(axis="x", labelbottom=False, length=0)
    tb.tick_params(axis="y", length=0)
    for s in tb.spines.values():
        s.set_visible(False)
    tb.axhline(0.5, color="#bbbbbb", lw=0.8)
    for c in (-2, 1, 3):
        ax.axvline(c, color=LIGHT, lw=1.0, zorder=0)
        tb.axvline(c, color="#cccccc", lw=0.8)

    mids = [0.5 * (a + b) for a, b in zip(CUTS3[:-1], CUTS3[1:])]
    for row, (_, signs) in enumerate(ROWS):
        for xm, s in zip(mids, signs):
            tb.text(xm, 3 - row, s, ha="center", va="center", fontsize=13, color=GREY)

    xs_all = branch_x(X3[0], X3[1], n=3000)
    ax.plot(xs_all, cut(p3(xs_all), Y3[1]), color=LIGHT, lw=2.0, zorder=2)
    for i in range(4):
        a, b = CUTS3[i], CUTS3[i + 1]
        col = BLUE if FROW[i] == "+" else RED
        if i == k and front is not None:
            ax.axvspan(a, b, color=col, alpha=0.07, lw=0, zorder=0)
            tb.axvspan(a, b, color=col, alpha=0.07, lw=0, zorder=0)
        if i < k or (i == k and front is not None):
            end = b if i < k else front
            xs = xs_all[(xs_all >= a) & (xs_all <= end)]
            ax.plot(xs, cut(p3(xs), Y3[1]), color=col, lw=2.4, zorder=4)
            if i < k or front >= b:
                tb.text(mids[i], 0, FROW[i], ha="center", va="center", fontsize=15,
                        color=col, weight="semibold")

    for r, lab, dx, ha in [(-2, "관통", 0.12, "left"), (1, "접함", 0, "center"),
                           (3, "관통", -0.12, "right")]:
        dot(ax, r, 0, INK)
        ax.text(r + dx, 2.5, lab, ha=ha, va="bottom", fontsize=9.5, color=INK)
    dot(ax, 0, -6, INK)
    ax.text(0.12, -7.5, "(0, −6)", fontsize=9, color=INK, va="top")
    ax.text(-2.8, 19, r"$f(x)=(x+2)(x-1)^2(x-3)$", fontsize=12, color=INK, va="top")
    if k == 4:
        ax.text(3.8, -19.5, "중복도 2인 x = 1 에서는 부호가 바뀌지 않는다",
                ha="right", fontsize=9.5, color=GREY)


def frames_signs():
    for _ in range(12):
        yield lambda f: draw_signs(f, 0)
    for k in range(4):
        a, b = CUTS3[k], CUTS3[k + 1]
        for fr in np.linspace(a, b, 10):
            yield lambda f, k=k, fr=fr: draw_signs(f, k, fr)
        for _ in range(8):
            yield lambda f, k=k, b=b: draw_signs(f, k, b)
    for _ in range(HOLD_END):
        yield lambda f: draw_signs(f, 4)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    save(frames_five, "five_steps.gif", (7.2, 4.8))
    save(frames_eps, "asymptote_to_hole.gif", (7.2, 4.6))
    save(frames_signs, "sign_chart.gif", (7.2, 5.0))
