import argparse
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.collections import EllipseCollection

import maxwell_boltzmann as base

SIDE_COUNTS = (5, 10, 20, 40)
DENSITY = 0.5
TARGET_TEMPERATURE = 1.0
STEP = 0.004
STEPS_PER_FRAME = 10
EQUILIBRATION_STEPS = 400
FRAMES_PER_STAGE = 55
SPEED_MAX = 5.0
BIN_COUNT = 34
SHADE_SPEED = 3.4
COMPARE_UP_TO = 4.0


def forces(positions, box):
    delta = positions[:, None, :] - positions[None, :, :]
    delta -= box * np.round(delta / box)
    distance_squared = np.einsum("ijk,ijk->ij", delta, delta)
    np.fill_diagonal(distance_squared, np.inf)
    inverse = np.where(distance_squared < base.CUTOFF_SQUARED, 1.0 / distance_squared, 0.0)
    inverse_six = inverse**3
    magnitude = 24.0 * (2.0 * inverse_six**2 - inverse_six) * inverse
    return np.einsum("ij,ijk->ik", magnitude, delta)


def advance(positions, velocities, force, box, steps):
    for _ in range(steps):
        velocities = velocities + 0.5 * STEP * force
        positions = positions + STEP * velocities
        force = forces(positions, box)
        velocities = velocities + 0.5 * STEP * force
    return positions, velocities, force


def run_stage(side_count, rng):
    count = side_count * side_count
    box = float(np.sqrt(count / DENSITY))
    grid = (np.arange(side_count) + 0.5) * box / side_count
    positions = np.array([[x, y] for x in grid for y in grid])
    velocities = rng.normal(0.0, np.sqrt(TARGET_TEMPERATURE), (count, 2))
    velocities -= velocities.mean(axis=0)
    force = forces(positions, box)
    positions, velocities, force = advance(positions, velocities, force, box, EQUILIBRATION_STEPS)
    snapshots = []
    for _ in range(FRAMES_PER_STAGE):
        speeds = np.hypot(velocities[:, 0], velocities[:, 1])
        snapshots.append((positions % box, speeds))
        positions, velocities, force = advance(positions, velocities, force, box, STEPS_PER_FRAME)
    temperature = float(np.mean([0.5 * np.mean(speeds**2) for _, speeds in snapshots]))
    return dict(count=count, box=box, snapshots=snapshots, temperature=temperature)


def with_edge_images(positions, box):
    pieces = [positions]
    for axis in (0, 1):
        for edge, shift in ((positions[:, axis] < 0.5, box), (positions[:, axis] > box - 0.5, -box)):
            moved = positions[edge].copy()
            moved[:, axis] += shift
            pieces.append(moved)
    return pieces


def build(output_dir, fps, hold_seconds):
    rng = np.random.default_rng(23)
    stages = [run_stage(side_count, rng) for side_count in SIDE_COUNTS]

    edges = np.linspace(0.0, SPEED_MAX, BIN_COUNT + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    compared = centres < COMPARE_UP_TO
    fine = np.linspace(0.0, SPEED_MAX, 300)
    for stage in stages:
        theory = base.maxwell_boltzmann_2d(centres, stage["temperature"])
        stage["histograms"] = [np.histogram(speeds, bins=edges, density=True)[0] for _, speeds in stage["snapshots"]]
        deviations = [float(np.sqrt(np.mean((h[compared] - theory[compared]) ** 2))) for h in stage["histograms"]]
        stage["running_deviation"] = np.cumsum(deviations) / (np.arange(len(deviations)) + 1)

    ink = base.INK
    fig = plt.figure(figsize=(6.0, 8.0), dpi=100)
    fig.patch.set_facecolor(base.PAPER)
    box_axes = fig.add_axes([0.12, 0.385, 0.76, 0.57])
    plot_axes = fig.add_axes([0.14, 0.115, 0.72, 0.195])
    box_axes.set_aspect("equal")
    box_axes.set_xticks([])
    box_axes.set_yticks([])
    for spine in box_axes.spines.values():
        spine.set_linewidth(1.4)

    disks = EllipseCollection(
        [1.0],
        [1.0],
        [0.0],
        units="x",
        offsets=np.zeros((1, 2)),
        offset_transform=box_axes.transData,
        edgecolors=ink,
        linewidths=0.7,
    )
    box_axes.add_collection(disks)

    fig.text(0.12, 0.968, "(a)", fontsize=13, ha="left", va="center")
    count_label = fig.text(0.2, 0.968, "", fontsize=12, ha="left", va="center")
    fig.text(0.88, 0.968, "dark: high speed", fontsize=11, ha="right", va="center")
    box_note = fig.text(0.88, 0.366, "", fontsize=10, ha="right", va="center")
    fig.text(0.14, 0.336, r"(b) $P(v)$", fontsize=13, ha="left", va="center")
    fig.text(0.86, 0.336, "dashed: Maxwell-Boltzmann, solid: one snapshot", fontsize=10, ha="right", va="center")
    fig.text(
        0.5,
        0.032,
        r"$P(v)=\dfrac{mv}{k_{\mathrm{B}}T}\,\exp\!\left(-\dfrac{mv^{2}}{2k_{\mathrm{B}}T}\right)$"
        r"$\qquad(\mathrm{two\ dimensions})$",
        fontsize=13,
        ha="center",
        va="center",
    )

    plot_axes.set_xlim(0.0, SPEED_MAX)
    plot_axes.set_ylim(0.0, 1.0)
    plot_axes.set_xlabel(r"$v\,/\,(\varepsilon/m)^{1/2}$", fontsize=11)
    plot_axes.set_ylabel(r"$P(v)$", fontsize=11)
    plot_axes.tick_params(labelsize=9, direction="in")
    (theory_line,) = plot_axes.plot([], [], color=ink, lw=1.0, ls=(0, (5, 3)))
    (measured_line,) = plot_axes.plot([], [], color=ink, lw=1.8, drawstyle="steps-mid")
    stage_label = plot_axes.text(0.97, 0.9, "", transform=plot_axes.transAxes, fontsize=13, ha="right", va="top")
    deviation_label = plot_axes.text(0.97, 0.7, "", transform=plot_axes.transAxes, fontsize=11, ha="right", va="top")

    total = len(stages) * FRAMES_PER_STAGE

    def draw(frame):
        frame = min(frame, total - 1)
        stage = stages[frame // FRAMES_PER_STAGE]
        local = frame % FRAMES_PER_STAGE
        positions, speeds = stage["snapshots"][local]
        box = stage["box"]
        box_axes.set_xlim(0.0, box)
        box_axes.set_ylim(0.0, box)

        shade = 1.0 - np.clip(speeds / SHADE_SPEED, 0.0, 1.0)
        pieces = with_edge_images(np.column_stack([positions, shade]), box)
        stacked = np.vstack(pieces)
        disks.set_offsets(stacked[:, :2])
        disks.set_facecolors(np.repeat(stacked[:, 2:3], 3, axis=1))
        disks.set_linewidths(0.7 if stage["count"] <= 400 else 0.3)

        measured_line.set_data(centres, stage["histograms"][local])
        theory_line.set_data(fine, base.maxwell_boltzmann_2d(fine, stage["temperature"]))
        count_label.set_text(rf"$N = {stage['count']}$")
        box_note.set_text(
            rf"periodic box, $\rho\sigma^2 = {DENSITY:.2f}$, "
            rf"$k_{{\mathrm{{B}}}}T/\varepsilon = {stage['temperature']:.2f}$"
        )
        stage_label.set_text(rf"$N = {stage['count']}$")
        deviation_label.set_text(rf"rms deviation $= {stage['running_deviation'][local]:.3f}$")
        return disks, measured_line, theory_line

    hold_frames = int(hold_seconds * fps)
    animation = FuncAnimation(fig, draw, frames=total + hold_frames, blit=False)
    output_dir.mkdir(parents=True, exist_ok=True)
    video_path = output_dir / "mb_convergence.mp4"
    animation.save(video_path, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-crf", "18"]))
    gif_path = output_dir / "mb_convergence.gif"
    palette = "fps=10,scale=450:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=16[p];[b][p]paletteuse=dither=none"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_path), "-filter_complex", palette, str(gif_path)],
        check=True,
    )
    stills = []
    for index in range(len(stages)):
        draw(index * FRAMES_PER_STAGE + FRAMES_PER_STAGE - 1)
        still = output_dir / f"mb_convergence_N{stages[index]['count']}.png"
        fig.savefig(still, facecolor=base.PAPER)
        stills.append(still)
    plt.close(fig)
    summary = [(stage["count"], stage["temperature"], float(stage["running_deviation"][-1])) for stage in stages]
    return video_path, gif_path, stills, summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "out")
    parser.add_argument("--fps", type=int, default=20)
    parser.add_argument("--hold", type=float, default=2.5)
    arguments = parser.parse_args()
    video_path, gif_path, stills, summary = build(arguments.out, arguments.fps, arguments.hold)
    print(f"mp4={video_path} size={video_path.stat().st_size / 1e6:.2f}MB")
    print(f"gif={gif_path} size={gif_path.stat().st_size / 1e6:.2f}MB")
    for count, temperature, deviation in summary:
        print(f"N={count:5d} kT={temperature:.3f} rms deviation={deviation:.4f} deviation*sqrt(N)={deviation * np.sqrt(count):.3f}")


if __name__ == "__main__":
    main()
