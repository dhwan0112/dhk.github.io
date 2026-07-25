---
title: "R4. Executables"
---

# R4. Executables

QE is a suite, not one program. This is the map of what each executable
takes and produces. Per-variable detail lives in each code's
`Doc/INPUT_<name>.txt`.

## Contents
{:.toc-title}

1. TOC
{:toc}

## The core pipeline

| Executable | Input namelists | Prerequisite | Products | Chapter |
|---|---|---|---|---|
| `pw.x` | `&CONTROL`+`&SYSTEM`+`&ELECTRONS` (+`&IONS`, `&CELL`) | none | Total energy, forces, stress, density, wavefunctions | [02](02-input-structure.html) |
| `dos.x` | `&DOS` | nscf | Total DOS (`fildos`) | [10](10-dos-bands.html) |
| `projwfc.x` | `&PROJWFC` | nscf | PDOS, Löwdin charges | [10](10-dos-bands.html) |
| `bands.x` | `&BANDS` | `calculation='bands'` | Band data (`.gnu`), symmetry labels | [10](10-dos-bands.html) |
| `pp.x` | `&INPUTPP` + `&PLOT` | scf | Densities, potentials, ELF (cube/XSF) | [11](11-postprocessing.html) |
| `average.x` | (free-format input) | pp.x | Planar averages (work function) | [15](15-surfaces.html) |
| `hp.x` | `&INPUTHP` | scf + HUBBARD card | Hubbard U and V (`*.Hubbard_parameters.dat`) | [14](14-hubbard-hp.html) |
| `ph.x` | `&INPUTPH` | scf | Dynamical matrices (`fildyn`) | [17](17-phonons-neb.html) |
| `q2r.x` / `matdyn.x` | own formats | ph.x | Real-space force constants / phonon dispersion and DOS | [17](17-phonons-neb.html) |
| `neb.x` | `&PATH` + engine input | both endpoints optimized | Minimum-energy path, barrier | [17](17-phonons-neb.html) |
| `cp.x` | separate CP input | none | Car-Parrinello MD | see [16](16-molecular-dynamics.html) |
| `pw2wannier90.x` | `&INPUTPP` | nscf + Wannier90 | Wannier interface files | [17](17-phonons-neb.html) |
| `plotband.x` | interactive | bands.x | Band-plot data | [10](10-dos-bands.html) |

## Post-processing namelists in brief

### dos.x: &DOS

`prefix`, `outdir`, `fildos`, `Emin`, `Emax`, `DeltaE`, `ngauss`,
`degauss`, `bz_sum`. The output columns are E (eV), DOS (two spin columns
in polarized runs), and the integrated DOS. Note that `Emin`/`Emax` are
**absolute energies in eV**; place the window around the actual Fermi level
of your system, which for PAW data can sit at 15–20 eV.

### projwfc.x: &PROJWFC

`prefix`, `outdir`, `filpdos`, `filproj`, `ngauss`, `degauss`, `Emin`,
`Emax`, `DeltaE`, `lsym` (symmetrized atomic orbitals), `pawproj`,
`lwrite_overlaps`, `kresolveddos`. Outputs the
`filpdos.pdos_atm#N(label)_wfc#M(orbital)` files plus the **Löwdin
charges** block on standard output.

### bands.x: &BANDS

`prefix`, `outdir`, `filband`, `lsym` (assign symmetry labels),
`spin_component`, `lp` (momentum matrix elements). `filband.gnu` is the
plottable file, and the `high-symmetry point` lines on standard output give
the tick positions.

### pp.x: &INPUTPP + &PLOT

`&INPUTPP`: `prefix`, `outdir`, `filplot`, `plot_num`, `spin_component`,
`sample_bias`, `kpoint`, `kband`.

| `plot_num` | Quantity |
|---|---|
| 0 | Valence charge density |
| 1 | Total potential (V_bare + V_H + V_xc) |
| 2 | Local ionic potential |
| 5 | STM image |
| 6 | Spin density ρ↑ − ρ↓ |
| 8 | ELF |
| 11 | Bare + Hartree potential (**work function**) |

`&PLOT`: `nfile`, `filepp(i)`, `weight(i)`, `iflag` (0 line / 1 spherical
average / 2 plane / 3 3D / 4 polar), `output_format` (0 gnuplot /
3 XCrySDen 2D / 5 XSF 3D / 6 Gaussian cube / 7 gnuplot 2D), `fileout`,
`e1,e2,e3`, `x0`, `nx,ny,nz`. PAW all-electron options vary by version;
check `Doc/INPUT_PP.txt`.

### hp.x: &INPUTHP

`prefix`, `outdir`, `nq1/nq2/nq3`, `conv_thr_chi`, `thresh_init`,
`iverbosity`, `start_q`/`last_q` (job splitting), `perturb_only_atom(i)`,
`skip_equivalence_q`, `determine_num_pert_only`, `compute_hp` (assemble
partial results).

### ph.x: &INPUTPH

`prefix`, `outdir`, `fildyn`, `tr2_ph`, `ldisp`, `nq1/nq2/nq3`, `epsil`,
`zeu`, `recover`, `start_q`/`last_q`, `alpha_mix(1)`.

### neb.x: &PATH

`string_method` (`'neb'`/`'smd'`), `num_of_images`, `nstep_path`,
`opt_scheme` (`'broyden'`/`'quick-min'`/`'sd'`),
`CI_scheme` (`'no-CI'`/`'auto'`/`'manual'`), `path_thr`, `ds`, `k_max`,
`k_min`, `restart_mode`. Input layout in [R2](ref-cards.html).

## The file flow on one page

```
                    ┌─ dos.x ──────→ total DOS
scf ──→ nscf ───────┼─ projwfc.x ──→ PDOS, Löwdin
 │                  └─ (frozen density)
 ├────→ bands ──────── bands.x ────→ bands (.gnu)
 ├────→ pp.x ─────────────────────→ density/potential (cube) ──→ average.x → work function
 ├────→ hp.x (HUBBARD required) ──→ U, V
 └────→ ph.x ──→ q2r.x ──→ matdyn.x → phonon dispersion
```

Every arrow is glued by the **same `prefix` and `outdir`**. Break the chain
and you get `cannot open file ... .save/...`
([R3](ref-errors.html)).
