---
title: "E5. fcc Al metal"
---

# E5. fcc Al metal

## Goal

Your first **metal**. See why `occupations='smearing'` is required, where
the Fermi level shows up, and measure how the smearing type and `degauss`
leave their fingerprints on the energy.

## New cards and variables

| Item | Role |
|---|---|
| `occupations='smearing'` | Partial occupations for a metal |
| `smearing='mv'` | Marzari-Vanderbilt (cold): the metal default |
| `degauss` | Smearing width (Ry) |
| `nbnd=8` | A generous band count |

## Input file

[Download al.scf.in](files/E05-al-metal/al.scf.in)

```fortran
! E05: fcc aluminium, the first metal.
! A metal has no gap, so occupations must be smeared around the Fermi level.

&CONTROL
  calculation = 'scf'
  prefix      = 'al'
  outdir      = './tmp/'
  pseudo_dir  = './pseudo/'
  verbosity   = 'high'
/
&SYSTEM
  ibrav       = 2           ! fcc
  celldm(1)   = 7.65        ! bohr (= 4.05 Angstrom, experimental)
  nat         = 1
  ntyp        = 1
  ecutwfc     = 40
  ecutrho     = 320         ! 8x rule
  occupations = 'smearing'  ! mandatory for a metal ('fixed' would abort)
  smearing    = 'mv'        ! Marzari-Vanderbilt cold smearing: free energy ~ E(sigma->0),
                            ! so no extrapolation in degauss is needed
  degauss     = 0.02        ! smearing width in Ry; converge it together with the k-grid
  nbnd        = 8           ! more bands than the default: partial occupations need headroom
/
&ELECTRONS
  conv_thr    = 1.0d-8
  mixing_beta = 0.7         ! simple sp metal: aggressive mixing still works
/

ATOMIC_SPECIES
  Al  26.9815  Al.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (alat)
  Al  0.00  0.00  0.00

! metals need dense grids to resolve the Fermi surface;
! 12x12x12 here vs the 8x8x8 that sufficed for the Si insulator
K_POINTS (automatic)
  12 12 12  0 0 0
```

## Run

```bash
mpirun -np 6 pw.x -nk 6 -in al.scf.in > al.scf.out
```

## What to check: measured

| Item | Measured (QE 7.5, PAW) |
|---|---|
| Total energy | −39.50323368 Ry |
| **Fermi level** | `the Fermi energy is 7.7450 ev`: the badge of a metal |
| `smearing contrib. (-TS)` | The size of the smearing contamination |

Where the insulator ([E1](ex-01-si-scf.html)) printed
`highest occupied level`, the metal prints `the Fermi energy is`.
**This line is itself the diagnosis "the run converged to a metal"**, and
you will meet it again with a twist in [E10](ex-10-feo-afm.html).

## The degauss scan by smearing type: measured

The same system, scanned over smearing types (gaussian/mv/fd) and degauss
(0.005 to 0.05 Ry):

<figure>
  <img src="assets/images/qe-e05-smearing.png"
       alt="Al total energy vs degauss for three smearing types" />
  <figcaption>
    Measured fcc Al (QE 7.5, 12×12×12 k). Cold smearing (mv) moves by only
    0.3 mRy from 0.01 to 0.05 Ry, while gaussian drifts 3 mRy and
    Fermi-Dirac 22 mRy. This is the measured meaning of "mv needs no
    extrapolation".
  </figcaption>
</figure>

One real accident happened during the scan: `mv` at `degauss=0.005` on the
12³ grid integrated the charge to 3.003 instead of 3 and **stopped with
`charge is wrong`**. Narrower smearing demands denser k-grids: degauss and
the k-grid are a **coupled pair** to converge together
([Chapter 06](06-occupations.html)).

## Exercises

1. Sweep the k-grid from 8³ to 16³ and watch the energy scatter per
   degauss. Smaller degauss should demand denser grids.
2. Remove `nbnd` and find in the output how many bands QE picks by itself.
3. Set `occupations='fixed'` and collect the error message in person (the
   exact one listed in [R3](ref-errors.html)).

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Leaving degauss large because "it converges so nicely". A large
    <code>smearing contrib. (-TS)</code> means your result sits far from
    the σ→0 limit. Always check that the property you care about is
    insensitive to degauss. In magnetic metals an oversized degauss erases
    the moment (<a href="ex-09-fe-bcc.html">E9</a>).
  </p>
</div>

## Related chapters

[06 Occupations and smearing](06-occupations.html) ·
[05 Cutoff and k-point convergence](05-convergence.html)
