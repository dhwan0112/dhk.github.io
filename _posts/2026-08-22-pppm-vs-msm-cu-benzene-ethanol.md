---
title: "PPPM+slab 와 MSM 비교: 같은 Cu/벤젠·에탄올 계에서 kspace만 바꾼 2 ns 계산"
date: 2026-08-22
category: Computation
tags: [LAMMPS, Electrostatics, PPPM, MSM, Analysis]
description: "kspace 세 줄만 다른 OPLS-AA 벤젠/에탄올–Cu 슬랩 두 계산에서 첫 흡착층 구조는 구분되지 않고, MSM이 1.6배 느리다. 더 중요한 결과는 따로 있다. 첫 층 조성의 통계 오차가 두 방법의 차이보다 크고, 벌크가 평평하지 않으면 표면 과잉량은 정의되지 않는다."
---

NOTE 35-20-01 · PPPM+slab 와 MSM 비교 (Cu–벤젠–에탄올)
{: .amm-id}

## 1. 일반 사항

### A. 목적

1. 이 노트는 같은 Cu/벤젠·에탄올 슬랩 계에서 장거리 정전기 방법만 PPPM + `slab 3.0` 과 MSM 으로 바꿔 비교한다.
2. 비교 항목은 첫 흡착층 구조, 첫 층 조성의 통계 오차, 표면 과잉량, 계산 비용이다.

### B. 적용 범위

1. 2,471원자, `p p f` 경계, 300 K NVT 계에 적용한다.
2. 40 MPI 랭크, 4,000,000 스텝(0.5 fs, 2 ns) 프로덕션에 적용한다.
3. Cu 슬랩은 fcc(100) 이 아니다(4.D). 첫 층의 절대 구조값은 이 슬랩에서만 유효하다.

### C. 결과 요약

1. 두 방법의 주요 결과는 다음과 같다. 조건은 같은 계, 같은 40코어, 같은 4,000,000 스텝(0.5 fs, 2 ns)이다.

| | PPPM + `slab 3.0` | MSM |
|---|---|---|
| 첫 흡착층 벤젠 몰분율 | 0.70 ± 0.05 | 0.66 ± 0.03 |
| 벤젠 첫 피크 위치 / 높이 | 4.1 Å / 0.69 g cm⁻³ | 4.1 Å / 0.67 g cm⁻³ |
| 벌크 밀도 | 0.855 g cm⁻³ | 0.855 g cm⁻³ |
| Loop time (4 M steps) | 19,647 s (8.8 ns/day) | 31,988 s (5.4 ns/day) |
| Kspace 비중 | 22 % | 65 % |

2. 구조는 같고 MSM 이 1.63배 느리다. `p p f` 경계에서 슬랩 보정 없이 쓸 수 있다는 MSM 의 장점은 2,471원자 계에서 비용으로 상쇄되고도 남는다.
3. 첫 층 벤젠 몰분율의 통계 오차가 두 방법의 차이보다 크다.
4. 벌크 조성이 평평하지 않으면 표면 과잉량은 정의되지 않는다. PPPM run 이 이 경우에 해당한다.

## 2. 준비 정보

### A. 참조 자료

| 참조 | 제목 |
|---|---|
| [LAMMPS 가이드 cu-05]({{ '/guides/lammps/cu-05-protocol.html' | relative_url }}) | 5단계 시뮬레이션 프로토콜 |
| [NOTE 35-10-01]({{ '/blog/2026/08/22/lammps-z-density-profile-ase-pandas/' | relative_url }}) | LAMMPS 덤프의 z-밀도 프로파일 계산, Gibbs 상대 표면 과잉량 함수 |
| Mishin 2001 EAM | Cu 퍼텐셜 `Cu_mishin1.eam.alloy` |

### B. 공구 및 장비

| 항목 | 용도 |
|---|---|
| LAMMPS (`eam/alloy`, `lj/cut/coul/long`, `lj/cut/coul/msm`, `pppm`, `msm`) | 두 run 계산, 40 MPI 랭크 |
| Python (`profiles.py`, `blocks.py`, `plot.py`) | 프로파일, 블록 평균, 그림 |

### C. 소모품

- [`master_wall_pppm.in`]({{ '/files/blog/pppm-vs-msm/master_wall_pppm.in' | relative_url }}), [`master_wall_msm.in`]({{ '/files/blog/pppm-vs-msm/master_wall_msm.in' | relative_url }}), [`master_wall.diff`]({{ '/files/blog/pppm-vs-msm/master_wall.diff' | relative_url }}) — LAMMPS 입력과 diff
- [`ff_params_pppm.in`]({{ '/files/blog/pppm-vs-msm/ff_params_pppm.in' | relative_url }}), [`ff_params_msm.in`]({{ '/files/blog/pppm-vs-msm/ff_params_msm.in' | relative_url }}), [`opls.data`]({{ '/files/blog/pppm-vs-msm/opls.data' | relative_url }}) — 힘장 파라미터와 초기 구조 (Cu는 `Cu_mishin1.eam.alloy` 필요)
- [`profiles.py`]({{ '/files/blog/pppm-vs-msm/profiles.py' | relative_url }}), [`blocks.py`]({{ '/files/blog/pppm-vs-msm/blocks.py' | relative_url }}) — 덤프에서 프로파일과 블록 평균을 뽑는 스크립트, [`plot.py`]({{ '/files/blog/pppm-vs-msm/plot.py' | relative_url }}) — 4.A 의 그림
- [`zprofile_pppm.csv`]({{ '/files/blog/pppm-vs-msm/zprofile_pppm.csv' | relative_url }}), [`zprofile_msm.csv`]({{ '/files/blog/pppm-vs-msm/zprofile_msm.csv' | relative_url }}) — 2 ns 평균 프로파일 (질량 밀도 + 분자 COM 수밀도)
- [`first_layer_pppm.csv`]({{ '/files/blog/pppm-vs-msm/first_layer_pppm.csv' | relative_url }}), [`first_layer_msm.csv`]({{ '/files/blog/pppm-vs-msm/first_layer_msm.csv' | relative_url }}) — 프레임별 첫 층 분자 수
- [`timing_pppm.txt`]({{ '/files/blog/pppm-vs-msm/timing_pppm.txt' | relative_url }}), [`timing_msm.txt`]({{ '/files/blog/pppm-vs-msm/timing_msm.txt' | relative_url }}) — 로그의 프로덕션 타이밍 블록

프로덕션 궤적(각 146 MB)은 공개하지 않는다.

### D. 선행 조건

1. NOTE 35-10-01 의 z-밀도 프로파일 계산과 표면 과잉량 함수를 알아야 한다.

## 3. 절차

### A. 계산 시스템 구성

1. CM3288(UROPS) 과정에서 구성한 계를 사용한다.
2. OPLS-AA 벤젠 100분자와 에탄올 100분자를 Cu 371원자 슬랩 위에 둔다.
3. 박스를 30 × 30 × 41.9 Å 으로 설정한다.
4. 액체 위쪽을 `wall/lj126` 으로 막는다.
5. Cu 원자 전체를 고정한다. 고정 범위와 슬랩 구조는 4.D 에서 점검한다.

### B. 정전기 설정

1. 두 run 의 입력 파일 차이를 kspace 관련 세 줄로 한정한다. diff 전체는 다음과 같다.

```diff
< pair_style        hybrid eam/alloy lj/cut/coul/msm 14.0
< kspace_style      msm 1.0e-5
< kspace_modify     pressure/scalar no
---
> pair_style        hybrid eam/alloy lj/cut/coul/long 14.0
> kspace_style      pppm 1.0e-5
> kspace_modify     slab 3.0
```

2. PPPM run 에는 `kspace_modify slab 3.0` 을 적용한다. FFT 격자는 12 × 12 × **32** 이다.
3. MSM run 은 비주기 경계를 그대로 받는다. 격자는 16 × 16 × 16 이다.
4. 힘 정확도 목표를 두 run 모두 10⁻⁵ 로 설정한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
PPPM 은 z 방향이 비주기적이면 박스를 z 방향으로 세 배 늘려 가짜 주기 이미지를 떼어 놓아야 한다. 그래서 z 방향 FFT 격자가 32 로 커진다. MSM 은 비주기 경계를 직접 다루므로 슬랩 보정이 필요 없다.
</div>

### C. 시뮬레이션 프로토콜

1. [LAMMPS 가이드 cu-05]({{ '/guides/lammps/cu-05-protocol.html' | relative_url }}) 의 5단계 프로토콜을 그대로 적용한다.
   1. 소프트 퍼텐셜.
   2. 최소화.
   3. 단계적 승온.
   4. 평형.
   5. 2 ns 프로덕션.
2. 온도를 300 K NVT 로 유지한다.
3. 프로덕션을 timestep 0.5 fs 로 4,000,000 스텝(2 ns) 실행한다.
4. 두 run 을 40 MPI 랭크로 실행한다.

### D. 분석 방법

1. LAMMPS 가 남긴 결과 파일은 쓰지 않는다.
2. 2,000 프레임 프로덕션 덤프에서 [NOTE 35-10-01]({{ '/blog/2026/08/22/lammps-z-density-profile-ase-pandas/' | relative_url }}) 의 방식으로 처음부터 다시 계산한다.
3. 밀도 프로파일은 원자 질량 기준으로 계산한다.
4. 첫 층 조성은 분자 질량중심 기준으로 계산한다.
5. 첫 층을 전체 분자 밀도의 첫 번째 극소(Cu 최상층에서 6.4 Å) 안쪽으로 정의한다.
6. 첫 층 벤젠 몰분율의 표준오차를 10개 블록(블록당 200 ps) 평균으로 구한다.
7. NOTE 35-10-01 의 Gibbs 상대 표면 과잉량 함수를 벌크 구간 세 가지에 대해 적용한다.
8. 로그의 프로덕션 타이밍 블록에서 루프 시간을 항목별로 분해한다.

## 4. 시험 및 검사

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
이 계의 Cu 슬랩은 fcc(100) 이 아니다(4.D). 두 run 의 비교는 같은 슬랩을 썼으므로 유효하다. 그러나 첫 층의 절대 구조(벤젠 피크 4.1 Å, 첫 층 분자 수)를 실제 Cu(100) 표면 값으로 해석하면 안 된다.
</div>

### A. 첫 흡착층 구조 비교

1. 프로덕션 2 ns 평균 밀도 프로파일과 첫 층 벤젠 몰분율을 그린다.

<figure>
<img src="{{ '/images/blog/pppm-vs-msm.png' | relative_url }}" alt="Density profiles and first-layer benzene fraction, PPPM vs MSM">
<figcaption>왼쪽: 프로덕션 2 ns 평균 질량 밀도 프로파일, 실선 PPPM, 점선 MSM. 점선 세로선은 전체 분자 밀도의 첫 번째 극소(6.4 Å)로, 이 안쪽을 첫 층으로 잡는다. 오른쪽: 첫 층 벤젠 몰분율. 점은 200 ps 블록 평균, 흐린 선은 50 ps 이동 평균.</figcaption>
</figure>

2. 벤젠 첫 피크를 비교한다. 두 run 모두 Cu 최상층에서 4.1 Å, 높이 0.67–0.69 g cm⁻³ 이다.
3. 에탄올 첫 피크를 비교한다. 에탄올은 벤젠 뒤로 밀려 첫 피크가 8.4–8.6 Å 에 있다.
4. 첫 층(6.4 Å 이내) 분자 수를 비교한다. 두 run 모두 프레임당 벤젠 16개, 에탄올 7–8개이다.
5. 판정: 장거리 정전기 처리 방법은 이 계의 계면 구조에 영향을 주지 않는다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
이 결과는 예상과 같다. 예상대로 나오는지 확인하는 것이 이 비교의 목적이었다.
</div>

### B. 첫 층 조성의 통계 오차

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
블록 평균 없이 전체 평균만 비교하면 "0.70 vs 0.66" 을 실제 차이로 해석하게 된다. 첫 층 조성은 반드시 블록 표준오차와 함께 비교한다.
</div>

1. 첫 층 벤젠 몰분율을 비교한다. PPPM 0.70, MSM 0.66 으로 차이는 0.04 이다.
2. 10개 블록(200 ps씩)의 표준오차를 확인한다. 각각 0.05 와 0.03 이다.
3. 판정: 차이가 표준오차보다 작으므로 두 방법은 구분되지 않는다.
4. 오차가 큰 원인을 확인한다.
   1. PPPM run 은 앞 1 ns 평균이 0.83, 뒤 1 ns 평균이 0.57 이다.
   2. 첫 층 분자가 24개뿐이라 한두 개가 드나들면 몰분율이 0.04씩 움직인다.
   3. 그 교환이 수백 ps 단위로 느리게 일어난다.
5. 판정: 2 ns 는 이 양의 평균을 내기에 짧다.

### C. 표면 과잉량의 벌크 구간 의존성

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
벌크 조성 프로파일이 평평하지 않으면 정의식의 $$\rho^b$$ 가 존재하지 않는다. 이때 계산된 Γ 는 오류 없이 나오지만 벌크 구간 선택에 따라 임의로 변한다.
</div>

1. 벌크 구간을 세 가지로 바꿔 Gibbs 상대 표면 과잉량을 계산한다.

| 벌크 구간 (Cu 위 거리) | PPPM Γ<sub>benzene</sub><sup>(ethanol)</sup> | MSM Γ<sub>benzene</sub><sup>(ethanol)</sup> |
|---|---|---|
| 10–20 Å | 0.0106 Å⁻² | 0.0121 Å⁻² |
| 12–24 Å | 0.0183 Å⁻² | 0.0124 Å⁻² |
| 15–28 Å | 0.0299 Å⁻² | 0.0111 Å⁻² |

2. MSM run 을 판정한다. 어느 구간에서도 0.011–0.012 Å⁻²(900 Å² 표면에 벤젠 10–11개 과잉)로 안정적이다.
3. PPPM run 을 판정한다. 구간에 따라 세 배가 변한다.
4. 4.A 그림의 PPPM 실선에서 원인을 확인한다.
   1. 액체막은 Cu 쪽이 벤젠 과잉, 위쪽 벽 쪽이 에탄올 과잉으로 기울어져 있다.
   2. 평평한 벌크 구간이 없으므로 Γ 의 정의식에 들어가는 $$\rho^b$$ 가 없다.
5. 판정: 이 계에서 표면 과잉량을 보고하려면 벌크 조성 프로파일이 시간에 따라 평평해지는지를 먼저 확인한다. 계면 통계는 그 다음이다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
두 run 은 같은 힘장, 같은 온도, 같은 초기 구조, 같은 난수 시드에서 출발했다. 두 run 이 이렇게 다른 이유는 kspace 가 구조를 바꿔서가 아니다. 힘이 조금만 달라도 궤적은 곧 갈라진다. 조성이 아직 정상 상태에 도달하지 않았으므로 갈라진 자리에 그대로 머물러 있다.
</div>

### D. Cu 슬랩 구조 점검

1. `opls.data` 의 Cu 371원자 배치를 확인한다.
   1. z = 0, 1.81, 3.62, 5.42, 7.23 Å 의 다섯 층에 원자가 81, 64, 81, 64, 81개씩 있다.
   2. 한 층 안 간격이 3.615 Å(Cu 의 격자 상수)인 정사각 격자이다.
   3. 층은 a/2 높이마다 반 칸씩 엇갈려 쌓여 있다.
2. 판정: 적층은 fcc(100) 이 아니라 bcc 이다. 최근접 거리는 3.13 Å 로, fcc Cu 의 2.56 Å 보다 길다.
3. 주기 경계의 이음매를 확인한다.
   1. 81원자 층은 한 줄에 9개이므로 길이가 9 × 3.615 = 32.5 Å 이다.
   2. 박스 가로는 30 Å 이다.
   3. x = 0 과 x = 28.92 Å 의 원자가 주기 경계를 사이에 두고 1.08 Å 까지 붙어 있다.
4. 고정 영역을 확인한다.
   1. `region cu_bottom` 은 z < 8.0 Å 이다.
   2. 최상층이 7.23 Å 이므로 아래층만이 아니라 Cu 전체가 `setforce 0` 으로 묶인다.
   3. 움직이는 Cu 원자는 없다. Cu 는 처음부터 끝까지 얼어 있는 벽이다.
5. 판정: 입력과 서술이 다르다. 두 run 이 같은 슬랩을 썼으므로 4.A–4.C 의 비교는 유효하다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
Cu 가 전체 고정이므로 EAM 에너지가 비정상 격자에서 크더라도 궤적이 발산하지 않았다. 첫 층 절대값을 Cu(100) 값으로 해석하면 안 되는 이유는 두 가지다. 원자 밀도가 다르고, 이음매 쪽 한 줄은 원자가 겹쳐 있다.
</div>

### E. 계산 비용

1. 40 MPI 랭크 기준 프로덕션 루프 시간을 항목별로 분해한다.

| 항목 | PPPM + slab | MSM |
|---|---|---|
| Pair | 7,228 s (37 %) | 4,477 s (14 %) |
| Kspace | 4,331 s (22 %) | 20,837 s (65 %) |
| Comm | 5,068 s (26 %) | 4,259 s (13 %) |
| 합계 | 19,647 s | 31,988 s |

2. Pair 항을 비교한다. MSM 의 실공간 쌍 상호작용이 더 싸다.
3. Kspace 항을 비교한다. MSM 은 kspace 에서 Pair 이득을 모두 잃는다.
4. 판정: 2,471원자 계에서는 PPPM + slab 이 1.63배 빠르다.
5. 랭크당 원자 수를 확인한다. 62개이며, 두 run 모두 통신 비중이 13–26 % 이다.
6. 판정: 이 크기의 계는 40코어가 아니라 8–16코어가 적합하다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
`coul/msm` 의 실공간 항은 `coul/long` 의 erfc 보다 가볍다. MSM 이 O(N) 이라 큰 계에서 유리하다는 점은 맞지만, 2,471원자는 그 교차점보다 훨씬 아래다.
</div>

## 5. 종료

### A. 결과 정리

1. 첫 흡착층 구조는 PPPM + slab 과 MSM 에서 구분되지 않는다.
2. MSM 은 이 계에서 1.63배 느리다.
3. 첫 층 조성의 블록 표준오차(0.03–0.05)가 두 방법의 차이(0.04)보다 크다.
4. PPPM run 은 벌크 조성이 평평하지 않아 표면 과잉량이 정의되지 않는다.
5. Cu 슬랩은 bcc 적층이며 전체 고정이다. 첫 층의 절대 구조값은 Cu(100) 값이 아니다.

### B. 후속 작업

다시 계산할 때는 다음 조건을 적용한다.

1. 조성 평형: 프로덕션 전에 벌크 조성 프로파일의 기울기가 사라질 때까지 실행한다.
   1. 프로덕션은 최소 10 ns 로 한다.
   2. 첫 층 분자 수가 24개인 계에서 몰분율 ±0.02 를 원하면 그 이상으로 한다.
2. 정전기: 이 크기에서는 PPPM + slab 을 쓴다. MSM 은 수만 원자 이상이거나 슬랩 보정의 진공 패딩이 부담될 때 쓴다.
3. 코어 수: 랭크당 원자가 200개 이상이 되도록 정한다.
4. 슬랩: `lattice fcc 3.615` + `orient` 로 fcc(100) 을 만든다.
   1. 박스 가로를 격자 상수의 정수배(예: 8 × 3.615 = 28.92 Å)로 맞춘다.
   2. 고정 영역의 z 경계를 층 사이에 두어 맨 아래 한두 층만 잡히게 한다.

### C. 개정 기록

1. 2026-10-03 수정: 처음에는 프로덕션 길이를 4 ns 로 적었으나, timestep 0.5 fs × 4,000,000 스텝이므로 2 ns 가 맞다. 블록 길이(400 → 200 ps), 앞뒤 절반(2 → 1 ns), 그림의 시간축을 함께 고쳤다. 몰분율과 오차, 루프 시간의 ns/day 는 원래 2 ns 기준으로 계산돼 있어 그대로다. "Cu 아래층만 고정"이라는 서술도 틀려서 "Cu 슬랩에 대해" 절(현재 4.D)을 추가했다.
