"""GIF for the note on synthetic division and Horner's method.

usage: python make_gifs.py   ->  images/blog/synthetic-division-and-horner-method/*.gif
Needs matplotlib + Pillow and the 'IBM Plex Sans KR' font.
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "images" / "blog" / "synthetic-division-and-horner-method"

FPS = 14
HOLD_END = 32
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


def timeline(*segments):
    frames = []
    for name, n in segments:
        for i in range(n):
            frames.append((name, i / (n - 1) if n > 1 else 1.0))
    return frames


def m(v):
    return f"{v:g}".replace("-", "−")


def save(anim, fig, name, nframes):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    anim.save(path, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    print(f"{name}: {nframes} frames, {path.stat().st_size / 1024:.0f} KB")


# P(x) = 2x^3 - 5x^2 + 3x - 7 divided by x - 2
def gif_synthetic():
    a = [2, -5, 3, -7]
    c = 2
    b = [a[0]]
    for k in a[1:]:
        b.append(k + c * b[-1])           # 2, -1, 1, -5
    mid = [None] + [c * v for v in b[:-1]]  # -, 4, -2, 2

    fig = plt.figure(figsize=(7.2, 4.8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.7)
    ax.axis("off")

    X = [3.2, 4.7, 6.2, 7.7]
    Y_TOP, Y_MID, Y_BOT = 4.9, 4.15, 3.25
    ax.text(0.5, 6.25, r"$P(x)=2x^3-5x^2+3x-7$ 를 $x-2$ 로 나눈다", fontsize=13.5, color=INK, va="center")
    ax.text(2.2, Y_MID, "c = 2", fontsize=13, color=ACCENT2, ha="right", va="center")
    ax.plot([2.45, 2.45], [Y_MID - 0.45, Y_TOP + 0.4], color=GREY, lw=1.2)
    ax.plot([2.45, 8.4], [Y_MID - 0.42, Y_MID - 0.42], color=GREY, lw=1.2)
    for x, v in zip(X, a):
        ax.text(x, Y_TOP, m(v), fontsize=17, color=INK, ha="center", va="center")
    mid_txt = [ax.text(x, Y_MID, "", fontsize=15, color=ACCENT2, ha="center", va="center") for x in X]
    bot_txt = [ax.text(x, Y_BOT, "", fontsize=17, color=ACCENT, ha="center", va="center") for x in X]
    arrow = ax.annotate("", xy=(0, 0), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="->", color=ACCENT2, lw=1.4))
    step_txt = ax.text(0.5, 2.35, "", fontsize=12, color="#555555", va="center")

    ax.text(0.5, 1.55, "Horner:", fontsize=12.5, color=INK, va="center")
    horner_txt = ax.text(2.0, 1.55, "", fontsize=13, color=INK, va="center")
    result_txt = ax.text(0.5, 0.65, "", fontsize=12.5, color=ACCENT, va="center")

    horner_steps = ["2",
                    "2 · 2 − 5 = −1",
                    "(−1) · 2 + 3 = 1",
                    "1 · 2 − 7 = −5"]

    segs = [("s0", 18)]
    for k in range(1, 4):
        segs += [(f"mul{k}", 16), (f"add{k}", 16)]
    segs += [("end", HOLD_END)]
    frames = timeline(*segs)

    def update(fr):
        name, t = fr
        if name == "s0":
            stage, phase = 0, "add"
        elif name == "end":
            stage, phase = 3, "end"
        else:
            stage, phase = int(name[-1]), name[:3]

        for k in range(4):
            mid_txt[k].set_text(m(mid[k]) if mid[k] is not None and (k < stage or (k == stage and phase in ("mul", "add", "end"))) else "")
            bot_txt[k].set_text(m(b[k]) if (k < stage or (k == stage and phase in ("add", "end"))) else "")

        arrow.set_visible(phase in ("mul",))
        if phase == "mul":
            k = stage
            arrow.xy = (X[k] - 0.25, Y_MID + 0.2)
            arrow.set_position((X[k - 1] + 0.25, Y_BOT + 0.15))
            step_txt.set_text(f"곱한다: 아랫줄 {m(b[k - 1])} × c = {m(mid[k])} 를 다음 칸에 쓴다")
        elif phase == "add" and stage > 0:
            k = stage
            step_txt.set_text(f"더한다: {m(a[k])} + {m(mid[k])} = {m(b[k])}")
        elif stage == 0:
            step_txt.set_text("내린다: 첫 계수 2 를 그대로 아랫줄로")
        else:
            step_txt.set_text("아랫줄 2, −1, 1 은 몫의 계수, 마지막 −5 는 나머지")

        shown = stage if phase != "mul" else stage - 1
        horner_txt.set_text("  →  ".join(horner_steps[: shown + 1]) if shown >= 0 else "")
        if phase == "end":
            result_txt.set_text("몫 2x² − x + 1, 나머지 −5 = P(2). 두 계산의 중간값이 같다")
        else:
            result_txt.set_text("")
        return []

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    save(anim, fig, "synthetic-horner.gif", len(frames))


if __name__ == "__main__":
    gif_synthetic()
