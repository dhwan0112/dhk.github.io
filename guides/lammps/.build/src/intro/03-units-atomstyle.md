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

## 3.1 왜 단위계가 중요한가

LAMMPS 내부의 산술은 늘 같지만, 입력값과 출력값을 어떤 물리 단위로 읽을지는
`units` 명령이 정한다. 한 번 정한 단위는 시뮬레이션 전체에 적용되고
**박스를 정의한 뒤에는 바꿀 수 없다**. 그래서 입력 스크립트 거의 첫 줄에 두는 게
관례다.

```lammps
units           real      # 또는 lj, metal, electron, si, cgs, micro, nano
```

기본값은 `lj` 다.

## 3.2 자주 쓰는 단위계 한눈에

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

실제로는 이 가운데 세 가지를 압도적으로 많이 쓴다.

- **`real`**: 생체분자, 폴리머, 일반 유기물. 시간 단위 fs와 에너지 kcal/mol이
  대부분의 분자역학 교과서와 같다.
- **`metal`**: 금속, 반도체, 산화물. EAM·Tersoff·MEAM 같은 금속용
  포텐셜과 짝을 이룬다.
- **`lj`**: 환원 단위. 교과서 예제, 모델 입자, 빠른 테스트에 알맞다.

## 3.3 단위 선택 기준

대부분은 다음 두 가지만 따져 보면 정해진다.

1. **어떤 힘장(또는 포텐셜)을 쓰는가?**
   힘장 파라미터가 보고된 단위에 맞추는 게 가장 안전하다.
   OPLS·AMBER·CHARMM 계열은 `real`,
   EAM·MEAM·Tersoff 등 금속 포텐셜은 `metal`,
   교과서 LJ 입자는 `lj`.

2. **결과를 어떤 단위로 보고 싶은가?**
   매뉴얼에 따르면 LAMMPS의 출력은 모두 `units` 가 정한 단위로 나온다.
   `dump` 의 좌표는 길이 단위, `thermo` 의 에너지는 에너지 단위 그대로다.
   결과를 보고할 단위와 맞춰 두면 분석할 때 단위를 따로 통일할 필요가 없다.

<div class="warning">
  <div class="note-title">단위를 바꾸면 수치를 모두 다시 환산해야 한다</div>
  <p>
    같은 시스템을 <code>real</code> 에서 <code>metal</code> 로 바꾸면
    온도·시간·에너지 값이 모두 다르게 해석된다.
    예를 들어 <code>timestep 1.0</code> 은 <code>real</code> 에서는 1 fs,
    <code>metal</code> 에서는 1 ps다.
    같은 숫자가 천 배 다른 시간을 가리킬 수 있으니, 단위를 바꿨다면 입력 전체를
    다시 점검해야 한다.
  </p>
</div>

## 3.4 atom_style: 원자가 갖는 속성

`atom_style` 은 시뮬레이션 안의 원자 하나가 어떤 속성을 갖는지 정한다.
이 역시 박스를 만들기 전에 한 번 선언한다.

```lammps
atom_style      atomic     # 또는 charge, molecular, full, bond, angle, ...
```

기본값은 `atomic` 이다.

### 자주 쓰는 atom_style

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

응용 단계에서 가장 흔히 고르게 되는 건 **`full`**(분자 + 전하)과
**`atomic`**(단순 입자)이다. 당분간은 이 둘만 기억해도 된다.

### 잘못 고른 atom_style 의 흔한 증상

- "Bonds defined but no bond_style" 오류: 데이터 파일에 결합 정보가 있는데
  `atom_style atomic` 으로 선언한 경우.
- 전하가 무시되어 에너지 값이 이상하게 나오는 경우: 데이터 파일에 전하가 있는데
  `atom_style atomic` 또는 `bond` 로 선언한 경우.

데이터 파일을 만들었거나 받았다면, 그 파일이 어떤 atom_style 을 가정하고
만들어졌는지부터 확인하자.

## 3.5 짝을 이루는 명령들

`units` 와 `atom_style` 은 뒤따르는 거의 모든 명령의 의미를 좌우한다.
특히 다음 명령들과 짝을 맞춰 두어야 한다.

- `mass`: 단위계에 맞는 질량 값을 입력
- `pair_style`, `pair_coeff`: 힘장 파라미터를 단위계에 맞게
- `timestep`: `real` 은 보통 1.0 (fs), `metal` 은 0.001 (ps),
  `lj` 는 0.005 정도가 출발점
- `velocity ... create T`: `T` 는 단위계의 온도 단위
