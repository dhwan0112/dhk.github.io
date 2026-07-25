---
title: "17. Phonons and reaction paths"
---

# 17. Phonons and reaction paths

## Contents
{:.toc-title}

1. TOC
{:toc}

This chapter is a **map, not a manual**. `ph.x` and `neb.x` are each a
book-sized topic, so here we only fix when you will need them and where to
start.

## ph.x: phonons (DFPT)

Computes dynamical matrices by density-functional perturbation theory. You
will need it when:

- **Validating structural stability**: is the optimized structure a true
  minimum (no imaginary frequencies)?
- Vibrational spectra, thermodynamic quantities (free energy, entropy),
  thermal expansion (with `thermo_pw`).
- Electron-phonon coupling.

The skeleton of the workflow:

```
pw.x (scf, very tight conv_thr) → ph.x (&INPUTPH, ldisp=.true., nq grid)
  → q2r.x (real-space force constants) → matdyn.x (dispersion and DOS at any q)
```

The essentials of `&INPUTPH`: `tr2_ph` (response threshold, typically
1.0d-14), `ldisp` with `nq1/nq2/nq3` (the q-grid), `epsil` (dielectric
tensor, needed for LO-TO splitting in polar insulators), `fildyn`. The cost
is heavy, so image parallelism (`-ni`) and `start_q`/`last_q` splitting are
standard practice.

Start with `PHonon/examples/` and a thoroughly converged structure, as in
[Example E6](ex-06-si-vcrelax.html). **Phonons on an under-optimized
structure are full of imaginary modes, and those are a symptom of
non-convergence, not physics.**

## neb.x: reaction paths and barriers

Nudged Elastic Band finds the minimum-energy path and transition state
between two structures. It is the central tool for oxidation mechanisms,
diffusion barriers, and surface reactions.

Its input format differs from `pw.x`: path settings (`&PATH`) and an engine
input (identical to a pw.x input) sit together inside `BEGIN`/`END` blocks.

```
BEGIN
BEGIN_PATH_INPUT
&PATH
  string_method = 'neb'
  num_of_images = 7
  nstep_path    = 100
  opt_scheme    = 'broyden'
  CI_scheme     = 'auto'      ! climbing image: nails the saddle point
  path_thr      = 0.05        ! eV/Å
/
END_PATH_INPUT
BEGIN_ENGINE_INPUT
&CONTROL
 ...                          ! same as a pw.x input
/
BEGIN_POSITIONS
FIRST_IMAGE
ATOMIC_POSITIONS (crystal)
 ...
LAST_IMAGE
ATOMIC_POSITIONS (crystal)
 ...
END_POSITIONS
END_ENGINE_INPUT
END
```

Practical notes:

- **Fully optimize both endpoints first**, then hand them to NEB.
- Start with an odd number of images (5–9) and parallelize over images with
  `-ni`.
- Turn on `CI_scheme='auto'` (climbing image) if you care about the barrier
  height.

## The wider map

| Goal | Tool | Notes |
|---|---|---|
| Localized orbitals, d-band analysis | `pw2wannier90.x` + Wannier90 | Also used for band interpolation |
| Workflow automation | AiiDA + aiida-quantumespresso, ASE, pymatgen | **Effectively mandatory for bulk data generation** |
| Finite-temperature thermodynamics | `thermo_pw` | Built on ph.x |
| Car-Parrinello MD | `cp.x` | A separate code from the BOMD of [Chapter 16](16-molecular-dynamics.html) |

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Building phonons or NEB on top of <strong>unconverged settings</strong>.
    Both methods live off tiny force and energy differences, so any
    looseness in the underlying SCF (its <code>conv_thr</code>, cutoffs,
    k-points) comes back as imaginary modes or jagged paths. Pass the
    program of <a href="05-convergence.html">Chapter 05</a> first.
  </p>
</div>
