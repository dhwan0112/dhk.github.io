---
title: "E10. FeO AFM (where GGA fails)"
---

# E10. FeO AFM (where GGA fails)

## Goal

The gateway example for antiferromagnetic oxides. Build the AFM-II order of
rocksalt FeO (alternating (111) spin planes) by **splitting one element
into two labels**, and then watch GGA (PBE) predict a **metal** for a
material that experiment says is an insulator with a gap of about 2.4 eV.
Seeing this failure with your own eyes is the motivation for
[E11 (DFT+U)](ex-11-feo-hubbard.html).

## New cards and variables

| Item | Role |
|---|---|
| `ntyp=3` (Fe1/Fe2/O) | **The same UPF under two labels**: the key to AFM |
| `starting_magnetization` ±0.6 | Fe1 up, Fe2 down |
| `ibrav=0` + rhombohedral magnetic cell | 2 Fe + 2 O, volume = 0.5 a³ |
| `mixing_beta=0.2` + `local-TF` | The mixing prescription for a touchy magnetic oxide |

## Input file

[Download feo.scf.in](files/E10-feo-afm/feo.scf.in)

```fortran
! E10: FeO in the rocksalt structure with AFM-II order
! (ferromagnetic (111) planes with alternating sign).
! The magnetic unit cell is rhombohedral: 2 Fe + 2 O, volume = 0.5 a^3.
! THE POINT of this run: the AFM order converges beautifully, and GGA
! still predicts a metal. Experiment says insulator, gap ~2.4 eV.

&CONTROL
  calculation = 'scf'
  prefix      = 'FeO'
  outdir      = './tmp/'
  pseudo_dir  = './pseudo/'
  verbosity   = 'high'        ! also prints the ns matrices once U is on (E11)
  tprnfor     = .true.
  tstress     = .true.
/
&SYSTEM
  ibrav       = 0             ! cell given explicitly below
  celldm(1)   = 8.18          ! cubic a in bohr (= 4.33 Angstrom); scales CELL_PARAMETERS (alat)
  nat         = 4
  ntyp        = 3             ! Fe1, Fe2, O: the label split that makes AFM possible
  ecutwfc     = 70
  ecutrho     = 700           ! the 10x Fe rule again
  occupations = 'smearing'    ! the GGA ground state is (wrongly) metallic, so smear
  smearing    = 'mv'
  degauss     = 0.01
  nspin       = 2
  starting_magnetization(1) =  0.6    ! Fe1 sublattice: up
  starting_magnetization(2) = -0.6    ! Fe2 sublattice: down  -> AFM seed
  starting_magnetization(3) =  0.0    ! O: no seed
/
&ELECTRONS
  conv_thr    = 1.0d-8
  mixing_beta = 0.2           ! touchy magnetic oxide: mix gently
  mixing_mode = 'local-TF'
  electron_maxstep = 300
/

! the SAME pseudopotential file under two labels: without this split QE
! treats the two Fe as symmetry-equivalent and no AFM state can form
ATOMIC_SPECIES
  Fe1  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
  Fe2  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
  O    15.999  O.pbe-n-kjpaw_psl.1.0.0.UPF

! rhombohedral doubling of the fcc cell along [111], in units of alat:
! these three vectors hold two rocksalt formula units, so that the two Fe
! (111) planes can carry opposite spins. det = 0.5 -> volume 0.5 a^3.
CELL_PARAMETERS (alat)
  0.5  0.5  1.0
  0.5  1.0  0.5
  1.0  0.5  0.5

! fractional coordinates: Fe at 0 and 1/2 along the cell diagonal are the
! two oppositely magnetized (111) planes; O sits between them
ATOMIC_POSITIONS (crystal)
  Fe1  0.00  0.00  0.00
  Fe2  0.50  0.50  0.50
  O    0.25  0.25  0.25
  O    0.75  0.75  0.75

K_POINTS (automatic)
  6 6 6  0 0 0
```

Without the label split, QE treats the two Fe atoms as
symmetry-equivalent and cannot form AFM order at all. The same split is
required later by [DFT+U (E11)](ex-11-feo-hubbard.html) and
[hp.x (E12)](ex-12-feo-hp.html).

## Run

```bash
mpirun -np 8 pw.x -nk 4 -in feo.scf.in > feo.scf.out
```

## What to check: measured (the real point of this example)

| Item | Measured (QE 7.5, PAW) | Reading |
|---|---|---|
| Total energy | −741.81592118 Ry (28 iterations) | |
| total magnetization | **0.00 μB** | AFM established |
| absolute magnetization | **7.17 μB** | total ≈ 0 with large absolute: the AFM badge |
| Fe local moments | +3.31 / −3.31 μB | The alternating (111) arrangement confirmed |
| O moment | 0.00 | |
| **`the Fermi energy is 14.2231 ev`** | **printed, so a metal** | **The GGA failure.** Experiment: an insulator (~2.4 eV) |

<figure>
  <img src="assets/images/qe-e10-e11-feo-dos.png"
       alt="FeO spin-resolved DOS: GGA metallic vs GGA+U" />
  <figcaption>
    Measured spin-resolved DOS of FeO (QE 7.5, nscf 8×8×8). Left (this
    example, GGA): Fe-3d states sit right at the Fermi level with
    DOS(E_F) ≈ 3.7, a metal. The right panel is
    <a href="ex-11-feo-hubbard.html">E11</a> with U on, showing the Hubbard
    splitting and the narrow-band trap that survives it.
  </figcaption>
</figure>

The AFM order itself came out perfectly (moments ±3.31 μB), yet the
electronic structure is metallic. That is the self-interaction error of
GGA delocalizing the Fe-3d electrons, and it is why the U correction
exists ([Chapter 13](13-dft-plus-u.html)).

## Exercises

1. Run the PDOS pipeline of [E7](ex-07-si-dos.html) and confirm that the
   states at the Fermi level are Fe-3d.
2. Converge the ferromagnetic arrangement (both +0.6) and compare its
   energy with AFM. Which is the ground state?
3. Verify by determinant that the cell really holds 2 formula units
   (volume = 0.5 a³).
4. Set all `starting_magnetization` to zero. Which solution do you land
   in?

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Keeping <code>ntyp=2</code> (Fe/O) and giving ± initial moments:
    atoms of one type share one initial magnetization, so no AFM forms.
    And if you built "AFM" but the total magnetization is not zero,
    suspect a failed label split or symmetry enforcing FM
    (<a href="ref-errors.html">R3</a>, silent failures).
  </p>
</div>

## Related chapters

[12 Spin polarization and magnetism](12-magnetism.html) ·
[13 DFT+U and the HUBBARD card](13-dft-plus-u.html) ·
[07 Controlling SCF convergence](07-scf-control.html)
