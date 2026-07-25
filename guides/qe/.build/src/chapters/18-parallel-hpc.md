---
title: "18. Parallel execution and HPC"
---

# 18. Parallel execution and HPC

## Contents
{:.toc-title}

1. TOC
{:toc}

## The parallelization cheat sheet

```bash
mpirun -np 32 pw.x -nk 8 -in input.in > output.out
```

| Flag | Alias | Meaning | Guidance |
|---|---|---|---|
| `-nk` | `-npool` | k-point pools | **Most efficient.** Make it divide the k-point count, and leave `nproc/nk` large enough for the FFT distribution |
| `-nb` | `-nband` | Band groups | Useful for hybrids and EXX |
| `-nt` | `-ntg` | FFT task groups | Many bands and many cores |
| `-nd` | `-ndiag` | Diagonalization group | **Must be a square number.** Large systems only |
| `-ni` | `-nimage` | Image parallelism | NEB, phonons, hp.x |

The default split (no flags) distributes plane waves (G-vectors). Small
cells with many k-points want `-nk`; large cells with few k-points lean on
the G-vector split and `-nd`. **If you run out of memory, lower `-nk`**:
every pool holds its own copy of the charge density.

## Measured: the thread trap on small systems

The two-atom Si SCF from this guide, on a 16-core WSL machine with the
conda-forge build:

| Setting | Wall time |
|---|---|
| `OMP_NUM_THREADS=16` (threads only) | about 2 minutes |
| `OMP_NUM_THREADS=1` + `mpirun -np 6 pw.x -nk 6` | **2.8 seconds** |

Conda builds ship with OpenMP enabled, and on small systems the idle-thread
spinning can cost you an order of magnitude or two. **On a local learning
machine, set `OMP_NUM_THREADS=1` explicitly and parallelize with MPI plus
`-nk`.** On HPC, if you use hybrid MPI×OpenMP, keep
ranks-per-node × threads = physical cores.

## Read the timing breakdown first

The timing block at the end of the output is where parallelization strategy
starts.

```
     init_run     :    ...
     electrons    :    ...      ← the whole SCF
     c_bands      :    ...      ← diagonalization (if large: -nd, diagonalization)
     sum_band     :    ...
     fft + ffts   :    ...      ← FFT (if large: G-vector split, -nt)
```

In `PWSCF : ... CPU ... WALL`, CPU much larger than WALL points at thread
spin; WALL much larger than CPU points at I/O or communication.

## HPC habits

- **Always set `max_seconds`.** The run saves state and exits cleanly just
  before the queue limit; continue with `restart_mode='restart'`.
- Point `outdir` at scratch (the fast parallel filesystem). Writing
  wavefunctions into your home directory slows you and everyone else down.
- Record the QE version, pseudopotential paths and names, and the commit of
  your scripts inside the batch script. "What settings produced this data?"
  is the question your future self asks most often.
- For large scans (convergence tests, U scans, MD frame recomputation),
  workflow tools like AiiDA and ASE beat shell loops on reproducibility.

A typical PBS/Slurm line:

```bash
mpirun -np $SLURM_NTASKS pw.x -nk 8 -nd 4 -in feo.scf.in > feo.scf.out
```

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    <code>npool must divide nproc</code>: your <code>-nk</code> does not
    divide the total rank count.
    <code>some processors have no planes</code>: more ranks than FFT
    z-planes (too many ranks for a small cell). Parallel setup errors are
    collected in section 4 of the
    <a href="ref-errors.html">R3 error dictionary</a>.
  </p>
</div>

## Related examples

- Every example page's "Run" section uses commands chosen by this chapter's
  rules. For splitting hp.x over q-points, see
  [Example E12](ex-12-feo-hp.html).
