---
title: "E11. FeO with DFT+U"
---

# E11. FeO with DFT+U

## Goal

Add **three `HUBBARD` lines** to the input of [E10](ex-10-feo-afm.html) and
turn on DFT+U. Measure what U does to the Fe-3d manifold, and then walk
into the famous trap of this system, the case where **the run stays
metallic even with U on**, and learn to diagnose it. Knowing this trap is
what lets you read FeO+U results in the literature critically.

## New cards and variables

| Item | Role |
|---|---|
| `HUBBARD (ortho-atomic)` | The v7.1+ card with its projector ([Chapter 13](13-dft-plus-u.html)) |
| `U Fe1-3d 4.6` | U (eV) per label and manifold |
| `starting_ns_eigenvalue` | Steering the d occupations toward a chosen minimum (see the trap section) |

## Input file

[Download feo_u.scf.in](files/E11-feo-hubbard/feo_u.scf.in) ·
[scan_U.sh](files/E11-feo-hubbard/scan_U.sh)

The input is E10 plus this at the end:

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 4.6
U Fe2-3d 4.6
```

U = 4.6 eV is a conventional literature value for FeO. Computing the U
proper to your own system is [E12](ex-12-feo-hp.html).

## Run

```bash
mpirun -np 8 pw.x -nk 4 -in feo_u.scf.in > feo_u.scf.out
```

## What to check: measured

| Item | GGA (E10) | GGA+U (this example) |
|---|---|---|
| Total energy | −741.81592 Ry | −741.52737 Ry (**do not compare directly**: different functionals) |
| total / absolute magnetization | 0.00 / 7.17 μB | −0.00 / **7.50 μB** |
| Fe local moments | ±3.31 μB | **±3.46 μB** (U strengthens the d localization) |
| Electronic structure | Metal | **Still (semi)metallic: see the trap below** |

<figure>
  <img src="assets/images/qe-e10-e11-feo-dos.png"
       alt="FeO spin-resolved DOS: GGA vs GGA+U" />
  <figcaption>
    Measured spin-resolved DOS of FeO (QE 7.5). With U on (right), the
    occupied and unoccupied d manifolds split apart and Hubbard gaps open
    above and below. But in the ideal cubic cell a <strong>narrow band of
    minority-spin t2g character stays pinned at the Fermi level</strong>:
    the measured face of the "U alone does not make it an insulator" trap.
  </figcaption>
</figure>

## The trap: why it stays metallic with U on (with measurements)

The DOS shows U doing real work (larger moments, wide Hubbard splitting).
The problem is that the single minority-spin electron of Fe²⁺ must choose
among **three t2g orbitals that are exactly degenerate in the ideal cubic
cell**. Unable to pick one, it spreads across all three and forms a narrow
metallic band. Since QE 7.1 the starting d occupations are read from the
pseudopotential (previously hardcoded), so the same input can land in
different metallic solutions on different versions, and **neither is the
correct ground state** (the mailing-list case cited in
[Chapter 13](13-dft-plus-u.html)).

The standard prescription is to steer the occupations:

```fortran
&SYSTEM
  ...
  starting_ns_eigenvalue(5,2,1) = 1.d0   ! Fe1: fill the top minority eigenvalue
  starting_ns_eigenvalue(5,1,2) = 1.d0   ! Fe2: mirrored spin channel
/
```

We report what actually happened when we tried:

1. With the seed above, the SCF **returned to the same metallic solution**
   (energies agree to 4×10⁻⁷ Ry).
2. A second attempt that pinned the full minority occupation pattern to
   [1,0,0,0,0], with `mixing_beta` lowered to 0.1 and `degauss` to 0.005,
   oscillated near 10⁻⁴ Ry for 98 iterations without converging.

In this geometry (ideal rocksalt) and setup, the metallic basin is simply
very deep. Real FeO distorts rhombohedrally along [111] below its Néel
temperature, and that distortion lifts the t2g degeneracy so that orbital
order and the insulating state settle in together. To reach the full
insulating solution you would combine (1) the experimentally distorted
structure, (2) a broader search over `starting_ns_eigenvalue` patterns,
and (3) the **orbital-resolved DFT+U** of QE 7.5 (different U for t2g and
eg, introduced for precisely this situation). A living example of
"converged does not mean correct".

## Exercises

1. Use [scan_U.sh](files/E11-feo-hubbard/scan_U.sh) to scan U = 0, 2, 4,
   6, 8 eV and tabulate the Fe moment and the Hubbard splitting in the
   DOS.
2. Switch the projector between `atomic` and `ortho-atomic` at fixed U and
   compare. You will feel in your hands that "U comes packaged with its
   projector".
3. Add a ~3% rhombohedral distortion along [111] to `CELL_PARAMETERS` and
   rerun with the occupation seed. Does a gap open now?
4. Try DFT+U+J0 by adding `J0 Fe1-3d 0.8`.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Concluding "U is on and the SCF converged, so it must be an insulator
    now". Always check whether <code>the Fermi energy is</code> disappeared
    in favor of <code>highest occupied, lowest unoccupied level</code>, and
    inspect the <code>Tr[ns(na)]</code> and ns eigenvalue blocks
    (<code>verbosity='high'</code>) for a physical occupation pattern.
    And never compare GGA and GGA+U total energies directly; they belong
    to different functionals.
  </p>
</div>

## Related chapters

[13 DFT+U and the HUBBARD card](13-dft-plus-u.html) ·
[14 Computing U with hp.x](14-hubbard-hp.html) ·
[12 Spin polarization and magnetism](12-magnetism.html)
