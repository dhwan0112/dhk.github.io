---
layout: default
title: "4. 시스템 정의"
nav_order: 5
---

# 4. 시스템 정의
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 4.1 매뉴얼이 제시하는 세 가지 방법

LAMMPS 매뉴얼은 박스와 원자를 만드는 방법으로 다음 세 가지를 제시합니다.

| 방법 | 핵심 명령 | 어떤 경우에 |
|------|-----------|-------------|
| 데이터 파일에서 읽기 | `read_data` | 분자 시스템, 토폴로지가 복잡한 경우 |
| 재시작 파일에서 읽기 | `read_restart` | 이전 시뮬레이션에서 이어 가는 경우 |
| 격자에서 만들기 | `lattice` → `region` → `create_box` → `create_atoms` | 결정, 슬랩, 단순 액체 |

세 방법 중 두 가지 이상을 한 입력에서 섞어 쓸 수도 있습니다.
예컨대 금속 슬랩은 격자에서 만들고, 그 위에 흡착할 분자는 데이터 파일에서
읽는 식입니다.

## 4.2 격자에서 만들기

가장 간단한 방법은 `lattice` 명령으로 결정 격자를 정의한 뒤 그 위에
원자를 채우는 것입니다.

```lammps
units           lj
atom_style      atomic

lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 box

mass            1 1.0
```

각 줄의 의미:

- `lattice fcc 0.8442` — fcc 격자, 환원 밀도 0.8442 (LJ 단위계)
- `region box block 0 10 0 10 0 10` — `box` 라는 이름의 직육면체 영역,
  격자 단위로 각 축 0~10
- `create_box 1 box` — 위 region 안에 원자 타입 1개를 위한 박스 생성
- `create_atoms 1 box` — 타입 1 원자로 채우기

격자 종류는 `fcc`, `bcc`, `hcp`, `sc`(단순입방), `diamond`, `custom` 등이
있습니다. `region` 은 `block`(직육면체) 외에 `sphere`, `cylinder`, `prism`
(비직교 박스용) 등을 지원합니다.

### 격자 상수 단위

`units real` 또는 `units metal` 에서는 격자 상수를 Å 단위로 직접 줍니다.

```lammps
units           metal
atom_style      atomic

lattice         fcc 3.615        # Cu 격자 상수 (Å)
region          slab block 0 8 0 8 0 6
create_box      1 slab
create_atoms    1 slab

mass            1 63.546
```

`units lj` 에서는 격자 상수 자리에 "환원 밀도"가 들어가는 점이 다릅니다.

## 4.3 데이터 파일에서 읽기

분자 시스템처럼 토폴로지(결합, 각도, 다이히드럴)가 복잡하면 외부 도구로
데이터 파일을 만든 뒤 `read_data` 로 읽어들이는 것이 훨씬 편합니다.

```lammps
units           real
atom_style      full

read_data       system.data
```

데이터 파일은 텍스트이며, 다음과 같은 헤더와 섹션으로 구성됩니다.

```text
LAMMPS data file from custom tool

   1234 atoms
    800 bonds
    600 angles
    400 dihedrals

      5 atom types
      4 bond types
      3 angle types
      2 dihedral types

   0.0  30.0  xlo xhi
   0.0  30.0  ylo yhi
   0.0  41.895 zlo zhi

Masses

1   12.011
2    1.008
...

Atoms       # full

1   1  1   -0.18   0.000   0.000   3.000
2   1  2    0.06   0.500   0.000   3.000
...

Bonds

1   1   1   2
...
```

- 헤더에는 박스 크기, 원자/결합/각도/다이히드럴 개수와 종류 수가 들어갑니다.
- `Atoms` 섹션의 형식은 `atom_style` 에 따라 달라집니다.
  `full` 의 경우 `atom-ID  molecule-ID  type  charge  x  y  z` 순서입니다.
- 토폴로지를 쓴다면 `Bonds`, `Angles`, `Dihedrals`, `Impropers` 섹션도 차례대로.

데이터 파일을 직접 손으로 작성하는 일은 드물고, 보통은 다음 도구로 생성합니다.

- **VMD + TopoTools** (가장 흔함)
- **OpenBabel / Avogadro**
- **moltemplate** (지정한 분자 템플릿을 LAMMPS 입력으로 변환)
- **MDAnalysis / ASE** 등 Python 라이브러리

## 4.4 경계 조건과 박스 모양

`boundary` 명령은 세 축의 경계 조건을 정합니다.

```lammps
boundary        p p p     # 3D 주기적 (기본)
boundary        p p f     # x, y는 주기적; z는 고정 (슬랩에 흔함)
boundary        f f f     # 클러스터 (모든 면 비주기)
```

- `p` — 주기적(periodic)
- `f` — 고정(fixed). 원자가 이 면을 넘으면 사라집니다("lost atom" 오류).
- `s` — 축소형(shrink-wrapped). 박스가 원자를 따라 줄어듭니다.
- `m` — minimum shrink-wrapped. `s` + 최소 박스 크기 보장.

슬랩 시뮬레이션(표면 위 흡착, 박막 등)에서는 보통 `p p f` 또는 `p p m`
조합을 사용합니다. 이 경우 장범위 정전기에는 슬랩 보정 (`kspace_modify slab`)이
함께 필요할 수 있습니다.

박스 자체가 비직교(triclinic)라면 `lattice` 명령 옵션이나 `region prism`
또는 `read_data` 헤더의 `xy xz yz` 항목으로 기울임을 정의합니다.

## 4.5 시스템 만들기의 흔한 패턴 세 가지

### 패턴 A: 단순 액체

```lammps
units           lj
atom_style      atomic
lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 box
mass            1 1.0
```

### 패턴 B: 결정 슬랩 + 진공

```lammps
units           metal
atom_style      atomic
boundary        p p f

lattice         fcc 3.615
region          slab block 0 8 0 8 0 6
create_box      1 slab
create_atoms    1 slab
mass            1 63.546

# 위쪽에 진공 영역 추가 (change_box)
change_box      all z final 0.0 60.0
```

### 패턴 C: 분자 시스템

```lammps
units           real
atom_style      full

read_data       system.data
include         ff_opls.in   # 힘장 정의는 별도 파일에
```

응용 단계로 가면 패턴 B와 패턴 C를 결합해 "결정 슬랩 + 그 위에 분자 시스템"을
구성하게 되는데, 이는 [Cu 응용 시리즈](cu-overview.html)에서 자세히 다룹니다.

## 4.6 다음 단계

박스와 원자가 만들어졌다면, 이제 그 원자들이 서로 어떻게 상호작용할지
정의할 차례입니다. 다음 장에서는 LAMMPS의 상호작용 모델
(`pair_style`, bonded styles, `kspace_style`)을 개관합니다.
