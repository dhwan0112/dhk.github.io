---
title: "10. DOS and band structure"
---

# 10. DOS and band structure

## Contents
{:.toc-title}

1. TOC
{:toc}

For electronic-structure post-processing, **pipeline order and matching
`prefix`/`outdir` are everything**.

## The DOS / PDOS pipeline

```
scf (coarse k) ─→ nscf (dense k, occupations='tetrahedra') ─┬─→ dos.x      (total DOS)
                                                             └─→ projwfc.x  (PDOS + Löwdin)
```

- **nscf**: densify the k-grid (say 8³ → 16³), raise `nbnd` to cover the
  conduction bands, set `occupations='tetrahedra'`. The tetrahedron method
  requires a **Γ-centered automatic grid with zero shift**. The optimized
  variant `'tetrahedra_opt'` is fine for dos.x, but we found (measured, QE
  7.5) that **projwfc.x writes all-zero PDOS on top of it**; if your
  pipeline includes PDOS, use the classic `'tetrahedra'`
  (see the note in [Example E7](ex-07-si-dos.html)).
- **`dos.x`** (`&DOS`): the total DOS. The `fildos` file has E (eV), DOS,
  and the integrated DOS. Check that the integral hits the valence electron
  count at the top of the valence bands.
- **`projwfc.x`** (`&PROJWFC`): atom- and orbital-resolved DOS (PDOS) and
  **Löwdin charges**. Files appear as
  `si.pdos_atm#1(Si)_wfc#2(p)` and so on. The d occupation of Fe,
  spin-resolved breakdowns, and d-band centers all come from here.

<figure>
  <img src="assets/images/qe-e07-dos-pdos.png"
       alt="Si total DOS and s/p-projected DOS" />
  <figcaption>
    Measured silicon total DOS with s/p PDOS (QE 7.5, nscf 16×16×16,
    tetrahedra). The lower valence band is s-dominated and the upper is
    p-dominated, exactly as the textbook says. Procedure and numbers in
    <a href="ex-07-si-dos.html">Example E7</a>.
  </figcaption>
</figure>

## The band-structure pipeline

```
scf ─→ calculation='bands' (K_POINTS tpiba_b path) ─→ bands.x ─→ plot
```

The k-path goes in the card of the `'bands'` run:

```fortran
K_POINTS (tpiba_b)
6
  0.500 0.500 0.500  30   ! L
  0.000 0.000 0.000  30   ! Gamma
  0.000 1.000 0.000  20   ! X
  0.500 1.000 0.000  20   ! W
  0.750 0.750 0.000  30   ! K
  0.000 0.000 0.000   0   ! Gamma  (last point gets 0 divisions)
```

Each line is a high-symmetry point plus the number of divisions to the next
point. `bands.x` (`&BANDS`) reorders the eigenvalues into bands and writes
`filband` (including a `.gnu` file).

<div class="tip">
  <div class="note-title">tpiba_b vs crystal_b, when the path looks wrong</div>
  <p>
    <code>tpiba_b</code> is Cartesian in units of 2π/a;
    <code>crystal_b</code> is fractional in the reciprocal basis. QE's
    primitive-vector convention for <code>ibrav=2</code> can differ from the
    textbook fcc convention, so pasting literature fractional coordinates
    into <code>crystal_b</code> produces the wrong path.
    <strong>When in doubt, <code>tpiba_b</code> is the safe choice.</strong>
    For complex lattices, generate the path with
    <a href="https://www.materialscloud.org/work/tools/seekpath">SeeK-path</a>.
  </p>
</div>

<figure>
  <img src="assets/images/qe-e08-bands.png"
       alt="Si band structure along L-Gamma-X-W-K-Gamma" />
  <figcaption>
    Measured silicon band structure (QE 7.5, PBE, L–Γ–X–W–K–Γ). The valence
    band maximum sits at Γ and the conduction band minimum on the Γ–X line:
    an indirect-gap semiconductor. PBE systematically underestimates the gap
    (experiment: 1.12 eV). Numbers in
    <a href="ex-08-si-bands.html">Example E8</a>.
  </figcaption>
</figure>

## Three ways to read a gap

1. The `highest occupied, lowest unoccupied level (ev)` line in the scf or
   nscf output: simplest.
2. Directly from the band data (VBM and CBM): also gives you the location of
   an indirect gap.
3. The zero-DOS window in the DOS: beware, a coarse k-grid makes gaps look
   wider than they are.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Shrinking <code>DeltaE</code> because the DOS looks jagged. The cause is
    almost always an <strong>insufficient nscf k-grid</strong>; densify it
    and use the tetrahedron method. Running <code>dos.x</code> straight off
    a coarse scf density works, but the resolution is poor. Respect the
    pipeline order.
  </p>
</div>

## Related examples

- [E7 · Si DOS and PDOS](ex-07-si-dos.html): the full measured pipeline plus
  Löwdin charges.
- [E8 · Si band structure](ex-08-si-bands.html): path setup and reading the
  indirect gap.
- [E10](ex-10-feo-afm.html) / [E11 · FeO](ex-11-feo-hubbard.html):
  spin-resolved DOS showing the GGA failure and the Hubbard splitting.
