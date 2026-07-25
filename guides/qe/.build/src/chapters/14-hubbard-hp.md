---
title: "14. Computing U with hp.x"
---

# 14. Computing U with hp.x

## Contents
{:.toc-title}

1. TOC
{:toc}

Instead of copying a U value from the literature, you can **compute the U
appropriate to your own system by linear response (DFPT)**. The tool is
`hp.x` (Timrov, Cococcioni, Marzari,
*Comput. Phys. Commun.* **2022**, *279*, 108455), and the result is far
easier to defend methodologically.

## The principle in one line

Hubbard U is defined by how strongly the system pushes back when the
occupation of the localized manifold is perturbed. `hp.x` computes that
response matrix χ with density-functional perturbation theory and returns
the screened interaction

$$U = (\chi_0^{-1} - \chi^{-1})$$

with no empirical input.

## Workflow

```
pw.x (scf with a tiny U, conv_thr 1e-12) → hp.x → prefix.Hubbard_parameters.dat
```

**Step 1.** Use the input of [Example E11](ex-11-feo-hubbard.html) with the
U set to a negligible value. The **HUBBARD card must be present** so hp.x
knows which atoms and manifolds to perturb.

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 1.0d-8
U Fe2-3d 1.0d-8
```

Set `conv_thr` in `&ELECTRONS` to about `1.0d-12`; linear response is
sensitive to the quality of the ground-state density.

**Step 2.** The `hp.x` input (`&INPUTHP`):

```fortran
&INPUTHP
  prefix       = 'FeO'
  outdir       = './tmp/'
  nq1 = 2, nq2 = 2, nq3 = 2
  conv_thr_chi = 1.0d-6
  iverbosity   = 2
/
```

```bash
pw.x -in feo_hp_scf.in > feo_hp_scf.out
hp.x -in feo.hp.in     > feo.hp.out
cat FeO.Hubbard_parameters.dat
```

The result file lists U per atom. The measured numbers are in
[Example E12](ex-12-feo-hp.html).

`conv_thr_chi` is the convergence threshold for the response function χ. In
systems whose GGA ground state is metallic (FeO is one), the numerical
noise floor of χ sits around 10⁻⁷, so 1.0d-8 may never be reached; the
measured evidence is in [Example E12](ex-12-feo-hp.html).

## Cautions

- **Convergence testing over the `nq` grid is mandatory.** A U from 1×1×1
  cannot be trusted, and the k-grid of the underlying scf must be converged
  along with it.
- `hp.x` is expensive. The number of perturbations scales with the number of
  inequivalent Hubbard atoms, and each perturbation runs a linear-response
  cycle per q-point. `-nk` pool parallelism applies, and q-points can be
  split across jobs with `start_q`/`last_q`.
- Feeding the computed U back into the HUBBARD card and repeating
  scf → hp.x gives a **self-consistent U**; one or two rounds usually
  stabilize it.
- If you split labels (`Fe1`/`Fe2`), hp.x recognizes symmetry-equivalent
  atoms and skips redundant perturbations.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Transplanting an hp.x U into a run with a <strong>different projector or
    pseudopotential</strong>. U is meaningful only within the conditions it
    was computed for (projector, pseudopotential, magnetic order). Also, a
    loose <code>conv_thr</code> on the preceding scf injects noise into the
    response matrix and swings U by whole eV: keep the 1.0d-12.
  </p>
</div>

## Related examples

- [E12 · Computing U with hp.x](ex-12-feo-hp.html): the measured U for FeO.
- [E11 · FeO with DFT+U](ex-11-feo-hubbard.html): where the U gets used.
