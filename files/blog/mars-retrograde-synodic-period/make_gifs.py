"""화성 역행 운동과 회합 주기 GIF 두 개를 만든다.

모형: 지구와 화성이 태양을 중심으로 같은 평면의 원궤도를 등속으로 돈다.
    지구 a = 1 AU,     P = 365.25 d
    화성 a = 1.524 AU, P = 686.98 d
    금성 a = 0.723 AU, P = 224.70 d (수치 비교만)

실행: python make_gifs.py
출력: <사이트 루트>/images/blog/mars-retrograde-synodic-period/*.gif
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.collections import LineCollection

P_E, P_M, P_V = 365.25, 686.98, 224.70
A_E, A_M, A_V = 1.0, 1.524, 0.723
W_E, W_M = 2 * np.pi / P_E, 2 * np.pi / P_M

FPS = 13
HOLD = 22  # 마지막 프레임 정지 (22 / 13 fps = 1.7 s)

INK = "#222222"
GREY = "#9a9a9a"
LIGHT = "#d9d9d9"
MARS = "#d55e00"
EARTH = "#0b5394"
LABEL_BOX = dict(boxstyle="square,pad=0.15", fc="white", ec="none")

plt.rcParams.update({
    "font.family": "IBM Plex Sans KR",
    "mathtext.fontset": "dejavusans",
    "axes.unicode_minus": False,
    "font.size": 10.5,
    "axes.edgecolor": "#555555",
    "axes.linewidth": 0.8,
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "images" / "blog" / "mars-retrograde-synodic-period"


def positions(t, a, w, phase=0.0):
    return a * np.cos(w * t + phase), a * np.sin(w * t + phase)


def apparent_longitude(t):
    """지구에서 본 화성의 겉보기 황경 (deg, 연속). t = 0이 충."""
    xe, ye = positions(t, A_E, W_E)
    xm, ym = positions(t, A_M, W_M)
    return np.degrees(np.unwrap(np.arctan2(ym - ye, xm - xe)))


def synodic(p1, p2):
    return 1.0 / abs(1.0 / p1 - 1.0 / p2)


def retrograde_window(a, p, dt=0.001):
    """원궤도 모형에서 역행 시작·끝 (충 기준 일) 과 역행 호 길이 (deg)."""
    w = 2 * np.pi / p
    t = np.arange(-250, 250, dt)
    xe, ye = positions(t, A_E, W_E)
    xp, yp = positions(t, a, w)
    lam = np.degrees(np.unwrap(np.arctan2(yp - ye, xp - xe)))
    idx = np.where(np.gradient(lam, t) < 0)[0]
    return t[idx[0]], t[idx[-1]], lam[idx[0]] - lam[idx[-1]]


def stationary_angle(a, p):
    """정류 조건 cos(theta) = (a^2 w_p + w_E) / (a (w_E + w_p)) 의 theta (deg)."""
    wp = 2 * np.pi / p
    return np.degrees(np.arccos((a**2 * wp + W_E) / (a * (W_E + wp))))


def report():
    s_m, s_v = synodic(P_E, P_M), synodic(P_E, P_V)
    t0, t1, arc = retrograde_window(A_M, P_M)
    v0, v1, varc = retrograde_window(A_V, P_V)
    th = stationary_angle(A_M, P_M)
    print(f"Mars  synodic  S = {s_m:.1f} d = {s_m / P_E:.3f} yr")
    print(f"Venus synodic  S = {s_v:.1f} d = {s_v / P_E:.3f} yr")
    print(f"Kepler  Mars  P = 1.524^1.5 = {A_M**1.5:.4f} yr = {A_M**1.5 * P_E:.1f} d")
    print(f"Kepler  Venus P = 0.723^1.5 = {A_V**1.5:.4f} yr = {A_V**1.5 * P_E:.1f} d")
    print(f"Mars  retrograde {t0:+.1f} .. {t1:+.1f} d -> {t1 - t0:.1f} d, arc {arc:.1f} deg")
    print(f"Venus retrograde {v0:+.1f} .. {v1:+.1f} d -> {v1 - v0:.1f} d, arc {varc:.1f} deg")
    print(f"Mars  stationary angle {th:.2f} deg -> "
          f"{2 * th / (360 / s_m):.1f} d")
    return t1 - t0


def colored_segments(x, y, retro):
    pts = np.column_stack([x, y]).reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    colors = [MARS if r else INK for r in retro[:-1]]
    widths = [2.4 if r else 1.4 for r in retro[:-1]]
    return segs, colors, widths


def make_retrograde_gif(retro_days):
    half = 274.0
    t_all = np.linspace(-half, half, 4001)
    lam_all = apparent_longitude(t_all)
    retro_all = np.gradient(lam_all, t_all) < 0
    t_frames = np.linspace(-half, half, 130)
    frames = list(range(len(t_frames))) + [len(t_frames) - 1] * HOLD

    fig = plt.figure(figsize=(8.6, 4.3), dpi=100)
    ax_o = fig.add_axes([0.02, 0.08, 0.40, 0.84])
    ax_l = fig.add_axes([0.53, 0.15, 0.44, 0.72])

    th = np.linspace(0, 2 * np.pi, 400)
    lim = 1.95
    ax_o.plot(A_E * np.cos(th), A_E * np.sin(th), color=LIGHT, lw=1)
    ax_o.plot(A_M * np.cos(th), A_M * np.sin(th), color=LIGHT, lw=1)
    ax_o.plot(0, 0, "o", color="#f2b134", ms=10, zorder=3)
    ax_o.set_xlim(-lim, lim)
    ax_o.set_ylim(-lim, lim)
    ax_o.set_aspect("equal")
    ax_o.axis("off")
    ax_o.annotate("", xy=(1.9, -1.72), xytext=(1.35, -1.72),
                  arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
    ax_o.text(1.9, -1.84, "황경 0° 방향", ha="right", va="top", fontsize=8.5, color=GREY,
              bbox=LABEL_BOX, zorder=5)
    fig.text(0.03, 0.96, "태양 중심, 위에서 본 궤도", ha="left", va="top", fontsize=10, color=INK)

    (sight,) = ax_o.plot([], [], color=GREY, lw=0.9, ls="--")
    (trail_e,) = ax_o.plot([], [], color=EARTH, lw=1.6, alpha=0.5)
    (trail_m,) = ax_o.plot([], [], color=MARS, lw=1.6, alpha=0.5)
    (dot_e,) = ax_o.plot([], [], "o", color=EARTH, ms=7, zorder=4)
    (dot_m,) = ax_o.plot([], [], "o", color=MARS, ms=6, zorder=4)
    lab_e = ax_o.text(0, 0, "지구", fontsize=9, color=EARTH, ha="center", va="center",
                      bbox=LABEL_BOX, zorder=5)
    lab_m = ax_o.text(0, 0, "화성", fontsize=9, color=MARS, ha="center", va="center",
                      bbox=LABEL_BOX, zorder=5)

    ax_l.set_xlim(-half, half)
    pad = 8
    ax_l.set_ylim(lam_all.min() - pad, lam_all.max() + pad)
    ax_l.set_xlabel("충으로부터 경과 일수 (일)")
    ax_l.set_ylabel("화성의 겉보기 황경 (°)")
    ax_l.set_title("배경별 기준 방향 (지구에서 본 화성)", fontsize=10, loc="left", color=INK)
    ax_l.axvline(0, color=LIGHT, lw=0.8, zorder=0)
    ax_l.text(4, lam_all.min() - pad + 3, "충", fontsize=9, color=GREY, va="bottom")
    for side in ("top", "right"):
        ax_l.spines[side].set_visible(False)
    ax_l.plot(t_all, lam_all, color=LIGHT, lw=1, zorder=0)
    lc = LineCollection([], zorder=2)
    ax_l.add_collection(lc)
    (cur,) = ax_l.plot([], [], "o", color=INK, ms=5, zorder=3, clip_on=False)
    status = ax_l.text(0.02, 0.97, "", transform=ax_l.transAxes, ha="left", va="top",
                       fontsize=10)
    r_idx = np.where(retro_all)[0]
    t_r0, t_r1 = t_all[r_idx[0]], t_all[r_idx[-1]]
    band = ax_l.axvspan(t_r0, t_r1, color=MARS, alpha=0.0, lw=0, zorder=0)
    note = ax_l.text(0.98, 0.05, "", transform=ax_l.transAxes, ha="right", va="bottom",
                     fontsize=9.5, color=MARS)

    trail_len = 60.0

    def draw(i):
        t = t_frames[i]
        xe, ye = positions(t, A_E, W_E)
        xm, ym = positions(t, A_M, W_M)
        tt = np.linspace(max(-half, t - trail_len), t, 40)
        trail_e.set_data(*positions(tt, A_E, W_E))
        trail_m.set_data(*positions(tt, A_M, W_M))
        dot_e.set_data([xe], [ye])
        dot_m.set_data([xm], [ym])
        lab_e.set_position((xe * 0.72, ye * 0.72))
        lab_m.set_position((xm * 1.17, ym * 1.17))
        ux, uy = xm - xe, ym - ye
        n = np.hypot(ux, uy)
        L = 6.0
        sight.set_data([xe, xe + L * ux / n], [ye, ye + L * uy / n])

        m = t_all <= t + 1e-9
        segs, colors, widths = colored_segments(t_all[m], lam_all[m], retro_all[m])
        lc.set_segments(segs)
        lc.set_color(colors)
        lc.set_linewidth(widths)
        lam_t = np.interp(t, t_all, lam_all)
        cur.set_data([t], [lam_t])
        is_retro = t_r0 <= t <= t_r1
        if is_retro:
            status.set_text("역행: 황경 감소")
            status.set_color(MARS)
            dot_m.set_markersize(8)
        else:
            status.set_text("순행: 황경 증가")
            status.set_color(INK)
            dot_m.set_markersize(6)
        if t > t_r1:
            band.set_alpha(0.10)
            note.set_text(f"역행 {retro_days:.1f}일 (원궤도 모형)")
        else:
            band.set_alpha(0.0)
            note.set_text("")
        return []

    anim = animation.FuncAnimation(fig, draw, frames=frames, blit=False)
    path = OUT / "retrograde-two-panel.gif"
    anim.save(path, writer=animation.PillowWriter(fps=FPS))
    plt.close(fig)
    return path


def make_synodic_gif():
    s = synodic(P_E, P_M)
    t_frames = np.linspace(0, s, 125)
    frames = list(range(len(t_frames))) + [len(t_frames) - 1] * HOLD

    fig = plt.figure(figsize=(8.6, 4.3), dpi=100)
    ax_o = fig.add_axes([0.02, 0.08, 0.40, 0.84])
    ax_a = fig.add_axes([0.53, 0.15, 0.44, 0.72])

    th = np.linspace(0, 2 * np.pi, 400)
    lim = 1.95
    ax_o.plot(A_E * np.cos(th), A_E * np.sin(th), color=LIGHT, lw=1)
    ax_o.plot(A_M * np.cos(th), A_M * np.sin(th), color=LIGHT, lw=1)
    ax_o.plot(0, 0, "o", color="#f2b134", ms=10, zorder=3)
    ax_o.plot([0, A_M], [0, 0], color=GREY, lw=0.9, ls=":", zorder=1)
    ax_o.set_xlim(-lim, lim)
    ax_o.set_ylim(-lim, lim)
    ax_o.set_aspect("equal")
    ax_o.axis("off")
    fig.text(0.03, 0.96, "t = 0에 태양·지구·화성 일직선 (충)", ha="left", va="top",
             fontsize=10, color=INK)
    counter = ax_o.text(-lim, -lim, "", ha="left", va="bottom", fontsize=12, color=INK)

    (line,) = ax_o.plot([], [], color=GREY, lw=0.9, ls="--", zorder=1)
    (dot_e,) = ax_o.plot([], [], "o", color=EARTH, ms=7, zorder=4)
    (dot_m,) = ax_o.plot([], [], "o", color=MARS, ms=6, zorder=4)
    lab_e = ax_o.text(0, 0, "지구", fontsize=9, color=EARTH, ha="center", va="center",
                      bbox=LABEL_BOX, zorder=5)
    lab_m = ax_o.text(0, 0, "화성", fontsize=9, color=MARS, ha="center", va="center",
                      bbox=LABEL_BOX, zorder=5)

    t_line = np.linspace(0, s, 400)
    ang_e = np.degrees(W_E * t_line)
    ang_m = np.degrees(W_M * t_line)
    ax_a.set_xlim(0, 820)
    ax_a.set_ylim(0, 800)
    ax_a.set_xlabel("경과 일수 (일)")
    ax_a.set_ylabel("t = 0부터 돈 각도 (°)")
    ax_a.set_title("누적 공전각과 그 차이", fontsize=10, loc="left", color=INK)
    for side in ("top", "right"):
        ax_a.spines[side].set_visible(False)
    ax_a.axhline(360, color=LIGHT, lw=0.8, zorder=0)
    ax_a.text(8, 366, "360°", fontsize=8.5, color=GREY, va="bottom")
    (l_e,) = ax_a.plot([], [], color=EARTH, lw=1.6, label="지구 $\\omega_E t$")
    (l_m,) = ax_a.plot([], [], color=MARS, lw=1.6, label="화성 $\\omega_M t$")
    (l_d,) = ax_a.plot([], [], color=INK, lw=2.0, ls="--",
                       label="차이 $(\\omega_E-\\omega_M)t$")
    ax_a.legend(loc="upper left", frameon=False, fontsize=9)
    vline = ax_a.axvline(s, color=MARS, lw=1, alpha=0.0)
    end_note = ax_a.text(s - 10, 120, "", ha="right", va="bottom", fontsize=9.5, color=MARS)

    def draw(i):
        t = t_frames[i]
        xe, ye = positions(t, A_E, W_E)
        xm, ym = positions(t, A_M, W_M)
        dot_e.set_data([xe], [ye])
        dot_m.set_data([xm], [ym])
        lab_e.set_position((xe * 0.72, ye * 0.72))
        lab_m.set_position((xm * 1.17, ym * 1.17))
        final = i == len(t_frames) - 1
        if final:
            line.set_data([0, xm], [0, ym])
            counter.set_text(f"{s:.1f}일 ({s / P_E:.2f}년): 다시 충")
            counter.set_color(MARS)
            vline.set_alpha(0.8)
            end_note.set_text(f"차이가 360°가 되는 순간\nS = {s:.1f}일")
        else:
            line.set_data([], [])
            counter.set_text(f"경과 {t:.0f}일")
            counter.set_color(INK)
            vline.set_alpha(0.0)
            end_note.set_text("")
        m = t_line <= t + 1e-9
        l_e.set_data(t_line[m], ang_e[m])
        l_m.set_data(t_line[m], ang_m[m])
        l_d.set_data(t_line[m], ang_e[m] - ang_m[m])
        return []

    anim = animation.FuncAnimation(fig, draw, frames=frames, blit=False)
    path = OUT / "synodic-period.gif"
    anim.save(path, writer=animation.PillowWriter(fps=FPS))
    plt.close(fig)
    return path


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    retro_days = report()
    for p in (make_retrograde_gif(retro_days), make_synodic_gif()):
        print(f"{p.name}: {p.stat().st_size / 1024:.0f} KB")
