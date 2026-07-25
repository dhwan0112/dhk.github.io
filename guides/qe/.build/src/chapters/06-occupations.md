---
title: "06. Occupations and smearing"
---

# 06. Occupations and smearing

## Contents
{:.toc-title}

1. TOC
{:toc}

Ninety percent of convergence trouble in metals and magnets traces back to
how occupations are handled. Choosing `occupations` is the physical judgment
"is this system an insulator or a metal?"

## occupations, by system type

| Value | Meaning | Use for |
|---|---|---|
| `'fixed'` | Integer occupations; requires a gap | Insulators and semiconductors |
| `'smearing'` | Smooth partial occupations around the Fermi level | **Metals**, and systems whose gap is uncertain |
| `'tetrahedra'` / `'tetrahedra_lin'` / `'tetrahedra_opt'` | Exact BZ integration without smearing | **nscf runs for DOS and bands only** |
| `'from_input'` | Occupations given per band via the `OCCUPATIONS` card | Special cases |

Using smearing on an insulator lets states near the gap edge acquire small
fractional occupations and contaminates the energy. Using `'fixed'` on a
metal stops the run with
`the system is metallic, specify occupations`.

## Smearing types and degauss

With `occupations='smearing'` two variables follow: which function to smear
with (`smearing`) and how wide (`degauss`, in Ry).

| Value | Character | Use for |
|---|---|---|
| `'gaussian'` | Simple, safe, slow to converge | General |
| `'mv'` (Marzari-Vanderbilt, cold) | Free energy ≈ E(σ→0), no extrapolation needed | **Default choice for metals** |
| `'mp'` (Methfessel-Paxton) | Higher-order expansion; occupations can go negative | Metals |
| `'fd'` (Fermi-Dirac) | A physical electronic temperature | Finite-temperature work |

Smearing is a numerical stabilizer and an approximation at the same time.
Larger `degauss` converges more easily but drifts further from the σ = 0
limit. The `smearing contrib. (-TS)` term in the output is the size of that
contamination: if it is large, your `degauss` is too big.

## Measured: degauss dependence per smearing type in Al

The scan below is from [Example E5](ex-05-al-metal.html): fcc Al at
12×12×12 k, with `degauss` scanned for each smearing type.

<figure>
  <img src="assets/images/qe-e05-smearing.png"
       alt="Al total energy vs degauss for gaussian, mv, and fd smearing" />
  <figcaption>
    Measured fcc Al (QE 7.5). Cold smearing (mv) moves by only 0.3 mRy from
    0.01 to 0.05 Ry, essentially flat, while gaussian drifts by 3 mRy and
    Fermi-Dirac by 22 mRy. This is the measured basis for "mv needs no
    extrapolation".
  </figcaption>
</figure>

## The tetrahedron method: post-processing only

`'tetrahedra_opt'` (the optimized tetrahedron method) integrates the BZ
without smearing and gives the cleanest DOS. Its constraints:

- It requires a **Γ-centered automatic grid with zero shift**
  (`K_POINTS automatic` with shifts `0 0 0`).
- Use it in the **nscf step for DOS and bands**, not in the SCF itself
  ([Chapter 10](10-dos-bands.html)).
- Measured caveat: on QE 7.5 we found that projwfc.x writes all-zero PDOS
  on top of a `'tetrahedra_opt'` nscf. If you need PDOS, use the classic
  `'tetrahedra'` ([Example E7](ex-07-si-dos.html)).

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Setting degauss to "whatever converges nicely" and forgetting about it.
    The smearing width is an approximation that stays in your results, so
    always check that your target property is insensitive to it. In magnetic
    systems, an oversized degauss is a classic cause of the
    <strong>magnetic moment collapsing to zero</strong>
    (<a href="12-magnetism.html">Chapter 12</a>). Also, k-grid convergence
    and degauss convergence are coupled in metals; scan them together.
  </p>
</div>

## Related examples

- [E5 · fcc Al metal](ex-05-al-metal.html): smearing SCF, Fermi level, and
  the measured degauss scan.
- [E4 · O₂ molecule](ex-04-o2-molecule.html): why even a molecule can need
  smearing (degenerate partial occupations) and `tot_magnetization`.
