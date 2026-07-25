---
title: "E4. O₂ molecule (triplet)"
---

# E4. O₂ molecule (triplet)

## Goal

Learn to treat an **isolated molecule** in a periodic code: a vacuum box, a
Γ-only calculation, periodic-image corrections, and pinning the spin state.
The ground state of O₂ is a triplet (S=1), and if you work on Fe–O systems
this molecule is a mandatory reference. It is also the famous case of GGA
badly overbinding O₂, which you will measure yourself.

## New cards and variables

| Item | Role |
|---|---|
| `K_POINTS gamma` | Γ only: no dispersion for a molecule, plus the real-wavefunction speedup |
| `assume_isolated='mt'` | Martyna-Tuckerman periodic-image correction |
| `nspin=2` + `tot_magnetization` | Spin polarization plus a **constrained** total moment (enforcing the triplet) |
| `ibrav=1` + a large `celldm(1)` | The vacuum box (20 bohr) |

## Input files

[o2.scf.in](files/E04-o2-molecule/o2.scf.in) ·
[o_atom.scf.in](files/E04-o2-molecule/o_atom.scf.in)

```fortran
&CONTROL
  calculation       = 'scf'
  prefix            = 'o2'
  outdir            = './tmp/'
  pseudo_dir        = './pseudo/'
  verbosity         = 'high'
  tprnfor           = .true.
/
&SYSTEM
  ibrav             = 1
  celldm(1)         = 20.0        ! bohr, the vacuum box
  nat               = 2
  ntyp              = 1
  ecutwfc           = 60
  ecutrho           = 480
  assume_isolated   = 'mt'        ! Martyna-Tuckerman image correction
  nspin             = 2
  tot_magnetization = 2.0         ! enforce the triplet (two Fermi levels)
  occupations       = 'smearing'
  smearing          = 'gaussian'
  degauss           = 0.001
/
&ELECTRONS
  conv_thr          = 1.0d-8
  mixing_beta       = 0.3
/

ATOMIC_SPECIES
  O  15.9994  O.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (angstrom)
  O  0.000  0.000  0.000
  O  0.000  0.000  1.210

K_POINTS gamma
```

The atomic input (`o_atom.scf.in`) is the same box and cutoffs with
`nat=1` and `tot_magnetization=2.0` (the ³P ground state of atomic O).

## Run

```bash
mpirun -np 6 pw.x -in o2.scf.in     > o2.scf.out
mpirun -np 6 pw.x -in o_atom.scf.in > o_atom.scf.out
```

With a single Γ point, `-nk` pools are pointless; only the G-vector split
applies.

## What to check: measured

| Item | Measured (QE 7.5, PAW) |
|---|---|
| E(O₂) | −83.03824491 Ry |
| E(O atom) | −41.26799048 Ry |
| total magnetization | 2.00 μB (the constrained value) |
| absolute magnetization | 2.05 μB (slightly above 2 because the spin density is spatially spread; normal) |
| **Binding energy D = 2E(O) − E(O₂)** | **0.50226 Ry = 6.83 eV** |

The experimental binding energy is 5.12 eV: **PBE overbinds by about
1.7 eV**, measured live. This is why oxide formation energies computed
against O₂ need corrections, the origin of the "O₂ correction" you see in
the literature.

`tot_magnetization` vs `starting_magnetization`:

| Variable | Meaning | When |
|---|---|---|
| `starting_magnetization(i)` | An **initial guess**; the SCF may change it | Most cases |
| `tot_magnetization` | **Constrains** the cell moment; separate up/down Fermi levels | When a specific spin state must be enforced |

## Exercises

1. Set `tot_magnetization = 0.0` (singlet) and compare energies. By how
   much is the triplet more stable?
2. Grow the box from 20 to 25 bohr. How much does the energy move (vacuum
   convergence)?
3. Remove `assume_isolated`. How large is the image interaction you just
   uncovered?
4. Scan the bond length from 1.16 to 1.26 Å, find the equilibrium, and
   compare with the experimental 1.21 Å.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Running the molecule with <code>occupations='fixed'</code>. Systems with
    intrinsic partial occupations (the degenerate π* of O₂) need a little
    smearing for stability even with the spin state pinned (here degauss
    0.001 Ry). And a too-small box leaves image interactions that even
    <code>assume_isolated</code> cannot fully remove: the box size is a
    convergence parameter too.
  </p>
</div>

## Related chapters

[06 Occupations and smearing](06-occupations.html) ·
[12 Spin polarization and magnetism](12-magnetism.html)
