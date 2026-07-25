---
title: "R1. Keyword dictionary"
---

# R1. Keyword dictionary

A lookup dictionary of `pw.x` input variables, namelist by namelist.
Defaults are as of QE 7.5, and **the final authority is always the
`Doc/INPUT_PW.txt` of your installed version**
([online](https://www.quantum-espresso.org/Doc/INPUT_PW.html)).
Card syntax is in [R2](ref-cards.html); post-processing variables in
[R4](ref-executables.html).

## Contents
{:.toc-title}

1. TOC
{:toc}

## &CONTROL

| Variable | Default | Description |
|---|---|---|
| `calculation` | `'scf'` | `scf` / `nscf` / `bands` / `relax` / `md` / `vc-relax` / `vc-md` |
| `title` | none | Free text echoed in the output; handy for batch bookkeeping |
| `verbosity` | `'low'` | `'high'` prints symmetry operations, ns matrices, the k-point list. **Always high while learning** |
| `restart_mode` | `'from_scratch'` | `'restart'` resumes an interrupted run |
| `nstep` | 1 for scf, 50 for relax/md | Number of ionic steps |
| `dt` | 20.0 | MD time step, in **Rydberg atomic units** (20 a.u. ≈ 0.968 fs) |
| `outdir` | `./` or `$ESPRESSO_TMPDIR` | Location of large temporaries. **Point it at a fast disk** |
| `wfcdir` | `outdir` | Separate location for wavefunctions if needed |
| `prefix` | `'pwscf'` | **Must match** across follow-up runs |
| `pseudo_dir` | `$ESPRESSO_PSEUDO` or `~/espresso/pseudo` | Where the UPF files live |
| `disk_io` | depends on calculation | `'none'` / `'low'` / `'medium'` / `'high'` / `'nowf'`. Use `'none'` for MD |
| `tprnfor` | `.false.` for scf | Print forces. **Mandatory for ML training data** |
| `tstress` | `.false.` | Print stress |
| `etot_conv_thr` | 1.0d-4 Ry | Energy criterion for ionic optimization |
| `forc_conv_thr` | 1.0d-3 Ry/bohr | Force criterion for ionic optimization |
| `max_seconds` | 1.0d7 | Save and exit cleanly before the time limit. **Essential in HPC batch jobs** |
| `tefield`, `dipfield` | `.false.` | Sawtooth field / dipole correction switches. **They live here in &CONTROL** (the position parameters `edir` etc. are in &SYSTEM) |
| `lelfield`, `gate`, `trism` | `.false.` | Special features (finite field / gate / RISM) |

## &SYSTEM: lattice and atoms

| Variable | Description |
|---|---|
| `ibrav` | 0 = explicit `CELL_PARAMETERS` / 1 simple cubic / 2 fcc / 3 bcc / 4 hexagonal / 5 rhombohedral / 6,7 tetragonal / 8–11 orthorhombic / 12,13 monoclinic / 14 triclinic |
| `celldm(1..6)` | Lattice parameters per `ibrav`. **`celldm(1)` is in bohr** |
| `A, B, C, cosAB, cosAC, cosBC` | Alternative to `celldm`. **`A` is in Å** (mind the mix) |
| `nat`, `ntyp` | Atom count / type count; must match the cards |
| `nosym`, `noinv` | Suppress symmetry / inversion. For special magnetic patterns, MD, or debugging |

`ibrav=0` is flexible but symmetry autodetection can degrade; check the
`Sym. Ops.` count in the output.

## &SYSTEM: basis and cutoffs

| Variable | Default | Description |
|---|---|---|
| `ecutwfc` | **required** | Wavefunction cutoff (Ry) |
| `ecutrho` | `4*ecutwfc` | Density cutoff (Ry). **US/PAW need 8–12x** |
| `nbnd` | `nelec/2` for insulators, more for metals | Number of bands; be generous for DOS and bands runs |

## &SYSTEM: occupations and smearing

| Variable | Description |
|---|---|
| `occupations` | `'fixed'` (insulators) / `'smearing'` (metals) / `'tetrahedra'` / `'tetrahedra_lin'` / `'tetrahedra_opt'` (nscf for DOS/bands) / `'from_input'` |
| `smearing` | `'gaussian'` / `'methfessel-paxton'` (`'mp'`) / `'marzari-vanderbilt'` (`'mv'`, `'cold'`) / `'fermi-dirac'` (`'fd'`) |
| `degauss` | Smearing width (Ry); metals typically 0.01–0.02 |

The tetrahedron methods require a **Γ-centered, unshifted automatic grid**
and belong in nscf runs.

## &SYSTEM: spin and magnetism

| Variable | Description |
|---|---|
| `nspin` | 1 unpolarized / 2 collinear / 4 noncollinear (prefer `noncolin`) |
| `starting_magnetization(i)` | **Initial polarization ratio (−1 to 1)** for type `i`. Not Bohr magnetons |
| `tot_magnetization` | Constrains the cell moment; separate up/down Fermi levels |
| `noncolin` | `.true.` for noncollinear magnetism |
| `lspinorb` | Spin-orbit coupling; needs fully relativistic pseudopotentials |
| `angle1(i)`, `angle2(i)` | Moment directions (degrees) for noncollinear runs |
| `constrained_magnetization` | `'atomic'`, `'total'`, ...; strength via `lambda` |

## &SYSTEM: DFT+U (v7.1+ syntax)

U parameters go in the **`HUBBARD` card** ([R2](ref-cards.html)), not in
`&SYSTEM`. The related variables that remain here:

| Variable | Description |
|---|---|
| `starting_ns_eigenvalue(m, ispin, ityp)` | Forces initial d/f occupation eigenvalues. **Essential for systems trapped in wrong minima, like FeO** |
| `Hubbard_occ(ityp, i)` | Overrides the initial occupation of the Hubbard manifold |

**Retired syntax**: `lda_plus_u`, `lda_plus_u_kind`, `Hubbard_U(i)`,
`U_projection_type`. All replaced by the `HUBBARD` card in v7.1.

## &SYSTEM: functionals, dispersion, isolation, fields

| Variable | Description |
|---|---|
| `input_dft` | Overrides the functional baked into the pseudopotential. Avoid |
| `vdw_corr` | `'grimme-d2'` / `'grimme-d3'` / `'ts-vdw'` / `'xdm'` / `'mbd'` |
| `assume_isolated` | `'none'` / `'makov-payne'` / `'martyna-tuckerman'` (`'mt'`) / `'esm'` / `'2D'` |
| `edir`, `emaxpos`, `eopreg`, `eamp` | Field direction (1/2/3), position, width, amplitude (the switches `tefield`/`dipfield` are in &CONTROL) |
| `exx_fraction`, `screening_parameter`, `nqx1..3` | Hybrid-functional parameters |

## &ELECTRONS

| Variable | Default | Description |
|---|---|---|
| `electron_maxstep` | 100 | Maximum SCF iterations |
| `conv_thr` | 1.0d-6 | SCF threshold (Ry). Use 1.0d-12 before `hp.x` |
| `mixing_mode` | `'plain'` | `'plain'` (Broyden) / `'TF'` / `'local-TF'`. **Metals, slabs, magnets: `'local-TF'`** |
| `mixing_beta` | 0.7 | Mixing fraction. Magnets and metals: 0.1–0.3 |
| `mixing_ndim` | 8 | Mixing history; more costs memory |
| `mixing_fixed_ns` | 0 | DFT+U: freeze the ns occupation matrix for the first N iterations. **Unsticks stalled SCF in the nosym+U combination (MD)**; measured in [E13](ex-13-slab-md.html) |
| `diagonalization` | `'david'` | `'david'` / `'cg'` / `'ppcg'` / `'paro'` / `'rmm-davidson'`. `'cg'` is slow but robust |
| `diago_david_ndim` | 2 | Davidson workspace; reduce if memory is tight |
| `startingwfc` | `'atomic+random'` | `'atomic'` / `'random'` / `'file'` |
| `startingpot` | `'atomic'` | `'atomic'` / `'file'` |
| `adaptive_thr` | `.false.` | Relaxed thresholds in early iterations (hybrids) |

## &IONS

| Variable | Description |
|---|---|
| `ion_dynamics` | relax: `'bfgs'` (default), `'damp'` / md: `'verlet'`, `'langevin'` |
| `ion_temperature` | `'not_controlled'` / `'rescaling'` / `'rescale-v'` / `'berendsen'` / `'andersen'` / `'svr'` / `'initial'` |
| `tempw` | Target temperature (K) |
| `nraise` | Thermostat coupling period |
| `pot_extrapolation`, `wfc_extrapolation` | `'none'` / `'atomic'` / `'first_order'` / `'second_order'`. Large effect on MD speed |
| `upscale` | Automatic SCF-threshold tightening factor in BFGS |
| `bfgs_ndim` | 1 (default); 2 or more for quasi-Newton |

## &CELL

| Variable | Description |
|---|---|
| `cell_dynamics` | vc-relax: `'bfgs'` / vc-md: `'pr'`, `'w'` |
| `press` | Target pressure (kbar) |
| `press_conv_thr` | 0.5 kbar (default) |
| `cell_dofree` | `'all'` / `'ibrav'` / `'x'`,`'y'`,`'z'` / `'xy'` etc. / `'2Dxy'` / `'2Dshape'` / `'volume'` / `'shape'`. **Slabs: `'2Dxy'`** |
| `cell_factor` | 2.0 (vc-relax); raise it if the cell changes a lot |
| `wmass` | Cell inertial mass (vc-md) |

## Command-line parallel flags

| Flag | Alias | Meaning | Guidance |
|---|---|---|---|
| `-nk` | `-npool` | k-point pools | **Most efficient.** Divide the k-count; lower it if memory runs out |
| `-nb` | `-nband` | Band groups | Hybrids and EXX |
| `-nt` | `-ntg` | FFT task groups | Many bands, many cores |
| `-nd` | `-ndiag` | Diagonalization group | **Square numbers only.** Large systems |
| `-ni` | `-nimage` | Image parallelism | NEB, phonons, hp.x |
| `-i` / `-in` / `-inp` | | Input file | |

## Environment variables

| Variable | Purpose |
|---|---|
| `ESPRESSO_PSEUDO` | Default pseudopotential path when `pseudo_dir` is absent |
| `ESPRESSO_TMPDIR` | Default `outdir` |
| `OMP_NUM_THREADS` | OpenMP threads. Beware oversubscription with MPI ([Chapter 18](18-parallel-hpc.html)) |
| `ESPRESSO_ROOT` | Source-tree path |
