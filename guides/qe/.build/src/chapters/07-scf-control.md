---
title: "07. Controlling SCF convergence"
---

# 07. Controlling SCF convergence

## Contents
{:.toc-title}

1. TOC
{:toc}

The SCF (self-consistent field) loop is the cycle "guess a density, solve
the Kohn-Sham equations, get a new density, mix, repeat". The `&ELECTRONS`
namelist controls that cycle.

## The key variables

| Variable | Default | Role |
|---|---|---|
| `conv_thr` | 1.0d-6 | Convergence threshold (Ry). Use 1.0d-8 when forces or stress matter; 1.0d-12 for a run feeding `hp.x` |
| `mixing_beta` | 0.7 | How much new density to mix in. **0.1–0.3 for magnets and metals** |
| `mixing_mode` | `'plain'` | `'plain'` (Broyden) / `'TF'` / `'local-TF'`. **Use `'local-TF'` for metals, slabs, magnets** |
| `mixing_ndim` | 8 | History length for mixing; more costs memory |
| `electron_maxstep` | 100 | Maximum iterations |
| `diagonalization` | `'david'` | `'david'` / `'cg'` / `'ppcg'` / `'paro'` / `'rmm-davidson'` |
| `startingwfc` / `startingpot` | `'atomic+random'` / `'atomic'` | `'file'` continues from a previous run |

In the output, watch `estimated scf accuracy` descend below `conv_thr`;
success prints `convergence has been achieved in N iterations`.

## Intuition for mixing_beta

Mixing aggressively (0.7) converges fast, but in systems with a soft
response (metals, magnets) the density oscillates and diverges. Such systems
need gentle mixing (0.2–0.3). `mixing_mode='local-TF'` is particularly
effective for spatially inhomogeneous systems: slabs, cells with vacuum,
magnetic oxides.

A measured example: the [FeO AFM run (E10)](ex-10-feo-afm.html) uses
`mixing_beta = 0.2` with `local-TF`. GGA FeO converges to a (wrong)
metallic state and is touchy; the default 0.7 oscillates.

## A diagnosis order for failures

When you see `convergence NOT achieved after N iterations`, try these
**in order**.

1. `mixing_beta` 0.7 → 0.3 → 0.1
2. `mixing_mode = 'local-TF'` (metals, slabs, magnets)
3. Increase `electron_maxstep` (200–500)
4. Increase `mixing_ndim` (8 → 12–16, if memory allows)
5. Temporarily raise `degauss` to converge, then restart with
   `startingpot='file'` while lowering it back
6. `diagonalization = 'cg'` or `'ppcg'` (slower but robust)
7. Check the structure for nonsense (atoms too close together)

Diagonalization-stage problems
(`c_bands: N eigenvalues not converged`,
`cdiaghg: problems computing cholesky`) and other errors are collected by
symptom in the [R3 error dictionary](ref-errors.html).

<div class="warning">
  <div class="note-title">Common mistakes</div>
  <p>
    Loosening <code>conv_thr</code> because the SCF will not converge. At
    1.0d-4 you will get the "convergence achieved" message, and garbage
    forces and stress along with it. The cause is almost always mixing
    (items 1–4 above), not the threshold. In the other direction: runs that
    consume forces or linear response (optimization, MD, hp.x) need a
    <strong>tighter</strong> threshold, 1.0d-8 to 1.0d-12.
  </p>
</div>

## Related examples

- [E9 · Ferromagnetic bcc Fe](ex-09-fe-bcc.html): mixing settings for a
  magnetic metal in practice.
- [E10 · FeO AFM](ex-10-feo-afm.html): a touchy system that needs local-TF
  and low beta.
