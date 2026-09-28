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

시뮬레이션은 다음 다섯 단계를 거친다.
단계마다 필요한 이유가 있고, 하나라도 건너뛰면 계가 불안정해지기 쉽다.

| 단계 | 적분기 (Integrator) | 온도 제어 | 압력 제어 | 목적 |
|------|---------------------|-----------|------------|------|
| 1. 소프트 완화 | NVE/limit | 없음 | 없음 | 원자 중첩 해소 |
| 2. 에너지 최소화 | (정적) | 없음 | 없음 | 국소 최소점 도달 |
| 3. 단계적 가열 | NVT (Langevin) | 0.1 → 300 K | 없음 (정용량) | 운동 에너지 점진 주입 |
| 4. 평형화 | NVT | 300 K | 없음 | 열역학 평형 분포 확보 |
| 5. Production | NVT | 300 K | 없음 | 통계 수집 |

<figure>
  <img src="assets/images/cu-protocol.svg" alt="5단계 시뮬레이션 프로토콜의 온도 일정 타임라인" style="width:100%;max-width:880px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    그림 1. 다섯 단계의 온도 일정. 1~2단계는 0 K 부근에서 중첩 해소와 최소화를 거치고,
    3단계에서 0.1 → 10 → 100 → 200 → 300 K로 단계적으로 가열한 뒤, 4~5단계는 300 K
    등온에서 평형화와 통계 수집을 한다. 각 박스 아래에 적분기/열욕과 대표 지속
    시간을 표기했다. 가로축 시간 폭은 비례 축척이 아니다.
  </figcaption>
</figure>

<div class="tip">
  <div class="note-title">입력 구성으로 보기</div>
  <p>
    5단계의 모듈식 입력 구성과 실행 흐름은
    <a href="ex-04-cu-adsorption.html">예제 E4 — Cu 벤젠-에탄올 흡착</a> 에 한데 모아 두었다
    (데이터 파일이 없어 그대로는 실행되지 않는다는 점도 거기 적었다).
  </p>
</div>

## 5.1 Stage 1: 소프트 완화 (Soft potential relaxation)

### 왜 이 단계가 필요한가

초기 데이터 파일에는 벤젠/에탄올 분자가 무작위로 놓여 있어서
일부 원자 쌍이 LJ σ 보다 가까이 붙어 있을 수 있다.
12-6 LJ는 $r \to 0$에서 발산하므로, 보통의 적분기로 그대로 적분하면 곧바로 수치 폭발(numerical explosion)이 일어난다.

소프트 포텐셜은 LJ를 잠시 다음과 같은 부드러운 함수로 바꿔 놓는다.

$$
U_{\text{soft}}(r) = A\left[1 + \cos\left(\frac{\pi r}{r_c}\right)\right] \quad (r < r_c)
$$

[LAMMPS pair_soft 문서](https://docs.lammps.org/pair_soft.html) 참조.

$A$ 를 0에서 조금씩 키우면 겹친 원자가 부드럽게 밀려나 떨어진다.
`fix nve/limit`로 한 시간 스텝의 최대 변위를 제한하는 방법도 있다.

### LAMMPS 입력

여기서는 `fix nve/limit`를 쓴다. 변위는 제한하되 실제 힘장을 그대로 쓰므로
다음 단계로 매끄럽게 넘어간다.

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
SHAKE 같은 구속과도 함께 쓸 수 있다.

## 5.2 Stage 2: 에너지 최소화 (Energy minimization)

### 왜 이 단계가 필요한가

Stage 1에서 변위를 제한해 큰 힘을 없앴다면, Stage 2에서는
실제 힘장 위에서 conjugate gradient (CG) 나 steepest descent 로
국소 최소점까지 내려간다. 결과는 운동 에너지가 없는 0 K 정적 평형 구조다.

0 K 구조 자체를 통계 평균에 쓰지는 않는다. 다만 이어지는 가열 단계에서
운동 에너지를 안전하게 넣을 수 있는 "안정된 출발점"이 된다.

### LAMMPS 입력

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

`min_style cg` (conjugate gradient) 가 대개 가장 효율적이지만,
초기 구조가 아주 나쁘면 `min_style sd` (steepest descent) 로 몇 백 스텝 먼저 돌려도 된다.

## 5.3 Stage 3: 단계적 가열 (Staged heating)

### 왜 단계적으로 가열하나

0 K 정적 구조를 한 번에 300 K 로 올리면 다음 문제가 생긴다.

1. **벤젠 π-π 적층 (stacking) 구조 붕괴**: 초기 잠재 에너지 곡면의 깊은 우물에서 갑작스러운 운동 에너지가
   국소 미세 구조를 무너뜨린다.
2. **에탄올 수소 결합 네트워크 형성 지연**: 수소 결합은 협동적으로 형성되는데,
   고온에서는 이러한 네트워크가 잘 만들어지지 않는다.
3. **표면 흡착층의 비물리적 탈리**: 0 K 흡착 분자가 갑자기 큰 운동 에너지를 받으면 표면에서 떨어진다.

그래서 다음처럼 나눠서 가열한다.

| 부단계 | 온도 범위 | 지속 시간 | 주요 변화 |
|--------|-----------|------------|------------------|
| 3.1 | 0.1 → 10 K | 50 ps | 벤젠 π-π stacking 안정화 |
| 3.2 | 10 → 100 K | 100 ps | 분자 진동/회전 모드 활성화 |
| 3.3 | 100 → 200 K | 100 ps | 에탄올 수소 결합 네트워크 재배열 |
| 3.4 | 200 → 300 K | 100 ps | 액체상 평형 분자 운동 도달 |

### LAMMPS 입력 (Langevin 동역학)

가열 단계에는 Langevin 열욕(thermostat)이 잘 맞는다.
평형화를 앞당기는 random force 항이 명시적으로 들어 있기 때문이다
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
- `damp`: 감쇠 시간 (시간 단위, 여기서 쓰는 `real` 단위계에서는 fs).
  100 fs가 흔히 쓰는 값이고, 임계 감쇠 조건에 가깝다 (PIMD_1MD 1.4절 참조).
- `seed`: 난수 시드 (스테이지마다 다른 값을 쓴다)

### 시간 스텝 (timestep) 고르기

- **OPLS-AA**: 가벼운 H 원자의 진동이 약 ~2700 cm⁻¹ (X-H stretch) 이므로,
  시간 스텝은 0.5-1.0 fs 정도로 잡는다. SHAKE를 쓰면 2.0 fs까지 늘릴 수 있다.
- **TraPPE-UA**: 무거운 united-atom 사이트의 진동만 다루므로 1.0-2.0 fs 도 된다.

여기서는 두 힘장을 맞추려고 가열 단계에서 **0.5 fs** 를 썼다.

## 5.4 Stage 4: 평형화 (Equilibration)

### 왜 이 단계가 필요한가

가열이 끝난 시점에 온도는 목표에 도달했어도,
분자 분포는 아직 평형(Boltzmann) 분포를 정확히 따르지 않을 수 있다.
그래서 평형화는 자기 상관 시간(autocorrelation time, $\tau_A$)의 10배 이상 돌려서
관심 물리량 $\langle A \rangle$ 을 믿고 잴 수 있게 만든다.

이 단계부터는 Langevin 대신 Nose-Hoover (fix nvt) 를 쓴다.
deterministic dynamics를 유지하면서도 canonical 앙상블을 정확히 샘플링하기 때문이다.

### LAMMPS 입력

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
- `damp`: 시간 단위. `real` 단위에서는 보통 100 fs.

### 평형화 진행 모니터링

평형화가 충분한지는 다음으로 확인한다.

1. **총 에너지의 안정화**: log 파일에서 etotal 의 평균이 변동 폭 이내에서 일정한지.
2. **표면 흡착층의 정착**: 표면 1차 흡착층 (Cu 표면 5 Å 이내) 의 평균 점유율이 일정한지.
3. **동경 분포 함수의 수렴**: 마지막 50% 와 그 이전 50% 의 g(r) 이 동일한지.

OPLS-AA는 수소 결합 협동 효과 때문에 평형화에 7.5 ns 가량 걸릴 수 있다(내 이전 런 기준).
TraPPE-UA는 그보다 짧은 2-3 ns 로 충분할 때가 많다.

## 5.5 Stage 5: Production

### 왜 이 단계가 필요한가

통계 평균에는 이 단계의 데이터만 쓴다.
평형화가 충분히 끝난 뒤, 자기 상관 시간보다 넉넉히 길게 돌린다.

### LAMMPS 입력

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

| 분석 대상 | production 시간 기준 |
|-----------|---------------------|
| 표면 흡착 비율 (SEI) | 2-3 ns 이상 |
| 흡착 에너지 평균 | 3-5 ns |
| 계면 장력 (Irving-Kirkwood) | 5 ns 이상 |
| 수소 결합 수명 분포 | 5 ns 이상 |

OPLS-AA는 수소 결합 동역학이 느려서 production을 더 길게 잡아야 할 수 있다.

## 5.6 통합 입력 파일 구조

`inputs/` 디렉토리는 다음과 같이 모듈로 나뉘어 있다.

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

각 stage 파일은 `include` 로 힘장과 kspace 설정을 불러온다.
프레임워크를 바꿀 때는 include 라인 두 줄만 수정하면 된다 ([LAMMPS include 문서](https://docs.lammps.org/include.html)).

```bash
# OPLS-AA + PPPM 사용 시
include ../ff_opls_aa.in
include ../kspace_pppm.in

# TraPPE-UA + MSM 사용 시
include ../ff_trappe_ua.in
include ../kspace_msm.in
```

이렇게 나눠 두면 기존 단계 구조는 그대로 둔 채 프레임워크만 바꿔 가며 비교할 수 있다.

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

