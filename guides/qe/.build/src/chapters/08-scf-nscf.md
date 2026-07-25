---
title: "08. SCF and NSCF"
---

# 08. SCF and NSCF

## Contents
{:.toc-title}

1. TOC
{:toc}

QE is not one program but a **suite of executables**, connected by a
pipeline that flows through `prefix` and `outdir`. The starting point of
that pipeline is the division of labor between `scf` and `nscf`.

## Division of labor

| calculation | What it does | Density | Use |
|---|---|---|---|
| `'scf'` | Converges the charge density self-consistently | Produces it | The starting point of everything: energies, forces, stress |
| `'nscf'` | Eigenvalues on a **frozen density** | Reads the scf one | Dense-grid DOS, Fermi surfaces |
| `'bands'` | An nscf variant on an arbitrary k-path | Reads the scf one | Band structures |

nscf and bands read the charge density that scf left in
`outdir/prefix.save/`, so the **`prefix` and `outdir` must match the scf
exactly** and the run must happen in the same directory. A mismatch gives
`cannot open file ... .save/charge-density.dat`.

```
scf (coarse k, converge density) ─→ nscf (dense k, tetrahedra) ─→ dos.x / projwfc.x
                                 └→ bands (k-path)             ─→ bands.x
```

Typical changes in the nscf step: densify the k-grid, switch
`occupations='tetrahedra'`, raise `nbnd` to cover the conduction bands.

## How to read the output (do not skip this)

Check these items in every `.out` file:

```
!    total energy              =     -93.45 Ry      ← lines marked "!" are converged values
     estimated scf accuracy    <       1.0E-09 Ry   ← below conv_thr?
     the Fermi energy is       6.2 ev               ← printed for metals
     highest occupied, lowest unoccupied level (ev):← printed for insulators (gap estimate)
     total magnetization       =     4.00 Bohr mag/cell  ← spin runs
     absolute magnetization    =     4.12 Bohr mag/cell  ← large difference means AFM components
     Total force               =     0.001 Ry/au
     convergence has been achieved in  12 iterations
```

- Only the total-energy line marked `!` is the converged value; the
  unmarked `total energy` lines are intermediate.
- **The gap between total and absolute magnetization is physical
  information.** For FM they nearly coincide; for AFM the total is near zero
  while the absolute stays large ([Chapter 12](12-magnetism.html)).
- Insulators print `highest occupied, lowest unoccupied level` (a gap
  estimate); metals print `the Fermi energy is` instead. **Which of the two
  appears is itself a diagnosis.** [Example E10](ex-10-feo-afm.html) uses
  exactly this line to catch GGA calling FeO a metal.
- The energy decomposition block (`one-electron contribution`,
  `hartree contribution`, `xc contribution`, `ewald contribution`) is useful
  when hunting anomalies.

The **timing breakdown** at the bottom (`init_run`, `electrons`, `c_bands`,
`sum_band`) tells you where the time goes, and is the first thing to read
when planning parallelization ([Chapter 18](18-parallel-hpc.html)).

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Running the nscf in a <strong>different directory</strong> from the scf,
    or deleting <code>outdir</code> in between. The nscf does not build a
    density; without the scf products it cannot even start. One more:
    learning with <code>verbosity='low'</code>. With <code>'high'</code>
    the output keeps the symmetry operations, the k-point list, and (for
    DFT+U) the ns occupation matrices.
  </p>
</div>

## Related examples

- [E1 · Si SCF](ex-01-si-scf.html): read every output block on a measured run.
- [E7 · Si DOS and PDOS](ex-07-si-dos.html): the scf → nscf handoff in practice.
- [E8 · Si band structure](ex-08-si-bands.html): the scf → bands handoff in practice.
