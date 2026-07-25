---
title: "01. Getting started"
---

# 01. Getting started

## Contents
{:.toc-title}

1. TOC
{:toc}

## Before touching QE: the minimum theory

The plan of "first I will understand all the theory, then touch the code"
almost always fails. Grasp the qualitative meaning of the six concepts below
and go straight to the install. What matters is knowing which input variable
each concept connects to.

| Concept | Why you need it | Corresponding input |
|---|---|---|
| Kohn–Sham DFT and the SCF loop | Required to read "estimated scf accuracy" in the output | `conv_thr`, `mixing_beta`, `electron_maxstep` |
| Plane-wave basis and cutoffs | Basis size = accuracy = cost | `ecutwfc`, `ecutrho` |
| Periodic boundary conditions, Bloch's theorem, the Brillouin zone | Why k-points are sampled at all | `K_POINTS` |
| Pseudopotentials (NC / US / PAW) | Control both the required cutoff and the accuracy | `ATOMIC_SPECIES`, `pseudo_dir` |
| The exchange-correlation ladder | The limits of LDA/GGA are the reason DFT+U exists | Built into the pseudopotential file; override with `input_dft` |
| Partial occupations and smearing in metals | 90% of convergence trouble in metals and magnets | `occupations`, `smearing`, `degauss` |

For theory, good starting points are
[Cottenier's online DFT course](https://compmatphys.epotentia.com/)
(QE exercises come bundled with the theory, the most efficient entry point),
[Giannozzi's hands-on tutorial](http://www.fisica.uniud.it/~giannozz/QE-Tutorial/)
(by one of the main QE authors), MIT OCW 3.320, and as books
Sholl &amp; Steckel (introductory) and R. Martin (reference).

## Choosing an install route

| Route | Pros | Cons | When |
|---|---|---|---|
| Source build (`./configure && make all`) | MKL/ScaLAPACK tuning, GPU builds | Dependency hell | HPC, performance-critical work |
| conda (`conda install -c conda-forge qe`) | Installed in 5 minutes | Limited performance tuning | Local learning and testing |
| Distribution packages (deb etc.) | Easiest | Often outdated | Local learning |

On a local workstation, install with conda first and start learning; pick up
source builds later on the HPC system. Burning days on the install is the
single most common place where people give up. GPU builds (`--with-cuda`)
need the NVHPC compiler, and a 12 GB GPU will not hold a large spin-polarized
transition-metal oxide cell anyway, so a CPU build is plenty for learning.

Every measured number in this guide comes from the conda-forge `qe 7.5`
build running under WSL Ubuntu on 16 cores. Small cells finish in seconds to
minutes in this setup.

```bash
# micromamba or conda, either works the same way
conda create -n qe -c conda-forge qe python numpy matplotlib
conda activate qe
pw.x -in /dev/null 2>&1 | head -5     # check the version banner
```

## Environment variables and directory layout

```bash
export ESPRESSO_PSEUDO=$HOME/pseudo     # pseudopotential store
export ESPRESSO_TMPDIR=/scratch/$USER   # large temporaries (use a fast disk)
```

A directory layout that works well:

```
project/
├── pseudo/          # UPF files
├── 01_convergence/  # convergence tests
├── 02_relax/
├── 03_scf/
└── scripts/
```

`outdir` (temporaries) and `pseudo_dir` can be given in the input or fall
back to these environment variables. `outdir` is where wavefunctions and
charge densities accumulate, so make sure it points at a **fast disk**.

## Verifying the install (do not skip this)

Check the banner first.

```bash
which pw.x
pw.x -in /dev/null 2>&1 | head -20
```

What to confirm:

- The banner says `Parallel version (MPI), running on N processors`.
- `Number of MPI processes` and `Threads/MPI process` are what you intended.

If you have the QE source tree, open **`PW/examples/` and `test-suite/`**.
These are not mere tests; they are **the best textbook you have**.

```bash
cd PW/examples/example01
./run_example
ls results/            # open every generated input and output
```

Work through `example01` onward and see what each example demonstrates. For
version consistency these beat any third-party tutorial.

## Getting pseudopotentials

You need one UPF file per element before the first run. Where to get them
and how to choose is covered in [Chapter 04](04-pseudopotentials.html); the
examples in this guide use PSlibrary PAW files
(`*.pbe-*-kjpaw_psl.1.0.0.UPF`), downloadable per element from the
[official QE pseudopotential site](https://pseudopotentials.quantum-espresso.org/).

```bash
mkdir -p pseudo tmp
# example: the Si PAW file
curl -O https://pseudopotentials.quantum-espresso.org/upf_files/Si.pbe-n-kjpaw_psl.1.0.0.UPF
mv *.UPF pseudo/
```

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Oversubscribing OpenMP threads and MPI at the same time can make small
    systems tens of times slower. The two-atom Si SCF in this guide took
    about 2 minutes with 16 OpenMP threads, and 2.8 seconds with
    <code>OMP_NUM_THREADS=1</code> plus
    <code>mpirun -np 6 pw.x -nk 6</code>. See
    <a href="18-parallel-hpc.html">Chapter 18</a> for parallel settings.
  </p>
</div>

## Related examples

- [E1 · Si SCF](ex-01-si-scf.html): go straight to your first calculation.
- [E3 · Automating convergence tests](ex-03-convergence.html): do this right
  after the first run.
