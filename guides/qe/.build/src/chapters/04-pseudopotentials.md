---
title: "04. Pseudopotentials"
---

# 04. Pseudopotentials

## Contents
{:.toc-title}

1. TOC
{:toc}

A pseudopotential replaces the rapidly oscillating all-electron wavefunction
near the nucleus with a smooth pseudo-wavefunction, which is what makes a
plane-wave basis workable. **Your choice of pseudopotential controls both
the cutoffs you need and the accuracy you get.**

## The three families: NC, US, PAW

| Family | Character | Cutoff demand | `ecutrho` multiple |
|---|---|---|---|
| NC (norm-conserving) | Simple and theoretically clean; plays well with GW and other advanced methods | High | The 4x default suffices |
| US (ultrasoft) | Much lower cutoffs via augmentation charges | Low | **8–12x required** |
| PAW (projector augmented wave) | US-like cost, plus reconstruction of all-electron quantities | Low | **8–12x required** |

The examples in this guide use PSlibrary **PAW** files. For demanding
elements like Fe, `ecutrho` is set to 10x `ecutwfc`.

<div class="warning">
  <div class="note-title">Common mistake: the ecutrho trap</div>
  <p>
    The default <code>ecutrho = 4 × ecutwfc</code> is a
    <strong>norm-conserving</strong> convention. Leaving that default with
    US/PAW potentials produces <code>negative rho</code> warnings or a
    <code>charge is wrong</code> error, or worse, a <strong>quietly wrong
    total energy with no error at all</strong>. Always set 8–12x explicitly
    for US/PAW.
  </p>
</div>

## Where to get them

- **[SSSP](https://www.materialscloud.org/discover/sssp/)** (Standard Solid
  State Pseudopotentials): a curated, element-by-element verified library.
  The *efficiency* set keeps cutoffs low at reasonable accuracy, good for
  everyday work and screening; the *precision* set stays closest to
  all-electron results for high-accuracy work. **For beginners the real
  treasure is the per-element recommended cutoff table**: take your
  convergence-test starting points from it.
- **[PSlibrary](https://pseudopotentials.quantum-espresso.org/)**: the
  NC/US/PAW library by the QE developers, downloadable per element from the
  official site.
- **[PseudoDojo](http://www.pseudo-dojo.org/)**: ONCVPSP norm-conserving
  potentials. Higher cutoffs, but very well validated.

## Decoding the filename

Being able to read the PSlibrary naming convention makes choosing much
easier.

```
Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
│   │   │    │        └─ PSlibrary version
│   │   │    └─ kjpaw = Kresse-Joubert PAW (rrkjus = ultrasoft)
│   │   └─ s = semicore s included, p = semicore p, n = nonlinear core correction
│   └─ exchange-correlation functional (pbe / pbesol / pz ...)
└─ element
```

For transition metals, prefer files that include the semicore states
(`s`, `p`) in the valence. DFT+U also needs the Hubbard manifold present in
the pseudopotential; if it is missing you get
`set_hubbard_l: pseudopotential not yet inserted`.

The `ATOMIC_SPECIES` card points at the file. If your filenames differ from
this guide, this card is the only thing you need to change.

```fortran
ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-kjpaw_psl.1.0.0.UPF
```

## The functional lives inside the pseudopotential

The exchange-correlation functional is fixed when the pseudopotential is
generated, and `pw.x` reads it from the file. You can override it with
`input_dft`, but that contradicts the generation conditions of the
potential, so **avoid it**. Use PBE potentials for PBE calculations; that is
the rule.

<div class="tip">
  <div class="note-title">Absolute total energies are not comparable</div>
  <p>
    Every pseudopotential has its own energy zero, so comparing absolute
    total energies across different potentials (or different cutoffs) is
    meaningless. Only <strong>differences</strong> between energies computed
    under identical conditions carry physics. If your total energy differs
    from a paper's, that alone means nothing.
  </p>
</div>

## Related examples

- [E1 · Si SCF](ex-01-si-scf.html): a first run with a PAW potential.
- [E3 · Automating convergence tests](ex-03-convergence.html): measure the
  cutoffs your pseudopotential actually demands.
