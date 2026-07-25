---
title: "11. Densities and potentials"
---

# 11. Densities and potentials

## Contents
{:.toc-title}

1. TOC
{:toc}

`pp.x` extracts densities and potentials from a finished SCF onto real-space
grids and writes them in visualizable formats. Its input has two namelists:
what to extract (`&INPUTPP`) and how to write it (`&PLOT`).

## Input skeleton

```fortran
&INPUTPP
  prefix   = 'si'
  outdir   = './tmp/'
  filplot  = 'si.rho.dat'
  plot_num = 0              ! 0 = valence charge density
/
&PLOT
  nfile         = 1
  filepp(1)     = 'si.rho.dat'
  weight(1)     = 1.0
  iflag         = 3         ! 3 = 3D
  output_format = 6         ! 6 = Gaussian cube
  fileout       = 'si.rho.cube'
/
```

`iflag`: 0 = 1D line, 1 = spherical average, 2 = 2D plane, 3 = 3D.
`output_format`: 0 = gnuplot, 5 = XSF (XCrySDen), 6 = Gaussian cube, among
others.

## Frequently used plot_num values

| Value | Quantity | Use |
|---|---|---|
| 0 | Valence charge density | Bonding character |
| 1 | Total potential (V_bare + V_H + V_xc) | |
| 2 | Local ionic potential | |
| 5 | STM image | Surfaces |
| 6 | Spin density ρ↑ − ρ↓ | **Visualizing magnetism** |
| 8 | ELF (electron localization function) | Bonds and lone pairs |
| 11 | Bare + Hartree potential | **Work-function calculations** |

The remaining values, and the PAW all-electron density options, vary by
version; always check the `Doc/INPUT_PP.txt` of your install.

## The skeleton of a work-function calculation

For a slab, extract the potential with `plot_num=11`, take the planar
average parallel to the surface (with `average.x` or your own parser), and
then:

$$\Phi = V_{\mathrm{vacuum}} - E_F$$

The vacuum level is the flat plateau of the planar-averaged potential in
the middle of the vacuum. The full procedure, including the dipole
correction, is in [Chapter 15](15-surfaces.html) and
[Example E13](ex-13-slab-md.html).

## Bader charges are not built into QE

Bader analysis means exporting the density as a cube with `pp.x` and feeding
it to the Henkelman group's
[`bader` code](https://theory.cm.utexas.edu/henkelman/code/bader/).
**With PAW you must export the all-electron density** (check the
corresponding `plot_num` in your version's `Doc/INPUT_PP.txt`); running
Bader on the valence-only density distorts the result because the core
charge is missing.

## Visualization tools

- **VESTA**: structures plus cube isosurfaces; the easiest starting point.
- **XCrySDen**: the classic companion to QE (XSF format).
- **Python (ASE, pymatgen)**: get in the habit of parsing outputs yourself;
  it pays off the moment you need automation. Every figure in this guide is
  drawn with Python.

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Extracting the spin density (<code>plot_num=6</code>) and getting nearly
    zero: check <code>spin_component</code>, and first check whether the SCF
    actually converged to a magnetic solution at all
    (<code>total/absolute magnetization</code>). Also, cube files reach
    hundreds of MB quickly; manage the grid with
    <code>nx, ny, nz</code> and your disk.
  </p>
</div>

## Related examples

- [E13 · Slabs and AIMD](ex-13-slab-md.html): a measured work function via
  `plot_num=11`.
- [E9 · bcc Fe](ex-09-fe-bcc.html): a good system to pair with spin-resolved
  DOS.
