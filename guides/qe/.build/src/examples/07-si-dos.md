---
title: "E7. Si DOS and PDOS"
---

# E7. Si DOS and PDOS

## Goal

Run the density-of-states pipeline end to end: scf → nscf → `dos.x` →
`projwfc.x`. Learn in your fingers that **order and matching
`prefix`/`outdir` are everything**, and read the Löwdin charges at the end.

```
scf (8³ k) ─→ nscf (16³ k, tetrahedra) ─┬─→ dos.x       (total DOS)
                                         └─→ projwfc.x   (PDOS + Löwdin)
```

## New cards and variables

| Item | Role |
|---|---|
| `calculation='nscf'` + `occupations='tetrahedra'` | Dense-grid eigenvalues on a frozen density ([Chapter 08](08-scf-nscf.html)) |
| `nbnd=12` | Enough bands to cover the conduction region |
| `&DOS` (dos.x) | Emin/Emax/DeltaE |
| `&PROJWFC` (projwfc.x) | PDOS decomposition, Löwdin |

## Input files

[si.scf.in](files/E07-si-dos/si.scf.in) ·
[si.nscf.in](files/E07-si-dos/si.nscf.in) ·
[si.dos.in](files/E07-si-dos/si.dos.in) ·
[si.projwfc.in](files/E07-si-dos/si.projwfc.in) ·
[run.sh](files/E07-si-dos/run.sh)

The nscf input in full (the scf is E1's, run under the same prefix):

```fortran
! E07 step 2: non-self-consistent run on a dense grid.
! Reads the frozen charge density of the scf (same prefix/outdir) and
! only recomputes eigenvalues, which is what a smooth DOS needs.

&CONTROL
  calculation = 'nscf'
  prefix      = 'si'          ! MUST match the scf
  outdir      = './tmp/'      ! MUST match the scf
  pseudo_dir  = './pseudo/'
  verbosity   = 'high'
/
&SYSTEM
  ibrav       = 2
  celldm(1)   = 10.26
  nat         = 2
  ntyp        = 1
  ecutwfc     = 30
  ecutrho     = 240
  nbnd        = 12                ! extra empty bands so the conduction DOS exists
  occupations = 'tetrahedra'      ! exact BZ integration for the DOS.
                                  ! ('tetrahedra_opt' makes projwfc.x write zero PDOS on QE 7.5)
/
&ELECTRONS
  conv_thr    = 1.0d-8
/

ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (alat)
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25

! the tetrahedron method requires a Gamma-centered, UNSHIFTED grid;
! 16^3 is dense enough for a smooth Si DOS
K_POINTS (automatic)
  16 16 16  0 0 0
```

<div class="warning">
  <div class="note-title">Measured note: tetrahedra_opt and projwfc.x</div>
  <p>
    We first ran this with the optimized tetrahedron method,
    <code>occupations='tetrahedra_opt'</code>, and found that on
    <strong>QE 7.5 dos.x and the Löwdin charges are fine but projwfc.x
    writes PDOS files that are entirely zero</strong> (serial or parallel,
    with or without lsym). Rerunning the nscf with the classic
    <code>'tetrahedra'</code> restores the PDOS. The distributed input
    therefore uses <code>'tetrahedra'</code>.
  </p>
</div>

The two post-processor inputs:

```fortran
! E07 step 3: dos.x sums the nscf eigenvalues into the total DOS.
! Output columns of 'si.dos': E (eV) | DOS | integrated DOS.
&DOS
  prefix = 'si'      ! same chain as before
  outdir = './tmp/'
  fildos = 'si.dos'  ! output file
  Emin   = -10.0     ! energy window in ABSOLUTE eV (not relative to E_F!);
  Emax   =  20.0     ! Si's valence bands sit near -6..+6 eV here, so this covers them
  DeltaE =  0.05     ! energy grid spacing in eV
/
```

```fortran
! E07 step 4: projwfc.x projects the states onto atomic orbitals.
! Products: one PDOS file per atom and orbital plus the Lowdin charges
! printed at the end of standard output.
&PROJWFC
  prefix  = 'si'
  outdir  = './tmp/'
  filpdos = 'si.pdos'   ! basename of the PDOS files
  ngauss  = 0           ! 0 = plain Gaussian broadening of the projections
  degauss = 0.01        ! broadening width, in Ry
  Emin    = -10.0       ! same absolute-eV window convention as dos.x
  Emax    =  20.0
  DeltaE  =  0.05
  lsym    = .true.      ! symmetrize the projections (recommended)
/
```

## Run

```bash
#!/bin/bash
# The whole pipeline in order; everything is glued by prefix + outdir.
set -e
pw.x       -in si.scf.in     > si.scf.out      # 1. converge the density
pw.x       -in si.nscf.in    > si.nscf.out     # 2. dense-grid eigenvalues
dos.x      -in si.dos.in     > si.dos.out      # 3. total DOS -> si.dos
projwfc.x  -in si.projwfc.in > si.projwfc.out  # 4. PDOS + Lowdin charges
grep -A20 'Lowdin Charges' si.projwfc.out      # show the per-orbital occupations
```

## Output and figure: measured

<figure>
  <img src="assets/images/qe-e07-dos-pdos.png"
       alt="Si total DOS with s/p projected DOS" />
  <figcaption>
    Measured silicon total DOS with s/p PDOS (QE 7.5, nscf 16×16×16,
    tetrahedra). The lower valence band (−12 to −8 eV) is s-dominated, the
    upper is p-dominated, and the gap is clean.
  </figcaption>
</figure>

Decoding the output files:

- `si.dos`: E (eV), DOS, integrated DOS. The integral should hit exactly 8
  (the valence electron count) at the top of the valence bands: a built-in
  sanity check.
- `si.pdos.pdos_atm#1(Si)_wfc#2(p)`: the p-projected DOS of atom 1.
- **Löwdin charges, measured**: 3.9637 e per atom (s 1.1617 + p 2.8020),
  spilling parameter 0.0091. The gap to the 4 valence electrons (the
  spilling) is the part of the plane-wave states the atomic-orbital basis
  cannot represent. Keep the same caveat in mind when reading Fe d
  occupations and moments.

## Exercises

1. Sweep the nscf grid from 8³ to 24³ and watch the DOS smooth out.
2. Replace `'tetrahedra'` with `'smearing'` and see how the DOS washes out.
   What happens to the PDOS if you try `'tetrahedra_opt'`?
3. Verify that column 3 of `si.dos` (the integrated DOS) reaches 8 at the
   valence-band top.
4. Compare the Löwdin total to the valence electron count and think about
   what the difference (the spilling) means.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Leaving a shift (<code>1 1 1</code>) on the nscf
    <code>K_POINTS</code>: the tetrahedron method demands a Γ-centered
    grid, and you get an error or quietly different numbers. And a single
    character of mismatch in <code>prefix</code>/<code>outdir</code> breaks
    the pipeline with <code>cannot open file ... .save</code>
    (<a href="ref-errors.html">R3</a>).
  </p>
</div>

## Related chapters

[10 DOS and band structure](10-dos-bands.html) ·
[08 SCF and NSCF](08-scf-nscf.html)
