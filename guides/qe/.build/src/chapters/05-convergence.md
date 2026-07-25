---
title: "05. Cutoff and k-point convergence"
---

# 05. Cutoff and k-point convergence

## Contents
{:.toc-title}

1. TOC
{:toc}

**This chapter is half of QE.** A number that has not passed a convergence
test is not a number, and QE will print physically wrong results in a
perfectly clean format.

## The standard procedure

1. **Converge `ecutwfc`.** Fix a reasonable k-grid and scan the cutoff from
   20 to 80 Ry. Judge by the **energy change per atom** (typically within
   1–5 meV/atom), not by the absolute total energy.
2. **Converge `ecutrho`.** For US/PAW, fix `ecutwfc` and scan from 4x to 12x.
3. **Converge the k-grid.** Fix the cutoffs and densify the grid. Metals need
   far denser grids than insulators.
4. **Converge `degauss`** (metals only). Check the behavior toward the
   σ → 0 limit ([Chapter 06](06-occupations.html)).

Convert Ry to meV/atom when judging:

$$\Delta E\,[\mathrm{meV/atom}] = \frac{|E(n) - E(n_{\max})| \times 13605.7}{N_\mathrm{at}}$$

Typical thresholds:

| Goal | Criterion |
|---|---|
| Total-energy differences (phase stability etc.) | 1–5 meV/atom |
| **Forces (ML potential training data)** | ~1 meV/Å per force component (≈ 2×10⁻⁵ Ry/bohr) |
| Stress (before any `vc-relax`) | ~0.1 kbar |

## Measured: convergence behavior of PAW silicon

Below are the measured curves from [Example E3](ex-03-convergence.html),
using the bundled scripts on silicon (PAW, with `ecutrho = 8 × ecutwfc`
scanned together).

<figure>
  <img src="assets/images/qe-e03-convergence.png"
       alt="Si convergence: total energy vs ecutwfc and k-grid, force vs ecutwfc" />
  <figcaption>
    Measured silicon convergence (QE 7.5, PAW). Left: the cutoff scan drops
    below 1 meV/atom at 40 Ry. Center: the k-grid scan; as an insulator,
    6×6×6 is already decent. Right: force convergence on a distorted
    structure, which lags the energy.
  </figcaption>
</figure>

## Common misconceptions

- **Absolute total energies have a different zero for every pseudopotential,
  so comparing them is meaningless.** Only differences computed under
  identical conditions matter.
- **A converged energy does not imply converged forces, stress, or DOS.**
  Verify convergence for the property you actually care about (an energy
  difference? forces? a band gap? a magnetic moment?). For ML training data,
  converge on **forces**.
- **Monotonic convergence in the cutoff is guaranteed by the variational
  principle; monotonic convergence in the k-grid is not.** Non-monotonic
  k-point behavior is normal.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Running one convergence test and declaring "this element needs 40 Ry"
    forever. Cutoff requirements attach to the <strong>pseudopotential
    file</strong>, not to the element. New potential, new test. And if a
    project mixes very different structures (bulk, surface, molecule),
    standardize on the settings demanded by the most demanding one.
  </p>
</div>

## Practical sense for k-grids

- In `K_POINTS (automatic)`, the six numbers are the Monkhorst-Pack grid
  `nk1 nk2 nk3` and shifts `s1 s2 s3`. A shift of `1` (half-step offset) can
  speed convergence for insulators at equal density. However, **any nscf
  that will use the tetrahedron method must have an unshifted, Γ-centered
  grid**.
- Scale the grid inversely with cell size. Large cells (slabs, supercells)
  need fewer points; one point suffices along a vacuum direction.
- Metals need dense grids to resolve the Fermi surface. See the 12×12×12 in
  [Example E5](ex-05-al-metal.html) and 16×16×16 in
  [Example E9](ex-09-fe-bcc.html).

## Related examples

- [E3 · Automating convergence tests](ex-03-convergence.html): this chapter's
  procedure, scripted and measured.
- [E5 · fcc Al metal](ex-05-al-metal.html): k-point and degauss convergence
  in a metal.
