---
layout: default
title: "7. 밴드와 DOS"
---

# 7. 밴드와 DOS
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

전체 에너지 다음으로 가장 많이 보는 결과가 밴드구조(band structure)와 상태밀도
(density of states, DOS)입니다. 둘 다 **SCF로 얻은 전하밀도를 고정한 채**, 원하는
k점에서 Kohn-Sham 고윳값을 다시 구하는 비자체무결(non-self-consistent, nscf)
계산으로 얻습니다.

## 7.1 공통 흐름: scf → (bands / nscf) → 후처리

```
scf   ─┬─▶  bands 계산 (경로 k점)  ─▶  bands.x  ─▶  밴드구조
       └─▶  nscf 계산 (촘촘한 격자) ─▶  dos.x    ─▶  상태밀도
                                     └─▶  projwfc.x ─▶  투영 DOS
```

세 단계 모두 같은 `prefix` 와 `outdir` 를 참조해야 SCF 전하밀도를 이어받습니다.

## 7.2 밴드구조 — bands 계산 + bands.x

먼저 고대칭점을 잇는 경로를 k점으로 주고 `calculation='bands'` 로 고윳값을
계산합니다.

```fortran
&control
  calculation = 'bands'
  prefix = 'si', outdir = './out', pseudo_dir = './pseudo'
/
&system
  ibrav=2, celldm(1)=10.26, nat=2, ntyp=1, ecutwfc=40, ecutrho=320
  nbnd = 8            ! 그리고 싶은 밴드 수(빈 밴드 포함)
/
...
K_POINTS {crystal_b}
5
  0.5000 0.5000 0.5000 40   ! L
  0.0000 0.0000 0.0000 40   ! Γ
  0.5000 0.0000 0.5000 40   ! X
  0.6250 0.2500 0.6250 40   ! U
  0.0000 0.0000 0.0000 1    ! Γ
```

각 줄은 고대칭점 좌표와 "다음 점까지 몇 개로 나눌지"입니다. 그 다음 `bands.x` 로
고윳값을 밴드별로 정렬해 그리기 좋은 형태로 내보냅니다.

```fortran
&bands
  prefix = 'si', outdir = './out'
  filband = 'si.bands.dat'
/
```

`bands.x` 는 `si.bands.dat.gnu`(k-거리 vs 에너지)와 고대칭점 위치를 출력합니다.

## 7.3 상태밀도 — nscf + dos.x

DOS는 경로가 아니라 **촘촘한 격자**에서 고윳값을 구해 에너지축으로 히스토그램을
만듭니다.

```fortran
&control
  calculation = 'nscf'
/
&system
  ...
  occupations = 'tetrahedra'   ! DOS에는 tetrahedra가 매끄럽습니다
/
K_POINTS (automatic)
  16 16 16 0 0 0
```

이어 `dos.x` 로 상태밀도를 만듭니다.

```fortran
&dos
  prefix = 'si', outdir = './out'
  fildos = 'si.dos', DeltaE = 0.05
/
```

`si.dos` 는 `E(eV)  dos(E)  적분 dos` 세 열이고, 헤더에 페르미(또는 최고 점유)
준위가 적힙니다.

## 7.4 실제 결과 — 실리콘 밴드 + DOS

아래는 위 흐름을 QE 7.5로 실제 실행해 얻은 실리콘 결과입니다.

<figure>
  <img src="assets/images/qe-si-bands-dos.png" alt="실리콘 밴드구조와 상태밀도" style="width:100%;max-width:940px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    실리콘 밴드구조(L–Γ–X–U–Γ)와 상태밀도(QE 7.5, PBE). 에너지는 최고 점유 준위
    (VBM)를 0으로 맞췄습니다. 원자가 밴드 최대는 Γ, 전도 밴드 최소는 X 근처라
    <b>간접 띠간격 ≈ 0.57 eV</b>가 나옵니다(PBE의 알려진 과소평가; 실험값 약 1.1 eV).
    오른쪽 DOS의 채워진 영역이 원자가 밴드, 간격 위가 전도 밴드입니다. 실행 절차는
    <a href="ex-02-si-bands.html">예제 E2</a> 참고.
  </figcaption>
</figure>

<div class="note">
  <div class="note-title">PBE 띠간격은 작게 나옵니다</div>
  <p>
    표준 DFT(LDA/PBE)는 반도체 띠간격을 체계적으로 작게 예측합니다. 실리콘의
    실험 간격은 약 1.1 eV지만 PBE는 0.6 eV 안팎이 나옵니다. 정확한 간격이 필요하면
    하이브리드 범함수(HSE)나 GW 같은 상위 방법이 필요합니다 — 밴드 <i>모양</i>은
    PBE도 잘 재현합니다.
  </p>
</div>

## 7.5 투영 DOS — projwfc.x

`projwfc.x` 는 상태밀도를 원자·궤도(s, p, d)별로 분해합니다. 어떤 원자의 어떤
궤도가 특정 에너지의 상태에 기여하는지 볼 때 씁니다.

```fortran
&projwfc
  prefix = 'si', outdir = './out'
  filpdos = 'si.pdos', DeltaE = 0.05
/
```

결과 `si.pdos.pdos_atm#...` 파일들을 합치면 궤도별 기여를 그릴 수 있습니다.

## 7.6 요점

- 밴드/DOS는 SCF 전하밀도를 고정한 nscf 계산입니다 — `prefix`·`outdir` 일치가 핵심.
- 밴드구조는 경로 k점(`crystal_b`) + `bands.x`, DOS는 촘촘한 격자 + `dos.x`.
- DOS에는 `tetrahedra`(또는 금속이면 smearing)가 매끄럽습니다.
- PBE 띠간격은 실험보다 작게 나오는 것이 정상입니다.
