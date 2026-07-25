---
title: "R2. Card reference"
---

# R2. Card reference

Syntax for the card blocks that follow the namelists in a `pw.x` input.
Namelist variables are in [R1](ref-keywords.html).

## Contents
{:.toc-title}

1. TOC
{:toc}

## Cards at a glance

| Card | Required | Options | Description |
|---|---|---|---|
| `ATOMIC_SPECIES` | yes | none | Label, mass, UPF filename |
| `ATOMIC_POSITIONS` | yes | `alat` / `bohr` / `angstrom` / `crystal` / `crystal_sg` | Optional trailing `if_pos` flags |
| `K_POINTS` | yes | `automatic` / `gamma` / `tpiba` / `crystal` / `tpiba_b` / `crystal_b` / `tpiba_c` / `crystal_c` | The `_b` variants are for band paths |
| `CELL_PARAMETERS` | with `ibrav=0` | `alat` / `bohr` / `angstrom` | 3×3 matrix |
| `HUBBARD` | for DFT+U | `atomic` / `ortho-atomic` / `norm-atomic` / `wf` / `pseudo` | v7.1+ syntax |
| `OCCUPATIONS` | with `occupations='from_input'` | none | Per-band occupations |
| `CONSTRAINTS` | constrained relax/MD | none | Bond and angle constraints |
| `ATOMIC_VELOCITIES` | MD restart | `a.u.` | |
| `ATOMIC_FORCES` | applied forces | none | |
| `ADDITIONAL_K_POINTS` | special | none | |
| `SOLVENTS` | RISM | none | |

## ATOMIC_SPECIES

```fortran
ATOMIC_SPECIES
  Fe1  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
  Fe2  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF   ! same file, second label: for AFM
  O    15.999  O.pbe-n-kjpaw_psl.1.0.0.UPF
```

The number of lines must equal `ntyp`. **The same pseudopotential may be
registered under several labels**; antiferromagnetic order
([Chapter 12](12-magnetism.html)) and per-atom U
([Chapter 13](13-dft-plus-u.html)) rely on exactly this. The mass matters
physically only in MD and phonons.

## ATOMIC_POSITIONS

```fortran
ATOMIC_POSITIONS (crystal)
  Fe  0.000  0.000  0.000   0 0 0    ! if_pos: fully fixed
  Fe  0.500  0.500  0.250   0 0 1    ! free along z only
  O   0.500  0.000  0.375              ! omitted = 1 1 1 (fully free)
```

| Option | Meaning |
|---|---|
| `alat` | Cartesian, in units of `celldm(1)` |
| `bohr` / `angstrom` | Absolute Cartesian |
| `crystal` | Fractional in the cell basis (safest in practice) |
| `crystal_sg` | Space-group coordinates (with `space_group`) |

The `if_pos` triplet (0/1) zeroes the force components in optimization and
MD, freezing motion along those directions.

## K_POINTS

```fortran
K_POINTS (automatic)      ! Monkhorst-Pack grid
  8 8 8  0 0 0            ! nk1 nk2 nk3  s1 s2 s3 (shifts 0/1)

K_POINTS gamma            ! Γ only (isolated molecules); real wavefunctions

K_POINTS (tpiba_b)        ! band path, Cartesian in 2π/a
6
  0.500 0.500 0.500  30   ! point + divisions to the next point
  ...
  0.000 0.000 0.000   0   ! last point gets 0

K_POINTS (crystal)        ! explicit list with weights
```

- The difference between `tpiba_b` (Cartesian, 2π/a) and `crystal_b`
  (fractional, reciprocal basis) is explained in
  [Chapter 10](10-dos-bands.html). When in doubt, `tpiba_b` is safe.
- An nscf feeding the tetrahedron method must use an **unshifted,
  Γ-centered automatic grid**.

## CELL_PARAMETERS

```fortran
CELL_PARAMETERS (angstrom)
  -2.715   0.000   2.715
   0.000   2.715   2.715
  -2.715   2.715   0.000
```

Three cell vectors as rows, used with `ibrav=0`. With the `alat` option the
matrix is scaled by `celldm(1)` (or `A`), which is convenient for volume
scans and vc-relax restarts.

## HUBBARD (v7.1+)

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 4.6
U Fe2-3d 4.6
V Fe1-3d O-2p  1 3  0.8    ! DFT+U+V; site indices follow ATOMIC_POSITIONS order
```

Grammar: `HUBBARD (<projector>)`, then lines of
`<parameter> <label>-<manifold> <value(eV)>`.

| Field | Options |
|---|---|
| Projector | `atomic` / `ortho-atomic` (**recommended**) / `norm-atomic` / `wf` / `pseudo` |
| Parameter | `U`, `J0`, `J`, `B`, `E2`, `E3`, `V`, `alpha` |
| Manifold | `3d`, `2p`, `4f`, ... (up to 3 channels per type) |

The old syntax (`lda_plus_u`, `Hubbard_U(i)`) is retired. Details in
[Chapter 13](13-dft-plus-u.html) and `Doc/Hubbard_input.pdf`.

## OCCUPATIONS

With `occupations='from_input'`, list the occupation of every band; in
spin-polarized runs the up block comes first, then the down block. Rarely
needed outside constrained or excited-state tricks.

## CONSTRAINTS

```fortran
CONSTRAINTS
1
'distance' 1 2 2.40      ! constrain the distance of atoms 1-2 to 2.40 bohr
```

For constrained optimization and MD. First line is the number of
constraints, then one per line (`'distance'`, `'planar_angle'`,
`'torsional_angle'`, ...).

## The neb.x input layout (for reference)

`neb.x` uses a **block structure** rather than cards:

```
BEGIN
BEGIN_PATH_INPUT
&PATH
  string_method = 'neb'
  num_of_images = 7
  nstep_path    = 100
  opt_scheme    = 'broyden'
  path_thr      = 0.05
/
END_PATH_INPUT
BEGIN_ENGINE_INPUT
&CONTROL
 ... (identical to a pw.x input)
/
BEGIN_POSITIONS
FIRST_IMAGE
ATOMIC_POSITIONS (crystal)
 ...
LAST_IMAGE
ATOMIC_POSITIONS (crystal)
 ...
END_POSITIONS
END_ENGINE_INPUT
END
```

Background in [Chapter 17](17-phonons-neb.html).
