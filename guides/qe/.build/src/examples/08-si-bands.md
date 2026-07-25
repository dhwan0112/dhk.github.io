---
title: "E8. Si band structure"
---

# E8. Si band structure

## Goal

Compute the silicon band structure along the high-symmetry path
L–Γ–X–W–K–Γ and read the indirect gap yourself. Learn `tpiba_b` path input
and the `bands.x` post-processor.

```
scf ─→ calculation='bands' (K_POINTS tpiba_b) ─→ bands.x ─→ plot
```

## New cards and variables

| Item | Role |
|---|---|
| `calculation='bands'` | Eigenvalues along an arbitrary k-path on a frozen density |
| `K_POINTS (tpiba_b)` | The path in Cartesian 2π/a units |
| `bands.x` (`&BANDS`) | Reorders bands, writes the `.gnu` file and symmetry labels |

## Input files

[si.bands.in](files/E08-si-bands/si.bands.in) ·
[si.bandspp.in](files/E08-si-bands/si.bandspp.in)
(the preceding scf is [E1's si.scf.in](files/E01-si-scf/si.scf.in))

The path card:

```fortran
K_POINTS (tpiba_b)
6
  0.500 0.500 0.500  30   ! L
  0.000 0.000 0.000  30   ! Gamma
  0.000 1.000 0.000  20   ! X
  0.500 1.000 0.000  20   ! W
  0.750 0.750 0.000  30   ! K
  0.000 0.000 0.000   0   ! Gamma
```

`tpiba_b` is Cartesian in 2π/a. QE's primitive-vector convention for
`ibrav=2` can differ from the textbook fcc setting, so literature
fractional coordinates pasted into `crystal_b` produce a wrong path.
**When unsure, `tpiba_b` is the safe choice**
([Chapter 10](10-dos-bands.html)).

## Run

```bash
pw.x    -in si.scf.in     > si.scf.out      # the prerequisite scf (prefix='si')
pw.x    -in si.bands.in   > si.bands.out
bands.x -in si.bandspp.in > si.bandspp.out
```

The `high-symmetry point` lines in `si.bandspp.out` give the tick
positions along the path. Measured: 0.000 (L), 0.866 (Γ), 1.866 (X),
2.366 (W), 2.720 (K), 3.780 (Γ).

## Output and figure: measured

<figure>
  <img src="assets/images/qe-e08-bands.png"
       alt="Si band structure along L-Gamma-X-W-K-Gamma" />
  <figcaption>
    Measured silicon band structure (QE 7.5, PBE). The valence maximum sits
    at Γ and the conduction minimum on the Γ–X line (at about 0.85 of the
    way to X): an <strong>indirect-gap</strong> semiconductor.
  </figcaption>
</figure>

- The zero is the VBM (the scf `highest occupied level`, measured
  6.212 eV).
- **Measured indirect gap: 0.57 eV** (VBM at Γ, CBM at 0.83 of Γ–X), and a
  **direct gap at Γ of 2.56 eV**. The experimental indirect gap is
  1.12 eV: the systematic PBE underestimate, on display.

## Exercises

1. Read both the direct gap at Γ and the indirect gap, and compare.
2. Put a nonzero division count on the last path point. What warning do
   you get?
3. Rewrite the same path in `crystal_b` and check whether the result
   changes. What is the `crystal_b` coordinate of the L point in QE's fcc
   convention?
4. Raise `nbnd` to 20 and plot the higher conduction bands.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Launching <code>calculation='bands'</code> without the scf: a bands run
    builds no density and needs the scf products under the same
    <code>prefix</code>/<code>outdir</code>. And a PBE gap below experiment
    does not mean your run is broken; it is a
    <strong>known limitation of the functional</strong>. If the gap itself
    is the target, move to hybrids or GW.
  </p>
</div>

## Related chapters

[10 DOS and band structure](10-dos-bands.html) ·
[08 SCF and NSCF](08-scf-nscf.html)
