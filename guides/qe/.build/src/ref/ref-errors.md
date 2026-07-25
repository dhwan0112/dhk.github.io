---
title: "R3. Error message dictionary"
---

# R3. Error message dictionary

Most QE errors arrive as `Error in routine <name> (<code>)`, and
**the routine name is the strongest clue to the cause**.

## Contents
{:.toc-title}

1. TOC
{:toc}

## How to read an error

```
     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
     Error in routine  cdiaghg (2):
      problems computing cholesky
     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
```

| Routine name | Problem area |
|---|---|
| `read_*`, `card_*`, `iosys` | Input syntax |
| `c_bands`, `cdiaghg`, `regterg`, `cegterg` | Diagonalization |
| `sum_band`, `v_of_rho` | Charge density (cutoffs, pseudopotential) |
| `electrons` | SCF convergence |
| `punch`, `openfil`, `davcio` | File I/O (paths, disk, `prefix` mismatch) |

The truly dangerous cases have no error at all; see
[the section on silent failures](#silent-failures-the-most-dangerous-category).

## Input syntax errors

| Message | Cause | Fix |
|---|---|---|
| `Error in routine card_xxx` | Card-name typo or wrong field count | Check the uppercase card name and column count |
| `too many atomic species` / `nat is wrong` | `nat`/`ntyp` disagree with the cards | Recount against the cards |
| `Unknown label of the Hubbard parameter` | Bad parameter letter in the `HUBBARD` card | Must be one of `U`, `J0`, `J`, `V`, `alpha` |
| `namelist not found` | Namelist typo or missing `/` | Every namelist ends with `/` |
| `input_dft not allowed` | Conflicts with the pseudopotential functional | Remove `input_dft`; use the built-in functional |
| `reading namelist ...` | Fortran parse failure (usually commas or quotes) | Single quotes for strings, `.true.`/`.false.` for logicals |
| `read_namelists ... bad line` | Variable placed in the wrong namelist | Example: `tefield`/`dipfield` belong in `&CONTROL`, not `&SYSTEM` (measured; see [E13](ex-13-slab-md.html)) |

## Pseudopotential and density problems

| Message | Cause | Fix |
|---|---|---|
| `charge is wrong: smearing is needed` | Assumed an insulator, got a metal | `occupations = 'smearing'` |
| `charge is wrong` (integrated charge off) | degauss too small for the k-grid, or `ecutrho` too low | Converge degauss with the grid; 8–12x `ecutrho` for US/PAW |
| `negative rho (up, down)` (warning) | `ecutrho` too low | 8–12x for US/PAW |
| `Error in routine readpp` / `upf_read` | Corrupt UPF, wrong path, version clash | Check `pseudo_dir`; re-download |
| `wrong number of valence electrons` | Pseudopotential does not match the species | Recheck `ATOMIC_SPECIES` |
| `set_hubbard_l: pseudopotential not yet inserted` | The Hubbard manifold is absent from the pseudopotential | Use a semicore pseudopotential |

Measured case: in the degauss scan of
[Example E5](ex-05-al-metal.html), `mv` smearing with `degauss=0.005` on a
12×12×12 grid integrated the charge to 3.003 instead of 3 and stopped with
`charge is wrong`. Smearing width and k-grid must be converged together.

## SCF and diagonalization failures

### convergence NOT achieved after N iterations

The most common problem. Try these **in order**.

1. `mixing_beta` 0.7 → 0.3 → 0.1
2. `mixing_mode = 'local-TF'` (metals, slabs, magnets)
3. Raise `electron_maxstep` (200–500)
4. Raise `mixing_ndim` (8 → 12–16, if memory allows)
5. Temporarily raise `degauss`, converge, restart with
   `startingpot='file'` while lowering it
6. `diagonalization = 'cg'` or `'ppcg'` (slow but robust)
7. Inspect the structure (atoms too close)

For DFT+U with `nosym` (MD in particular): the SCF stalls because rotations
among degenerate orbitals keep the density sloshing. Add
`mixing_fixed_ns = 30` (measured in [E13](ex-13-slab-md.html): stuck at
7×10⁻⁵ after 100 iterations without it, converged in 28 with it).

### c_bands: N eigenvalues not converged

- Often ignorable as a warning; repeated occurrences mean diagonalization
  failure.
- Switch `diagonalization`, raise `nbnd` (metals and magnets especially).
- `diago_david_ndim` 2 → 4 can help (more memory).

### cdiaghg: problems computing cholesky / S matrix not positive definite

- The overlap matrix went singular. Usual causes: **atoms too close, a bad
  initial wavefunction, or a linearly dependent basis**.
- Try `startingwfc = 'random'`.
- Recheck the structure: overlapping atoms are more common than you think.

### Not enough space allocated for radial FFT

- A very large cell, or atoms straddling the cell boundary.
- Raise `cell_factor` or move atoms inside the cell.

### checkallsym: some of the original symmetry operations not satisfied

- Atomic motion broke the symmetry detected on the initial structure.
  **In MD you will hit this almost immediately** (thermal motion destroys
  symmetric positions in the first step).
- Set `nosym = .true.` for MD
  ([Chapter 16](16-molecular-dynamics.html)). If it appears during a
  relaxation, the initial symmetry only held to numerical noise; refine the
  structure or use `nosym` there too.

## Parallel, memory, and I/O problems

| Message | Cause | Fix |
|---|---|---|
| `some processors have no planes` | More MPI ranks than FFT planes | Fewer ranks, or larger `-nk` |
| `npool must divide nproc` | Bad `-nk` | Make `nproc` divisible by `-nk` |
| `ndiag must be a square number` | Bad `-nd` | 1, 4, 9, 16, ... |
| `Error in routine davcio` | Disk full, permissions, `outdir` mismatch | Check space and paths |
| `cannot open file ... .save/charge-density.dat` | `prefix`/`outdir` differ from the previous step | Keep them identical along the pipeline |
| Out of memory | `-nk` too large (each pool copies the density) | Lower `-nk`, lower `diago_david_ndim` |

## Silent failures: the most dangerous category

QE prints physically wrong results in a perfectly clean format. Make these
checks habitual.

| Symptom | Hidden cause | Check |
|---|---|---|
| Total energy far from the literature | Different pseudopotential | **Absolute energies are not comparable**; only same-condition differences |
| Magnetic moment collapses to zero | Weak initial magnetization, excess smearing | Raise `starting_magnetization`, lower `degauss` |
| AFM but total magnetization is nonzero | Label split missing; symmetry enforcing FM | Split labels via `ntyp`; check `Sym. Ops.` |
| FeO comes out metallic | GGA self-interaction error | Apply DFT+U; if U alone fails, `starting_ns_eigenvalue` |
| Still metallic with U on | d occupations trapped in a wrong minimum | Steer the pattern with `starting_ns_eigenvalue` |
| `vc-relax` results not reproducible | Pulay stress | Fresh `scf` on the final structure |
| Jagged DOS | Too few nscf k-points | Densify and use the tetrahedron method |
| Weird band path | `crystal_b` convention confusion | Use `tpiba_b` or SeeK-path |
| Slab energy sensitive to vacuum size | Dipole interactions | Enable `dipfield`, add vacuum |
| Forces will not converge | You only converged the energy | Run a separate force-based convergence test |

## A checklist for magnetic transition-metal oxides

Recurring issues in systems like FeO, Fe₂O₃, Fe₃O₄:

- Is `ecutrho` at least 10x `ecutwfc`? (Fe PAW is demanding)
- Are spin-up and spin-down sublattices split into separate labels?
- Is `mixing_beta` at 0.3 or below with `mixing_mode='local-TF'`?
- Did you converge from several initial magnetizations and pick the
  **lowest-energy** solution?
- Is the `HUBBARD` card in the **new syntax** (no `lda_plus_u` remnants)?
- Is the projector (`ortho-atomic` etc.) recorded together with the U value?
- Did you steer the orbital occupations with `starting_ns_eigenvalue`?
- If you use `hp.x`, did you converge the `nq` grid?
- Are cutoffs, k-grid, smearing, and U identical across the whole dataset?

## When you ask for help

Search the
[QE users mailing list archive](https://www.mail-archive.com/users@lists.quantum-espresso.org/)
first. Most problems are already answered, and threads answered by the
developers (Giannozzi, Timrov, and others) are effectively official
documentation.

Always include:

1. The QE version and how it was built
2. The **complete input file**
3. The error section of the output, **with 30 lines of context**
4. What you already tried
