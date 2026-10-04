---
layout: default
title: "2. 입력 스크립트 구조"
nav_order: 3
---

# 2. 입력 스크립트 구조
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---
<p class="amm-id">NOTE 31-02-00 · 입력 스크립트 4단계 구조</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 LAMMPS 공식 매뉴얼이 정의하는 입력 스크립트의 4단계 구조를 다룬다.
2. 각 단계의 핵심 명령과 자주 쓰는 문법 요소(주석, 줄 바꿈, 변수, `include`)를 다룬다.

### B. 적용 범위

1. 모든 LAMMPS 입력 스크립트에 적용한다.
2. 명령어 순서는 대부분 이 4단계 구조로 정해진다.

### C. 결과 요약

1. 입력 스크립트는 초기화, 시스템 정의, 시뮬레이션 설정, 실행의 네 부분으로 구성된다.
2. 마지막 두 부분(설정과 실행)은 원하는 만큼 반복할 수 있다.
3. 실제 계산은 `run` 이나 `minimize` 를 호출해야 시작된다.

## 2. 준비 정보

### A. 참조 자료

| 참조 | 제목 |
|---|---|
| LAMMPS 공식 매뉴얼 | 입력 스크립트 구조 |
| NOTE 31-01-00 | [시작하기](01-getting-started.html) |

### D. 선행 조건

1. NOTE 31-01-00 의 LJ 액체 예제(`in.lj`)를 알아야 한다.

## 3. 절차

### A. 4단계 구조 확인

1. 입력 스크립트를 다음 네 부분 순서로 구성한다. 매뉴얼은 "전형적인 입력 스크립트는 다음 네 부분으로 구성된다"고 밝힌다.
    1. 초기화 (Initialization): 원자를 만들거나 읽기 전에 정해야 하는 전역 설정
    2. 시스템 정의 (System Definition): 시뮬레이션 박스와 원자를 만드는 단계
    3. 시뮬레이션 설정 (Simulation Settings): 힘장 계수, 출력, fix 등 모든 운영 옵션
    4. 실행 (Run a Simulation): `minimize`, `run` 등 실제 적분/최소화 명령
2. 필요하면 마지막 두 부분을 반복한다. 매뉴얼은 "**마지막 두 부분은 원하는 만큼 반복할 수 있다**"고 적어 두었다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
한 입력 파일 안에서 *설정 변경 → 짧은 run → 다른 설정 → 또 run* 처럼 여러 단계를 이어 쓰는 것이 정상적인 사용법이다. 입력 스크립트를 작성할 때마다 이 4단계 구조를 떠올린다.
</div>

<figure>
  <img src="assets/images/input-flow.svg" alt="LAMMPS 입력 스크립트의 4단계 표준 구조 다이어그램" style="width:100%;max-width:880px;height:auto;border:1px solid var(--border-color);border-radius:6px;background:#ffffff;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    그림 1. LAMMPS 입력 스크립트의 4단계 표준 구조와 각 단계의 대표 명령어.
    화살표가 가리키는 정방향은 한 번 실행 시 순서이고, 점선 화살표는 매뉴얼이
    명시한 "마지막 두 부분(Settings · Run)은 원하는 만큼 반복할 수 있다" 규칙.
  </figcaption>
</figure>

### B. 1단계: 초기화

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
아래 전역 설정은 원자를 만든 뒤에는 바꿀 수 없다.
</div>

1. 원자를 만들기 전에 다음 전역 설정을 선언한다.

| 명령 | 역할 |
|------|------|
| `units` | 단위계 선택 (lj, real, metal, …) |
| `dimension` | 시뮬레이션 차원 (2 또는 3) |
| `boundary` | 경계 조건 (p 주기적, f 고정, s 축소, m 다항식) |
| `atom_style` | 원자가 가지는 속성 종류 (atomic, charge, full, …) |
| `newton` | 작용-반작용 처리 방식 |
| `processors` | MPI 프로세스 분할 방식 |
| `pair_style`, `bond_style` 등 | 상호작용 모델의 종류 선언 |

### C. 2단계: 시스템 정의

1. 매뉴얼이 제시하는 세 가지 방법 중 하나로 박스와 원자를 만든다.
    1. 데이터 파일에서 읽기: `read_data`
    2. 재시작 파일에서 읽기: `read_restart`
    3. 격자/영역을 정의하고 원자를 채우기: `lattice` → `region` → `create_box` → `create_atoms`

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
분자 단위 시스템(단백질, 폴리머 등)은 거의 항상 `read_data` 로 외부 파일에서 읽어 들인다. 결정이나 단순 액체는 격자에서 직접 만드는 편이다.
</div>

### D. 3단계: 시뮬레이션 설정

1. 다음 명령으로 힘장 계수, 출력, fix 등 운영 옵션을 설정한다. 명령이 가장 많이 등장하는 단계다.

| 명령 | 역할 |
|------|------|
| `pair_coeff`, `bond_coeff` 등 | 힘장 계수 입력 |
| `kspace_style` | 장범위 정전기 알고리즘 (ewald, pppm) |
| `neighbor`, `neigh_modify` | 이웃 리스트 관리 |
| `group` | 원자 집합을 이름으로 묶기 |
| `velocity` | 초기 속도 설정 |
| `timestep` | 적분 시간 간격 |
| `fix` | NVE/NVT/NPT, 제약, 외력 등 거의 모든 운영 효과 |
| `compute` | 특정 양(에너지, RDF 등) 계산 정의 |
| `thermo`, `dump` | 화면 출력 / 좌표 출력 |
| `restart` | 재시작 파일 저장 주기 |

### E. 4단계: 실행

1. 다음 명령 중 하나로 계산을 시작한다.

| 명령 | 역할 |
|------|------|
| `minimize` | 에너지 최소화 |
| `run` | 지정 스텝 수만큼 동역학 적분 |
| `rerun` | 기존 trajectory를 다시 처리 |
| `temper` | parallel tempering(레플리카 교환) |

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
실제 계산은 `run` 이나 `minimize` 를 호출해야 비로소 시작된다. 그 전까지의 명령은 "설정을 쌓아 둘" 뿐이다.
</div>

### F. 예제 스크립트에 단계 주석 달기

1. [1장](01-getting-started.html)의 LJ 액체 예제를 위 4단계로 나눈다.
2. 각 단계 앞에 주석을 단다.

```lammps
# === 1단계: 초기화 ===
units           lj
atom_style      atomic

# === 2단계: 시스템 정의 ===
lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 box
mass            1 1.0

# === 3단계: 시뮬레이션 설정 ===
pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5

velocity        all create 1.44 87287 loop geom

neighbor        0.3 bin
neigh_modify    every 20 delay 0 check no

fix             1 all nve
thermo          50

# === 4단계: 실행 ===
run             250
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
이 정도 단위로 주석을 달아 두면 나중에 다시 읽을 때 각 명령이 속한 단계가 한눈에 보인다.
</div>

### G. 주석과 줄 바꿈

1. 주석은 `#` 으로 시작한다. 줄 중간에 `#` 이 나오면 그 뒤도 주석으로 무시된다.
2. 명령이 길어지면 줄 끝에 `&` 를 붙여 다음 줄로 이어 쓴다.

```lammps
fix             1 all npt &
                temp 300.0 300.0 100.0 &
                iso  1.0   1.0   1000.0
```

### H. 변수와 치환

1. `variable` 로 입력 안에서 변수를 정의한다.
2. 정의한 변수는 `${var}` 형태로 어디서나 참조한다.

```lammps
variable        T equal 300.0
variable        seed equal 12345

velocity        all create ${T} ${seed}
fix             1 all nvt temp ${T} ${T} 100.0
```

3. 필요하면 명령줄에서 변수를 넘긴다(`-var` 또는 `-v`).

```bash
lmp -in in.run -var T 400 -var seed 99999
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
명령줄 변수는 같은 입력을 여러 온도에서 돌릴 때 편하다.
</div>

### I. include: 입력 파일 분할

1. 입력이 길어지면 `include` 로 여러 파일에 나눈다.

```lammps
include         ff_opls.in       # 힘장 정의 한 파일
include         system.in        # 박스/원자 한 파일
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
파일을 나누면 관리하기 쉽다. 응용 시리즈에서는 이 방식을 많이 쓴다.
</div>
