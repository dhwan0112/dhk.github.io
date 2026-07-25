---
title: "E1. Si SCF"
---

# E1. Si SCF

## Goal

Run one SCF on the simplest system there is (diamond-structure silicon, two
atoms) and read every block of the output. This input is the skeleton for
every later example.

## New cards and variables

| Item | Role |
|---|---|
| `&CONTROL` / `&SYSTEM` / `&ELECTRONS` | The three required namelists ([Chapter 02](02-input-structure.html)) |
| `ibrav=2` + `celldm(1)` | The fcc lattice by convention ([Chapter 03](03-units-coordinates.html)) |
| `ATOMIC_SPECIES` / `ATOMIC_POSITIONS` / `K_POINTS` | The three required cards |
| `verbosity='high'`, `tprnfor`, `tstress` | Verbose output plus forces and stress |

## Input file

[Download si.scf.in](files/E01-si-scf/si.scf.in)

```fortran
&CONTROL
  calculation  = 'scf'
  prefix       = 'si'
  outdir       = './tmp/'
  pseudo_dir   = './pseudo/'
  verbosity    = 'high'
  tprnfor      = .true.
  tstress      = .true.
/
&SYSTEM
  ibrav        = 2
  celldm(1)    = 10.26
  nat          = 2
  ntyp         = 1
  ecutwfc      = 30
  ecutrho      = 240
  occupations  = 'fixed'
/
&ELECTRONS
  conv_thr     = 1.0d-8
  mixing_beta  = 0.7
/

ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (alat)
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25

K_POINTS (automatic)
  8 8 8  0 0 0
```

## Run

```bash
mkdir -p pseudo tmp        # put the Si PAW UPF in pseudo/ (Chapter 01)
pw.x -in si.scf.in > si.scf.out                     # serial
mpirun -np 6 pw.x -nk 6 -in si.scf.in > si.scf.out  # the parallel setup used for the measurements
```

## What to check in the output

| Item | Search for | Measured (QE 7.5, PAW) |
|---|---|---|
| Final total energy | `!    total` | **−93.45273690 Ry** |
| Convergence | `convergence has been achieved` | 6 iterations |
| Irreducible k-points | `number of k points` | 29 (8×8×8 reduced by symmetry) |
| Symmetry operations | `Sym. Ops.` | 48 (with inversion) |
| Highest occupied level | `highest occupied level` | 6.2124 eV |
| Force | `Total force` | 0.000000 (exactly zero on symmetric sites) |
| Stress | `total   stress` | P = 20.28 kbar |
| Wall time | `PWSCF ... WALL` | 2.75 s (6 ranks) |

A few reading notes:

- Only the total-energy line marked `!` is the converged value. The
  absolute number differs wildly from ultrasoft results because this is
  PAW, and
  [absolute total energies are not comparable anyway](04-pseudopotentials.html).
- With `occupations='fixed'` and the default `nbnd` (occupied bands only),
  the output shows `highest occupied level` but no gap estimate
  (`lowest unoccupied` is missing). To see the gap, raise `nbnd`
  (Exercise 3).
- P = +20 kbar means this lattice constant (5.43 Å, the experimental
  value) is compressed relative to the PBE equilibrium. The PBE equilibrium
  constant is found in [E6](ex-06-si-vcrelax.html).

## Exercises

1. Switch `verbosity` to `'low'`, watch how much output disappears, and
   explain why `'high'` is the right choice while learning.
2. Change `occupations` to `'smearing'`. How does the energy move, and why
   is smearing wrong for a semiconductor?
3. Add `nbnd = 8` so that `highest occupied, lowest unoccupied level`
   appears, and read off the gap estimate.
4. Delete `ecutrho` (falling back to the 4x default) and see what happens.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    A missing UPF in <code>pseudo_dir</code>, or a filename that does not
    match <code>ATOMIC_SPECIES</code>, stops the run with
    <code>Error in routine readpp</code>. And do not delete this run's
    <code>outdir</code> (<code>./tmp/</code>): the nscf steps of E7 and E8
    cannot start without it (<a href="08-scf-nscf.html">Chapter 08</a>).
  </p>
</div>

## Related chapters

[02 Input file structure](02-input-structure.html) ·
[03 Units and coordinates](03-units-coordinates.html) ·
[08 SCF and NSCF](08-scf-nscf.html)
