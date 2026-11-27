import argparse
import subprocess
from collections import deque
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.collections import EllipseCollection

INK = "#111111"
PAPER = "#ffffff"

SIDE_COUNT = 14
PARTICLES = SIDE_COUNT * SIDE_COUNT
DENSITY = 0.5
BOX = float(np.sqrt(PARTICLES / DENSITY))
CUTOFF_SQUARED = 2.0 ** (1.0 / 3.0)
STEP = 0.004
STEPS_PER_FRAME = 10
RELAX_FRAMES = 150
HEATED_FRAMES = 90
HEATING_FACTOR = 2.0
SPEED_MAX = 5.0
BIN_COUNT = 34
SHADE_SPEED = 3.4
WINDOW = 8

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


def forces(positions):
    delta = positions[:, None, :] - positions[None, :, :]
    delta -= BOX * np.round(delta / BOX)
    distance_squared = np.einsum("ijk,ijk->ij", delta, delta)
    np.fill_diagonal(distance_squared, np.inf)
    inverse = np.where(distance_squared < CUTOFF_SQUARED, 1.0 / distance_squared, 0.0)
    inverse_six = inverse**3
    magnitude = 24.0 * (2.0 * inverse_six**2 - inverse_six) * inverse
    potential = np.where(inverse > 0.0, 4.0 * (inverse_six**2 - inverse_six) + 1.0, 0.0)
    return np.einsum("ij,ijk->ik", magnitude, delta), 0.5 * float(potential.sum())


def initial_state(rng):
    spacing = BOX / SIDE_COUNT
    grid = (np.arange(SIDE_COUNT) + 0.5) * spacing
    positions = np.array([[x, y] for x in grid for y in grid])
    directions = rng.uniform(0.0, 2.0 * np.pi, PARTICLES)
    velocities = np.sqrt(2.0) * np.column_stack([np.cos(directions), np.sin(directions)])
    velocities -= velocities.mean(axis=0)
    return positions, velocities


def simulate():
    rng = np.random.default_rng(11)
    positions, velocities = initial_state(rng)
    force, potential = forces(positions)
    frames = []
    energies = []
    total_frames = RELAX_FRAMES + HEATED_FRAMES
    for frame in range(total_frames):
        if frame == RELAX_FRAMES:
            velocities = velocities * np.sqrt(HEATING_FACTOR)
        kinetic = 0.5 * float((velocities**2).sum())
        frames.append((positions % BOX, np.hypot(velocities[:, 0], velocities[:, 1]), kinetic / PARTICLES))
        energies.append(kinetic + potential)
        for _ in range(STEPS_PER_FRAME):
            velocities = velocities + 0.5 * STEP * force
            positions = positions + STEP * velocities
            force, potential = forces(positions)
            velocities = velocities + 0.5 * STEP * force
    return frames, np.array(energies)


def maxwell_boltzmann_2d(speed, temperature):
    return speed / temperature * np.exp(-(speed**2) / (2.0 * temperature))


def stage_text(frame):
    if frame < 6:
        return "every particle starts at the same speed"
    if frame < RELAX_FRAMES:
        return "collisions redistribute the energy"
    return r"heated: kinetic energy $\times\,2$"


def checks(frames, energies):
    relaxed = frames[RELAX_FRAMES // 2 : RELAX_FRAMES]
    mean_speed = float(np.mean([speeds.mean() for _, speeds, _ in relaxed]))
    temperature = float(np.mean([t for _, _, t in relaxed]))
    expected = float(np.sqrt(np.pi * temperature / 2.0))
    first = energies[:RELAX_FRAMES]
    second = energies[RELAX_FRAMES:]
    drift = max(
        float(np.ptp(first) / abs(first.mean())),
        float(np.ptp(second) / abs(second.mean())),
    )
    return mean_speed, expected, temperature, drift


def build(output_dir, fps, hold_seconds):
    frames, energies = simulate()
    mean_speed, expected, temperature, drift = checks(frames, energies)

    edges = np.linspace(0.0, SPEED_MAX, BIN_COUNT + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    fine = np.linspace(0.0, SPEED_MAX, 300)
    histograms = [np.histogram(speeds, bins=edges, density=True)[0] for _, speeds, _ in frames]

    fig = plt.figure(figsize=(6.0, 8.0), dpi=100)
    fig.patch.set_facecolor(PAPER)
    box_axes = fig.add_axes([0.12, 0.385, 0.76, 0.57])
    plot_axes = fig.add_axes([0.14, 0.115, 0.72, 0.195])

    box_axes.set_xlim(0.0, BOX)
    box_axes.set_ylim(0.0, BOX)
    box_axes.set_aspect("equal")
    box_axes.set_xticks([])
    box_axes.set_yticks([])
    for spine in box_axes.spines.values():
        spine.set_linewidth(1.4)

    shifts = np.array([[dx, dy] for dx in (-BOX, 0.0, BOX) for dy in (-BOX, 0.0, BOX)])
    image_count = len(shifts)
    diameters = np.ones(PARTICLES * image_count)
    disks = EllipseCollection(
        diameters,
        diameters,
        np.zeros_like(diameters),
        units="x",
        offsets=np.zeros((PARTICLES * image_count, 2)),
        offset_transform=box_axes.transData,
        edgecolors=INK,
        linewidths=0.7,
    )
    box_axes.add_collection(disks)

    fig.text(0.12, 0.968, "(a)", fontsize=13, ha="left", va="center")
    clock = fig.text(0.2, 0.968, "", fontsize=11, ha="left", va="center")
    fig.text(0.88, 0.968, "dark: high speed", fontsize=11, ha="right", va="center")
    fig.text(
        0.88,
        0.366,
        rf"periodic box, $N = {PARTICLES}$, $\rho\sigma^2 = {DENSITY:.2f}$",
        fontsize=10,
        ha="right",
        va="center",
    )
    fig.text(0.14, 0.336, r"(b) $P(v)$", fontsize=13, ha="left", va="center")
    fig.text(
        0.86,
        0.336,
        "dashed: Maxwell-Boltzmann, solid: simulation",
        fontsize=10,
        ha="right",
        va="center",
    )
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
    plot_axes.set_ylim(0.0, 0.9)
    plot_axes.set_xlabel(r"$v\,/\,(\varepsilon/m)^{1/2}$", fontsize=11)
    plot_axes.set_ylabel(r"$P(v)$", fontsize=11)
    plot_axes.tick_params(labelsize=9, direction="in")
    (theory_line,) = plot_axes.plot([], [], color=INK, lw=1.0, ls=(0, (5, 3)))
    (measured_line,) = plot_axes.plot([], [], color=INK, lw=1.8, drawstyle="steps-mid")
    stage = plot_axes.text(0.97, 0.9, "", transform=plot_axes.transAxes, fontsize=11, ha="right", va="top")
    thermometer = plot_axes.text(0.97, 0.72, "", transform=plot_axes.transAxes, fontsize=11, ha="right", va="top")

    recent = deque(maxlen=WINDOW)
    state = {"last": -1}

    def draw(frame):
        frame = min(frame, len(frames) - 1)
        if frame != state["last"] + 1 or frame == RELAX_FRAMES:
            recent.clear()
            start = RELAX_FRAMES if frame >= RELAX_FRAMES else 0
            for earlier in range(max(start, frame - WINDOW + 1), frame):
                recent.append(histograms[earlier])
        recent.append(histograms[frame])
        state["last"] = frame

        positions, speeds, current_temperature = frames[frame]
        offsets = (positions[None, :, :] + shifts[:, None, :]).reshape(-1, 2)
        shade = 1.0 - np.clip(speeds / SHADE_SPEED, 0.0, 1.0)
        disks.set_offsets(offsets)
        disks.set_facecolors(np.tile(np.repeat(shade[:, None], 3, axis=1), (image_count, 1)))

        measured_line.set_data(centres, np.mean(recent, axis=0))
        theory_line.set_data(fine, maxwell_boltzmann_2d(fine, current_temperature))
        clock.set_text(rf"$t = {frame * STEPS_PER_FRAME * STEP:.2f}$")
        stage.set_text(stage_text(frame))
        thermometer.set_text(rf"$k_{{\mathrm{{B}}}}T/\varepsilon = {current_temperature:.2f}$")
        return disks, measured_line, theory_line, clock, stage, thermometer

    hold_frames = int(hold_seconds * fps)
    animation = FuncAnimation(fig, draw, frames=len(frames) + hold_frames, blit=False)
    output_dir.mkdir(parents=True, exist_ok=True)
    video_path = output_dir / "maxwell_boltzmann.mp4"
    animation.save(video_path, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-crf", "18"]))
    gif_path = output_dir / "maxwell_boltzmann.gif"
    palette = "fps=12,scale=450:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=16[p];[b][p]paletteuse=dither=none"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_path), "-filter_complex", palette, str(gif_path)],
        check=True,
    )
    stills = {}
    for name, frame in [("start", 0), ("relaxed", RELAX_FRAMES - 1), ("heated", len(frames) - 1)]:
        draw(frame)
        stills[name] = output_dir / f"maxwell_boltzmann_{name}.png"
        fig.savefig(stills[name], facecolor=PAPER)
    plt.close(fig)
    return video_path, gif_path, stills, mean_speed, expected, temperature, drift


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "out")
    parser.add_argument("--fps", type=int, default=20)
    parser.add_argument("--hold", type=float, default=2.0)
    arguments = parser.parse_args()
    video_path, gif_path, stills, mean_speed, expected, temperature, drift = build(arguments.out, arguments.fps, arguments.hold)
    print(f"mp4={video_path} size={video_path.stat().st_size / 1e6:.2f}MB")
    print(f"gif={gif_path} size={gif_path.stat().st_size / 1e6:.2f}MB")
    print(f"relaxed kT={temperature:.3f} mean speed={mean_speed:.3f} analytic sqrt(pi kT/2m)={expected:.3f}")
    print(f"relative total-energy spread within each phase <= {drift:.2e}")


if __name__ == "__main__":
    main()
