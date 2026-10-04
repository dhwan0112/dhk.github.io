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

<p class="amm-id">NOTE 31-05-00 · 상호작용 모델</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 LAMMPS 입력에서 원자 사이의 상호작용을 정의하는 명령을 다룬다.
2. 대상 명령은 `pair_style`, 결합 계열 style, `kspace_style` 이다.

### B. 적용 범위

1. LAMMPS는 원자 사이의 상호작용을 크게 두 갈래로 나눠 표현한다.
    1. 비결합 상호작용 (non-bonded): `pair_style` 로 정의한다. 두 원자 사이의 거리만으로 정해지는 상호작용(LJ, 쿨롱, EAM 등)이 여기 속한다.
    1. 결합 상호작용 (bonded): `bond_style`, `angle_style`, `dihedral_style`, `improper_style` 로 정의한다. 분자 시스템에서만 쓴다.
2. 여기에 장범위 정전기를 위한 **`kspace_style`** 이 더해진다.

### C. 결과 요약

1. style은 박스를 정의하기 *전에* 한 번 선언한다.
2. 계수는 박스를 정의한 *뒤에* `pair_coeff`, `bond_coeff` 등으로 준다.
3. 이 단계의 오류는 거의 항상 4.A 의 네 가지 사례 중 하나다.

## 2. 준비 정보

### A. 필요한 개념

1. 단위계(`units`)와 `atom_style` 을 정해 두어야 한다.
2. 박스 정의 명령의 위치를 알아야 한다. style 선언은 그 앞에, 계수 입력은 그 뒤에 온다.

### B. 참조 자료

| 참조 | 제목 |
|---|---|
| LAMMPS 매뉴얼, style별 페이지 | 각 style의 계수 의미 |
| 사용할 힘장의 원본 논문 | 힘장이 가정하는 functional form |

### D. 관련 파일

| 항목 | 용도 |
|---|---|
| `Cu_u3.eam` | EAM 매개변수 파일 (3.D) |
| 데이터 파일 (`Bonds`, `Angles`, `Dihedrals` 섹션) | 결합 type 지정 (3.E) |

## 3. 절차

### A. pair_style 선택

1. 쓰려는 힘장의 원본 논문이 어떤 functional form을 가정하는지 확인한다.
2. 그에 맞는 style을 아래 표에서 고른다.

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

### B. lj/cut 설정 (LJ 액체)

1. `pair_style` 과 `pair_coeff` 를 다음과 같이 입력한다.

```lammps
pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5
#                ^ ^  ^   ^   ^
#                i j  ε   σ   cutoff (옵션)
```

2. `pair_coeff i j eps sigma cutoff` 형식으로 type 조합마다 한 번씩 입력한다.
3. i ≠ j 조합은 `pair_modify mix arithmetic` 또는 `geometric` 으로 자동 생성할 수도 있다.

### C. lj/cut/coul/long 설정 (분자 시스템)

1. 단위계, atom_style, pair_style, kspace_style 을 다음과 같이 함께 입력한다.

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

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
`lj/cut/coul/long` 은 단거리 LJ와 단거리 쿨롱을 직접 계산하고, 장거리 쿨롱은 `kspace_style` 에 맡긴다. OPLS-AA, AMBER, CHARMM 계열은 대부분 이 조합을 쓴다.
</div>

### D. eam 설정 (금속)

1. 단위계, atom_style, pair_style 을 다음과 같이 입력한다.

```lammps
units           metal
atom_style      atomic

pair_style      eam
pair_coeff      * * Cu_u3.eam
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
EAM은 매개변수 파일 하나에 모든 정보가 들어 있어서 `pair_coeff` 가 아주 간단하다. `* *` 는 "모든 type 조합"을 뜻한다.
</div>

### E. 결합 상호작용 설정

1. 분자 시스템(`atom_style full` 또는 `molecular`)에서는 결합·각·이면각 계수를 함께 정의한다.

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

2. 계수가 무엇을 뜻하는지는 style마다 다르므로 매뉴얼의 해당 페이지에서 확인한다.
3. 데이터 파일에서 `Bonds`, `Angles`, `Dihedrals` 섹션을 읽는다. 어느 결합이 어떤 type 인지는 자동으로 들어간다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
`harmonic` 말고도 `morse`, `class2`, `fourier`, `charmm` 등의 style이 있다.
</div>

### F. 장범위 정전기 설정: kspace_style

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
쿨롱 상호작용을 그냥 절단하면(`coul/cut`) 시스템에 따라 큰 인공물이 생긴다. 그래서 정전기가 있는 시스템은 거의 다 장범위 처리를 한다.
</div>

1. 정전기가 있는 시스템에 `kspace_style` 을 선언한다.

```lammps
kspace_style    pppm 1.0e-4      # Particle-Particle Particle-Mesh, 정확도 1e-4
# 또는
kspace_style    ewald 1.0e-6     # 작은 시스템용
# 또는
kspace_style    msm 1.0e-4       # 슬랩/비주기 일부에 유리
```

2. 시스템 크기와 경계 조건에 맞는 알고리즘을 아래 표에서 고른다.

| 알고리즘 | 특징 |
|----------|------|
| `ewald` | 정통 Ewald 합. 작은 시스템(원자 수 < ~수천)에 효율적 |
| `pppm` | mesh 기반 Ewald. 큰 시스템에서 가장 흔히 쓰임 |
| `msm`  | multi-level summation. 비주기 차원 처리에 강점 |

3. *완전 주기적*(p p p) 시스템에는 PPPM을 쓴다. PPPM은 이 경우에 가장 잘 동작한다.
4. *일부 차원이 비주기적*(p p f) 인 슬랩 시스템에는 MSM을 검토한다. MSM은 이 경우 보정 비용이 작다.
5. 슬랩 시스템에서 PPPM을 쓰려면 `kspace_modify slab 3.0` 같은 보정을 더한다.

## 4. 시험 및 검사

### A. 잘못 짝지은 흔한 사례 점검

1. `atom_style atomic` 인데 `bond_style` 을 선언하지 않았는지 확인한다. 결합 정보를 저장할 공간 자체가 없어 오류가 난다.
2. `kspace_style` 을 선언했다면 `pair_style` 이 `coul/long` 류인지 확인한다. 아니면 `kspace_style` 은 의미가 없다.
3. 단위계와 계수 단위가 맞는지 확인한다. 예: `units real` 인데 eV 단위의 EAM 파일.
4. 데이터 파일 안의 type 수와 `pair_coeff` 의 type 수가 맞는지 확인한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
이 단계에서 오류가 나면 거의 항상 위 넷 중 하나다.
</div>
