---
title: "E12. Computing U with hp.x"
---

# E12. Computing U with hp.x

## Goal

In [E11](ex-11-feo-hubbard.html) the U of 4.6 eV was "a given". This time,
**compute the U by linear response (DFPT)**: no empirical parameters, and a
value that belongs to this system, this pseudopotential, and this
projector. Background in [Chapter 14](14-hubbard-hp.html).

```
pw.x (scf with U ≈ 0, conv_thr 1e-12) → hp.x → FeO.Hubbard_parameters.dat
```

## New cards and variables

| Item | Role |
|---|---|
| A `HUBBARD` card with U = 1.0d-8 | Tells hp.x which atoms and manifolds to perturb (effectively zero U) |
| `conv_thr = 1.0d-12` | Linear response is sensitive to ground-state quality |
| `&INPUTHP` | The hp.x input: `nq1/nq2/nq3`, `conv_thr_chi` |

## Input files

[feo_hp_scf.in](files/E12-feo-hp/feo_hp_scf.in) ·
[feo.hp.in](files/E12-feo-hp/feo.hp.in) ·
[run.sh](files/E12-feo-hp/run.sh)

The scf input is the cell of [E10](ex-10-feo-afm.html) with two changes:

```fortran
&ELECTRONS
  conv_thr         = 1.0d-12    ! very tight: the response matrix inherits this quality
  mixing_beta      = 0.2
  mixing_mode      = 'local-TF'
  electron_maxstep = 300
/
...
! effectively-zero U: registers the Fe-3d manifolds with hp.x without
! biasing the ground state
HUBBARD (ortho-atomic)
U Fe1-3d 1.0d-8
U Fe2-3d 1.0d-8
```

The hp.x input in full:

```fortran
! E12 step 2: hp.x computes the response matrices chi0 and chi by DFPT
! and returns U = chi0^-1 - chi^-1 per Hubbard atom.
&INPUTHP
  prefix       = 'FeO'       ! must match the scf of step 1
  outdir       = './tmp/'
  nq1 = 2, nq2 = 2, nq3 = 2  ! q-point grid for the perturbation; CONVERGE THIS
                             ! (a 1x1x1 U is not trustworthy)
  conv_thr_chi = 1.0d-6      ! chi convergence; 1.0d-8 is unreachable on a metallic
                             ! (GGA) ground state, noise floor ~1e-7 (measured)
  iverbosity   = 2           ! print per-iteration chi values (worth watching)
/
```

A measured note on `conv_thr_chi`: we first ran with 1.0d-8, and even
after the χ values had stabilized to seven digits, the residual kept
bouncing around a noise floor near 10⁻⁷ (checked out to 46 iterations)
without ever crossing the threshold. For systems whose GGA ground state is
metallic, like FeO, that is where the numerical noise of the response
function lives, so we relaxed the threshold to 1.0d-6. The relative
scatter of χ is below 0.1%, which moves U by less than 0.01 eV.

## Run

```bash
#!/bin/bash
# tightly converged scf first, then the hp.x linear-response run
set -e
pw.x -in feo_hp_scf.in > feo_hp_scf.out   # ~3 min on 8 ranks (measured)
hp.x -in feo.hp.in     > feo.hp.out       # ~2 h on 8 ranks, 4 irreducible q (measured)
echo "--- computed Hubbard parameters ---"
cat FeO.Hubbard_parameters.dat
```

hp.x runs one perturbation series per inequivalent Hubbard atom, so it
takes a while (`-nk` pools apply, and q-points can be split with
`start_q`/`last_q`).

## What to check: measured

| Item | Measured (QE 7.5, PAW, ortho-atomic) |
|---|---|
| The preceding scf | −741.81592119 Ry (conv_thr 1e-12, 3 min 15 s) |
| Perturbed atoms | 1 (hp.x recognized Fe2 as symmetry-equivalent and skipped it) |
| **Computed U (Fe-3d)** | **5.2235 eV** (identical for Fe1 and Fe2) |
| Wall time | 1 h 57 min (8 ranks, 2×2×2 q → 4 irreducible q-points) |

`FeO.Hubbard_parameters.dat` lists the per-atom U along with the full χ₀
and χ matrices. The computed U = 5.22 eV sits 0.6 eV above the
conventional 4.6 eV used in [E11](ex-11-feo-hubbard.html). Neither number
is "the right one" in isolation; the pair illustrates that U only has
meaning together with its projector, pseudopotential, and magnetic order.
The principle: for your own system, use the U computed for it.

## Exercises

1. Change `nq` from 1×1×1 to 2×2×2 and watch U shift. A U without q-grid
   convergence cannot be trusted.
2. Put the computed U into the HUBBARD card of
   [E11](ex-11-feo-hubbard.html) and see how the moments and DOS respond.
3. Iterate scf → hp.x once more with the new U (self-consistent U) and
   check that the value stabilizes.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Leaving the preceding scf at the everyday
    <code>conv_thr</code> of 1.0d-8: the noise leaks into the response
    matrix and swings U. Keep the 1.0d-12. And running hp.x without a
    <code>HUBBARD</code> card fails outright, because the code cannot know
    which atoms to perturb; give it at least the tiny 1.0d-8 U.
  </p>
</div>

## Related chapters

[14 Computing U with hp.x](14-hubbard-hp.html) ·
[13 DFT+U and the HUBBARD card](13-dft-plus-u.html)
