---
layout: default
title: "5. 상호작용 모델"
nav_order: 6
---

# 5. 상호작용 모델
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 5.1 LAMMPS의 상호작용 표현

LAMMPS에서 원자 사이의 상호작용은 크게 두 갈래로 표현됩니다.

- **비결합 상호작용 (non-bonded)** — `pair_style` 로 정의.
  두 원자 사이의 거리만으로 결정되는 모든 상호작용(LJ, 쿨롱, EAM 등).
- **결합 상호작용 (bonded)** — `bond_style`, `angle_style`,
  `dihedral_style`, `improper_style`. 분자 시스템에서만 사용.

추가로 장범위 정전기를 위한 **`kspace_style`** 이 있습니다.

각 style은 박스가 정의되기 *전에* 한 번 선언되고, 계수 입력은 박스 정의
*후에* `pair_coeff`, `bond_coeff` 등으로 줍니다.

## 5.2 pair_style 개관

가장 자주 마주치는 pair_style 들을 짧게 정리하면 다음과 같습니다.

| pair_style | 용도 |
|-----------|------|
| `lj/cut` | 순수 Lennard-Jones, 절단 거리 |
| `lj/cut/coul/cut` | LJ + 단순 절단 쿨롱 |
| `lj/cut/coul/long` | LJ + 장범위 쿨롱 (kspace 필요) |
| `morse` | Morse 포텐셜 (결합 해리 모델) |
| `buck` | Buckingham (산화물 등) |
| `eam`, `eam/alloy`, `eam/fs` | EAM (금속) |
| `tersoff`, `tersoff/mod` | Tersoff (공유 결합 비금속) |
| `meam`, `meam/c` | MEAM (금속·반도체) |
| `reaxff` | ReaxFF (반응성 시뮬레이션) |
| `airebo`, `rebo` | 탄소 시스템 (REBO/AIREBO) |
| `sw` | Stillinger-Weber (Si, Ge) |
| `hybrid`, `hybrid/overlay` | 위 style들을 한 시뮬레이션에서 조합 |

자신이 쓰려는 힘장의 원본 논문이 어떤 functional form을 가정하는지 확인한 뒤
그에 해당하는 style을 골라야 합니다.

### lj/cut 예제 (LJ 액체)

```lammps
pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5
#                ^ ^  ^   ^   ^
#                i j  ε   σ   cutoff (옵션)
```

`pair_coeff i j eps sigma cutoff` 형식. 모든 type 조합에 대해 한 번씩 입력해야
하지만, `pair_modify mix arithmetic` 또는 `geometric` 으로 i ≠ j 조합을
자동 생성할 수도 있습니다.

### lj/cut/coul/long 예제 (분자 시스템)

```lammps
units           real
atom_style      full

pair_style      lj/cut/coul/long 10.0 10.0
pair_coeff      1 1 0.1660 3.5000   # 예: OPLS-AA의 C, kcal/mol·Å
pair_coeff      2 2 0.0300 2.5000   # 예: H
# ...
pair_modify     mix geometric tail yes
kspace_style    pppm 1.0e-4
```

`lj/cut/coul/long` 은 단거리 LJ + 단거리 쿨롱은 직접 계산하고, 장거리
쿨롱은 `kspace_style` 에 위임합니다. OPLS-AA, AMBER, CHARMM 계열의
대부분이 이 조합을 사용합니다.

### eam 예제 (금속)

```lammps
units           metal
atom_style      atomic

pair_style      eam
pair_coeff      * * Cu_u3.eam
```

EAM은 단일 매개변수 파일에 모든 정보가 들어 있으므로 `pair_coeff` 가 매우
간단합니다. `* *` 는 "모든 type 조합"을 뜻합니다.

## 5.3 결합 상호작용

분자 시스템(`atom_style full` 또는 `molecular`)은 결합·각·다이히드럴
계수도 함께 정의해야 합니다.

```lammps
bond_style      harmonic
bond_coeff      1   340.0  1.090     # K(kcal/mol/Å²), r0(Å)

angle_style     harmonic
angle_coeff     1    33.0  107.8     # K(kcal/mol/rad²), θ0(°)

dihedral_style  opls
dihedral_coeff  1   0.0  0.0  0.30  0.0

improper_style  harmonic
improper_coeff  1   1.1   0.0
```

각 style의 계수 의미는 매뉴얼의 해당 페이지에서 확인하셔야 합니다.
`harmonic` 외에 `morse`, `class2`, `fourier`, `charmm` 등이 있습니다.

데이터 파일에서 `Bonds`, `Angles`, `Dihedrals` 섹션을 가져오면 어떤 결합이
어떤 type 인지가 자동으로 들어갑니다.

## 5.4 장범위 정전기 — kspace_style

쿨롱 상호작용을 단순히 절단하면(`coul/cut`) 시스템에 따라 큰 인공물이
생깁니다. 따라서 정전기가 있는 시스템은 거의 대부분 장범위 처리를 합니다.

```lammps
kspace_style    pppm 1.0e-4      # Particle-Particle Particle-Mesh, 정확도 1e-4
# 또는
kspace_style    ewald 1.0e-6     # 작은 시스템용
# 또는
kspace_style    msm 1.0e-4       # 슬랩/비주기 일부에 유리
```

| 알고리즘 | 특징 |
|----------|------|
| `ewald` | 정통 Ewald 합. 작은 시스템(원자 수 < ~수천)에 효율적 |
| `pppm` | mesh 기반 Ewald. 큰 시스템에서 가장 흔히 쓰임 |
| `msm`  | multi-level summation. 비주기 차원 처리에 강점 |

PPPM은 *완전 주기적*(p p p) 시스템에 가장 잘 동작하고, MSM은 *일부 차원이
비주기적*(p p f) 인 슬랩 시스템에서 보정 비용이 작습니다.

슬랩 시스템에서 PPPM을 쓰려면 `kspace_modify slab 3.0` 같은 보정을 추가합니다.

## 5.5 잘못 매칭한 흔한 사례

- `atom_style atomic` 인데 `bond_style` 을 선언 → 결합 정보 자체를 저장할
  공간이 없어 오류.
- `kspace_style` 을 선언했는데 `pair_style` 이 `coul/long` 류가 아니면 의미 X.
- 단위계와 계수 단위가 어긋남 — 예: `units real` 인데 eV 단위의 EAM 파일.
- 데이터 파일 안의 type 수와 `pair_coeff` 의 type 수가 어긋남.

오류 메시지가 떨어지면 거의 항상 위 네 가지 중 하나입니다.

## 5.6 다음 단계

상호작용이 정의되면 비로소 시뮬레이션을 "돌릴" 준비가 끝납니다. 다음 장에서는
시뮬레이션 셋업의 마지막 단계 — 초기 속도, 시간 간격, fix(앙상블),
minimize, run — 를 다룹니다.
