---
title: "12. Spin polarization and magnetism"
---

# 12. Spin polarization and magnetism

## Contents
{:.toc-title}

1. TOC
{:toc}

This is the gateway to transition-metal oxides. Collinear spin polarization
is switched on by `nspin = 2`; the real problem is **which magnetic solution
the SCF converges to**.

## Basic setup

```fortran
&SYSTEM
  nspin = 2
  starting_magnetization(1) =  0.6   ! Fe1 (up)
  starting_magnetization(2) = -0.6   ! Fe2 (down), AFM
  starting_magnetization(3) =  0.0   ! O
  occupations = 'smearing'
  smearing    = 'mv'
  degauss     = 0.01
/
&ELECTRONS
  mixing_beta = 0.2                  ! keep it low for magnets
  mixing_mode = 'local-TF'
/

ATOMIC_SPECIES
  Fe1  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
  Fe2  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF   ! same file, different label
  O    15.999  O.pbe-n-kjpaw_psl.1.0.0.UPF
```

- `starting_magnetization` is a **dimensionless ratio between −1 and 1**
  (not μB), and it is only an **initial guess**. The SCF is free to change
  it.
- To **constrain** the total magnetization, use `tot_magnetization`
  (separate Fermi levels for up and down). The O₂ triplet in
  [Example E4](ex-04-o2-molecule.html) does exactly this.

## AFM order is built with labels

The key trick for antiferromagnetic order: **register the same
pseudopotential under two labels** (`Fe1`, `Fe2`) and give them opposite
initial magnetizations. Without the label split, QE treats the two Fe atoms
as symmetry-equivalent and **cannot form an AFM state at all**. The same
label split is needed later by DFT+U and `hp.x`.

Classify the converged state from two output lines:

| Order | total magnetization | absolute magnetization |
|---|---|---|
| FM | Large | About equal to total |
| AFM | **≈ 0** | **Large** |
| Collapsed (nonmagnetic) | ≈ 0 | ≈ 0 |

## Measured: bcc Fe and FeO

[Example E9](ex-09-fe-bcc.html) (ferromagnetic metal) and
[Example E10](ex-10-feo-afm.html) (antiferromagnetic oxide) are this
chapter in practice.

<figure>
  <img src="assets/images/qe-e09-fe-dos.png"
       alt="bcc Fe spin-resolved DOS" />
  <figcaption>
    Measured spin-resolved DOS of bcc Fe (QE 7.5, PBE). Exchange splits the
    up and down d bands; the occupation difference is the ferromagnetic
    moment (measured 2.19 μB per atom, experiment 2.22).
  </figcaption>
</figure>

## When a magnet will not converge

It is common for the magnetization to collapse to zero during the SCF. In
order:

1. `mixing_beta` 0.7 → 0.3 → 0.1
2. `mixing_mode = 'local-TF'`
3. Larger `starting_magnetization` (0.4–0.9)
4. Smaller `degauss` (excess smearing erases moments). If the SCF itself
   fails, temporarily raise it, converge, then restart with
   `startingpot='file'` while lowering it
5. `diagonalization = 'cg'` or `'ppcg'`

And the fundamental caution:

<div class="warning">
  <div class="note-title">Magnets have multiple local minima</div>
  <p>
    Every magnetic ordering is its own <strong>metastable
    solution</strong>. One converged answer is not evidence of the ground
    state. The standard practice is to start from several initial
    magnetizations (FM, AFM, nonmagnetic), converge each, and pick the
    lowest energy.
  </p>
</div>

Noncollinear magnetism and spin-orbit coupling exist behind
`noncolin=.true.` and `lspinorb=.true.` (with fully relativistic
pseudopotentials), at a much higher cost. Learn them when you need them.

## Related examples

- [E9 · Ferromagnetic bcc Fe](ex-09-fe-bcc.html): FM metal, measured moment
  2.19 μB.
- [E10 · FeO AFM](ex-10-feo-afm.html): the AFM-II state built by the label
  trick, measured.
- [E4 · O₂ molecule](ex-04-o2-molecule.html): constraining the triplet with
  `tot_magnetization`.
