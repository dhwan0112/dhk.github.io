---
layout: default
title: "6. 셋업과 실행"
nav_order: 7
---

# 6. 셋업과 실행
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 6.1 동역학을 돌리기 위한 마지막 한 묶음

박스, 원자, 힘장을 모두 정의했다면 시뮬레이션을 시작하기 전에 보통 다음을
더 정한다.

1. 초기 속도: `velocity`
2. 시간 간격: `timestep`
3. 이웃 리스트: `neighbor`, `neigh_modify`
4. 앙상블 / 제약: `fix`
5. 실행: `minimize` 또는 `run`

이 명령들은 늘 함께 다니다시피 해서, 입력 스크립트 3·4단계의 전형적인 마무리로
봐도 된다.

## 6.2 velocity: 초기 속도 부여

```lammps
velocity        all create 300.0 12345 mom yes rot yes dist gaussian
```

- `all`: 속도를 줄 그룹 이름 (`group` 명령으로 정의 가능, `all` 은 기본 제공)
- `create 300.0 12345`: 가우시안 분포로 온도 300 K, 시드 12345
- `mom yes`: 시스템 전체 운동량을 0으로 보정
- `rot yes`: 시스템 전체 각운동량을 0으로 보정 (비주기 시스템이라면 켜 둔다)
- `dist gaussian`: 가우시안 분포 (기본은 `uniform`)

비주기 시스템에서 `mom`/`rot` 을 켜지 않으면 시스템 전체가 일정한 속도로 흘러가
버린다(drift). 그냥 항상 켜 두는 편이 낫다.

## 6.3 timestep: 적분 시간 간격

```lammps
timestep        1.0      # units real 의 경우 1 fs
```

| `units` | 보통 출발점 |
|---------|-------------|
| `real`  | 1.0 (fs) |
| `metal` | 0.001 (ps = 1 fs) |
| `lj`    | 0.005 (τ) |

물이나 H 가 있는 시스템에서 1 fs로도 불안하다면, 보통은 결합을 SHAKE/RATTLE 로
구속하고 timestep을 2 fs로 늘린다.

```lammps
fix             shake all shake 0.0001 20 0 b 1 a 1
timestep        2.0
```

## 6.4 neighbor: 이웃 리스트

```lammps
neighbor        2.0 bin
neigh_modify    every 1 delay 0 check yes
```

- `neighbor 2.0 bin`: 이웃 리스트의 buffer skin 2.0 (단위계 길이), bin 방식
- `neigh_modify ...`: 매 step 마다 체크하고 필요하면 재구성

`units lj` 에서는 `neighbor 0.3 bin`, `units real / metal` 에서는
`neighbor 2.0 bin` 정도에서 시작하면 무난하다. 잘못 잡으면 "Lost atoms" 나
"Neighbor list overflow" 오류가 나기 쉽다.

## 6.5 fix: 거의 모든 것을 하는 명령

`fix` 는 LAMMPS에서 가장 자주 등장하는 명령이다.
앙상블 적분, 제약 조건, 외력, 측정량 평균, 통계 출력까지 거의 모두 fix로 표현한다.

기본 형식:

```lammps
fix             ID  group-ID  style  arguments...
```

자주 쓰는 적분 fix는 다음과 같다.

### NVE (마이크로캐노니컬)

```lammps
fix             1 all nve
```

가장 단순하다. 에너지 보존이 검증되는 유일한 앙상블이라 처음 시험할 때 자주 쓴다.

### NVT (캐노니컬, Nose-Hoover 열욕)

```lammps
fix             1 all nvt temp 300.0 300.0 100.0
#                          T_start T_stop T_damp
```

`T_damp` 는 timestep × 100 정도에서 시작한다(`units real` 에서 100 fs).

### NPT (등압등온)

```lammps
fix             1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
#                                                  ^ ^   ^   ^
#                                              P_axis P_s P_e P_damp
```

`iso` 외에 `aniso`(축별 독립), `tri`(완전 비등방), `x`/`y`/`z`(축 지정) 등이
가능하다. `P_damp` 는 보통 `T_damp × 10` 정도.

### Langevin 열욕 (NVT 대안)

```lammps
fix             1 all nve
fix             2 all langevin 300.0 300.0 100.0 12345
```

Langevin은 NVT와 비슷한 효과를 내면서, 표면 흡착이나 거대 분자 시스템에서는
Nose-Hoover보다 빨리 평형으로 끌고 간다.

<div class="caution">
  <div class="note-title">적분 fix는 한 개만</div>
  <p>
    같은 그룹에 적분 fix 두 개(예: <code>nve</code>와 <code>nvt</code>)를 동시에
    걸면 적분이 두 번 일어나 결과가 망가진다.
    Langevin과 NVE 조합처럼 "적분은 nve가, 온도 제어는 langevin이" 맡도록
    역할을 나눈 경우에만 두 fix를 같이 쓴다.
  </p>
</div>

### 그 외 자주 쓰는 fix

| fix | 역할 |
|-----|------|
| `fix shake` | 결합/각도 구속 (긴 timestep용) |
| `fix wall/lj93` | LJ 벽 (슬랩 비주기 면) |
| `fix recenter` | 시스템 무게 중심 고정 |
| `fix momentum` | 주기적으로 운동량 0으로 리셋 |
| `fix print` | 시뮬레이션 중 변수를 파일에 출력 |
| `fix ave/time` | 시간 평균 출력 |
| `fix indent` | 점진적 압축(인덴터) |

## 6.6 minimize: 에너지 최소화

격자에서 만들었거나 데이터 파일에서 막 읽은 시스템에는 너무 가깝게 놓인 원자가
종종 있어서, 첫 적분에서 폭주하곤 한다. `minimize` 를 먼저 돌려 두면 안전하다.

```lammps
min_style       cg                    # 또는 sd, fire, hftn
minimize        1.0e-4 1.0e-6 1000 10000
#               etol    ftol  maxiter maxeval
```

- `etol`: 에너지 수렴 기준 (상대 변화량)
- `ftol`: 힘 수렴 기준 (norm)
- `maxiter`: 최대 iteration
- `maxeval`: 최대 에너지/힘 평가 횟수

대개는 `cg`(conjugate gradient)면 충분하고, 초기 구조가 아주 거칠다면
`fire` 가 안정적이다.

## 6.7 run: 적분 실행

```lammps
run             10000
```

2장에서 말했듯 `run` 이나 `minimize` 를 호출하기 전까지는 설정만 쌓일 뿐
실제 계산은 일어나지 않는다.

`run` 명령에는 이런 옵션도 있다.

```lammps
run             10000 every 100 "print 'step $step done'"   # 매 100 step 후 명령 실행
run             50000 pre no post no                         # 연속 run의 초기화 생략
run             20000 start 0 stop 100000                    # fix nvt 의 T_start~T_stop 보정용
```

## 6.8 전형적인 입력 마무리

이것들을 한데 묶으면 입력 스크립트의 끝은 대개 다음과 같은 모양이 된다.

```lammps
# === 시뮬레이션 설정 ===
velocity        all create 300.0 12345 mom yes rot yes
timestep        1.0
neighbor        2.0 bin
neigh_modify    every 1 delay 0 check yes

# === 단계별 fix ===
min_style       cg
minimize        1.0e-4 1.0e-6 1000 10000

fix             1 all nvt temp 300.0 300.0 100.0
thermo          1000
run             50000              # 평형화

unfix           1
fix             1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
run             200000             # 생성 시뮬레이션
```

입문 예제는 거의 다 이 순서로 짤 수 있다.

<div class="tip">
  <div class="note-title">전체 예제로 보기</div>
  <p>
    아래에서 요약한 <code>in.demo</code> 의 전체 스크립트와 RDF·MSD 분석은
    <a href="ex-02-lj-demo.html">예제 E2 — LJ 5단계</a> 한 페이지에 모아 두었다.
  </p>
</div>

### 돌려 본 결과: LJ 액체의 NPT 안정성

위 패턴을 LJ 액체에 적용해 직접 돌려 보았다.
8 × 8 × 8 격자(fcc 0.8442, 원자 2048개)를 최소화 → NVT (T = 1.0, 2000 step) →
NPT (T = 1.0, P = 0.5, 3000 step) → production (NPT, 5000 step) 순서로 돌렸고,
LAMMPS 22 Jul 2025(conda-forge) 직렬 빌드에서 약 7초 걸렸다.

```lammps
# in.demo (요약) — 위 패턴의 LJ 버전, 실제 실행된 입력
units           lj
atom_style      atomic
lattice         fcc 0.8442
region          box block 0 8 0 8 0 8
create_box      1 box
create_atoms    1 box
mass            1 1.0
pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5
velocity        all create 1.0 12345 mom yes rot yes dist gaussian
neighbor        0.3 bin
neigh_modify    every 20 delay 0 check no

min_style       cg
minimize        1.0e-4 1.0e-6 1000 10000

fix             1 all nvt temp 1.0 1.0 0.5
run             2000
unfix           1

fix             2 all npt temp 1.0 1.0 0.5 iso 0.5 0.5 5.0
run             3000
# (이후 reset_timestep 0; production run 5000)
```

production 단계의 thermo를 보면 온도는 setpoint 1.0 부근에서 ±0.04 정도,
압력은 setpoint 0.5 부근에서 ±0.2 정도로 진동하며 평형을 유지한다.
밀도는 0.69–0.70 부근에서 NPT 평형에 이르렀다.

<figure>
  <img src="assets/images/lj-production.png" alt="LJ 액체 NPT production 단계의 온도·압력·밀도 추이" style="width:100%;max-width:980px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    그림 1. NPT production 5000 step의 thermo 추이. 좌: 온도가 setpoint T = 1.0
    근방에서 정착(thermostat 동작 확인). 중: 압력이 setpoint P = 0.5 근방으로
    수렴(barostat 동작 확인). 우: 밀도가 0.69–0.70 부근에서 평형.
  </figcaption>
</figure>

<div class="tip">
  <div class="note-title">NVT → NPT 흐름</div>
  <p>
    위 패턴(velocity → minimize → 짧은 NVT → NPT)은 작은 LJ 시스템부터 큰 분자
    시스템까지 거의 그대로 쓸 수 있다. 시스템에 따라 timestep, T_damp, P_damp 값만
    조정하면 된다. in.demo 와 출력 파일은 저장소의
    <code>guides/lammps/.build/lammps-demo/</code> 에 있다.
  </p>
</div>
