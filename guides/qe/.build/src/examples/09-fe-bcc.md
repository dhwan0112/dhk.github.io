---
title: "E9. Ferromagnetic bcc Fe"
---

# E9. Ferromagnetic bcc Fe

## Goal

Your first **magnetic** calculation. Converge the ferromagnetic ground
state of bcc Fe with a spin-polarized SCF (`nspin=2`) and compare the
moment with experiment. This is the hands-on version of the metal-plus-
magnetism convergence craft of [Chapter 12](12-magnetism.html).

## New cards and variables

| Item | Role |
|---|---|
| `nspin=2` + `starting_magnetization` | Collinear polarization with an initial guess (a ratio, −1 to 1) |
| `mixing_beta=0.3` + `mixing_mode='local-TF'` | The mixing prescription for magnetic metals |
| `ecutrho = 10×ecutwfc` | The heavy density cutoff Fe PAW demands |

## Input file

[Download fe.scf.in](files/E09-fe-bcc/fe.scf.in)

```fortran
! E09: ferromagnetic bcc iron. Metal + magnetism, the convergence
! combination that transition-metal oxides are made of.

&CONTROL
  calculation = 'scf'
  prefix      = 'fe'
  outdir      = './tmp/'
  pseudo_dir  = './pseudo/'
  verbosity   = 'high'
/
&SYSTEM
  ibrav       = 3               ! bcc
  celldm(1)   = 5.42            ! bohr (= 2.87 Angstrom, experimental)
  nat         = 1
  ntyp        = 1
  ecutwfc     = 70              ! Fe semicore PAW is demanding
  ecutrho     = 700             ! 10x, not 8x: Fe needs it
  occupations = 'smearing'
  smearing    = 'mv'
  degauss     = 0.02
  nspin       = 2               ! collinear spin polarization
  starting_magnetization(1) = 0.7   ! INITIAL GUESS, a dimensionless ratio in [-1,1]
                                    ! (not Bohr magnetons); the SCF refines it
/
&ELECTRONS
  conv_thr    = 1.0d-8
  mixing_beta = 0.3             ! magnetic metals need gentle mixing
  mixing_mode = 'local-TF'      ! and the local-TF preconditioner
  electron_maxstep = 200        ! allow more iterations than the default 100
/

ATOMIC_SPECIES
  Fe  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (alat)
  Fe  0.00  0.00  0.00

! a dense grid: the Fermi surface of a magnetic metal needs resolution
K_POINTS (automatic)
  16 16 16  0 0 0
```

## Run

```bash
mpirun -np 6 pw.x -nk 6 -in fe.scf.in > fe.scf.out
```

## What to check: measured

| Item | Measured (QE 7.5, PAW) | Note |
|---|---|---|
| Total energy | −329.26290531 Ry | |
| **total magnetization** | **2.19 μB/cell** | Experiment 2.22 μB: PBE nearly nails it |
| absolute magnetization | 2.32 μB/cell | Close to total, so FM |
| Fermi level | 17.4481 eV | A metal |

Total ≈ absolute is the badge of ferromagnetism. For AFM the total is near
zero while the absolute stays large; that case is
[E10](ex-10-feo-afm.html).

## Spin-resolved DOS: an extra measurement

On top of the same density we ran an nscf (20³, tetrahedra) plus `dos.x`
to get the spin-resolved DOS (dos.x prints up and down columns for
polarized runs).

<figure>
  <img src="assets/images/qe-e09-fe-dos.png"
       alt="bcc Fe spin-resolved DOS" />
  <figcaption>
    Measured spin-resolved DOS of bcc Fe (QE 7.5, PBE). Exchange splitting
    pushes the majority (up) d band down to near-full occupation while the
    minority (down) d band straddles the Fermi level. The occupation
    difference is exactly the 2.2 μB moment.
  </figcaption>
</figure>

## Exercises

1. Set `starting_magnetization = 0.0`. Does the run collapse to the
   nonmagnetic solution?
2. Compare with a `nspin=1` run and extract the magnetic stabilization
   energy.
3. Run the PDOS pipeline of [E7](ex-07-si-dos.html), observe the exchange
   splitting of the up/down d bands, read the local moment from the Löwdin
   charges, and compare with the cell magnetization.
4. Raise `degauss` to 0.05. What happens to the moment?

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Declaring the first converged solution the ground state. Magnets hold
    several metastable solutions; converge from several initial
    magnetizations (0.3 / 0.7 / −0.7) and compare energies. And remember,
    <code>starting_magnetization</code> is a <strong>ratio</strong>, not
    μB (<a href="03-units-coordinates.html">Chapter 03</a>).
  </p>
</div>

## Related chapters

[12 Spin polarization and magnetism](12-magnetism.html) ·
[07 Controlling SCF convergence](07-scf-control.html)
