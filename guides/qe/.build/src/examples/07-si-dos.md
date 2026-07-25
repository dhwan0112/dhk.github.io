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

The heart of the nscf input:

```fortran
&SYSTEM
  ...
  nbnd = 12                   ! cover the conduction bands
  occupations = 'tetrahedra'  ! tetrahedron method (see the note below)
/
K_POINTS (automatic)
  16 16 16  0 0 0             ! tetrahedra require a Γ-centered, unshifted grid
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

The `dos.x` input:

```fortran
&DOS
  prefix = 'si'
  outdir = './tmp/'
  fildos = 'si.dos'
  Emin   = -10.0
  Emax   =  20.0
  DeltaE =  0.05
/
```

## Run

```bash
pw.x       -in si.scf.in     > si.scf.out
pw.x       -in si.nscf.in    > si.nscf.out
dos.x      -in si.dos.in     > si.dos.out
projwfc.x  -in si.projwfc.in > si.projwfc.out
grep -A20 'Lowdin Charges' si.projwfc.out
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
