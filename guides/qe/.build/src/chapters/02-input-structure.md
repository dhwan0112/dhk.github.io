---
title: "02. Input file structure"
---

# 02. Input file structure

## Contents
{:.toc-title}

1. TOC
{:toc}

## Two layers: namelists and cards

A `pw.x` input consists of two kinds of blocks.

- **Namelists**: Fortran namelists such as `&CONTROL`, `&SYSTEM`,
  `&ELECTRONS`, opened with `&NAME` and closed with `/`. Entries are
  `variable = value`, and the order is fixed:
  `&CONTROL → &SYSTEM → &ELECTRONS → (&IONS) → (&CELL)`.
- **Cards**: blocks such as `ATOMIC_SPECIES`, `ATOMIC_POSITIONS`,
  `K_POINTS`, `CELL_PARAMETERS`, and `HUBBARD`, with an uppercase title
  followed by tabular data. They come after the namelists, and some take a
  unit or option in parentheses, as in `ATOMIC_POSITIONS (crystal)`.

Strings use single quotes (`'scf'`), logicals are `.true.`/`.false.`, and
comments start with `!`.

## A minimal input, dissected: the silicon SCF

Make your first calculation a **simple semiconductor like silicon**. If you
jump straight to an Fe system, you cannot tell whether a convergence failure
is physics or a setup error.

```fortran
&CONTROL
  calculation  = 'scf'        ! scf / nscf / bands / relax / vc-relax / md
  prefix       = 'si'         ! output prefix (must match follow-up runs)
  outdir       = './tmp/'
  pseudo_dir   = './pseudo/'
  verbosity    = 'high'       ! always 'high' while learning
  tprnfor      = .true.       ! print forces
  tstress      = .true.       ! print stress
/
&SYSTEM
  ibrav        = 2            ! fcc; 0 means CELL_PARAMETERS given explicitly
  celldm(1)    = 10.26        ! bohr (= 5.43 Å)
  nat          = 2
  ntyp         = 1
  ecutwfc      = 30           ! Ry, wavefunction cutoff
  ecutrho      = 240          ! Ry, density cutoff (8x for PAW/US)
  occupations  = 'fixed'      ! insulator/semiconductor
/
&ELECTRONS
  conv_thr     = 1.0d-8       ! Ry
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

What each block is responsible for:

| Block | Role | Details |
|---|---|---|
| `&CONTROL` | What to compute and where to write it | Calculation types: [Chapter 08](08-scf-nscf.html), [Chapter 09](09-relaxation.html) |
| `&SYSTEM` | What the system is (cell, atoms, basis, occupations) | Units and coordinates: [Chapter 03](03-units-coordinates.html); occupations: [Chapter 06](06-occupations.html) |
| `&ELECTRONS` | How to converge the SCF | [Chapter 07](07-scf-control.html) |
| `ATOMIC_SPECIES` | Label, mass, pseudopotential file | [Chapter 04](04-pseudopotentials.html) |
| `ATOMIC_POSITIONS` | Atomic coordinates (plus optional `if_pos` flags) | [Chapter 03](03-units-coordinates.html) |
| `K_POINTS` | Brillouin-zone sampling | [Chapter 05](05-convergence.html) |

Full card syntax is collected in the
[R2 card reference](ref-cards.html).

## Running it

```bash
pw.x -in si.scf.in > si.scf.out                       # serial
mpirun -np 8 pw.x -nk 4 -in si.scf.in > si.scf.out    # parallel, 4 k-point pools
```

Output goes to standard output, so redirect it with `>`. Intermediate files
accumulate in `outdir/prefix.save/`, and follow-up runs (nscf,
post-processing) locate that directory through the **same `prefix` and
`outdir`**.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Forgetting the closing <code>/</code> of a namelist raises
    <code>namelist not found</code>. Double quotes around strings and bare
    <code>true</code> for logicals are classic parse failures. A typo in a
    card name shows up as <code>Error in routine card_xxx</code>. Input
    syntax errors in general are collected in the
    <a href="ref-errors.html">R3 error dictionary</a>.
  </p>
</div>

## Related examples

- [E1 · Si SCF](ex-01-si-scf.html): run exactly this input and read the output.
- [E2 · Rewriting with ibrav=0](ex-02-si-ibrav0.html): the same system in a
  different syntax.
