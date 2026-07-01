---
layout: default
title: "3. Cu(100) 슬랩"
---

# 3. Cu(100) 슬랩 — 금속 표면 만들기
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 무엇을 하는 예제인가

`metal` 단위와 EAM 포텐셜로 fcc 구리 (100) 슬랩을 만들고, 위쪽에 진공을 둔
`boundary p p f` 계를 300 K에서 짧게 돌린다. 표면 흡착 응용 시리즈가 전제하는
"슬랩 + 진공" 기하를 가장 작은 형태로 실제로 구성해 보는 예제다. 외부 데이터
파일 없이 `lattice` + `create_atoms` 로 슬랩을 만들기 때문에 EAM 포텐셜 파일
하나만 있으면 그대로 돌아간다.

관련 개념은 [응용 · 1. 시스템 개요](cu-01-system.html) 에서 다룬다.

<figure>
  <img src="assets/images/cu-cell.svg" alt="Cu 표면 흡착 시뮬레이션 셀의 슬랩 기하 모식도" style="width:100%;max-width:860px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    본 예제가 만드는 셀 기하의 모식도. 아래 예제는 이 중 Cu 슬랩 부분만 단독으로
    실행한다(유기 분자·상부 벽은 응용 시리즈에서 추가한다).
  </figcaption>
</figure>

## 전체 입력 스크립트 — `in.cu_slab`

```lammps
# Cu(100) 슬랩 — 슬랩+진공 기하 (cu-01 §1.2 예시)
units           metal
atom_style      atomic
boundary        p p f

lattice         fcc 3.615
region          sim   block 0 8 0 8 0 12 units lattice
create_box      1 sim
region          slab  block 0 8 0 8 0 6  units lattice
create_atoms    1 region slab
mass            1 63.546

pair_style      eam/alloy
pair_coeff      * * Cu_mishin1.eam.alloy Cu

# 하단 한 층 고정, 나머지는 열냉수
region          bot   block INF INF INF INF 0 0.6 units lattice
group           bottom region bot
group           mobile subtract all bottom

velocity        mobile create 300.0 4928459 mom yes rot yes dist gaussian
fix             freeze bottom setforce 0.0 0.0 0.0
fix             integ  mobile nvt temp 300.0 300.0 0.1

timestep        0.002
thermo          500
thermo_style    custom step temp pe etotal press
run             10000

# z 방향 수 밀도 프로파일
reset_timestep  0
compute         cc all chunk/atom bin/1d z lower 0.25 units box
fix             zd all ave/chunk 100 50 5000 cc density/number file zdens.dat
run             5000

write_dump      all custom slab_final.dump id type x y z modify sort id
```

`region sim` 은 z를 12셀(약 43 Å)까지 잡지만 원자는 아래 6셀(약 22 Å)에만
만들어, 위쪽 절반이 진공으로 남는다. `boundary p p f` 로 x·y는 주기, z는 비주기다.
하단 한 층을 `setforce 0` 으로 고정해 슬랩이 z 방향으로 떠내려가지 않게 한다.

## 실행

```bash
# EAM 포텐셜을 먼저 받는다 (lammps.org 배포 포텐셜)
#   Cu_mishin1.eam.alloy  (Mishin et al., Phys. Rev. B 63, 224106, 2001)
lmp -in in.cu_slab > out.cu_slab
```

포텐셜 파일 `Cu_mishin1.eam.alloy` 를 입력과 같은 디렉토리에 두어야 한다. 이
포텐셜은 구리 응집 에너지 −3.54 eV/atom 을 재현한다.

## 출력과 결과

원자 1664개, 300 K NVT로 약 20 ps 데운 뒤 밀도 프로파일을 측정한다.

<figure>
  <img src="assets/images/cu-slab.png" alt="Cu(100) 슬랩의 측면도와 z 방향 원자 밀도 프로파일" style="width:100%;max-width:880px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    왼쪽 측면도(x–z 투영)에 하단의 이산적인 Cu 원자층과 그 위 진공이 그대로 보인다.
    오른쪽 z-밀도 프로파일의 각 봉우리는 (100) 원자 한 층(층 간격 ≈ 1.81 Å)이며,
    진공에서 밀도가 0으로 떨어진다. LAMMPS 22 Jul 2025, EAM Mishin 2001.
  </figcaption>
</figure>

## 요점

- `metal` 단위에서 거리는 Å, 에너지는 eV, timestep은 ps다(여기서 0.002 ps = 2 fs).
- `boundary p p f` + 위쪽 진공이 표면 흡착 시뮬레이션의 표준 슬랩 설정이다.
- `compute chunk/atom bin/1d z` + `fix ave/chunk` 로 z 방향 밀도 프로파일을 얻는다.
- 하단 층 고정(`setforce 0`)은 슬랩 표류를 막는 관용적인 방법이다.

## 관련 개념 챕터

- [응용 · 1. 시스템 개요](cu-01-system.html) — 슬랩 기하와 결정면
- [04 시스템 정의](04-system.html) — `lattice` · `create_atoms`
- [05 상호작용 모델](05-forcefield.html) — EAM 등 `pair_style`

앞 예제는 [E2 — LJ 5단계](ex-02-lj-demo.html), 다음은
[E4 — Cu 벤젠-에탄올 흡착](ex-04-cu-adsorption.html) 이다.
