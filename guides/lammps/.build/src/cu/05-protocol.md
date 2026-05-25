---
layout: default
title: "5. 5단계 시뮬레이션 프로토콜"
nav_order: 6
---

# 5. 5단계 시뮬레이션 프로토콜
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

본 가이드는 다음 다섯 단계 프로토콜을 모두 유지한다.
각 단계는 분자동역학적/화학적 정당화가 있으며, 어느 하나라도 생략하면 시뮬레이션 안정성이 위협받는다.

| 단계 | 통합기 (Integrator) | 온도 제어 | 압력 제어 | 목적 |
|------|---------------------|-----------|------------|------|
| 1. 소프트 완화 | NVE/limit | 없음 | 없음 | 원자 중첩 해소 |
| 2. 에너지 최소화 | (정적) | 없음 | 없음 | 국소 최소점 도달 |
| 3. 단계적 가열 | NVT (Langevin) | 0.1 → 300 K | 없음 (정용량) | 운동 에너지 점진 주입 |
| 4. 평형화 | NVT | 300 K | 없음 | 열역학 평형 분포 확보 |
| 5. 생성 동역학 | NVT | 300 K | 없음 | 통계 수집 |

## 5.1 Stage 1: 소프트 완화 (Soft potential relaxation)

### 화학적 정당화

초기 데이터 파일은 무작위로 배치된 벤젠/에탄올 분자를 포함하므로,
일부 원자 쌍이 LJ σ 거리보다 가까운 위치에 있을 수 있다.
표준 12-6 LJ는 $r \to 0$에서 발산하므로, 일반 통합기로 통합하면 즉시 폭발 (numerical explosion) 한다.

소프트 포텐셜은 다음과 같은 부드러운 함수로 LJ를 임시 대체한다.

$$
U_{\text{soft}}(r) = A\left[1 + \cos\left(\frac{\pi r}{r_c}\right)\right] \quad (r < r_c)
$$

[LAMMPS pair_soft 문서](https://docs.lammps.org/pair_soft.html) 참조.

$A$ 값을 0에서 점진적으로 증가시키면 중첩된 원자가 부드럽게 밀려나면서 분리된다.
대안으로 `fix nve/limit`를 사용해 한 시간 스텝의 최대 변위를 제한하는 방법도 있다.

### 권장 LAMMPS 명령어

본 가이드는 `fix nve/limit`를 사용한다. 이는 변위를 제한하면서도
실제 힘장을 그대로 쓰므로 단계 전환이 매끄럽다.

```bash
# Stage 1: Soft relaxation (fix nve/limit 방식)
include  ff_opls_aa.in     # 또는 ff_trappe_ua.in
include  kspace_pppm.in    # 또는 kspace_msm.in

velocity        all create 1.0 12345 mom yes rot yes dist gaussian
fix             1 all nve/limit 0.05    # 한 스텝당 최대 변위 0.05 Å
fix             2 wall all wall/lj93 zhi EDGE 0.1 3.0 10.0 units box

thermo          100
thermo_style    custom step temp press pe ke etotal
timestep        0.5
run             5000

unfix           1
unfix           2 wall
write_data      01_soft_relaxed.data nocoeff
```

`fix nve/limit 0.05`: 한 시간 스텝에 5 % σ 정도의 변위만 허용 (이상값은 5%σ 미만의 0.05 Å).
[LAMMPS fix nve/limit 문서](https://docs.lammps.org/fix_nve_limit.html)에서 자세히 다룬다.
이 방법은 SHAKE 등 강제 구속과 호환된다.

## 5.2 Stage 2: 에너지 최소화 (Energy minimization)

### 화학적 정당화

Stage 1에서 변위 제한으로 큰 힘이 사라졌다면, Stage 2에서는
실제 힘장 위에서 conjugate gradient (CG) 또는 steepest descent 방법으로
국소 최소점으로 이동한다. 이는 운동 에너지가 없는 0 K 정적 평형 구조를 의미한다.

분자동역학적으로 0 K 구조는 통계 평균에 직접 사용되지 않지만,
이후 가열 단계에서 안전하게 운동 에너지를 주입할 수 있는 "안정된 출발점" 을 제공한다.

### 권장 LAMMPS 명령어

```bash
# Stage 2: Energy minimization
include  ff_opls_aa.in
include  kspace_pppm.in
read_data 01_soft_relaxed.data add append

fix      wall_top all wall/lj93 zhi EDGE 0.1 3.0 10.0 units box

min_style cg
minimize  1.0e-4 1.0e-6 1000 10000

unfix     wall_top
write_data 02_minimized.data nocoeff
```

`minimize 1.0e-4 1.0e-6 1000 10000`의 의미 ([LAMMPS minimize 문서](https://docs.lammps.org/minimize.html)):

- `etol = 1.0e-4`: 에너지 변화 허용치 (상대값)
- `ftol = 1.0e-6`: 힘의 norm 허용치 (kcal/mol/Å)
- `maxiter = 1000`: 최대 반복 횟수
- `maxeval = 10000`: 최대 힘/에너지 평가 횟수

`min_style cg` (conjugate gradient) 는 일반적으로 가장 효율적이지만,
초기 구조가 매우 나쁘면 `min_style sd` (steepest descent) 로 먼저 몇 백 스텝을 돌리는 것도 좋다.

## 5.3 Stage 3: 단계적 가열 (Staged heating)

### 화학적 정당화 — 왜 단계적으로 가열해야 하는가

분자가 0 K 정적 구조에서 갑자기 300 K 로 가열되면 다음 문제가 발생한다.

1. **벤젠 π-π 적층 (stacking) 구조 붕괴**: 초기 잠재 에너지 곡면의 깊은 우물에서 갑작스러운 운동 에너지가
   국소 미세 구조를 무너뜨린다.
2. **에탄올 수소 결합 네트워크 형성 지연**: 수소 결합은 협동적으로 형성되는데,
   고온에서는 이러한 네트워크가 잘 만들어지지 않는다.
3. **표면 흡착층의 비물리적 탈리**: 0 K 흡착 분자가 갑자기 큰 운동 에너지를 받으면 표면에서 떨어진다.

따라서 다음 단계적 가열이 권장된다:

| 부단계 | 온도 범위 | 지속 시간 | 핵심 화학적 사건 |
|--------|-----------|------------|------------------|
| 3.1 | 0.1 → 10 K | 50 ps | 벤젠 π-π stacking 안정화 |
| 3.2 | 10 → 100 K | 100 ps | 분자 진동/회전 모드 활성화 |
| 3.3 | 100 → 200 K | 100 ps | 에탄올 수소 결합 네트워크 재배열 |
| 3.4 | 200 → 300 K | 100 ps | 액체상 평형 분자 운동 도달 |

### 권장 LAMMPS 명령어 — Langevin 동역학 사용

가열 단계에서는 Langevin 열냉수 (thermostat) 가 효과적이다.
이는 가속화된 평형화를 위한 random force 항을 명시적으로 포함하기 때문이다
([LAMMPS fix langevin 문서](https://docs.lammps.org/fix_langevin.html)).

```bash
# Stage 3: Staged heating (Langevin 방식)
include  ff_opls_aa.in
include  kspace_pppm.in
read_data 02_minimized.data add append

# 그룹 정의 (분석/구속용)
group    organic   type 1:11    # OPLS-AA의 경우
group    copper    type 12

# Cu 슬랩 고정 (옵션: 가열 단계에서 슬랩이 움직이지 않도록)
fix      freeze_cu copper setforce 0.0 0.0 0.0

# 상부 벽
fix      wall_top organic wall/lj93 zhi EDGE 0.1 3.0 10.0 units box

# Langevin 열냉수: 시간 변동 온도 사용
fix      integrator organic nve
fix      thermostat organic langevin 0.1 10.0 100.0 12345

velocity organic create 0.1 12345 mom yes rot yes dist gaussian

thermo        100
thermo_style  custom step temp press pe ke etotal
timestep      0.5
run           100000     # 0.1 → 10 K, 50 ps

unfix    thermostat
fix      thermostat organic langevin 10.0 100.0 100.0 12346
run      200000           # 10 → 100 K, 100 ps

unfix    thermostat
fix      thermostat organic langevin 100.0 200.0 100.0 12347
run      200000           # 100 → 200 K, 100 ps

unfix    thermostat
fix      thermostat organic langevin 200.0 300.0 100.0 12348
run      200000           # 200 → 300 K, 100 ps

unfix    thermostat
unfix    integrator
unfix    wall_top
unfix    freeze_cu
write_data 03_heated.data nocoeff
```

`fix langevin T_start T_stop damp seed`의 의미:

- `T_start, T_stop`: 시작/종료 온도 (K)
- `damp`: 감쇠 시간 (시간 단위, 본 단위계 `real`에서는 fs).
  100 fs는 일반적인 권장값으로, 임계 감쇠 조건에 가깝다 (PIMD_1MD 1.4절 참조).
- `seed`: 난수 시드 (스테이지마다 다른 값 권장)

### 시간 스텝 (timestep) 의 화학적 선택

- **OPLS-AA**: 가벼운 H 원자의 진동이 약 ~2700 cm⁻¹ (X-H stretch) 이므로,
  시간 스텝은 0.5-1.0 fs 권장. SHAKE 사용 시 2.0 fs까지 가능.
- **TraPPE-UA**: 무거운 united-atom 사이트의 진동만 다루므로 1.0-2.0 fs 가능.

본 가이드에서는 두 힘장 통일성을 위해 가열 단계에서 **0.5 fs** 사용.

## 5.4 Stage 4: 평형화 (Equilibration)

### 화학적 정당화

가열 단계 종료 시점의 시스템은 목표 온도에 도달했지만,
분자 분포는 아직 평형 (Boltzmann) 분포를 정확히 따르지 않을 수 있다.
평형화 단계는 자기 상관 시간 (autocorrelation time, $\tau_A$) 의 최소 10배 정도 진행하여
관심 물리량 $\langle A \rangle$의 측정이 신뢰할 수 있도록 한다.

이 시점에서는 Langevin 보다 Nose-Hoover (fix nvt) 가 권장되는데,
이는 deterministic dynamics를 보존하면서도 정확한 canonical 앙상블을 샘플링하기 때문이다.

### 권장 LAMMPS 명령어

```bash
# Stage 4: Equilibration (NVT, Nose-Hoover)
include  ff_opls_aa.in
include  kspace_pppm.in
read_data 03_heated.data add append

group    organic   type 1:11
group    copper    type 12

fix      freeze_cu copper setforce 0.0 0.0 0.0
fix      wall_top organic wall/lj93 zhi EDGE 0.1 3.0 10.0 units box
fix      thermostat organic nvt temp 300.0 300.0 100.0

velocity organic scale 300.0

thermo          1000
thermo_style    custom step temp press pe ke etotal
timestep        1.0
run             2000000   # 2 ns 평형화

unfix    thermostat
unfix    wall_top
unfix    freeze_cu
write_data 04_equilibrated.data nocoeff
```

`fix nvt temp T_start T_stop damp`의 의미 ([LAMMPS fix nvt 문서](https://docs.lammps.org/fix_nh.html)):

- `T_start, T_stop`: 평형화 중에는 동일하게 설정 (목표 온도)
- `damp`: 시간 단위. `real` 단위에서는 100 fs가 일반 권장값.

### 평형화 진행 모니터링

평형화가 충분히 진행되었는지 다음을 확인한다:

1. **총 에너지의 안정화**: log 파일에서 etotal 의 평균이 변동 폭 이내에서 일정한지.
2. **표면 흡착층의 정착**: 표면 1차 흡착층 (Cu 표면 5 Å 이내) 의 평균 점유율이 일정한지.
3. **방사 분포 함수의 수렴**: 마지막 50% 와 그 이전 50% 의 g(r) 이 동일한지.

OPLS-AA의 경우 수소 결합 협동 효과로 인해 평형화에 약 7.5 ns 가 필요할 수 있다 (사용자 사전 경험).
TraPPE-UA는 더 짧은 시간 (2-3 ns) 으로 충분한 경우가 많다.

## 5.5 Stage 5: 생성 동역학 (Production)

### 화학적 정당화

이 단계의 데이터만 통계 평균에 사용된다.
평형화가 충분히 진행된 후, 시뮬레이션 시간이 자기 상관 시간의 충분한 배수가 되도록 한다.

### 권장 LAMMPS 명령어

```bash
# Stage 5: Production (NVT, 데이터 수집)
include  ff_opls_aa.in
include  kspace_pppm.in
read_data 04_equilibrated.data add append

group    organic   type 1:11
group    copper    type 12

fix      freeze_cu copper setforce 0.0 0.0 0.0
fix      wall_top organic wall/lj93 zhi EDGE 0.1 3.0 10.0 units box
fix      thermostat organic nvt temp 300.0 300.0 100.0

# RDF 계산 (예: Cu-O, Cu-benzene C 등)
# 본 가이드는 외부 후처리 (integrated_analysis.py) 를 사용하므로
# 여기서는 궤적과 thermo 정보만 저장
compute  msd_org organic msd com yes
compute  stress_atom all stress/atom NULL pair kspace bond angle dihedral improper

thermo          1000
thermo_style    custom step temp press pe ke etotal c_msd_org[4]
thermo_modify   norm no

# 궤적 저장
dump            traj all custom 1000 05_production.lammpstrj id type mol x y z
dump_modify     traj sort id

# 응력 텐서 (Irving-Kirkwood 계면 장력 계산용) 저장
fix             stress_save all ave/chunk 100 10 1000 &
                bin/1d z lower 1.0 units box file stress_profile.dat &
                density/mass v_stress_xx v_stress_yy v_stress_zz

variable        stress_xx atom -c_stress_atom[1]
variable        stress_yy atom -c_stress_atom[2]
variable        stress_zz atom -c_stress_atom[3]

timestep        1.0
run             5000000   # 5 ns production
write_data      05_produced.data nocoeff
```

### Production 단계의 시간 결정 기준

| 분석 대상 | 권장 production 시간 |
|-----------|---------------------|
| 표면 흡착 비율 (SEI) | 2-3 ns 이상 |
| 흡착 에너지 평균 | 3-5 ns |
| 계면 장력 (Irving-Kirkwood) | 5 ns 이상 |
| 수소 결합 수명 분포 | 5 ns 이상 |

OPLS-AA의 경우 수소 결합 동역학이 더 느리므로 더 긴 production이 필요할 수 있다.

## 5.6 통합 입력 파일 구조

본 가이드의 `inputs/` 디렉토리는 다음 모듈식 구조를 채택한다.

```
inputs/
├── common.in          # 단위, atom_style 등 공통 설정
├── ff_opls_aa.in      # OPLS-AA 파라미터 (pair_coeff 등)
├── ff_trappe_ua.in    # TraPPE-UA 파라미터
├── kspace_pppm.in     # PPPM 정전기 설정
├── kspace_msm.in      # MSM 정전기 설정
├── 01_soft.in         # Stage 1
├── 02_min.in          # Stage 2
├── 03_heat.in         # Stage 3
├── 04_eq.in           # Stage 4
└── 05_prod.in         # Stage 5
```

각 stage 파일은 `include` 명령어로 힘장과 kspace 설정을 불러온다.
프레임워크를 바꿀 때는 include 라인 두 줄만 수정하면 된다 ([LAMMPS include 문서](https://docs.lammps.org/include.html)).

```bash
# OPLS-AA + PPPM 사용 시
include ../ff_opls_aa.in
include ../kspace_pppm.in

# TraPPE-UA + MSM 사용 시
include ../ff_trappe_ua.in
include ../kspace_msm.in
```

이러한 모듈화는 사용자의 기존 단계 구조를 모두 유지하면서 프레임워크 교차 비교를 용이하게 한다.

## 참고문헌

1. LAMMPS 공식 문서, `pair_soft`:
   [https://docs.lammps.org/pair_soft.html](https://docs.lammps.org/pair_soft.html)

2. LAMMPS 공식 문서, `fix nve/limit`:
   [https://docs.lammps.org/fix_nve_limit.html](https://docs.lammps.org/fix_nve_limit.html)

3. LAMMPS 공식 문서, `minimize`:
   [https://docs.lammps.org/minimize.html](https://docs.lammps.org/minimize.html)

4. LAMMPS 공식 문서, `fix langevin`:
   [https://docs.lammps.org/fix_langevin.html](https://docs.lammps.org/fix_langevin.html)

5. LAMMPS 공식 문서, `fix nvt` (fix_nh):
   [https://docs.lammps.org/fix_nh.html](https://docs.lammps.org/fix_nh.html)

6. LAMMPS 공식 문서, `include`:
   [https://docs.lammps.org/include.html](https://docs.lammps.org/include.html)

7. M. P. Allen, D. J. Tildesley,
   "Computer Simulation of Liquids", 2nd ed., Oxford University Press (2017).
   ISBN: 9780198803195.

8. D. Frenkel, B. Smit,
   "Understanding Molecular Simulation: From Algorithms to Applications", 2nd ed.,
   Academic Press (2002). ISBN: 9780122673511.

---

[← 이전: 4. 정전기 방법](04-electrostatics) ｜ [다음: 6. 4가지 프레임워크 비교 →](06-frameworks)
