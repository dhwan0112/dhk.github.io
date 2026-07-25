---
layout: default
title: "Quantum ESPRESSO: A Practical Guide"
permalink: /
---

# Quantum ESPRESSO: A Practical Guide

Quantum ESPRESSO (QE) is an open-source first-principles (DFT) package built on
plane waves and pseudopotentials. It computes electronic structure, total
energies, forces and stress, band structures and densities of states, phonons,
and ab initio molecular dynamics for crystals, surfaces, and molecules, and it
is free for academic use.

This guide is written so that a newcomer does not get lost in front of `pw.x`.
It starts from the simplest possible silicon SCF and works through input
syntax, convergence testing, structure optimization, and post-processing, then
continues into spin polarization and antiferromagnetism, the `HUBBARD` card
for DFT+U, computing U with `hp.x`, and slabs with ab initio MD. In other
words, it covers the full path you need for transition-metal oxide research
(the Fe–O system in particular).

## Three principles to hold on to

**1. QE is less a program than a piece of lab equipment.** Every input
parameter corresponds to a physical approximation. `ecutwfc = 60` is not "the
number 60"; it is a physical decision about where to truncate the plane-wave
basis. Asking "what does this value approximate?" every time, instead of
memorizing the manual, is what determines how fast you learn.

**2. A number that has not passed a convergence test is not a number.** The
most common beginner mistake is equating "the calculation ran" with "the
result is right". QE will happily print physically wrong results in a
perfectly clean format. [Chapter 05](05-convergence.html) and
[Example E3](ex-03-convergence.html) cover the procedure.

**3. Check the version before trusting third-party tutorials.** A large share
of QE examples on the internet use obsolete syntax. The prime case is DFT+U:
in v7.1 the `lda_plus_u` / `Hubbard_U(i)` style was replaced by the
**`HUBBARD` card**. Pasting old examples gets you input that is silently
ignored or fails. This guide uses the new syntax only.

## About this guide

- **The target version is QE 7.5** (released August 2025). All 13 examples
  were actually executed with QE 7.5 (conda-forge build, WSL Ubuntu), and the
  pages report the **measured numbers and figures** from those runs. Every
  example page links its input files, and a
  [complete bundle](files/qe-examples.tar.gz) is available.
- The chapters (01–18) are organized by concept; the
  [examples (E1–E13)](ex-01-si-scf.html) are organized by system. Look up
  "what does this variable mean" in the chapters and "how do I run this
  system" in the examples, and follow the cross-links between them.
- The [reference pages (R1–R4)](ref-keywords.html) are for searching, not
  reading: keyword, card, and error-message dictionaries.
- The final authority on input variables is always the `Doc/INPUT_PW.txt` of
  your installed version
  ([online version](https://www.quantum-espresso.org/Doc/INPUT_PW.html)).

## Where to start

### Basics · Getting started

<div class="cards">
  <a class="card" href="01-getting-started.html">
    <div class="card-num">01 · START</div>
    <div class="card-title">Getting started</div>
    <div class="card-desc">Minimum background, install routes, verifying the install.</div>
  </a>
  <a class="card" href="02-input-structure.html">
    <div class="card-num">02 · INPUT</div>
    <div class="card-title">Input file structure</div>
    <div class="card-desc">Namelists and cards, a minimal input dissected, running pw.x.</div>
  </a>
  <a class="card" href="03-units-coordinates.html">
    <div class="card-num">03 · UNITS</div>
    <div class="card-title">Units and coordinates</div>
    <div class="card-desc">Ry and bohr conventions, ibrav and celldm, alat/crystal/angstrom.</div>
  </a>
</div>

### Basics · Core concepts

<div class="cards">
  <a class="card" href="04-pseudopotentials.html">
    <div class="card-num">04 · PSEUDO</div>
    <div class="card-title">Pseudopotentials</div>
    <div class="card-desc">NC/US/PAW, SSSP and PSlibrary, decoding filenames.</div>
  </a>
  <a class="card" href="05-convergence.html">
    <div class="card-num">05 · CONV</div>
    <div class="card-title">Cutoff and k-point convergence</div>
    <div class="card-desc">The standard procedure, meV/atom conversion, common misconceptions.</div>
  </a>
  <a class="card" href="06-occupations.html">
    <div class="card-num">06 · SMEARING</div>
    <div class="card-title">Occupations and smearing</div>
    <div class="card-desc">Insulators vs metals, smearing types and degauss.</div>
  </a>
  <a class="card" href="07-scf-control.html">
    <div class="card-num">07 · SCF</div>
    <div class="card-title">Controlling SCF convergence</div>
    <div class="card-desc">Mixing and diagonalization, a diagnosis order for failures.</div>
  </a>
</div>

### Basics · Calculation types

<div class="cards">
  <a class="card" href="08-scf-nscf.html">
    <div class="card-num">08 · SCF/NSCF</div>
    <div class="card-title">SCF and NSCF</div>
    <div class="card-desc">Division of labor between runs, reading the output.</div>
  </a>
  <a class="card" href="09-relaxation.html">
    <div class="card-num">09 · RELAX</div>
    <div class="card-title">Structure optimization</div>
    <div class="card-desc">relax/vc-relax, BFGS, if_pos, Pulay stress.</div>
  </a>
  <a class="card" href="10-dos-bands.html">
    <div class="card-num">10 · DOS·BANDS</div>
    <div class="card-title">DOS and band structure</div>
    <div class="card-desc">The dos.x, projwfc.x and bands.x pipelines.</div>
  </a>
  <a class="card" href="11-postprocessing.html">
    <div class="card-num">11 · PP</div>
    <div class="card-title">Densities and potentials</div>
    <div class="card-desc">pp.x plot_num, cube files, Bader, visualization tools.</div>
  </a>
</div>

### Advanced · Magnetism and correlation

<div class="cards">
  <a class="card" href="12-magnetism.html">
    <div class="card-num">12 · SPIN</div>
    <div class="card-title">Spin polarization and magnetism</div>
    <div class="card-desc">nspin, starting_magnetization, AFM by atom labels, bcc Fe.</div>
  </a>
  <a class="card" href="13-dft-plus-u.html">
    <div class="card-num">13 · DFT+U</div>
    <div class="card-title">DFT+U and the HUBBARD card</div>
    <div class="card-desc">v7.1+ syntax, projector choice, opening the FeO gap.</div>
  </a>
  <a class="card" href="14-hubbard-hp.html">
    <div class="card-num">14 · HP.X</div>
    <div class="card-title">Computing U with hp.x</div>
    <div class="card-desc">Linear-response U, q-grid convergence, self-consistent U.</div>
  </a>
</div>

### Advanced · Applications and operations

<div class="cards">
  <a class="card" href="15-surfaces.html">
    <div class="card-num">15 · SLAB</div>
    <div class="card-title">Surfaces, slabs, work function</div>
    <div class="card-desc">Slab generation, dipole correction, planar-averaged potential.</div>
  </a>
  <a class="card" href="16-molecular-dynamics.html">
    <div class="card-num">16 · AIMD</div>
    <div class="card-title">Molecular dynamics</div>
    <div class="card-desc">Born-Oppenheimer MD, SVR thermostat, sampling ML training data.</div>
  </a>
  <a class="card" href="17-phonons-neb.html">
    <div class="card-num">17 · PH·NEB</div>
    <div class="card-title">Phonons and reaction paths</div>
    <div class="card-desc">ph.x and neb.x: when you need them, where to start.</div>
  </a>
  <a class="card" href="18-parallel-hpc.html">
    <div class="card-num">18 · HPC</div>
    <div class="card-title">Parallel execution and HPC</div>
    <div class="card-desc">-nk/-nd/-ni levels, scaling intuition, operational habits.</div>
  </a>
</div>

### Reference

<div class="cards">
  <a class="card" href="ref-keywords.html">
    <div class="card-num">R1 · KEYWORDS</div>
    <div class="card-title">Keyword dictionary</div>
    <div class="card-desc">Main variables and defaults, namelist by namelist.</div>
  </a>
  <a class="card" href="ref-cards.html">
    <div class="card-num">R2 · CARDS</div>
    <div class="card-title">Card reference</div>
    <div class="card-desc">ATOMIC_*, K_POINTS, CELL_PARAMETERS, HUBBARD.</div>
  </a>
  <a class="card" href="ref-errors.html">
    <div class="card-num">R3 · ERRORS</div>
    <div class="card-title">Error message dictionary</div>
    <div class="card-desc">Symptom, cause, fix. Includes failures without errors.</div>
  </a>
  <a class="card" href="ref-executables.html">
    <div class="card-num">R4 · BINARIES</div>
    <div class="card-title">Executables</div>
    <div class="card-desc">From pw.x to hp.x: inputs, prerequisites, outputs.</div>
  </a>
</div>

### Examples · Hands-on

Each example is a self-contained page in a fixed order: goal, new cards and
variables, input files (downloadable), how to run, what to check in the
output, exercises, and common mistakes. All numbers are measured from real
QE 7.5 runs.

<div class="cards">
  <a class="card" href="ex-01-si-scf.html">
    <div class="card-num">E1</div>
    <div class="card-title">Si SCF</div>
    <div class="card-desc">The simplest SCF, and how to read the output.</div>
  </a>
  <a class="card" href="ex-02-si-ibrav0.html">
    <div class="card-num">E2</div>
    <div class="card-title">Rewriting with ibrav=0</div>
    <div class="card-desc">The same crystal via CELL_PARAMETERS.</div>
  </a>
  <a class="card" href="ex-03-convergence.html">
    <div class="card-num">E3</div>
    <div class="card-title">Automating convergence tests</div>
    <div class="card-desc">Cutoff, k-point and force scans by script.</div>
  </a>
  <a class="card" href="ex-04-o2-molecule.html">
    <div class="card-num">E4</div>
    <div class="card-title">O₂ molecule (triplet)</div>
    <div class="card-desc">Isolation corrections, fixed spin, binding energy.</div>
  </a>
  <a class="card" href="ex-05-al-metal.html">
    <div class="card-num">E5</div>
    <div class="card-title">fcc Al metal</div>
    <div class="card-desc">Smearing SCF and the Fermi level.</div>
  </a>
  <a class="card" href="ex-06-si-vcrelax.html">
    <div class="card-num">E6</div>
    <div class="card-title">Si vc-relax</div>
    <div class="card-desc">Variable-cell optimization, equilibrium lattice constant.</div>
  </a>
  <a class="card" href="ex-07-si-dos.html">
    <div class="card-num">E7</div>
    <div class="card-title">Si DOS and PDOS</div>
    <div class="card-desc">The nscf, dos.x and projwfc.x pipeline.</div>
  </a>
  <a class="card" href="ex-08-si-bands.html">
    <div class="card-num">E8</div>
    <div class="card-title">Si band structure</div>
    <div class="card-desc">A high-symmetry path and the indirect gap.</div>
  </a>
  <a class="card" href="ex-09-fe-bcc.html">
    <div class="card-num">E9</div>
    <div class="card-title">Ferromagnetic bcc Fe</div>
    <div class="card-desc">Spin-polarized SCF, moment of 2.2 μB.</div>
  </a>
  <a class="card" href="ex-10-feo-afm.html">
    <div class="card-num">E10</div>
    <div class="card-title">FeO AFM (where GGA fails)</div>
    <div class="card-desc">Watch GGA predict a metal for an insulator.</div>
  </a>
  <a class="card" href="ex-11-feo-hubbard.html">
    <div class="card-num">E11</div>
    <div class="card-title">FeO with DFT+U</div>
    <div class="card-desc">The HUBBARD card, Hubbard splitting, and a famous trap.</div>
  </a>
  <a class="card" href="ex-12-feo-hp.html">
    <div class="card-num">E12</div>
    <div class="card-title">Computing U with hp.x</div>
    <div class="card-desc">First-principles U by linear response.</div>
  </a>
  <a class="card" href="ex-13-slab-md.html">
    <div class="card-num">E13</div>
    <div class="card-title">Slabs and AIMD</div>
    <div class="card-desc">Slab generation, work function, BOMD sampling.</div>
  </a>
</div>

<div class="divider"></div>

## The shortest path to the Fe–O system

If transition-metal oxides (say, iron oxidation) are your end goal, you can
compress the examples into this sequence.

1. **Si (E1–E3, E6–E8).** Learn the syntax, convergence, and optimization
   instincts. Two or three days is enough.
2. **bcc Fe (E9).** A metal plus ferromagnetism. Meet the difficulties of
   smearing and magnetization convergence here, on an easy system.
3. **FeO in the AFM phase (E10).** Verify for yourself that without DFT+U the
   calculation comes out metallic.
4. **FeO with U (E11–E12).** Turn on U with the `HUBBARD` card, observe the
   Hubbard splitting (and walk into the famous trap of the ideal cubic cell),
   then compute U from first principles with `hp.x`. This one cycle is the
   heart of the whole curriculum.
5. **Slab and AIMD (E13).** The starting point for generating training data
   for machine-learned potentials.

If ML training data is the goal, one criterion changes: converge with respect
to **forces**, not energies, and keep the cutoffs, k-grid, smearing, and U
absolutely identical across every structure. A dataset with mixed settings
cannot be repaired at the training stage.

## Self-check list

Move on only when you can answer these.

- **Basics (E1–E3).** You can explain the physical difference between
  `ecutwfc` and `ecutrho`. You can convert between `alat`, `crystal`, and
  `angstrom` coordinates. You can explain why absolute total energies must
  not be compared.
- **System types (E4–E6).** You know which `occupations` to use for a metal,
  a semiconductor, and a molecule. You know the difference between
  `starting_magnetization` and `tot_magnetization`. You can explain why a
  fresh `scf` is required after `vc-relax` (Pulay stress).
- **Post-processing (E7–E8).** You know the role of `prefix` and `outdir` in
  the scf, nscf, dos.x chain. You know why the tetrahedron method requires a
  Γ-centered, unshifted grid.
- **Magnetism and correlation (E9–E12).** You know why the same element needs
  two labels to build an AFM state. You can classify a magnetic solution from
  total vs absolute magnetization. You know that the meaning of U depends on
  the projector. You have seen GGA predict metallic FeO with your own eyes.

## How to cite

When publishing work that used Quantum ESPRESSO, the convention is to cite
the following papers, together with the original papers of any modules you
used (such as `hp.x`) and the source of your pseudopotentials.

- P. Giannozzi et al. *J. Phys.: Condens. Matter* **2009**, *21*, 395502.
- P. Giannozzi et al. *J. Phys.: Condens. Matter* **2017**, *29*, 465901.
- P. Giannozzi et al. *J. Chem. Phys.* **2020**, *152*, 154105.
- (if you use `hp.x`) I. Timrov, N. Marzari, M. Cococcioni.
  *Comput. Phys. Commun.* **2022**, *279*, 108455.

<div class="note">
  <div class="note-title">Resources</div>
  <p>
    Primary sources first: the <code>Doc/</code> folder of your installed
    version (<code>INPUT_PW.txt</code>, <code>user_guide.pdf</code>,
    <code>Hubbard_input.pdf</code>), the
    <a href="https://www.quantum-espresso.org/documentation/input-data-description/">official input documentation</a>,
    and the <code>PW/examples/</code> and <code>test-suite/</code> trees in
    the source distribution. For learning material, try
    <a href="https://compmatphys.epotentia.com/">Cottenier's online DFT course</a>,
    <a href="http://www.fisica.uniud.it/~giannozz/QE-Tutorial/">Giannozzi's hands-on tutorial</a>,
    MIT OCW 3.320, and as books Sholl &amp; Steckel (introductory) and
    R. Martin (reference). When you get stuck, search the
    <a href="https://www.mail-archive.com/users@lists.quantum-espresso.org/">QE users mailing list archive</a>
    first; most problems have already been answered there.
  </p>
</div>
