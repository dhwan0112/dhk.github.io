"""Export the Rutherford scattering run as a small JSON file for the in-browser SVG player.

Physics, seed and parameters come from rutherford_paper.py in the same folder, so
the printed checks are the ones that script reports. The browser integrates the
trajectories again from y0 with the same velocity Verlet step.

    python export_web_data.py --out data
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rutherford_paper as rp  # noqa: E402


def rounded(values, digits):
    return [round(float(v), digits) for v in np.asarray(values).ravel()]


def export_rutherford(out):
    rng = np.random.default_rng(5)
    impact = rp.BEAM_RADIUS * np.sqrt(rng.uniform(0.0, 1.0, rp.PARTICLES))
    side = rng.choice([-1.0, 1.0], rp.PARTICLES)
    nuclear = rp.schedule(rp.simulate(impact, side, 0.0), 20, rng)
    pudding = rp.schedule(rp.simulate(impact, side, rp.PUDDING_RADIUS), 40, rng)

    def scene(data, charge_radius):
        depth = np.hypot(data["hit_points"][:, 0], data["hit_points"][:, 1])
        return dict(
            chargeRadius=charge_radius,
            launchPerFrame=int(data["launch_per_frame"]),
            frames=int(data["frames"]),
            flightFrames=int(data["flight_frames"]),
            launch=rounded(data["launch_time"], 4),
            depth=rounded(depth, 3),
            exitIndex=[int(v) for v in data["exit_index"]],
            finalAngle=rounded(data["final_angle"], 3),
        )

    report = dict(
        nuclearError=float(np.max(np.abs(nuclear["final_angle"] - np.degrees(2.0 * np.arctan2(rp.HALF_APPROACH, impact))))),
        nuclearBack=int((nuclear["final_angle"] > 90.0).sum()),
        expectedBack=rp.PARTICLES * (rp.HALF_APPROACH / rp.BEAM_RADIUS) ** 2,
        puddingLargest=float(pudding["final_angle"].max()),
        puddingError=float(np.max(np.abs(pudding["final_angle"] - rp.pudding_impulse_angle(impact)))),
        puddingBack=int((pudding["final_angle"] > 90.0).sum()),
    )
    payload = dict(
        constants=dict(
            particles=rp.PARTICLES,
            halfApproach=rp.HALF_APPROACH,
            beamRadius=rp.BEAM_RADIUS,
            puddingRadius=rp.PUDDING_RADIUS,
            speed=rp.SPEED,
            startX=rp.START_X,
            view=rp.VIEW,
            detectorRadius=rp.DETECTOR_RADIUS,
            screenRadius=rp.SCREEN_RADIUS,
            screenGapDegrees=rp.SCREEN_GAP_DEGREES,
            step=rp.STEP,
            sampleEvery=rp.SAMPLE_EVERY,
            totalTime=rp.TOTAL_TIME,
            frameDt=rp.FRAME_DT,
            nuclearBins=rounded(rp.NUCLEAR_BINS, 3),
            puddingBins=rounded(rp.PUDDING_BINS, 3),
            trailSamples=list(rp.TRAIL_SAMPLES),
            bendThreshold=rp.BEND_THRESHOLD,
            interludeFrames=rp.INTERLUDE_FRAMES,
            nucleusMetres=rp.NUCLEUS_METRES,
            atomMetres=rp.ATOM_METRES,
            screenMetres=rp.SCREEN_METRES,
            zoomKeys=[list(k) for k in rp.ZOOM_KEYS],
        ),
        y0=[float(f"{v:.8g}") for v in side * impact],
        nuclear=scene(nuclear, 0.0),
        pudding=scene(pudding, rp.PUDDING_RADIUS),
        report=report,
    )
    (out / "rutherford.json").write_text(json.dumps(payload, separators=(",", ":")))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "data")
    arguments = parser.parse_args()
    arguments.out.mkdir(parents=True, exist_ok=True)
    r = export_rutherford(arguments.out)
    print(
        f"nuclear: max angle error {r['nuclearError']:.2f} deg, beyond 90: {r['nuclearBack']} "
        f"(expected {r['expectedBack']:.1f})"
    )
    print(
        f"pudding: largest angle {r['puddingLargest']:.2f} deg, beyond 90: {r['puddingBack']}, "
        f"impulse-approximation difference {r['puddingError']:.2f} deg"
    )


if __name__ == "__main__":
    main()
