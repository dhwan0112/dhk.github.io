---
title: "E2. Rewriting with ibrav=0"
---

# E2. Rewriting with ibrav=0

## Goal

Define the **physically identical system** of [E1](ex-01-si-scf.html) using
`ibrav=0` and an explicit `CELL_PARAMETERS` card, verify the equivalence
through the total energy, and internalize the coordinate options
(`alat`/`crystal`/`angstrom`). Every generator (ASE and friends) emits this
format, so you must be able to read it.

## New cards and variables

| Item | Role |
|---|---|
| `ibrav = 0` | Declares an explicit cell |
| `CELL_PARAMETERS (angstrom)` | Three cell vectors as rows |
| `ATOMIC_POSITIONS (crystal)` | Fractional coordinates: structure decoupled from cell |

## Input file

[Download si_ibrav0.scf.in](files/E02-si-ibrav0/si_ibrav0.scf.in)

```fortran
&CONTROL
  calculation = 'scf'
  prefix      = 'si_ibrav0'
  outdir      = './tmp/'
  pseudo_dir  = './pseudo/'
  verbosity   = 'high'
/
&SYSTEM
  ibrav       = 0           ! explicit cell follows
  nat         = 2
  ntyp        = 1
  ecutwfc     = 30
  ecutrho     = 240
  occupations = 'fixed'
/
&ELECTRONS
  conv_thr    = 1.0d-8
/

ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-kjpaw_psl.1.0.0.UPF

CELL_PARAMETERS (angstrom)
  -2.715   0.000   2.715
   0.000   2.715   2.715
  -2.715   2.715   0.000

ATOMIC_POSITIONS (crystal)
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25

K_POINTS (automatic)
  8 8 8  0 0 0
```

## Run

```bash
mpirun -np 6 pw.x -nk 6 -in si_ibrav0.scf.in > si_ibrav0.scf.out
```

## What to check: the measured comparison

| Item | E1 (`ibrav=2`) | E2 (`ibrav=0`) |
|---|---|---|
| Total energy | −93.45273690 Ry | −93.45274992 Ry |
| `Sym. Ops.` | 48 (with inversion) | 48 (with inversion) |

- Symmetry detection found all 48 operations in both cases. A cleanly
  written `CELL_PARAMETERS` does not necessarily lose symmetry (it can in
  general, so always check).
- The energies differ by 1.3×10⁻⁵ Ry (0.09 meV/atom): not an exact match.
  The cause is not the syntax but **rounding in the lattice constant**:
  E1's `celldm(1)=10.26 bohr` is 5.4293 Å, while E2's cell (half-vectors of
  2.715 Å) is exactly 5.4300 Å. Writing "the same structure" twice requires
  matching the unit conversion to full precision, which is a lesson in
  itself.

## Exercises

1. Switch `CELL_PARAMETERS` from `angstrom` to `alat`, introducing
   `celldm(1)`. With `celldm(1)=10.2614` (= 5.4300 Å), does the energy now
   match E2 to all digits?
2. Convert `ATOMIC_POSITIONS (crystal)` to `(angstrom)` and confirm the
   total energy is unchanged.
3. Perturb one cell-vector component by 0.001 Å. How far does the
   `Sym. Ops.` count drop, and how many irreducible k-points do you get?

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    With <code>ibrav=0</code> and a <code>celldm(1)</code> both present, a
    <code>CELL_PARAMETERS</code> card without a unit option is interpreted
    in <code>alat</code> units (that is, scaled by <code>celldm(1)</code>).
    Always write the unit explicitly. The full coordinate conventions are
    in <a href="03-units-coordinates.html">Chapter 03</a>.
  </p>
</div>

## Related chapters

[03 Units and coordinates](03-units-coordinates.html) ·
[02 Input file structure](02-input-structure.html)
