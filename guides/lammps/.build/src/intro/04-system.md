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
<p class="amm-id">NOTE 31-04-00 · 박스와 원자 만들기</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 시뮬레이션 박스와 원자를 만드는 절차를 다룬다.
2. 이 노트는 `boundary` 명령으로 경계 조건과 박스 모양을 정하는 절차를 다룬다.

### B. 적용 범위

1. 입력 스크립트 4단계 구조 중 2단계(시스템 정의)에 적용한다.
2. 단순 액체, 결정 슬랩 + 진공, 분자 시스템의 세 패턴을 다룬다.

### C. 결과 요약

1. 매뉴얼이 제시하는 방법은 `read_data`, `read_restart`, `lattice` → `region` → `create_box` → `create_atoms` 의 세 가지다.
2. 한 입력에서 두 가지 이상을 섞어 써도 된다.
3. 슬랩 시뮬레이션은 보통 `p p f` 나 `p p m` 경계 조건을 쓴다.

## 2. 준비 정보

### A. 필요한 개념

1. NOTE 31-03-00 의 `units` 와 `atom_style` 선택을 알아야 한다.

### B. 참조 자료

| 참조 | 제목 |
|---|---|
| LAMMPS 공식 매뉴얼 | 시스템 정의 명령 |
| NOTE 31-03-00 | [단위계와 atom_style](03-units-atomstyle.html) |
| NOTE 32-00-00 | [Cu 응용 시리즈](cu-overview.html) |

### C. 사용 프로그램

| 항목 | 용도 |
|---|---|
| VMD + TopoTools (가장 흔함) | 데이터 파일 생성 |
| OpenBabel / Avogadro | 데이터 파일 생성 |
| moltemplate | 지정한 분자 템플릿을 LAMMPS 입력으로 변환 |
| MDAnalysis / ASE 등 Python 라이브러리 | 데이터 파일 생성 |

### D. 관련 파일

| 항목 | 용도 |
|---|---|
| `system.data` | 분자 시스템 데이터 파일(3.D, 3.H) |
| `ff_opls.in` | 힘장 정의 파일(3.H) |

## 3. 절차

### A. 생성 방법 선택

1. 아래 표에서 시스템에 맞는 방법을 고른다. LAMMPS 매뉴얼은 박스와 원자를 만드는 방법으로 다음 세 가지를 든다.

| 방법 | 핵심 명령 | 어떤 경우에 |
|------|-----------|-------------|
| 데이터 파일에서 읽기 | `read_data` | 분자 시스템, 토폴로지가 복잡한 경우 |
| 재시작 파일에서 읽기 | `read_restart` | 이전 시뮬레이션에서 이어 가는 경우 |
| 격자에서 만들기 | `lattice` → `region` → `create_box` → `create_atoms` | 결정, 슬랩, 단순 액체 |

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
한 입력에서 두 가지 이상을 섞어 써도 된다. 예컨대 금속 슬랩은 격자에서 만들고, 그 위에 흡착할 분자는 데이터 파일에서 읽는다.
</div>

### B. 격자에서 만들기

1. `lattice` 명령으로 결정 격자를 정의한다.
2. `region` 으로 영역을 정의한다.
3. `create_box` 로 박스를 만든다.
4. `create_atoms` 로 원자를 채운다.

```lammps
units           lj
atom_style      atomic

lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 box

mass            1 1.0
```

5. 각 줄의 의미를 확인한다.
    1. `lattice fcc 0.8442`: fcc 격자, 환원 밀도 0.8442 (LJ 단위계)
    2. `region box block 0 10 0 10 0 10`: `box` 라는 이름의 직육면체 영역, 격자 단위로 각 축 0~10
    3. `create_box 1 box`: 위 region 안에 원자 타입 1개를 위한 박스 생성
    4. `create_atoms 1 box`: 타입 1 원자로 채우기

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
격자 종류로는 `fcc`, `bcc`, `hcp`, `sc`(단순입방), `diamond`, `custom` 등이 있다. `region` 은 `block`(직육면체) 말고도 `sphere`, `cylinder`, `prism`(비직교 박스용) 등을 지원한다.
</div>

### C. 격자 상수 단위 확인

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
`units lj` 에서는 격자 상수 자리에 "환원 밀도"가 들어간다. `units real` 이나 `units metal` 과 의미가 다르다.
</div>

1. `units real` 이나 `units metal` 에서는 격자 상수를 Å 단위로 직접 준다.

```lammps
units           metal
atom_style      atomic

lattice         fcc 3.615        # Cu 격자 상수 (Å)
region          slab block 0 8 0 8 0 6
create_box      1 slab
create_atoms    1 slab

mass            1 63.546
```

### D. 데이터 파일에서 읽기

1. 외부 도구(2.C)로 데이터 파일을 만든다.
2. `read_data` 로 데이터 파일을 읽어 들인다.

```lammps
units           real
atom_style      full

read_data       system.data
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
분자 시스템처럼 토폴로지(결합, 각도, 이면각)가 복잡하면 이 방법이 훨씬 편하다. 데이터 파일을 손으로 직접 쓰는 일은 드물다.
</div>

3. 데이터 파일의 헤더와 섹션 구성을 확인한다. 데이터 파일은 텍스트이고, 다음과 같은 헤더와 섹션으로 이루어진다.

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

4. 헤더에 박스 크기, 원자/결합/각도/이면각 개수와 종류 수가 있는지 확인한다.
5. `Atoms` 섹션의 형식이 `atom_style` 과 맞는지 확인한다.
    1. `full` 이라면 `atom-ID  molecule-ID  type  charge  x  y  z` 순서다.
6. 토폴로지를 쓴다면 `Bonds`, `Angles`, `Dihedrals`, `Impropers` 섹션이 차례대로 있는지 확인한다.

### E. 경계 조건과 박스 모양 설정

1. `boundary` 명령으로 세 축의 경계 조건을 정한다.

```lammps
boundary        p p p     # 3D 주기적 (기본)
boundary        p p f     # x, y는 주기적; z는 고정 (슬랩에 흔함)
boundary        f f f     # 클러스터 (모든 면 비주기)
```

2. 각 기호의 의미를 확인한다.
    1. `p`: 주기적(periodic)
    2. `f`: 고정(fixed). 원자가 이 면을 넘으면 사라진다("lost atom" 오류).
    3. `s`: 축소형(shrink-wrapped). 박스가 원자를 따라 줄어든다.
    4. `m`: minimum shrink-wrapped. `s` + 최소 박스 크기 보장.
3. 슬랩 시뮬레이션(표면 흡착, 박막 등)에서는 보통 `p p f` 나 `p p m` 조합을 쓴다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
슬랩 조합에서는 장범위 정전기에 슬랩 보정(`kspace_modify slab`)이 함께 필요할 수 있다.
</div>

4. 박스가 비직교(triclinic)라면 기울기를 정의한다. `lattice` 명령 옵션, `region prism`, 또는 `read_data` 헤더의 `xy xz yz` 항목을 쓴다.

### F. 패턴 A: 단순 액체

1. 격자에서 LJ 액체를 만든다.

```lammps
units           lj
atom_style      atomic
lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 box
mass            1 1.0
```

### G. 패턴 B: 결정 슬랩 + 진공

1. 격자에서 Cu 슬랩을 만든다.
2. `change_box` 로 위쪽에 진공 영역을 추가한다.

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

### H. 패턴 C: 분자 시스템

1. 데이터 파일을 읽는다.
2. 힘장 정의는 별도 파일에서 `include` 로 읽는다.

```lammps
units           real
atom_style      full

read_data       system.data
include         ff_opls.in   # 힘장 정의는 별도 파일에
```

## 5. 종료

### B. 후속 작업

1. 응용 단계에서는 패턴 B와 C를 합쳐 "결정 슬랩 + 그 위의 분자 시스템"을 만든다. 자세한 내용은 [Cu 응용 시리즈](cu-overview.html)에 있다.
