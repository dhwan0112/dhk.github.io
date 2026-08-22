---
title: "PPPM+slab vs MSM — 같은 Cu/벤젠·에탄올 계를 kspace만 바꿔 4 ns 돌렸더니"
date: 2026-08-22
category: Computation
tags: [LAMMPS, Electrostatics, PPPM, MSM, Analysis]
description: "UROPS 때 돌린 OPLS-AA 벤젠/에탄올–Cu 슬랩 두 run은 입력 파일 diff가 kspace 세 줄뿐이다. 프로덕션 궤적 4 ns를 다시 분석해 보니 첫 흡착층 구조는 두 방법이 구분이 안 되고, 비용은 MSM이 1.6배 비쌌다. 그리고 정작 중요한 건 다른 데 있었다 — 첫 층 조성의 통계 오차가 두 방법의 차이보다 훨씬 컸고, 벌크가 평평하지 않으면 표면 과잉량은 정의조차 되지 않는다."
---

결론부터. 같은 계, 같은 40코어, 같은 4,000,000 스텝에서

| | PPPM + `slab 3.0` | MSM |
|---|---|---|
| 첫 흡착층 벤젠 몰분율 | 0.70 ± 0.05 | 0.66 ± 0.03 |
| 벤젠 첫 피크 위치 / 높이 | 4.1 Å / 0.69 g cm⁻³ | 4.1 Å / 0.67 g cm⁻³ |
| 벌크 밀도 | 0.855 g cm⁻³ | 0.855 g cm⁻³ |
| Loop time (4 M steps) | 19,647 s (8.8 ns/day) | 31,988 s (5.4 ns/day) |
| Kspace 비중 | 22 % | 65 % |

구조는 같고 MSM이 1.63배 느렸다. `p p f` 경계에서 슬랩 보정 없이 쓸 수 있다는 MSM의 장점은 2,471원자짜리 계에서는 비용으로 상쇄되고도 남는다. 그런데 이 비교를 하려고 궤적을 다시 들여다보다가 더 중요한 두 가지가 보였다. 아래에 순서대로 적는다.

## 무엇을 비교했나

CM3288(UROPS) 때 돌린 OPLS-AA 벤젠 100 + 에탄올 100 분자 / Cu 371원자 슬랩, 30 × 30 × 41.9 Å 박스, 300 K NVT. 위쪽은 `wall/lj126`로 막고 Cu 아래층은 고정. 소프트 퍼텐셜 → 최소화 → 단계적 승온 → 평형 → 4 ns 프로덕션의 5단계 프로토콜은 [LAMMPS 가이드 cu-05]({{ '/guides/lammps/cu-05-protocol.html' | relative_url }})에 있는 그대로다.

두 run의 입력 파일 diff는 이게 전부다.

```diff
< pair_style        hybrid eam/alloy lj/cut/coul/msm 14.0
< kspace_style      msm 1.0e-5
< kspace_modify     pressure/scalar no
---
> pair_style        hybrid eam/alloy lj/cut/coul/long 14.0
> kspace_style      pppm 1.0e-5
> kspace_modify     slab 3.0
```

PPPM은 z 방향이 비주기적이면 `kspace_modify slab 3.0`으로 박스를 세 배 늘려 가짜 주기 이미지를 떼어 놓아야 하고(그래서 FFT 격자가 12 × 12 × **32**), MSM은 비주기 경계를 그대로 받는다(격자 16 × 16 × 16). 힘 정확도 목표는 둘 다 10⁻⁵. 분석은 LAMMPS가 남긴 결과 파일을 쓰지 않고, 2,000 프레임 프로덕션 덤프를 [지난 글]({{ '/blog/2026/08/22/lammps-z-density-profile-ase-pandas/' | relative_url }})의 방식으로 처음부터 다시 계산했다. 밀도 프로파일은 원자 질량 기준, 첫 층 조성은 분자 질량중심 기준이다.

<figure>
<img src="{{ '/images/blog/pppm-vs-msm.png' | relative_url }}" alt="Density profiles and first-layer benzene fraction, PPPM vs MSM">
<figcaption>왼쪽: 프로덕션 4 ns 평균 질량 밀도 프로파일, 실선 PPPM, 점선 MSM. 점선 세로선은 전체 분자 밀도의 첫 번째 극소(6.4 Å)로, 이 안쪽을 첫 층으로 잡았다. 오른쪽: 첫 층 벤젠 몰분율. 점은 400 ps 블록 평균, 흐린 선은 50 ps 이동 평균.</figcaption>
</figure>

## 1. 첫 층은 같다

벤젠 첫 피크는 두 run 모두 Cu 최상층에서 4.1 Å, 높이 0.67–0.69 g cm⁻³. 에탄올은 벤젠 뒤로 밀려 첫 피크가 8.4–8.6 Å에 있다. 첫 층(6.4 Å 이내) 안의 분자 수는 프레임당 벤젠 16개, 에탄올 7–8개로 같다. 장거리 정전기를 어떤 방법으로 푸느냐는 이 계의 계면 구조에 영향을 주지 않는다 — 예상한 결과고, 예상대로 나왔다는 걸 확인한 것 자체가 이 비교의 목적이었다.

## 2. 조성의 오차는 두 방법의 차이보다 크다

첫 층 벤젠 몰분율은 0.70 대 0.66. 차이 0.04인데, 10개 블록(400 ps씩)으로 잡은 표준오차가 각각 0.05와 0.03이다. 즉 구분이 안 된다. 문제는 그 오차가 왜 그렇게 큰가다. 오른쪽 그림을 보면 PPPM run은 앞 2 ns 평균이 0.83, 뒤 2 ns 평균이 0.57이다. 첫 층에 분자가 24개뿐이라 한두 개가 드나들면 몰분율이 0.04씩 움직이고, 그 교환이 수백 ps 단위로 느리게 일어난다. 4 ns는 이 양의 평균을 내기에 짧다. 블록 평균을 안 냈으면 "0.70 vs 0.66"을 차이라고 읽었을 것이다.

## 3. 벌크가 평평하지 않으면 표면 과잉량은 정의되지 않는다

지난 글에서 만든 Gibbs 상대 표면 과잉량 함수를 여기에 적용해 봤다. 벌크 구간을 어디로 잡느냐에 따라:

| 벌크 구간 (Cu 위 거리) | PPPM Γ<sub>benzene</sub><sup>(ethanol)</sup> | MSM Γ<sub>benzene</sub><sup>(ethanol)</sup> |
|---|---|---|
| 10–20 Å | 0.0106 Å⁻² | 0.0121 Å⁻² |
| 12–24 Å | 0.0183 Å⁻² | 0.0124 Å⁻² |
| 15–28 Å | 0.0299 Å⁻² | 0.0111 Å⁻² |

MSM run은 어디를 벌크로 잡아도 0.011–0.012 Å⁻²(900 Å² 표면에 벤젠 10–11개 과잉)로 안정적이다. PPPM run은 구간에 따라 세 배가 움직인다. 왼쪽 그림의 실선을 보면 이유가 보인다. PPPM run의 액체막은 Cu 쪽이 벤젠 과잉, 위쪽 벽 쪽이 에탄올 과잉으로 기울어져 있고, 평평한 벌크 구간이 없다. Γ의 정의식에 들어가는 ρ<sup>b</sup>가 없는 것이다. 같은 힘장, 같은 온도, 심지어 같은 초기 구조와 같은 난수 시드에서 출발한 두 run이 이렇게 다른 건 kspace가 구조를 바꿔서가 아니라, 힘이 조금만 달라도 궤적은 금방 갈라지는데 조성이 아직 정상 상태에 도달하지 않아서 갈라진 자리에 그대로 머물러 있기 때문이다. 이 계에서 표면 과잉량을 보고하려면 계면 통계보다 벌크 조성 프로파일이 시간에 따라 평평해지는지를 먼저 봐야 한다.

## 비용

40 MPI 랭크 기준 프로덕션 루프 시간 분해.

| 항목 | PPPM + slab | MSM |
|---|---|---|
| Pair | 7,228 s (37 %) | 4,477 s (14 %) |
| Kspace | 4,331 s (22 %) | 20,837 s (65 %) |
| Comm | 5,068 s (26 %) | 4,259 s (13 %) |
| 합계 | 19,647 s | 31,988 s |

MSM은 실공간 쌍 상호작용은 더 싸고(`coul/msm`의 실공간 항이 `coul/long`의 erfc보다 가볍다) kspace에서 다 잃는다. MSM이 O(N)이라 큰 계에서 유리하다는 건 맞지만, 2,471원자는 그 교차점 훨씬 아래다. 덧붙여 랭크당 원자가 62개라 두 run 모두 통신 비중이 13–26 %였다 — 이 크기면 40코어가 아니라 8–16코어가 맞다.

## 다시 한다면

- 조성 평형: 프로덕션 전에 벌크 조성 프로파일의 기울기가 사라질 때까지 돌리고, 프로덕션은 최소 10 ns. 첫 층 분자 수가 24개인 계에서 몰분율 ±0.02를 원하면 그 이상.
- 정전기: 이 크기에서는 PPPM + slab. MSM은 수만 원자 이상이거나 슬랩 보정의 진공 패딩이 부담될 때.
- 코어 수: 랭크당 원자 200개 이상이 되도록.

## 파일

- [`master_wall_pppm.in`]({{ '/files/blog/pppm-vs-msm/master_wall_pppm.in' | relative_url }}), [`master_wall_msm.in`]({{ '/files/blog/pppm-vs-msm/master_wall_msm.in' | relative_url }}), [`master_wall.diff`]({{ '/files/blog/pppm-vs-msm/master_wall.diff' | relative_url }}) — LAMMPS 입력과 diff
- [`ff_params_pppm.in`]({{ '/files/blog/pppm-vs-msm/ff_params_pppm.in' | relative_url }}), [`ff_params_msm.in`]({{ '/files/blog/pppm-vs-msm/ff_params_msm.in' | relative_url }}), [`opls.data`]({{ '/files/blog/pppm-vs-msm/opls.data' | relative_url }}) — 힘장 파라미터와 초기 구조 (Cu는 `Cu_mishin1.eam.alloy` 필요)
- [`profiles.py`]({{ '/files/blog/pppm-vs-msm/profiles.py' | relative_url }}), [`blocks.py`]({{ '/files/blog/pppm-vs-msm/blocks.py' | relative_url }}) — 덤프에서 프로파일과 블록 평균을 뽑는 스크립트
- [`zprofile_pppm.csv`]({{ '/files/blog/pppm-vs-msm/zprofile_pppm.csv' | relative_url }}), [`zprofile_msm.csv`]({{ '/files/blog/pppm-vs-msm/zprofile_msm.csv' | relative_url }}) — 4 ns 평균 프로파일 (질량 밀도 + 분자 COM 수밀도)
- [`first_layer_pppm.csv`]({{ '/files/blog/pppm-vs-msm/first_layer_pppm.csv' | relative_url }}), [`first_layer_msm.csv`]({{ '/files/blog/pppm-vs-msm/first_layer_msm.csv' | relative_url }}) — 프레임별 첫 층 분자 수
- [`timing_pppm.txt`]({{ '/files/blog/pppm-vs-msm/timing_pppm.txt' | relative_url }}), [`timing_msm.txt`]({{ '/files/blog/pppm-vs-msm/timing_msm.txt' | relative_url }}) — 로그의 프로덕션 타이밍 블록

프로덕션 궤적(각 146 MB)은 올리지 않았다.
