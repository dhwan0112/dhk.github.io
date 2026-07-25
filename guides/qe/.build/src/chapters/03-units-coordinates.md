---
title: "03. Units and coordinates"
---

# 03. Units and coordinates

## Contents
{:.toc-title}

1. TOC
{:toc}

A large fraction of beginner errors in QE are unit confusions. Memorizing the
one table in this chapter will save you days.

## The unit conventions you must memorize

QE uses **Rydberg atomic units**.

| Quantity | QE unit | Notes |
|---|---|---|
| Energy (input and output) | **Ry** | 1 Ry = 13.6057 eV. `ecutwfc`, `conv_thr`, `degauss` are all in Ry |
| Length (`celldm`) | **bohr** | 1 bohr = 0.5292 Å. `CELL_PARAMETERS angstrom` is available |
| Force | Ry/bohr | `forc_conv_thr` defaults to 1.0d-3. 1 Ry/bohr = 25.711 eV/Å |
| Stress | kbar (Ry/bohr³ also printed) | |
| MD time step (`dt`) | Rydberg atomic units | 20.0 a.u. ≈ 0.968 fs |
| `starting_magnetization` | **dimensionless, −1 to 1** | Not Bohr magnetons (a very common mistake) |
| DOS and band output | eV | The post-processing codes print eV; do not mix this up |

The lattice parameters in `&SYSTEM` come either as `celldm(1..6)` (bohr) or
as `A, B, C, cosAB, ...` (**Å**). One set is in bohr and the other in
angstrom for the same quantities; that asymmetry is the trap.

## ibrav: choosing the Bravais lattice

`ibrav` decides how the cell is defined.

| `ibrav` | Lattice | Required `celldm` |
|---|---|---|
| 0 | Explicit `CELL_PARAMETERS` card | (`celldm(1)` may still act as the `alat` scale) |
| 1 | Simple cubic | `celldm(1)` |
| 2 | Face-centered cubic | `celldm(1)` |
| 3 | Body-centered cubic | `celldm(1)` |
| 4 | Hexagonal | `celldm(1)`, `celldm(3)=c/a` |
| 5 | Rhombohedral | `celldm(1)`, `celldm(4)=cos α` |
| 6, 7 | Tetragonal | `celldm(1)`, `celldm(3)` |
| 8–11 | Orthorhombic | `celldm(1..3)` |
| 12–13 | Monoclinic | `celldm(1..4)` |
| 14 | Triclinic | `celldm(1..6)` |

With `ibrav > 0`, QE defines the primitive vectors **by its own
convention**, which may differ from the convention in your favorite
textbook. This bites later, especially for band paths; see the `tpiba_b`
discussion in [Chapter 10](10-dos-bands.html).

`ibrav = 0` is flexible, but **automatic symmetry detection can silently
degrade**. Check the `Sym. Ops.` count in the output: fewer symmetry
operations means more irreducible k-points and a slower run. A measured
comparison is in [Example E2](ex-02-si-ibrav0.html).

## Coordinates: the four units of ATOMIC_POSITIONS

```fortran
ATOMIC_POSITIONS (crystal)
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25
```

| Option | Meaning |
|---|---|
| `alat` | Cartesian coordinates in units of `celldm(1)` (= `A`) |
| `bohr` / `angstrom` | Absolute Cartesian coordinates |
| `crystal` | Fractional coordinates in the cell basis. Decouples structure from cell size, the safest choice in practice |

The `CELL_PARAMETERS` card likewise accepts `alat`, `bohr`, or `angstrom`.
With `alat` you can rescale the whole cell through `celldm(1)`, which is
convenient for volume scans and vc-relax restarts.

## if_pos: constraint flags after the coordinates

Appending three integers to a coordinate line constrains motion along each
direction (1 = free, 0 = fixed). They only matter in optimization and MD.

```fortran
ATOMIC_POSITIONS (crystal)
  Fe  0.000  0.000  0.000   0 0 0    ! fully fixed
  Fe  0.500  0.500  0.250   0 0 1    ! free along z only (bottom slab layers)
  O   0.500  0.000  0.375   1 1 1    ! fully free (default, can be omitted)
```

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Writing <code>starting_magnetization = 2.2</code> as if it were a moment
    in Bohr magnetons. The variable is a <strong>dimensionless ratio between
    −1 and 1</strong> (the spin polarization of the valence electrons). Out
    of range it gets clipped or rejected, and the initial magnetization you
    intended never happens. Magnetic calculations are covered in
    <a href="12-magnetism.html">Chapter 12</a>.
  </p>
</div>

## Related examples

- [E2 · Rewriting with ibrav=0](ex-02-si-ibrav0.html): the same crystal
  defined with `ibrav=2` and with `ibrav=0 + CELL_PARAMETERS`, checking
  equivalence and symmetry detection.
