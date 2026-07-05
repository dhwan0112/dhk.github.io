---
layout: default
title: "2. Si 밴드 + DOS"
---

# 2. Si 밴드구조 + 상태밀도
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 무엇을 하는 예제인가

[E1](ex-01-si-scf.html) 의 실리콘 SCF를 이어받아, 밴드구조와 상태밀도(DOS)를
구합니다. `scf → bands → bands.x` 로 밴드를, `scf → nscf → dos.x` 로 DOS를 얻는
표준 흐름을 한자리에서 실행합니다.

관련 개념은 [07 밴드와 DOS](07-bands-dos.html)에서 다룹니다.

## 1단계 — SCF

먼저 [E1](ex-01-si-scf.html)의 `si.scf.in` 과 동일한 SCF를 돌려 전하밀도를
`./out` 에 저장합니다.

```bash
export OMP_NUM_THREADS=1
mpirun -np 8 pw.x -nk 8 -in scf.in > scf.out
```

## 2단계 — 밴드 경로 계산 + bands.x

고대칭점 L–Γ–X–U–Γ 을 잇는 경로에서 고윳값을 계산합니다.

```fortran
&control
  calculation = 'bands'
  prefix='si', outdir='./out', pseudo_dir='./pseudo'
/
&system
  ibrav=2, celldm(1)=10.26, nat=2, ntyp=1, ecutwfc=40, ecutrho=320, nbnd=8
/
&electrons
  conv_thr=1.0d-8
/
ATOMIC_SPECIES
  Si 28.0855 Si.pbe-n-rrkjus_psl.1.0.0.UPF
ATOMIC_POSITIONS (alat)
  Si 0.00 0.00 0.00
  Si 0.25 0.25 0.25
K_POINTS {crystal_b}
5
  0.5000 0.5000 0.5000 40   ! L
  0.0000 0.0000 0.0000 40   ! Γ
  0.5000 0.0000 0.5000 40   ! X
  0.6250 0.2500 0.6250 40   ! U
  0.0000 0.0000 0.0000 1    ! Γ
```

```bash
mpirun -np 8 pw.x -nk 8 -in bands.in > bands.out
```

이어 `bands.x` 로 고윳값을 밴드별로 정렬합니다.

```fortran
&bands
  prefix='si', outdir='./out', filband='si.bands.dat'
/
```

```bash
bands.x -in bandsx.in > bandsx.out
```

`si.bands.dat.gnu`(k-거리 vs 에너지)와 함께 `bandsx.out` 에 고대칭점 위치가
출력됩니다.

## 3단계 — DOS (nscf + dos.x)

촘촘한 격자에서 nscf로 고윳값을 구하고 `dos.x` 로 상태밀도를 만듭니다.

```fortran
&control
  calculation = 'nscf'
  prefix='si', outdir='./out', pseudo_dir='./pseudo'
/
&system
  ibrav=2, celldm(1)=10.26, nat=2, ntyp=1, ecutwfc=40, ecutrho=320
  occupations='tetrahedra'
/
&electrons
  conv_thr=1.0d-8
/
...
K_POINTS (automatic)
  16 16 16 0 0 0
```

```bash
mpirun -np 8 pw.x -nk 8 -in nscf.in > nscf.out
# dos.x: &dos prefix='si', outdir='./out', fildos='si.dos', DeltaE=0.05 /
dos.x -in dosx.in > dosx.out
```

## 결과

<figure>
  <img src="assets/images/qe-si-bands-dos.png" alt="실리콘 밴드구조와 상태밀도" style="width:100%;max-width:940px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    실리콘 밴드구조(L–Γ–X–U–Γ)와 DOS(QE 7.5, PBE). 에너지는 최고 점유 준위(VBM)를
    0으로. 원자가 밴드 최대는 Γ, 전도 밴드 최소는 X 근처 → <b>간접 띠간격 ≈ 0.57 eV</b>.
    오른쪽 DOS의 채워진 영역이 원자가 밴드입니다.
  </figcaption>
</figure>

밴드구조에서 원자가 밴드 최대(VBM)가 Γ에, 전도 밴드 최소(CBM)가 X 근처에 있어
**간접 반도체**임이 보입니다. PBE 간격 0.57 eV는 실험값(약 1.1 eV)보다 작은데,
이는 표준 DFT의 알려진 특성입니다([07장](07-bands-dos.html)).

## 요점

- 밴드/DOS는 SCF 전하밀도를 고정한 nscf 계산 — `prefix`·`outdir` 일치가 핵심.
- 밴드구조는 경로 k점(`crystal_b`) + `bands.x`.
- DOS는 촘촘한 격자 + `tetrahedra` + `dos.x`.
- 궤도별 기여가 필요하면 `projwfc.x`(투영 DOS).

## 관련 개념 챕터

- [07 밴드와 DOS](07-bands-dos.html) · [04 k점 샘플링](04-kpoints.html)

앞 예제는 [E1 — Si SCF](ex-01-si-scf.html), 다음은
[E3 — 금속 smearing](ex-03-metal-smearing.html) 입니다.
