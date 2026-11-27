import argparse
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.patches import Arc

INK = "#111111"
PAPER = "#ffffff"
GHOST = "#9a9a9a"

PARTICLES = 4000
HALF_APPROACH = 0.15
BEAM_RADIUS = 2.0
PUDDING_RADIUS = 3.5
SPEED = 1.0
START_X = -7.0
VIEW = 5.0
DETECTOR_RADIUS = 6.0
SCREEN_RADIUS = 4.5
SCREEN_GAP_DEGREES = 28.0
STEP = 0.005
SAMPLE_EVERY = 12
SAMPLE_DT = STEP * SAMPLE_EVERY
TOTAL_TIME = 24.0
FRAME_DT = 0.25
NUCLEAR_BINS = np.arange(10.0, 181.0, 10.0)
PUDDING_BINS = np.concatenate([np.arange(0.0, 10.0, 2.0), np.arange(10.0, 181.0, 10.0)])
TRAIL_SAMPLES = (18, 45)
BEND_THRESHOLD = 30.0
INTERLUDE_FRAMES = 36
NUCLEUS_METRES = 7.0e-15
ATOM_METRES = 1.4e-10
SCREEN_METRES = 2.0e-2
ZOOM_KEYS = ((0, -13.5), (14, -13.5), (44, -9.65), (58, -9.65), (94, -1.5), (118, -1.5))
INTRO_FRAMES = ZOOM_KEYS[-1][0]

plt.rcParams.update(
    {
        "font.family": "cmr10",
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "text.color": INK,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
    }
)


def zoom_exponent(frame):
    for (start, low), (stop, high) in zip(ZOOM_KEYS[:-1], ZOOM_KEYS[1:]):
        if frame <= stop:
            fraction = (frame - start) / (stop - start)
            eased = fraction * fraction * (3.0 - 2.0 * fraction)
            return low + (high - low) * eased
    return ZOOM_KEYS[-1][1]


def simulate(impact, side, charge_radius):
    positions = np.column_stack([np.full(PARTICLES, START_X), side * impact])
    velocities = np.column_stack([np.full(PARTICLES, SPEED), np.zeros(PARTICLES)])
    strength = HALF_APPROACH * SPEED**2

    def acceleration(points):
        distance = np.maximum(np.hypot(points[:, 0], points[:, 1]), charge_radius)
        return strength * points / distance[:, None] ** 3

    steps = int(TOTAL_TIME / STEP)
    samples = steps // SAMPLE_EVERY + 1
    path = np.empty((PARTICLES, samples, 2), dtype=np.float32)
    angle = np.empty((PARTICLES, samples), dtype=np.float32)
    path[:, 0] = positions
    angle[:, 0] = 0.0
    accel = acceleration(positions)
    for step in range(1, steps + 1):
        half = velocities + 0.5 * STEP * accel
        positions = positions + STEP * half
        accel = acceleration(positions)
        velocities = half + 0.5 * STEP * accel
        if step % SAMPLE_EVERY == 0:
            index = step // SAMPLE_EVERY
            path[:, index] = positions
            angle[:, index] = np.abs(np.degrees(np.arctan2(velocities[:, 1], velocities[:, 0])))
    radius = np.hypot(path[:, :, 0], path[:, :, 1])
    closest = np.argmin(radius, axis=1)
    after = np.arange(samples)[None, :] > closest[:, None]
    exit_index = np.argmax(after & (radius > DETECTOR_RADIUS), axis=1)
    direction = velocities / np.hypot(velocities[:, 0], velocities[:, 1])[:, None]
    return dict(
        path=path,
        angle=angle,
        final_angle=angle[:, -1].astype(float),
        exit_index=exit_index,
        direction=direction,
    )


def schedule(scene, launch_per_frame, rng):
    launch_frame = np.arange(PARTICLES) // launch_per_frame
    scene["launch_per_frame"] = launch_per_frame
    scene["launch_time"] = (launch_frame + rng.uniform(0.0, 1.0, PARTICLES)) * FRAME_DT
    scene["detect_time"] = scene["launch_time"] + scene["exit_index"] * SAMPLE_DT
    scene["frames"] = int(np.ceil(scene["detect_time"].max() / FRAME_DT)) + 2
    scene["flight_frames"] = int(np.ceil(scene["exit_index"].max() * SAMPLE_DT / FRAME_DT)) + 2
    depth = SCREEN_RADIUS + 0.06 + 0.3 * rng.uniform(0.0, 1.0, PARTICLES)
    scene["hit_points"] = scene["direction"] * depth[:, None]
    scene["flash_points"] = scene["direction"] * SCREEN_RADIUS
    return scene


def rutherford_per_solid_angle(theta_degrees, detected):
    half = np.radians(theta_degrees) / 2.0
    return detected * (HALF_APPROACH / 2.0) ** 2 / (np.pi * BEAM_RADIUS**2 * np.sin(half) ** 4)


def solid_angles(edges):
    return 2.0 * np.pi * (np.cos(np.radians(edges[:-1])) - np.cos(np.radians(edges[1:])))


def per_solid_angle(angles, edges):
    counts = np.histogram(angles, bins=edges)[0].astype(float)
    return np.where(counts > 0, counts / solid_angles(edges), np.nan)


def band_of(angle):
    if angle > 90.0:
        return 2
    if angle > BEND_THRESHOLD:
        return 1
    return 0


def pudding_impulse_angle(impact):
    inside = 1.0 - (1.0 - (impact / PUDDING_RADIUS) ** 2) ** 1.5
    return np.degrees(2.0 * HALF_APPROACH / impact * inside)


def build(output_dir, fps, hold_seconds):
    rng = np.random.default_rng(5)
    impact = BEAM_RADIUS * np.sqrt(rng.uniform(0.0, 1.0, PARTICLES))
    side = rng.choice([-1.0, 1.0], PARTICLES)
    nuclear = schedule(simulate(impact, side, 0.0), 20, rng)
    pudding = schedule(simulate(impact, side, PUDDING_RADIUS), 40, rng)

    nuclear_error = float(np.max(np.abs(nuclear["final_angle"] - np.degrees(2.0 * np.arctan2(HALF_APPROACH, impact)))))
    pudding_error = float(np.max(np.abs(pudding["final_angle"] - pudding_impulse_angle(impact))))
    pudding_largest = float(pudding["final_angle"].max())

    nuclear_centres = 0.5 * (NUCLEAR_BINS[:-1] + NUCLEAR_BINS[1:])
    pudding_centres = 0.5 * (PUDDING_BINS[:-1] + PUDDING_BINS[1:])
    pudding_final = per_solid_angle(pudding["final_angle"], PUDDING_BINS)
    fine = np.linspace(9.0, 180.0, 300)

    fig = plt.figure(figsize=(6.0, 8.0), dpi=100)
    fig.patch.set_facecolor(PAPER)
    box_axes = fig.add_axes([0.12, 0.385, 0.76, 0.57])
    plot_axes = fig.add_axes([0.14, 0.115, 0.72, 0.195])

    box_axes.set_xlim(-VIEW, VIEW)
    box_axes.set_ylim(-VIEW, VIEW)
    box_axes.set_aspect("equal")
    box_axes.set_xticks([])
    box_axes.set_yticks([])
    for spine in box_axes.spines.values():
        spine.set_linewidth(1.4)

    cloud = plt.Circle((0.0, 0.0), PUDDING_RADIUS, facecolor="#e4e4e4", edgecolor=INK, lw=0.9, ls=(0, (4, 3)), zorder=1)
    box_axes.add_patch(cloud)
    kept = LineCollection([], colors=INK, linewidths=1.3, alpha=0.85, zorder=2)
    layers = [
        LineCollection([], colors="#8a8a8a", linewidths=0.5, zorder=3),
        LineCollection([], colors="#4a4a4a", linewidths=1.0, zorder=4),
        LineCollection([], colors=INK, linewidths=2.2, zorder=5, capstyle="round"),
    ]
    for collection in [kept] + layers:
        box_axes.add_collection(collection)
    nucleus = plt.Circle((0.0, 0.0), 0.09, color=INK, lw=0, zorder=6)
    box_axes.add_patch(nucleus)
    label_box = dict(facecolor=PAPER, edgecolor="none", alpha=0.9, pad=2.0)
    centre_label = box_axes.text(0.0, -0.45, "", fontsize=10, ha="center", va="top", bbox=label_box, zorder=7)
    beam_arrow = box_axes.annotate(
        "",
        xy=(-3.3, 4.4),
        xytext=(-4.7, 4.4),
        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0),
        zorder=7,
    )
    beam_text = box_axes.text(-3.1, 4.4, r"$\alpha$ beam", fontsize=10, ha="left", va="center", bbox=label_box, zorder=7)
    fired_label = box_axes.text(-4.7, -4.5, "", fontsize=10, ha="left", va="center", bbox=label_box, zorder=7)
    screen_arc = Arc(
        (0.0, 0.0),
        2.0 * SCREEN_RADIUS,
        2.0 * SCREEN_RADIUS,
        theta1=-180.0 + SCREEN_GAP_DEGREES,
        theta2=180.0 - SCREEN_GAP_DEGREES,
        color=INK,
        lw=1.1,
        zorder=6,
    )
    box_axes.add_patch(screen_arc)
    screen_label = box_axes.text(4.8, -4.72, "ZnS screen (not to scale)", fontsize=9, ha="right", va="center", bbox=label_box, zorder=7)
    beam_edge = float(np.degrees(2.0 * np.arctan2(HALF_APPROACH, BEAM_RADIUS)))
    direct_beam = Arc(
        (0.0, 0.0),
        2.0 * SCREEN_RADIUS + 0.42,
        2.0 * SCREEN_RADIUS + 0.42,
        theta1=-beam_edge,
        theta2=beam_edge,
        color="#c4c4c4",
        lw=7.0,
        zorder=5,
    )
    box_axes.add_patch(direct_beam)
    direct_label = box_axes.text(4.3, 0.0, "direct beam", fontsize=9, ha="right", va="center", bbox=label_box, zorder=7)
    hits = box_axes.scatter([], [], s=1.6, color=INK, alpha=0.55, linewidths=0, zorder=6)
    flashes = box_axes.scatter([], [], s=26.0, facecolors=PAPER, edgecolors=INK, linewidths=0.9, zorder=8)

    model_label = fig.text(0.12, 0.968, "", fontsize=13, ha="left", va="center")
    key_label = fig.text(0.88, 0.968, "", fontsize=11, ha="right", va="center")
    setup_note = fig.text(0.88, 0.366, "", fontsize=10, ha="right", va="center")
    panel_label = fig.text(0.14, 0.336, "", fontsize=13, ha="left", va="center")
    chart_key = fig.text(0.86, 0.336, "", fontsize=10, ha="right", va="center")
    footer = fig.text(0.5, 0.032, "", fontsize=14, ha="center", va="center")

    plot_axes.set_xlim(0.0, 180.0)
    plot_axes.set_ylim(0.1, 3.0e6)
    plot_axes.set_yscale("log")
    plot_axes.set_xticks(np.arange(0, 181, 30))
    plot_axes.set_yticks([1.0, 1.0e2, 1.0e4, 1.0e6])
    plot_axes.set_xlabel(r"scattering angle $\theta$ (degrees)", fontsize=11)
    plot_axes.set_ylabel(r"$dN/d\Omega$", fontsize=11)
    plot_axes.tick_params(labelsize=9, direction="in", which="both")
    (theory_line,) = plot_axes.plot([], [], color=INK, lw=1.0, ls=(0, (5, 3)))
    (nuclear_points,) = plot_axes.plot([], [], ls="none", marker="o", ms=5.0, mfc=PAPER, mec=INK, mew=1.3)
    (pudding_points,) = plot_axes.plot([], [], ls="none", marker="s", ms=5.0, mfc=INK, mec=INK, zorder=5)
    first_note = plot_axes.text(0.97, 0.92, "", transform=plot_axes.transAxes, fontsize=11, ha="right", va="top")
    second_note = plot_axes.text(0.97, 0.76, "", transform=plot_axes.transAxes, fontsize=11, ha="right", va="top")
    empty_span = plot_axes.annotate(
        "",
        xy=(178.0, 0.17),
        xytext=(12.0, 0.17),
        arrowprops=dict(arrowstyle="|-|", color=INK, lw=1.0, mutation_scale=3.0),
    )
    empty_text = plot_axes.text(95.0, 0.55, "plum pudding predicts no counts here", fontsize=10, ha="center", va="center")

    intro_nucleus = plt.Circle((0.0, 0.0), NUCLEUS_METRES, color=INK, lw=0, zorder=4)
    intro_atom = plt.Circle((0.0, 0.0), ATOM_METRES, facecolor="none", edgecolor=INK, lw=1.0, ls=(0, (4, 3)), zorder=3)
    intro_screen = Arc(
        (0.0, 0.0),
        2.0 * SCREEN_METRES,
        2.0 * SCREEN_METRES,
        theta1=-180.0 + SCREEN_GAP_DEGREES,
        theta2=180.0 - SCREEN_GAP_DEGREES,
        color=INK,
        lw=1.1,
        zorder=3,
    )
    for patch in (intro_nucleus, intro_atom, intro_screen):
        box_axes.add_patch(patch)
    (intro_dot,) = box_axes.plot([0.0], [0.0], marker="o", ms=2.2, color=INK, ls="none", zorder=5)
    intro_tags = [
        (box_axes.text(0.0, 0.0, "nucleus", fontsize=11, ha="center", va="bottom", zorder=7), NUCLEUS_METRES),
        (box_axes.text(0.0, 0.0, "atom", fontsize=11, ha="center", va="bottom", zorder=7), ATOM_METRES),
        (box_axes.text(0.0, 0.0, "ZnS screen", fontsize=11, ha="center", va="bottom", zorder=7), SCREEN_METRES),
    ]
    unseen_note = box_axes.text(
        0.5, 0.455, "nucleus (far too small to see)", transform=box_axes.transAxes, fontsize=10, ha="center", va="top"
    )
    view_note = box_axes.text(0.03, 0.955, "", transform=box_axes.transAxes, fontsize=11, ha="left", va="center")
    intro_caption = box_axes.text(0.5, 0.06, "", transform=box_axes.transAxes, fontsize=12, ha="center", va="center")

    ruler_axes = fig.add_axes([0.14, 0.115, 0.72, 0.195])
    ruler_axes.set_xscale("log")
    ruler_axes.set_xlim(1.0e-15, 1.0)
    ruler_axes.set_ylim(0.0, 1.15)
    ruler_axes.set_yticks([])
    ruler_axes.set_xticks([10.0**k for k in range(-15, 1, 3)])
    ruler_axes.set_xticks([10.0**k for k in range(-15, 1)], minor=True)
    ruler_axes.set_xticklabels([], minor=True)
    ruler_axes.set_xlabel("length (m)", fontsize=11)
    ruler_axes.tick_params(labelsize=9, direction="in", which="both")
    for length, name in ((1.4e-14, "nucleus"), (2.8e-10, "atom"), (SCREEN_METRES, "screen distance")):
        ruler_axes.plot([length, length], [0.0, 0.42], color=INK, lw=1.4)
        ruler_axes.text(length, 0.47, name, fontsize=10, ha="center", va="bottom")
    (ruler_marker,) = ruler_axes.plot([], [], marker="v", ms=8.0, color=INK, ls="none")
    ruler_marker_label = ruler_axes.text(1.0, 0.98, "view", fontsize=10, ha="center", va="bottom")

    main_artists = [kept, centre_label, beam_arrow, beam_text, fired_label, screen_arc, screen_label, hits, flashes]
    main_artists += layers
    intro_artists = [intro_nucleus, intro_dot, unseen_note, view_note, intro_caption]

    def set_mode(intro):
        for artist in main_artists:
            artist.set_visible(not intro)
        for artist in intro_artists:
            artist.set_visible(intro)
        plot_axes.set_visible(not intro)
        ruler_axes.set_visible(intro)
        if intro:
            for artist in (cloud, nucleus, direct_beam, direct_label):
                artist.set_visible(False)
        else:
            for artist in (intro_atom, intro_screen):
                artist.set_visible(False)
            for tag, _ in intro_tags:
                tag.set_visible(False)
            box_axes.set_xlim(-VIEW, VIEW)
            box_axes.set_ylim(-VIEW, VIEW)
            panel_label.set_text(r"(b) $dN/d\Omega$")
            setup_note.set_text(rf"schematic, distances not to scale; $N = {PARTICLES}$, same beam for both models")

    def draw_intro(frame):
        set_mode(True)
        exponent = zoom_exponent(frame)
        half_width = 10.0**exponent
        box_axes.set_xlim(-half_width, half_width)
        box_axes.set_ylim(-half_width, half_width)
        intro_atom.set_visible(half_width > ATOM_METRES / 40.0)
        intro_screen.set_visible(half_width > SCREEN_METRES / 40.0)
        for tag, radius in intro_tags:
            tag.set_visible(0.12 * half_width < radius < 0.9 * half_width)
            tag.set_position((0.0, radius + 0.03 * half_width))
        unseen_note.set_visible(NUCLEUS_METRES < 0.01 * half_width)
        view_note.set_text(rf"view width $\approx 10^{{{int(round(np.log10(2.0 * half_width)))}}}$ m")
        if exponent < -12.5:
            intro_caption.set_text(r"gold nucleus: about $10^{-14}$ m across")
        elif exponent < -6.0:
            intro_caption.set_text(r"atom: about $10^{-10}$ m, ten thousand times wider")
        else:
            intro_caption.set_text(r"screen: centimetres away, $10^{12}$ nuclear widths")
        ruler_marker.set_data([2.0 * half_width], [0.9])
        ruler_marker_label.set_position((2.0 * half_width, 0.98))
        model_label.set_text("(a) real proportions")
        key_label.set_text("zooming out from the nucleus")
        setup_note.set_text("drawn to scale")
        panel_label.set_text("(b) length scale")
        chart_key.set_text("each small tick is a factor of ten")
        footer.set_text("the panels that follow are schematic: distances not to scale")
        footer.set_fontsize(12)

    def trails(scene, local_frame, now):
        first = max(0, (local_frame - scene["flight_frames"]) * scene["launch_per_frame"])
        last = min(PARTICLES, (local_frame + 1) * scene["launch_per_frame"])
        segments = [[], [], []]
        for index in range(first, last):
            sample = int((now - scene["launch_time"][index]) / SAMPLE_DT)
            if sample < 1 or sample >= scene["exit_index"][index]:
                continue
            band = band_of(scene["angle"][index, sample])
            begin = 0 if band == 2 else max(0, sample - TRAIL_SAMPLES[band])
            segments[band].append(scene["path"][index, begin : sample + 1])
        for collection, lines in zip(layers, segments):
            collection.set_segments(lines)
        return last

    def show_hits(scene, done, now):
        fresh = done & (now - scene["detect_time"] < 3.0 * FRAME_DT)
        hits.set_offsets(scene["hit_points"][done])
        flashes.set_offsets(scene["flash_points"][fresh])

    def draw_pudding(local_frame):
        scene = pudding
        now = (local_frame + 1) * FRAME_DT
        fired = trails(scene, local_frame, now)
        kept.set_segments([])
        done = scene["detect_time"] <= now
        show_hits(scene, done, now)
        detected = int(done.sum())
        largest = float(scene["final_angle"][done].max()) if detected else 0.0

        cloud.set_visible(True)
        nucleus.set_visible(False)
        direct_beam.set_visible(False)
        direct_label.set_visible(False)
        centre_label.set_text("positive charge spread over the atom")
        centre_label.set_position((0.0, -PUDDING_RADIUS - 0.2))
        model_label.set_text("(a) plum pudding atom")
        key_label.set_text("prediction before 1909")
        chart_key.set_text("squares: plum pudding prediction")
        footer.set_text(r"spread-out charge cannot turn an $\alpha$ particle around")
        footer.set_fontsize(12)
        fired_label.set_text(rf"fired: ${fired}$")

        nuclear_points.set_data([], [])
        theory_line.set_data([], [])
        pudding_points.set_data(pudding_centres, per_solid_angle(scene["final_angle"][done], PUDDING_BINS))
        pudding_points.set_markerfacecolor(INK)
        pudding_points.set_markeredgecolor(INK)
        empty_span.set_visible(True)
        empty_text.set_visible(True)
        first_note.set_text(rf"detected: ${detected}$")
        second_note.set_text(rf"largest angle: ${largest:.1f}^\circ$,  beyond $90^\circ$: $0$")

    def draw_nuclear(local_frame):
        scene = nuclear
        now = (local_frame + 1) * FRAME_DT
        fired = trails(scene, local_frame, now)
        done = scene["detect_time"] <= now
        show_hits(scene, done, now)
        back = np.flatnonzero(done & (scene["final_angle"] > 90.0))
        kept.set_segments([scene["path"][index, : scene["exit_index"][index] + 1] for index in back])
        detected = int(done.sum())

        cloud.set_visible(False)
        nucleus.set_visible(True)
        direct_beam.set_visible(True)
        direct_label.set_visible(True)
        centre_label.set_text("nucleus")
        centre_label.set_position((0.0, -0.45))
        model_label.set_text("(a) nuclear atom")
        key_label.set_text(r"thick: deflected beyond $90^\circ$")
        chart_key.set_text("grey: plum pudding, circles: nuclear, dashed: theory")
        footer.set_text(r"$\dfrac{dN}{d\Omega}\;\propto\;\dfrac{1}{\sin^{4}(\theta/2)}$")
        footer.set_fontsize(14)
        fired_label.set_text(rf"fired: ${fired}$")

        pudding_points.set_data(pudding_centres, pudding_final)
        pudding_points.set_markerfacecolor(GHOST)
        pudding_points.set_markeredgecolor(GHOST)
        nuclear_points.set_data(nuclear_centres, per_solid_angle(scene["final_angle"][done], NUCLEAR_BINS))
        if detected:
            theory_line.set_data(fine, rutherford_per_solid_angle(fine, detected))
        else:
            theory_line.set_data([], [])
        empty_span.set_visible(False)
        empty_text.set_visible(False)
        first_note.set_text(rf"nuclear atom, detected: ${detected}$")
        second_note.set_text(rf"beyond $90^\circ$: ${int((scene['final_angle'][done] > 90.0).sum())}$")

    nuclear_start = INTRO_FRAMES + pudding["frames"] + INTERLUDE_FRAMES
    total_frames = nuclear_start + nuclear["frames"]

    def draw(frame):
        frame = min(frame, total_frames - 1)
        if frame < INTRO_FRAMES:
            draw_intro(frame)
        elif frame < nuclear_start:
            set_mode(False)
            draw_pudding(min(frame - INTRO_FRAMES, pudding["frames"] - 1))
        else:
            set_mode(False)
            draw_nuclear(frame - nuclear_start)
        return layers

    hold_frames = int(hold_seconds * fps)
    animation = FuncAnimation(fig, draw, frames=total_frames + hold_frames, blit=False)
    output_dir.mkdir(parents=True, exist_ok=True)
    video_path = output_dir / "rutherford_paper.mp4"
    animation.save(video_path, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-crf", "18"]))
    gif_path = output_dir / "rutherford_paper.gif"
    palette = "fps=10,scale=450:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=16[p];[b][p]paletteuse=dither=none"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_path), "-filter_complex", palette, str(gif_path)],
        check=True,
    )
    stills = []
    for name, frame in [
        ("intro_nucleus", 5),
        ("intro_atom", 50),
        ("intro_screen", INTRO_FRAMES - 2),
        ("pudding_final", INTRO_FRAMES + pudding["frames"] - 1),
        ("nuclear_mid", nuclear_start + nuclear["frames"] // 2),
        ("nuclear_final", total_frames - 1),
    ]:
        draw(frame)
        still = output_dir / f"rutherford_paper_{name}.png"
        fig.savefig(still, facecolor=PAPER)
        stills.append(still)
    plt.close(fig)

    report = dict(
        nuclear_error=nuclear_error,
        nuclear_back=int((nuclear["final_angle"] > 90.0).sum()),
        expected_back=PARTICLES * (HALF_APPROACH / BEAM_RADIUS) ** 2,
        pudding_largest=pudding_largest,
        pudding_error=pudding_error,
        pudding_back=int((pudding["final_angle"] > 90.0).sum()),
        seconds=(total_frames + hold_frames) / fps,
    )
    return video_path, gif_path, stills, report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "out")
    parser.add_argument("--fps", type=int, default=20)
    parser.add_argument("--hold", type=float, default=3.0)
    arguments = parser.parse_args()
    video_path, gif_path, stills, report = build(arguments.out, arguments.fps, arguments.hold)
    print(f"mp4={video_path} size={video_path.stat().st_size / 1e6:.2f}MB length={report['seconds']:.1f}s")
    print(f"gif={gif_path} size={gif_path.stat().st_size / 1e6:.2f}MB")
    print(f"nuclear: max angle error {report['nuclear_error']:.2f} deg, beyond 90: {report['nuclear_back']} (expected {report['expected_back']:.1f})")
    print(
        f"pudding: largest angle {report['pudding_largest']:.2f} deg, beyond 90: {report['pudding_back']}, "
        f"max difference from impulse approximation {report['pudding_error']:.2f} deg"
    )


if __name__ == "__main__":
    main()
