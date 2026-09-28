---
layout: default
title: "6. 4가지 프레임워크 비교"
nav_order: 7
---

# 6. 4가지 프레임워크 비교
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 6.1 2×2 비교 설계

4가지 프레임워크는 힘장 두 가지와 정전기 처리 두 가지를 엇갈려 조합한 것이다.

|             | PPPM | MSM |
|-------------|------|-----|
| **OPLS-AA**   | OPLS+PPPM | OPLS+MSM |
| **TraPPE-UA** | TraPPE+PPPM | TraPPE+MSM |

이렇게 짜 두면 다음을 따로 떼어 볼 수 있다.

- 힘장 효과: PPPM을 고정하고 OPLS-AA와 TraPPE-UA를 비교
- 정전기 처리 효과: 같은 힘장에서 PPPM과 MSM을 비교
- 상호작용 효과: 두 인자를 조합했을 때만 나타나는 효과 (예: TraPPE+MSM이 다른 조합보다 유독 잘/못 동작하는 경우)

## 6.2 프레임워크별 사전 관찰 (내 이전 run)

다음은 이 시스템에서 내가 직접 본 정성적 경향이다.
이 가이드는 이 결과를 출발점으로 삼았다.

| 프레임워크 | 안정성 | SEI (분리 효율) | 흡착 에너지 (벤젠) | 비고 |
|-------------|--------|--------|--------------------|------|
| OPLS-AA + PPPM | 가열 단계 불안정 가능 | 부분 성공 | - | 온도 폭주 (runaway) 경향 |
| OPLS-AA + MSM | 안정 | 양호 | - | slab 보정 불필요 |
| TraPPE-UA + PPPM | 안정 | 0.85-0.95 | -0.27 ~ -0.30 eV | 표준 |
| TraPPE-UA + MSM | 매우 안정 | 0.93-1.00 | -0.27 ~ -0.32 eV | 최고 성능 |

흡착 에너지 단위 변환: -0.30 eV ≈ -6.92 kcal/mol ≈ -28.95 kJ/mol.
벤젠이 에탄올보다 표면에 더 강하게 흡착되는 경향은 π-d 분산 상호작용(London dispersion)과
LJ 파라미터 fit으로 잘 재현된다.

## 6.3 프레임워크별 예측 비교

| 물리량 | OPLS-AA 예측 | TraPPE-UA 예측 | 원인 |
|--------|---------------|------------------|-------------|
| 표면 1차 흡착층 조성 | 벤젠 우세, 에탄올 협동 효과 가능 | 벤젠 강한 우세 | 수소 결합 처리 차이 |
| 에탄올-에탄올 g(r) 첫 피크 | 약 2.8 Å (O-H...O 수소 결합) | 약 2.8 Å (동등) | 명시적 H 차이 |
| 평형화 시간 | 7-10 ns | 2-3 ns | 협동성 vs 단순 LJ |
| 계면 장력 | 약 25-30 mJ/m² | 약 22-27 mJ/m² | 분극성 처리 차이 |

위 값은 내 시뮬레이션 결과와 문헌값을 참고한 정성적 예측이다.
논문에 쓸 때는 직접 잰 값을 써야 한다.

### 왜 OPLS-AA는 가열 단계에서 불안정한가

OPLS-AA 시스템이 가열 단계에서 불안정해지는 원인은 대개 다음 중 하나다.

1. 시간 스텝이 너무 큼: OPLS-AA에 SHAKE를 쓰지 않으면 1.0 fs는 큰 편이다.
   X-H 진동(~3000 cm⁻¹) 주기가 약 11 fs이므로 Nyquist 기준으로는 0.5 fs 이하로 잡는다.
2. SHAKE를 안 씀: SHAKE로 X-H 결합을 고정하면 시간 스텝을 2.0 fs까지 늘릴 수 있다.
3. Langevin damp가 너무 짧음: damp가 너무 작으면(예: 10 fs) 에너지를 무리하게 밀어 넣어 폭주한다.
4. PPPM accuracy가 너무 낮음: 1.0e-3 정도로 두면 슬랩 보정과 겹쳐 정전기 오차가 크게 쌓인다.

### 몇 줄만 고치는 수정

기존 입력 파일에서 다음 두 줄만 바꿔도 훨씬 안정해진다.

```bash
# 기존
timestep 1.0

# 수정 권장 (소수 줄)
timestep 0.5
fix shake_hydrogens organic shake 1.0e-4 20 0 b 2 4 6 7 8 9 10 11 a 3
# b 다음에 X-H 결합 타입 번호들, a 다음에 H-X-H 각도 타입 번호
```

`fix shake`의 b (bonds), a (angles), t (atom types), m (atom mass) 옵션은
[LAMMPS fix shake 문서](https://docs.lammps.org/fix_shake.html)에 정리되어 있다.

## 6.4 이 시스템에서의 정전기 처리 비교

이 시스템(슬랩 기하, ~1500-2500 원자)에서는 다음과 같다.

| 항목 | PPPM | MSM |
|------|------|-----|
| 초기 설정 복잡도 | 중간 (`kspace_modify slab 3.0` 필요) | 낮음 (slab 보정 불필요) |
| 단일 노드 속도 | 빠름 | 약간 느림 |
| 다중 노드 확장성 | 큰 시스템에서 FFT 병목 | 더 좋음 |
| 슬랩 처리 | 보정하면 문제없음 | 별도 처리 없이 지원 |
| 여기서의 역할 | 기준 비교군 | 슬랩 기하에 알맞음 |

목적별로 고르면 다음과 같다.

1. 기준 비교: OPLS-AA + PPPM(가장 널리 쓰는 조합)과 OPLS-AA + MSM(슬랩에 유리)을 함께 돌린다.
2. 빠른 스크리닝: TraPPE-UA + PPPM (비용이 낮다).
3. 슬랩 정밀 분석: TraPPE-UA + MSM (안정적이고 슬랩에 유리하다).

## 6.5 논문용 비교

논문을 목표로 한다면 4가지 프레임워크를 모두 돌려 다음을 보고하는 편이 탄탄하다.

- 힘장 효과: 같은 정전기 처리(예: MSM)에서 OPLS와 TraPPE 결과 비교
- 정전기 효과: 같은 힘장(예: TraPPE)에서 PPPM과 MSM 결과 비교
- 상호작용 효과: 4가지 조합의 ANOVA 또는 직접 비교

이렇게 엇갈려 비교해 두면 결과가 특정 힘장이나 정전기 방식에 기대지 않는다는 점을 보이기 쉽고,
방법에서 생긴 artifact와 실제 물리 효과를 가려내는 데도 도움이 된다.

## 6.6 앞으로의 진행 순서

내 이전 결과(TraPPE-UA + MSM 성공, OPLS-AA + PPPM 부분 성공)를 보면
다음 순서로 진행하는 것이 좋겠다.

1. OPLS-AA + PPPM 안정화부터: 시간 스텝을 줄이고 SHAKE를 쓴다 (위 6.3절 참조).
2. OPLS-AA + MSM 실행: PPPM이 안정된 뒤 같은 OPLS-AA 파라미터에서 MSM으로만 바꾼다.
   기존 입력 파일에서 `kspace_style` 라인만 고치면 된다.
3. TraPPE-UA + PPPM 추가: 이미 안정한 TraPPE-UA 시스템에서 정전기만 PPPM으로 바꾼다.
   역시 기존 입력 파일에서 `kspace_style` 라인만 고친다.
4. 결과 비교: 4가지 모두에서 SEI, 흡착 에너지, 표면 조성을 표로 정리한다.

프레임워크 사이의 차이가 힘장과 정전기 처리에서만 나오도록 다음은 모두 똑같이 맞춘다.

- 같은 초기 데이터 파일 (`opls.data` 또는 `trappe.data`)
- 같은 시간 스텝, dump 빈도, thermo 출력 빈도
- 같은 평형화/production 시간
- 같은 분석 스크립트 (`integrated_analysis.py`)

## 6.7 출력 파일 이름 규칙

여러 프레임워크의 출력 파일이 섞이지 않도록 다음처럼 이름을 붙인다.

```text
<framework>/
├── 01_soft.log
├── 01_soft.lammpstrj
├── 02_min.log
├── 02_min.data
├── 03_heat.log
├── 03_heat.lammpstrj
├── 04_eq.log
├── 04_eq.lammpstrj
├── 04_equilibrated.data
├── 05_prod.log
├── 05_production.lammpstrj
└── analysis_results/
```

여기서 `<framework>`는 `opls-pppm`, `opls-msm`, `trappe-pppm`, `trappe-msm` 중 하나다.

## 참고문헌

1. 이 문서의 LAMMPS 명령어는 모두 LAMMPS 공식 문서와 대조해 확인했다:
   [https://docs.lammps.org/](https://docs.lammps.org/)

2. LAMMPS 공식 문서, `fix shake`:
   [https://docs.lammps.org/fix_shake.html](https://docs.lammps.org/fix_shake.html)

3. M. P. Allen, D. J. Tildesley,
   "Computer Simulation of Liquids", 2nd ed., Oxford University Press (2017).

4. 내 이전 시뮬레이션 결과를 이 가이드의 출발점으로 삼았다.
