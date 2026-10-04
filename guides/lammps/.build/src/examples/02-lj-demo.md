---
layout: default
title: "2. LJ 5단계 + RDF·MSD"
---

# 2. LJ 액체: 최소화 → NVT → NPT → production + 분석
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<p class="amm-id">NOTE 33-02-00 · LJ 5단계 + RDF·MSD</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 [E1](ex-01-lj-basic.html) 의 LJ 계를 실제 연구에서 쓰는 형태로 넓힌다.
2. 에너지 최소화, NVT 가열, NPT 압력 평형화를 차례로 수행한다.
3. production 단계에서 동경 분포 함수 `g(r)` 와 평균 제곱 변위(MSD)를 측정한다.

### B. 적용 범위

1. 입력 파일 하나에 `minimize → fix nvt → fix npt → compute/fix ave` 흐름이 모두 들어 있다.
2. 이 골격은 입문 예제 대부분이 따르는 구조다.

### C. 결과 요약

1. production 단계에서 온도는 1.0 ± 0.04, 압력은 0.5 ± 0.2 부근에서 진동한다.
2. 밀도는 0.69–0.70 부근에서 NPT 평형에 이른다.
3. `g(r)` 첫 피크는 r ≈ 1.09 σ 에서 g(r) ≈ 2.41 이다.
4. 자기확산계수는 D ≈ 0.117 (LJ 단위)이다.

## 2. 준비 정보

### A. 참조 자료

| 참조 | 제목 |
|---|---|
| [E1](ex-01-lj-basic.html) | LJ 액체 (NVE) 첫 실행 |
| [06 셋업과 실행](06-fix-run.html) | `fix nvt/npt`, `minimize`, `run` |
| [07 출력과 분석](07-output.html) | `compute`, `fix ave/*`, 후처리 |
| [05 상호작용 모델](05-forcefield.html) | `pair_style lj/cut` |

### B. 공구 및 장비

| 항목 | 용도 |
|---|---|
| LAMMPS (`lmp`) | 시뮬레이션 실행. 3.B 의 실행 시간과 4절의 결과는 LAMMPS 22 Jul 2025 직렬 빌드 기준이다. |

### C. 소모품

| 항목 | 내용 |
|---|---|
| `in.demo` | 입력 스크립트 (3.A 에서 작성) |
| 데이터·포텐셜 파일 | 없음 |

### D. 선행 조건

1. NOTE 33-01-00 ([E1](ex-01-lj-basic.html))을 수행할 수 있어야 한다.

## 3. 절차

### A. 입력 작성: `in.demo`

1. 아래 내용으로 `in.demo` 를 작성한다.

```lammps
# LJ liquid: minimize -> NVT (T=1.0) -> NPT (T=1.0, P=0.5) -> production + rdf + msd
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

thermo_style    custom step temp press pe ke etotal density
thermo          200

# 1단계: 에너지 최소화
min_style       cg
minimize        1.0e-4 1.0e-6 1000 10000

# 2단계: NVT 가열/평형
fix             1 all nvt temp 1.0 1.0 0.5
run             2000
unfix           1

# 3단계: NPT 압력 평형 (T = 1.0, P = 0.5)
fix             2 all npt temp 1.0 1.0 0.5 iso 0.5 0.5 5.0
run             3000

# 4단계: 생성 + 측정 (RDF, MSD)
reset_timestep  0
compute         rdf1 all rdf 100
fix             rdfavg all ave/time 10 100 1000 c_rdf1[*] file rdf.dat mode vector

compute         msd1 all msd
fix             msdavg all ave/time 1 1 100 c_msd1[1] c_msd1[2] c_msd1[3] c_msd1[4] file msd.dat

thermo          100
run             5000
```

2. 원자 수를 확인한다. 8 × 8 × 8 격자이므로 원자는 2048개다.
3. `compute rdf` 결과가 `fix ave/time` 으로 시간 평균되어 `rdf.dat` 에 저장되는지 확인한다.
4. `compute msd` 결과가 `fix ave/time` 으로 시간 평균되어 `msd.dat` 에 저장되는지 확인한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
`compute` 는 값을 "정의"만 한다. 파일에 저장하려면 `fix ave/time` 으로 "꺼내야" 한다.
</div>

### B. 실행

1. 입력을 실행한다.

```bash
lmp -in in.demo > out.demo
```

2. 실행 시간을 확인한다. LAMMPS 22 Jul 2025 직렬 빌드에서 전체가 약 7초 걸렸다.

### C. 출력 확인

1. `out.demo`, `rdf.dat`, `msd.dat` 가 생겼는지 확인한다.

## 4. 시험 및 검사

### A. production 단계 안정성

1. production 단계의 thermo 에서 온도를 확인한다. setpoint 1.0 부근에서 ±0.04 정도로 진동하면 정상이다.
2. 압력을 확인한다. setpoint 0.5 부근에서 ±0.2 정도로 진동하면 정상이다.
3. 밀도를 확인한다. 0.69–0.70 부근에서 NPT 평형에 이르면 합격이다.

<figure>
  <img src="assets/images/lj-production.png" alt="LJ 액체 NPT production 단계의 온도·압력·밀도 추이" style="width:100%;max-width:980px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    NPT production 5000 step. 좌: 온도 setpoint 1.0 근방 정착(thermostat).
    중: 압력 setpoint 0.5 근방 수렴(barostat). 우: 밀도 0.69–0.70 평형.
  </figcaption>
</figure>

### B. 동경 분포 함수 `g(r)`

1. `rdf.dat` 를 그린다. 액체 특유의 진동 구조가 나와야 한다.
2. 첫 피크를 확인한다. r ≈ 1.09 σ 에서 g(r) ≈ 2.41 이다.
3. 두 번째 봉우리를 확인한다. ~ 2.1 σ 부근에 있다.

<figure>
  <img src="assets/images/lj-rdf.png" alt="LJ 액체의 동경 분포 함수 g(r) 과 누적 배위수 N(r)" style="width:100%;max-width:760px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    파란 선이 g(r), 주황 점선이 누적 배위수 N(r). 가까운 배위수는 약 12–14 다.
  </figcaption>
</figure>

### C. MSD 와 자기확산계수

1. `msd.dat` 를 그린다. MSD 가 시간에 따라 선형으로 늘어나는 정상 확산이어야 한다.
2. Einstein 관계 ⟨Δr²(t)⟩ = 6 D t 에 직선을 맞춘다.
3. 기울기로 자기확산계수를 구한다. 5000-step 데이터로 fit 하면 D ≈ 0.117 (LJ 단위)이다.

<figure>
  <img src="assets/images/lj-msd.png" alt="LJ 액체의 평균 제곱 변위 (MSD) 와 선형 fit" style="width:100%;max-width:760px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    녹색이 3차원 총 MSD, x/y/z 성분이 거의 겹쳐 등방 확산. 검은 점선은 후반 75 %
    선형 fit 으로 D ≈ 0.117.
  </figcaption>
</figure>

### D. 재현성

1. 같은 입력을 다시 실행한다. 시드가 고정돼 있으므로 `rdf.dat`·`msd.dat` 가 똑같이 나와야 한다.

## 5. 종료

### A. 결과 정리

1. `minimize → nvt → npt` 순서는 작은 LJ 계부터 큰 분자계까지 그대로 쓸 수 있다.
2. `compute` 는 값을 정의만 하고, 파일 저장은 `fix ave/time` 으로 한다.
3. `g(r)` 로는 구조를, MSD 기울기로는 동역학(확산)을 정량화한다.
