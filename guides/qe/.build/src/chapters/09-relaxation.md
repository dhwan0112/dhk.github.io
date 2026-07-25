---
title: "09. Structure optimization"
---

# 09. Structure optimization

## Contents
{:.toc-title}

1. TOC
{:toc}

Structure optimization drives the forces (energy gradients with respect to
atomic positions) and the stress (gradients with respect to the cell) to
zero. `relax` moves atoms only; `vc-relax` (variable-cell) moves the cell
too.

## Input skeleton

```fortran
&CONTROL
  calculation   = 'vc-relax'
  etot_conv_thr = 1.0d-5      ! Ry, energy change between ionic steps
  forc_conv_thr = 1.0d-4      ! Ry/bohr, force criterion
  nstep         = 100         ! max ionic steps
/
&ELECTRONS
  conv_thr = 1.0d-10          ! tighter SCF for vc-relax
/
&IONS
  ion_dynamics  = 'bfgs'
/
&CELL
  cell_dynamics  = 'bfgs'
  press_conv_thr = 0.1        ! kbar
  cell_dofree    = 'ibrav'    ! keep the Bravais symmetry
/
```

- This run consumes forces and stress, so tighten the SCF `conv_thr` beyond
  your usual value. Forces from a sloppy density are noise, and BFGS
  wanders on noise.
- `cell_dofree` constrains the cell degrees of freedom: `'all'`, `'ibrav'`
  (keep the Bravais lattice), `'2Dxy'` (slabs: freeze z), `'volume'`,
  `'shape'`, and others.
- Per-atom constraints go through the `if_pos` flags on `ATOMIC_POSITIONS`
  ([Chapter 03](03-units-coordinates.html)).

## The mandatory follow-up: Pulay stress

When `vc-relax` finishes, the final structure appears between
`Begin final coordinates` and `End final coordinates`. **Run a fresh `scf`
on that structure.**

The plane-wave basis is tied to the cell. When the cell changes, the basis
set changes with it (Pulay stress), so the energy and stress of the last
vc-relax step were computed in the old basis and cannot be trusted. QE
prints a warning saying exactly this. A measured check is in
[Example E6](ex-06-si-vcrelax.html).

## Symmetry and the optimization path

QE detects the symmetry of the initial structure and preserves it
throughout the optimization. This cuts both ways.

- An atom on a symmetric site feels exactly zero force along directions the
  symmetry forbids, so it **never moves off them**. To find lower-energy
  broken-symmetry structures, distort the starting geometry slightly or set
  `nosym=.true.`.
- Conversely, keeping symmetry saves a great deal of compute. Choose
  deliberately.

## When BFGS struggles

| Symptom | Response |
|---|---|
| Energy oscillates without converging | Tighten the SCF `conv_thr`; check `upscale` |
| Fails while the cell changes a lot | Increase `cell_factor` (default 2.0) |
| Diverges from the first step | Inspect the starting structure: overlapping atoms, absurd distances |
| Forces are small but stress will not drop | Check `press_conv_thr`; suspect an insufficient cutoff (stress is more cutoff-sensitive than energy) |

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Keeping the lattice constant from <code>vc-relax</code> and also quoting
    the last step's energy. The lattice constant is fine; the energy carries
    Pulay contamination. Always use the energy from the fresh
    <code>scf</code> on the final structure. Also, stress demands higher
    cutoffs than energies and forces, so pass a
    <a href="05-convergence.html">stress-based convergence test</a> before
    any <code>vc-relax</code>.
  </p>
</div>

## Related examples

- [E6 · Si vc-relax](ex-06-si-vcrelax.html): start from a deliberately wrong
  lattice constant, find equilibrium, and measure the usual PBE
  overestimate.
- [E13 · Slabs and AIMD](ex-13-slab-md.html): a slab relaxation with the
  bottom layers pinned via `if_pos`.
