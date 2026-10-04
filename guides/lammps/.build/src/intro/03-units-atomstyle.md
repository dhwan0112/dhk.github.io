---
layout: default
title: "3. 단위계와 atom_style"
nav_order: 4
---

# 3. 단위계와 atom_style
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---
<p class="amm-id">NOTE 31-03-00 · 단위계와 atom_style 선택</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 `units` 명령으로 단위계를 정하는 절차를 다룬다.
2. 이 노트는 `atom_style` 명령으로 원자가 갖는 속성을 정하는 절차를 다룬다.
3. 두 명령과 짝을 맞춰야 하는 명령을 확인한다.

### B. 적용 범위

1. 모든 LAMMPS 입력 스크립트의 초기화 단계에 적용한다.
2. `units` 와 `atom_style` 은 모두 박스를 만들기 전에 선언한다.

### C. 결과 요약

1. 실제로는 `real`, `metal`, `lj` 세 단위계를 압도적으로 많이 쓴다.
2. 응용 단계에서 가장 흔히 고르는 atom_style 은 `full`(분자 + 전하)과 `atomic`(단순 입자)이다.
3. 기본값은 `units lj`, `atom_style atomic` 이다.
4. `units` 와 `atom_style` 은 뒤따르는 거의 모든 명령의 의미를 좌우한다.

## 2. 준비 정보

### A. 필요한 개념

1. NOTE 31-02-00 의 4단계 구조 중 초기화 단계를 알아야 한다.

### B. 참조 자료

| 참조 | 제목 |
|---|---|
| LAMMPS 공식 매뉴얼 | `units`, `atom_style` 명령 |
| NOTE 31-02-00 | [입력 스크립트 구조](02-input-structure.html) |

## 3. 절차

### A. 단위계 선언

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
한 번 정한 단위는 시뮬레이션 전체에 적용되고 **박스를 정의한 뒤에는 바꿀 수 없다**.
</div>

1. 입력 스크립트의 거의 첫 줄에 `units` 를 둔다. 이것이 관례다.

```lammps
units           real      # 또는 lj, metal, electron, si, cgs, micro, nano
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
LAMMPS 내부의 산술은 늘 같다. 입력값과 출력값을 어떤 물리 단위로 해석할지는 `units` 명령이 정한다. 기본값은 `lj` 다.
</div>

### B. 단위계 비교

1. 아래 표에서 각 단위계의 길이·시간·에너지·질량 단위를 확인한다.

| `units` | 길이 | 시간 | 에너지 | 질량 | 주된 사용처 |
|---------|------|------|--------|------|-------------|
| `lj`       | σ (환원) | τ (환원) | ε (환원) | m (환원) | LJ/입자 시뮬레이션 |
| `real`     | Å | fs | kcal/mol | g/mol | 생체·유기 분자 (OPLS, AMBER, CHARMM) |
| `metal`    | Å | ps | eV | g/mol | 금속·결정 (EAM, MEAM, Tersoff) |
| `electron` | Bohr | fs | Hartree | amu | 전자 구조 또는 양자 결합 |
| `si`       | m | s | J | kg | 표준 SI |
| `cgs`      | cm | s | erg | g | 고전 CGS |
| `micro`    | µm | µs | 유도값 | pg | 마이크로 입자 / 콜로이드 |
| `nano`     | nm | ns | 유도값 | ag | 나노 스케일 MD |

2. 실제로 많이 쓰는 세 단위계의 용도를 확인한다.
    1. **`real`**: 생체분자, 폴리머, 일반 유기물. 시간 단위 fs와 에너지 kcal/mol이 대부분의 분자역학 교과서와 같다.
    2. **`metal`**: 금속, 반도체, 산화물. EAM·Tersoff·MEAM 같은 금속용 포텐셜과 짝을 이룬다.
    3. **`lj`**: 환원 단위. 교과서 예제, 모델 입자, 빠른 테스트에 알맞다.

### C. 단위계 선택

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
단위를 바꾸면 수치를 모두 다시 환산해야 한다. 같은 시스템을 <code>real</code> 에서 <code>metal</code> 로 바꾸면 온도·시간·에너지 값이 모두 다르게 해석된다. 예를 들어 <code>timestep 1.0</code> 은 <code>real</code> 에서는 1 fs, <code>metal</code> 에서는 1 ps다. 같은 숫자가 천 배 다른 시간을 가리킬 수 있다. 단위를 바꿨다면 입력 전체를 다시 점검한다.
</div>

1. 사용할 힘장(또는 포텐셜)을 확인한다.
2. 힘장 파라미터가 보고된 단위에 맞춰 단위계를 고른다. 이것이 가장 안전하다.
    1. OPLS·AMBER·CHARMM 계열은 `real` 을 쓴다.
    2. EAM·MEAM·Tersoff 등 금속 포텐셜은 `metal` 을 쓴다.
    3. 교과서 LJ 입자는 `lj` 를 쓴다.
3. 결과를 보고할 단위를 확인한다.
4. 단위계를 결과 보고 단위와 맞춘다. 맞추면 분석할 때 단위를 따로 통일할 필요가 없다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
매뉴얼에 따르면 LAMMPS 의 출력은 모두 `units` 가 정한 단위로 나온다. `dump` 의 좌표는 길이 단위, `thermo` 의 에너지는 에너지 단위 그대로다.
</div>

### D. atom_style 선언

1. 박스를 만들기 전에 `atom_style` 을 한 번 선언한다. `atom_style` 은 원자 하나가 갖는 속성을 정한다.

```lammps
atom_style      atomic     # 또는 charge, molecular, full, bond, angle, ...
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
기본값은 `atomic` 이다.
</div>

### E. atom_style 선택

1. 아래 표에서 시스템에 맞는 atom_style 을 고른다.

| `atom_style` | 갖는 속성 | 대표 사용 사례 |
|--------------|-----------|----------------|
| `atomic`     | 위치, 속도, type | LJ 입자, 단순 금속(EAM 등) |
| `charge`     | atomic + 전하 | 이온 결정, 단순 전해질 |
| `bond`       | atomic + 결합 정보 | 결합만 있는 단순 폴리머 |
| `angle`      | bond + 각도 | 가벼운 분자 (e.g. SPC 물 모델은 angle 또는 full) |
| `molecular`  | bond + angle + dihedral + improper | 분자 시스템 (전하 X) |
| `full`       | molecular + 전하 | 대부분의 생체분자 시뮬레이션 (CHARMM, AMBER, OPLS) |
| `dipole`     | atomic + 쌍극자 모멘트 | 점쌍극자 모델 |
| `sphere`     | atomic + 회전·반지름 | 거대 입자(DEM, granular) |
| `ellipsoid`  | sphere + 비등방 회전 | Gay-Berne 같은 비대칭 입자 |

2. 데이터 파일을 만들었거나 받았다면, 그 파일이 가정하는 atom_style 을 먼저 확인한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
응용 단계에서 가장 흔히 고르는 것은 **`full`**(분자 + 전하)과 **`atomic`**(단순 입자)이다. 입문 단계에서는 이 둘만 기억해도 된다.
</div>

### F. 짝을 이루는 명령 맞추기

1. 다음 명령의 값을 `units` 와 `atom_style` 에 맞춘다.
    1. `mass`: 단위계에 맞는 질량 값을 입력한다.
    2. `pair_style`, `pair_coeff`: 힘장 파라미터를 단위계에 맞게 입력한다.
    3. `timestep`: `real` 은 보통 1.0 (fs), `metal` 은 0.001 (ps), `lj` 는 0.005 정도가 출발점이다.
    4. `velocity ... create T`: `T` 는 단위계의 온도 단위다.

## 4. 시험 및 검사

### A. atom_style 불일치 점검

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
데이터 파일에 전하가 있는데 `atom_style atomic` 또는 `bond` 로 선언하면 전하가 무시된다. 이 경우 에너지 값이 이상하게 나온다.
</div>

1. "Bonds defined but no bond_style" 오류가 나는지 확인한다. 데이터 파일에 결합 정보가 있는데 `atom_style atomic` 으로 선언한 경우에 난다.
2. 데이터 파일에 전하가 있다면 선언한 atom_style 이 전하를 포함하는지 확인한다.
