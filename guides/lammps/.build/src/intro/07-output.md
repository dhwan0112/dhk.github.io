---
layout: default
title: "7. 출력과 분석"
nav_order: 8
---

# 7. 출력과 분석
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 7.1 LAMMPS가 내보내는 다섯 갈래 결과

LAMMPS의 출력은 보통 다음 다섯 가지로 정리할 수 있습니다.

| 결과 | 명령 | 파일 |
|------|------|------|
| 열역학 수치 (화면/log) | `thermo`, `thermo_style` | `log.lammps` |
| 좌표/속도 트라젝토리 | `dump` | `*.lammpstrj`, `*.xyz`, `*.dcd` |
| 사용자 정의 계산값 | `compute` + `fix ave/*` | 별도 파일 |
| 재시작 파일 | `restart` | `*.restart` |
| 그 외 진단 출력 | `print`, `fix print` | 임의 파일 |

각각을 살펴봅니다.

## 7.2 thermo — 화면과 log에 찍히는 열역학

`thermo N` 은 매 N 스텝마다 한 줄을 출력합니다. `thermo_style` 로 어떤 열을
표시할지 정합니다.

```lammps
thermo          100
thermo_style    custom step temp pe ke etotal press density
```

기본 컬럼은 `step temp epair emol etotal press` 정도이며,
사용자 정의에는 다음 같은 컬럼들을 자유롭게 섞을 수 있습니다.

| 컬럼 | 의미 |
|------|------|
| `step` | 스텝 번호 |
| `temp` | 온도 |
| `pe`, `ke`, `etotal` | 포텐셜·운동·총 에너지 |
| `enthalpy` | enthalpy |
| `press`, `vol`, `density` | 압력, 부피, 밀도 |
| `pxx pyy pzz` | 응력 텐서 대각 |
| `cpu`, `cpuremain` | 누적 CPU 시간, 남은 추정 시간 |
| `c_<computeID>` | compute 결과 |
| `v_<variableID>` | 변수 값 |

`thermo` 출력은 평형화 모니터링과 성능 점검의 출발점입니다.

## 7.3 dump — 좌표·속도 트라젝토리

```lammps
dump            1 all custom 1000 traj.lammpstrj id type x y z
```

- `1` — dump의 ID (취소할 때 `undump 1`)
- `all` — 출력 대상 그룹
- `custom` — dump style
- `1000` — 매 1000 step
- `traj.lammpstrj` — 파일명
- `id type x y z` — 출력 컬럼

대표 dump style은 다음과 같습니다.

| dump style | 특징 |
|------------|------|
| `atom` | LAMMPS 기본 텍스트, 가벼움 |
| `custom` | 컬럼을 자유롭게 선택. 가장 흔히 사용 |
| `xyz` | 단순 XYZ 포맷 (VMD 즉시 열림) |
| `dcd` | CHARMM/NAMD 호환 바이너리 |
| `netcdf` | AMBER 호환 바이너리 (대용량 효율적) |
| `image`, `movie` | 시뮬레이션 도중 png/avi 생성 (디버그용) |

또한 `dump_modify` 로 추가 설정이 가능합니다.

```lammps
dump_modify     1 sort id           # 원자 ID 순으로 정렬
dump_modify     1 element Cu C O H  # type → 원소 매핑 (OVITO에서 색깔 자동)
```

`sort id` 는 후처리 도구가 원자를 추적할 때 매우 중요합니다.

## 7.4 compute — 시뮬레이션 중 계산

LAMMPS는 시뮬레이션 도중에 다양한 양을 직접 계산할 수 있습니다.

```lammps
compute         myT  all temp
compute         myKE all ke
compute         myPE all pe
compute         myRDF all rdf 100 1 1 1 2
compute         myMSD all msd
```

자주 쓰는 compute:

| compute style | 계산하는 양 |
|---------------|-------------|
| `temp`, `temp/com`, `temp/region` | 온도 (집단별·영역별) |
| `pe`, `ke`, `pe/atom` | 에너지 |
| `pressure` | 압력 |
| `rdf` | 동경 분포 함수 g(r) |
| `msd` | 평균 제곱 변위 |
| `coord/atom` | 원자별 배위수 |
| `cna/atom`, `centro/atom` | 결정 구조 분석 |
| `chunk/atom`, `density/atom` | 공간 영역별 평균 |
| `stress/atom` | 원자별 응력 |

compute의 결과는 그 자체로는 어디에도 저장되지 않습니다.
`thermo_style custom ... c_myT` 또는 다음에 나오는 `fix ave/time` 으로
"꺼내야" 비로소 값을 볼 수 있습니다.

### 실제 결과 ① — g(r) (동경 분포 함수)

위 chapter 6 에서 돌린 LJ NPT production 5000 step 에 다음 두 줄을 더해
RDF 를 함께 계산했습니다.

```lammps
compute         rdf1 all rdf 100              # 100 bin 까지의 g(r)
fix             rdfavg all ave/time 10 100 1000 c_rdf1[*] file rdf.dat mode vector
```

결과 파일 `rdf.dat` 를 그림으로 그리면 LJ 액체의 전형적인 동경 분포 함수를
얻습니다 — 첫 피크가 r ≈ 1.09 σ 에서 g(r) ≈ 2.41, 두 번째 piek 가 ~ 2.1 σ
부근에 보이는 액체 특유의 진동 구조입니다.

<figure>
  <img src="assets/images/lj-rdf.png" alt="LJ 액체의 동경 분포 함수 g(r) 과 누적 배위수 N(r)" style="width:100%;max-width:760px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    그림 1. NPT (T = 1.0, P = 0.5, ρ ≈ 0.70) 평형에서 측정한 LJ 액체의 g(r) (파란).
    첫 피크 r ≈ 1.09 σ 는 σ ≈ 0.94 (Lennard-Jones 의 σ ≈ 0.89 × r<sub>min</sub>)와
    근접하며, 두 번째 봉우리 ~ 2.1 σ 는 두 번째 배위 껍질입니다. 함께 그린
    주황 점선은 누적 배위수 N(r) = 4π ρ ∫₀ʳ r'² g(r') dr' 로, 단순한 LJ 액체에서도
    한 입자 주위의 가까운 배위수가 약 12–14 정도임을 보여 줍니다.
  </figcaption>
</figure>

### 실제 결과 ② — MSD 와 자기확산계수

같은 production 단계에서 MSD 도 함께 계산했습니다.

```lammps
compute         msd1 all msd
fix             msdavg all ave/time 1 1 100 c_msd1[1] c_msd1[2] c_msd1[3] c_msd1[4] file msd.dat
```

⟨Δr²(t)⟩ 가 시간에 대해 선형으로 증가하는 정상 확산(normal diffusion) 거동이
관찰되고, Einstein 관계 ⟨Δr²(t)⟩ = 6 D t 에서 직선 fit 의 기울기로 자기확산
계수 D 를 추정할 수 있습니다. 본 가이드의 5000-step 데이터에서 fit 결과는
D ≈ 0.117 (LJ 단위) 입니다.

<figure>
  <img src="assets/images/lj-msd.png" alt="LJ 액체의 평균 제곱 변위 (MSD) 와 선형 fit" style="width:100%;max-width:760px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    그림 2. NPT (T = 1.0, P = 0.5, 2048 LJ 입자) 의 평균 제곱 변위. 녹색 굵은 선이
    3차원 총 MSD, 옅은 보라/주황/빨강 선은 x/y/z 성분으로 거의 동일 — 등방 확산을
    의미합니다. 검은 점선은 후반 75 % 구간의 선형 fit 이고, Einstein 관계로부터
    D ≈ 0.117 (LJ 단위). dt = 0.005 τ 의 5000 step ≈ 25 τ 시간 동안 측정한 값입니다.
  </figcaption>
</figure>

<div class="tip">
  <div class="note-title">compute 결과는 fix ave/time 으로 꺼내라</div>
  <p>
    위 두 예제는 모두 <code>compute</code> 가 정의하고 <code>fix ave/time</code> 이
    실제 파일로 출력하는 패턴입니다. <code>compute</code> 자체는 <em>한 스텝의</em>
    값만 유지하므로, 그것을 직접 thermo 컬럼(<code>c_msd1[4]</code>)으로 꺼내거나
    <code>fix ave/time</code> 으로 시간 평균을 파일에 쓰는 방식이 표준입니다.
    <code>rdf</code> 같은 vector 출력에는 <code>mode vector</code> 옵션을 잊지
    마십시오.
  </p>
</div>

## 7.5 fix ave/* — 시간 평균을 자동으로

```lammps
fix             1 all ave/time 10 100 1000 c_myT c_myPE file thermo_ave.txt
```

위 한 줄의 의미는 "1000 스텝마다, 직전 100개 sample을 10 스텝 간격으로 모아
평균"입니다.

- `Nevery` (10) — sampling 간격
- `Nrepeat` (100) — 평균에 사용할 sample 개수
- `Nfreq` (1000) — 출력 주기

`fix ave/atom` 은 원자별 양을 시간 평균, `fix ave/chunk` 는 공간 chunk별
시간 평균을 만듭니다. RDF, 밀도 프로파일, 응력 분포 같은 대부분의 분석은
이 두 fix 위에 구현됩니다.

```lammps
# 밀도 프로파일 (z축 슬라이스)
compute         cc all chunk/atom bin/1d z 0.0 1.0 units box
fix             dens all ave/chunk 10 100 1000 cc density/mass file dens.txt
```

## 7.6 restart — 중간 저장

```lammps
restart         50000 sim.restart
```

50000 스텝마다 `sim.restart.50000` 같은 파일을 남깁니다. 다음에는

```lammps
read_restart    sim.restart.50000
```

로 이어서 시작할 수 있습니다. 장시간 시뮬레이션은 항상 restart를 켜 두는 것이
안전합니다.

## 7.7 후처리 도구

LAMMPS는 트라젝토리만 충실히 남기고, 시각화·분석은 외부 도구에 맡기는
설계입니다. 자주 쓰이는 도구는 다음과 같습니다.

| 도구 | 강점 |
|------|------|
| **OVITO** | 결정 구조 분석, 결함 식별, 가벼운 GUI |
| **VMD** | 분자 시각화의 표준. CHARMM/AMBER와 호환 |
| **Ovito Python / MDAnalysis / MDTraj** | Python에서 trajectory 분석 |
| **PyLammps** | Python 안에서 LAMMPS를 직접 호출 |
| **ParaView** | 대용량 mesh/필드 시각화 |

대부분의 도구는 `dump custom ... id type x y z` 또는 `xyz`/`dcd` 출력을
바로 읽을 수 있습니다.

## 7.8 분석을 위한 좋은 출력 습관

- **dump_modify sort id** 를 켜라. 후처리 도구에서 원자 추적이 단순해집니다.
- **element 매핑**을 dump_modify에 넣어라 (`element Cu C O H` 식).
  OVITO/VMD가 원자 색을 자동으로 부여합니다.
- **thermo와 dump의 주기를 다르게** 두라. thermo는 자주(`100`),
  dump는 드물게(`1000`–`10000`). 디스크 절약과 진단 두 마리 토끼.
- **fix ave/time을 평형화 후로 미루라**. 평형화 단계의 값이 평균에 섞이면
  결과가 왜곡됩니다. `unfix` 후 새로 등록하거나 `start` 옵션을 활용.
- **항상 restart를 켜라**. 시뮬레이션 시간이 4시간을 넘으면 거의 필수.

## 7.9 다음 단계

이제 시뮬레이션을 만들고, 돌리고, 결과를 뽑는 한 사이클이 모두 끝났습니다.
마지막 장에서는 처음 LAMMPS를 돌릴 때 가장 자주 마주치는 오류들과
운영·성능 팁을 모았습니다.
