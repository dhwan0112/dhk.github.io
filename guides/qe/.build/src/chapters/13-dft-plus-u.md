---
title: "13. DFT+U and the HUBBARD card"
---

# 13. DFT+U and the HUBBARD card

## Contents
{:.toc-title}

1. TOC
{:toc}

## Why it is needed

GGA mishandles the self-interaction error of localized 3d electrons. The
spurious interaction of an electron with itself delocalizes orbitals that
should be localized, and in systems like FeO the result is a computed metal
where experiment sees an insulator (gap ≈ 2.4 eV). You can watch this
failure happen in [Example E10](ex-10-feo-afm.html).

DFT+U adds a Hubbard correction on a chosen orbital manifold (Fe-3d, say)
and repairs the error at nearly zero extra cost.

## The new syntax: the HUBBARD card (v7.1+)

U parameters go in a **`HUBBARD` card at the end of the input**, not in
`&SYSTEM`.

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 4.6
U Fe2-3d 4.6
```

The grammar:

```
HUBBARD (<projector>)
<parameter> <label>-<manifold> <value(eV)>
```

| Field | Options | Notes |
|---|---|---|
| Projector | `atomic`, `ortho-atomic`, `norm-atomic`, `wf`, `pseudo` | **`ortho-atomic` recommended.** With `atomic`, the correction double-counts in orbital-overlap regions |
| Parameter | `U`, `J0`, `J`, `B`, `E2`, `E3`, `V`, `alpha` | |
| Manifold | `3d`, `2p`, `4f`, ... | Up to 3 channels per atomic type |

Inter-site interactions (DFT+U+V) also take neighbor indices (numbered by
order in `ATOMIC_POSITIONS`):

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 4.6
U Fe2-3d 4.6
V Fe1-3d O-2p  1 3  0.8
```

The authoritative document is `Doc/Hubbard_input.pdf`
([online](https://www.quantum-espresso.org/Doc/user_guide_PDF/Hubbard_input.pdf)).

<div class="warning">
  <div class="note-title">Do not use the old syntax</div>
  <p>
    The <code>lda_plus_u = .true.</code> / <code>Hubbard_U(1) = 4.6</code> /
    <code>U_projection_type</code> style was retired in v7.1. Much of the
    internet still shows it, and pasting it gets you input that is silently
    ignored or fails. The only DFT+U variables left in
    <code>&amp;SYSTEM</code> are <code>starting_ns_eigenvalue</code> and
    <code>Hubbard_occ</code>.
  </p>
</div>

## Measured: what U does in FeO, and what it cannot do alone

[Example E11](ex-11-feo-hubbard.html) is the same FeO AFM-II cell with just
the three HUBBARD lines added.

<figure>
  <img src="assets/images/qe-e10-e11-feo-dos.png"
       alt="FeO DOS: GGA (metallic) vs GGA+U (Hubbard splitting)" />
  <figcaption>
    Measured spin-resolved DOS of FeO (QE 7.5, PBE, AFM-II). Left, GGA:
    Fe-3d states sit at the Fermi level and the system is metallic
    (experiment: an insulator). Right, GGA+U (4.6 eV, ortho-atomic): the
    Hubbard splitting opens gaps above and below, but in the ideal cubic
    cell a narrow band derived from the minority-spin t2g states survives at
    the Fermi level. That last trap is treated below and in E11.
  </figcaption>
</figure>

## If it is still metallic with U on: the occupation-pattern trap

It is common to switch U on and still converge to a metal. The culprit is
the **occupation pattern** of the d orbitals. Since QE 7.1 the initial d
occupations are read from the pseudopotential (they used to be hardcoded),
so the same input can converge to different metallic solutions on different
versions. **Both are wrong ground states** (this is the mailing-list case
the community knows well).

The prescription is to steer the occupations explicitly with
`starting_ns_eigenvalue`:

```fortran
&SYSTEM
  ...
  starting_ns_eigenvalue(5, 2, 1) = 0.0d0   ! (orbital index, spin, atom type)
/
```

The constraint holds only for the first few SCF iterations and is then
released; think of it as a device that pushes the run into the basin of the
correct minimum. After convergence, inspect the `Tr[ns(na)]` values and the
ns eigenvalue blocks in the output (`verbosity='high'` required) to confirm
the occupation pattern is physical. This is the canonical example of
"converged does not mean correct".

## U comes as a package with its projector

The same U = 4.6 eV gives different results under `atomic` and
`ortho-atomic` projectors. **A U value has meaning only together with its
projector (and pseudopotential)**, so when borrowing U from a paper, check
the projector conventions, and when publishing, record your own. The way to
avoid borrowing altogether is to compute U for your own system:
[Chapter 14, hp.x](14-hubbard-hp.html).

QE 7.5 adds **orbital-resolved DFT+U** (Macke &amp; Timrov, *JCTC* 2024),
which can assign different U values to t2g and eg within one 3d manifold. It
was designed for octahedral transition-metal oxides, exactly the FeO
situation.

## Related examples

- [E10 · FeO AFM (where GGA fails)](ex-10-feo-afm.html): confirm the metal
  without U.
- [E11 · FeO with DFT+U](ex-11-feo-hubbard.html): the HUBBARD card and the
  trap, measured.
- [E12 · Computing U with hp.x](ex-12-feo-hp.html): first-principles U.
