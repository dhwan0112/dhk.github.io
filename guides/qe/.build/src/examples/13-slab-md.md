---
title: "E13. Slabs and AIMD"
---

# E13. Slabs and AIMD

## Goal

Three applications in one pass: (1) **generate** a FeO(100) slab with ASE
(never by hand), (2) relax it with the dipole correction on and extract the
**work function** with `pp.x`, and (3) run **Born-Oppenheimer MD** on the
bulk FeO cell as the starting point for sampling ML training data.
Background in [Chapter 15](15-surfaces.html) and
[Chapter 16](16-molecular-dynamics.html).

## New here

| Item | Role |
|---|---|
| `ase.build.surface` | The slab generator; no hand-written coordinates |
| `tefield`/`dipfield`/`edir`/`emaxpos` | The dipole correction |
| `FixAtoms` → `if_pos 0 0 0` | Pinning the bottom layers |
| `calculation='md'` + SVR | BOMD with a thermostat |
| `pp.x plot_num=11` | The electrostatic potential for the work function |

## Input files

[gen_slab.py](files/E13-slab-md/gen_slab.py) ·
[feo_md.in](files/E13-slab-md/feo_md.in) ·
[pp_workfunction.in](files/E13-slab-md/pp_workfunction.in)

The core of the generator:

```python
from ase.build import bulk, surface
from ase.constraints import FixAtoms

feo = bulk("FeO", "rocksalt", a=4.33)
slab = surface(feo, (1, 0, 0), layers=4, vacuum=8.0)   # 8 Å vacuum per side
slab.center(axis=2)
# pin the bottom half of the layers -> becomes QE if_pos flags
```

Open the generated `feo100.scf.in` and **read it yourself**: the
`CELL_PARAMETERS`, the `ATOMIC_POSITIONS (angstrom)`, the `if_pos` flags.
Being able to read generator output is what
[E2](ex-02-si-ibrav0.html) was for. The slab input carries the dipole
correction (`tefield`/`dipfield` in `&CONTROL`, `edir=3` and
`emaxpos=0.90` in `&SYSTEM`) and a 6×6×1 grid (one point along the
vacuum). The slab SCF is nonmagnetic by design: a 1×1 (100) cell **cannot
geometrically hold** the AFM-II order of FeO
([Chapter 15](15-surfaces.html)).

## Run

```bash
python gen_slab.py                                     # writes feo100.scf.in
mpirun -np 8 pw.x -nk 4 -in feo100.scf.in > feo100.relax.out
mpirun -np 8 pp.x -in pp_workfunction.in  > pp_workfunction.out
mpirun -np 8 pw.x -nk 4 -in feo_md.in     > feo_md.out
```

For the measurements we capped the relaxation at 25 BFGS steps and ran the
MD on an `nstep=200` copy (about 0.2 ps); the distributed input keeps the
original `nstep=2000`. Along the way we found and fixed several defects in
the original decks (the `tefield`/`dipfield` namelist placement, the
missing `nosym` and `mixing_fixed_ns` for MD; see the common-mistakes box).

## Output and figure: measured (1) slab and work function

| Item | Measured (QE 7.5) |
|---|---|
| Slab | FeO(100), 4 layers, 8 atoms (1×1), 16 Å vacuum, nonmagnetic demo |
| Relaxation | 25-step BFGS copy (final total force 0.005 Ry/au: a partial optimization for the demo) |
| Vacuum level / Fermi level | 7.35 eV / 2.40 eV (vacuum flatness std 0.05 eV) |
| **Work function Φ = V_vac − E_F** | **4.95 eV** |

<figure>
  <img src="assets/images/qe-e13-workfunction.png"
       alt="Planar-averaged electrostatic potential of the FeO(100) slab" />
  <figcaption>
    Measured planar-averaged electrostatic potential of the FeO(100) slab
    (pp.x plot_num=11). Confirm the vacuum plateau is flat, then read the
    work function as the distance from the plateau to the Fermi level.
  </figcaption>
</figure>

## Output and figure: measured (2) BOMD

<figure>
  <img src="assets/images/qe-e13-md.png"
       alt="FeO BOMD: temperature and energy trace" />
  <figcaption>
    Measured BOMD of the FeO(+U) bulk cell (SVR 300 K, dt = 20 a.u. ≈
    0.968 fs, 200 steps ≈ 0.19 ps). In the first steps the ions leave
    their ideal lattice sites and release about 2.5 eV of potential energy
    (blue): thermal motion lifting the t2g degeneracy, the physics of E11
    continued. The ±100 K temperature swings (orange) are not a bug but the
    normal statistics of a 4-atom cell (relative fluctuations ~1/√N),
    while the SVR thermostat (nraise=100, ≈0.1 ps coupling) equilibrates
    slowly.
  </figcaption>
</figure>

That early transient is itself the practical lesson: **extract training
frames only after equilibration**. Mixing the transient into a dataset
contaminates it with artificially high-energy structures.

Principles for ML datasets ([Chapter 16](16-molecular-dynamics.html)):
identical cutoffs, k-grid, smearing and U on every frame; converge on
forces; subsample (every 50 steps or so) against frame correlation; and if
you need stress, compute it in separate scf runs on the extracted frames
(see the box).

## Exercises

1. Rebuild with `layers=4 → 6` and see how the work function moves (layer
   count is a convergence parameter too).
2. Turn `dipfield` off and watch the vacuum region of the planar average
   acquire a slope.
3. Write a parser that pulls energy and force frames from the MD log every
   50 steps.
4. Recompute one frame at 60 and 90 Ry cutoffs and compare the forces
   against your ML accuracy target (~50 meV/Å).

<div class="warning">
  <div class="note-title">Common mistakes (all measured on QE 7.5)</div>
  <p>
    <strong><code>tefield</code>/<code>dipfield</code> belong to
    <code>&amp;CONTROL</code>.</strong> Put them in <code>&amp;SYSTEM</code>
    and the run dies instantly with
    <code>read_namelists ... bad line</code> (only the position parameters
    <code>edir</code> etc. are &amp;SYSTEM variables); we hit this and
    fixed the generator.
    <strong>MD requires <code>nosym=.true.</code></strong>: thermal motion
    breaks the initial symmetry in the first step, and without it the run
    stops at <code>checkallsym</code>.
    <strong>DFT+U with nosym stalls the SCF</strong>: rotations among the
    degenerate t2g orbitals keep the density sloshing (stuck at 7×10⁻⁵ Ry
    after 100 iterations); <code>mixing_fixed_ns=30</code> (freeze the ns
    matrix for the first iterations) releases it, after which even 10⁻⁸ is
    hard to reach, so the distributed input uses the BOMD-conventional
    <code>conv_thr = 1.0d-6</code>.
    <strong>Hubbard stress dies under nosym</strong>: with
    <code>tstress=.true.</code> the run aborts at
    <code>stres_hub: non-symmetric stress contribution</code>; NVT sampling
    does not need stress, so it is off, and stress for training data comes
    from separate scf runs on extracted frames. Finally, <code>emaxpos</code>
    (the sawtooth peak) must sit in the middle of the vacuum, and
    <code>dt</code> is in Rydberg atomic units (20 a.u. ≈ 0.968 fs);
    read it as femtoseconds and the trajectory explodes at once.
  </p>
</div>

## Related chapters

[15 Surfaces, slabs, work function](15-surfaces.html) ·
[16 Molecular dynamics](16-molecular-dynamics.html) ·
[11 Densities and potentials](11-postprocessing.html)
