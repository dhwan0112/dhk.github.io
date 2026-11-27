"""Export the Maxwell-Boltzmann runs as small JSON files for the in-browser SVG players.

Physics, seeds and parameters come from maxwell_boltzmann.py and mb_convergence.py
in the same folder. Positions and speeds are stored as 16-bit integers
(positions as a fraction of the box, speeds as a fraction of SPEED_SCALE).

    python export_web_data.py --out data
"""

import argparse
import base64
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import maxwell_boltzmann as mb  # noqa: E402
import mb_convergence as conv  # noqa: E402

SPEED_SCALE = 8.0


def pack_uint16(values):
    data = np.ascontiguousarray(np.clip(np.rint(values), 0, 65535).astype("<u2"))
    return base64.b64encode(data.tobytes()).decode("ascii")


def rounded(values, digits):
    return [round(float(v), digits) for v in np.asarray(values).ravel()]


def export_maxwell_boltzmann(out):
    frames, energies = mb.simulate()
    mean_speed, expected, temperature, drift = mb.checks(frames, energies)
    positions = np.stack([p for p, _, _ in frames]) / mb.BOX * 65535.0
    speeds = np.stack([s for _, s, _ in frames]) / SPEED_SCALE * 65535.0
    payload = dict(
        particles=mb.PARTICLES,
        density=mb.DENSITY,
        box=mb.BOX,
        step=mb.STEP,
        stepsPerFrame=mb.STEPS_PER_FRAME,
        relaxFrames=mb.RELAX_FRAMES,
        heatedFrames=mb.HEATED_FRAMES,
        speedMax=mb.SPEED_MAX,
        binCount=mb.BIN_COUNT,
        shadeSpeed=mb.SHADE_SPEED,
        window=mb.WINDOW,
        speedScale=SPEED_SCALE,
        frames=len(frames),
        temperature=rounded([t for _, _, t in frames], 4),
        positions=pack_uint16(positions),
        speeds=pack_uint16(speeds),
        report=dict(meanSpeed=mean_speed, expected=expected, temperature=temperature, drift=drift),
    )
    (out / "maxwell_boltzmann.json").write_text(json.dumps(payload, separators=(",", ":")))
    return payload["report"]


def export_convergence(out):
    rng = np.random.default_rng(23)
    stages = [conv.run_stage(side_count, rng) for side_count in conv.SIDE_COUNTS]
    edges = np.linspace(0.0, conv.SPEED_MAX, conv.BIN_COUNT + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    compared = centres < conv.COMPARE_UP_TO
    exported = []
    for stage in stages:
        theory = mb.maxwell_boltzmann_2d(centres, stage["temperature"])
        histograms = [np.histogram(s, bins=edges, density=True)[0] for _, s in stage["snapshots"]]
        deviations = [float(np.sqrt(np.mean((h[compared] - theory[compared]) ** 2))) for h in histograms]
        running = np.cumsum(deviations) / (np.arange(len(deviations)) + 1)
        positions = np.stack([p for p, _ in stage["snapshots"]]) / stage["box"] * 65535.0
        speeds = np.stack([s for _, s in stage["snapshots"]]) / SPEED_SCALE * 65535.0
        exported.append(
            dict(
                count=stage["count"],
                box=stage["box"],
                temperature=stage["temperature"],
                runningDeviation=rounded(running, 4),
                positions=pack_uint16(positions),
                speeds=pack_uint16(speeds),
            )
        )
    payload = dict(
        density=conv.DENSITY,
        framesPerStage=conv.FRAMES_PER_STAGE,
        speedMax=conv.SPEED_MAX,
        binCount=conv.BIN_COUNT,
        shadeSpeed=conv.SHADE_SPEED,
        speedScale=SPEED_SCALE,
        stages=exported,
    )
    (out / "mb_convergence.json").write_text(json.dumps(payload, separators=(",", ":")))
    return [(s["count"], s["temperature"], s["runningDeviation"][-1]) for s in exported]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "data")
    arguments = parser.parse_args()
    arguments.out.mkdir(parents=True, exist_ok=True)
    m = export_maxwell_boltzmann(arguments.out)
    print(
        f"relaxed kT={m['temperature']:.3f} mean speed={m['meanSpeed']:.3f} "
        f"sqrt(pi kT/2m)={m['expected']:.3f} energy spread <= {m['drift']:.2e}"
    )
    for count, temperature, deviation in export_convergence(arguments.out):
        print(f"N={count:5d} kT={temperature:.3f} rms deviation={deviation:.4f}")


if __name__ == "__main__":
    main()
