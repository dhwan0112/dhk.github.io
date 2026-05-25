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

## 6.1 직교 실험 설계

본 가이드의 4가지 프레임워크는 다음과 같은 직교 (orthogonal) 실험 설계를 따른다.

|             | PPPM | MSM |
|-------------|------|-----|
| **OPLS-AA**   | OPLS+PPPM | OPLS+MSM |
| **TraPPE-UA** | TraPPE+PPPM | TraPPE+MSM |

이러한 설계의 강점:

- **힘장 효과 분리**: PPPM 고정 조건에서 OPLS-AA vs TraPPE-UA 비교
- **정전기 처리 효과 분리**: 동일 힘장에서 PPPM vs MSM 비교
- **상호작용 효과 검출**: 두 인자의 조합 효과 (예: TraPPE+MSM이 다른 조합 대비 특히 잘/못 동작) 식별

## 6.2 프레임워크별 사전 관찰 (사용자 보고)

다음은 본 시스템에서 사용자가 실제로 관찰한 정성적 경향이다.
이는 본 가이드의 기준 baseline 으로 활용된다.

| 프레임워크 | 안정성 | SEI (분리 효율) | 흡착 에너지 (벤젠) | 비고 |
|-------------|--------|--------|--------------------|------|
| OPLS-AA + PPPM | 가열 단계 불안정 가능 | 부분 성공 | - | 온도 폭주 (runaway) 경향 |
| OPLS-AA + MSM | 안정 | 양호 | - | slab 보정 불필요 |
| TraPPE-UA + PPPM | 안정 | 0.85-0.95 | -0.27 ~ -0.30 eV | 표준 |
| TraPPE-UA + MSM | 매우 안정 | 0.93-1.00 | -0.27 ~ -0.32 eV | 최고 성능 |

흡착 에너지 단위 변환: -0.30 eV ≈ -6.92 kcal/mol ≈ -28.95 kJ/mol.
벤젠이 에탄올보다 더 강하게 표면에 흡착되는 것은 π-d 분산 상호작용 (London dispersion)
과 LJ 파라미터의 적합 (fit) 으로 잘 재현된다.

## 6.3 프레임워크별 화학적 예측 비교

| 물리량 | OPLS-AA 예측 | TraPPE-UA 예측 | 화학적 기원 |
|--------|---------------|------------------|-------------|
| 표면 1차 흡착층 조성 | 벤젠 우세, 에탄올 협동 효과 가능 | 벤젠 강한 우세 | 수소 결합 처리 차이 |
| 에탄올-에탄올 g(r) 첫 피크 | 약 2.8 Å (O-H...O 수소 결합) | 약 2.8 Å (동등) | 명시적 H 차이 |
| 평형화 시간 | 7-10 ns | 2-3 ns | 협동성 vs 단순 LJ |
| 계면 장력 | 약 25-30 mJ/m² | 약 22-27 mJ/m² | 분극성 처리 차이 |

위 값들은 사용자의 실제 시뮬레이션 결과와 문헌값을 참고한 정성적 예측이며,
출판 시에는 직접 측정한 값을 사용해야 한다.

### 왜 OPLS-AA는 가열 단계에서 불안정한가

OPLS-AA 시스템의 가열 단계 불안정성은 다음 원인이 흔하다:

1. **시간 스텝이 너무 큰 경우**: 1.0 fs는 OPLS-AA + 비 SHAKE 조합에서는 큰 편.
   X-H 진동 (~3000 cm⁻¹) 주기는 약 11 fs로, Nyquist 기준으로 0.5 fs 이하 권장.
2. **SHAKE 미사용**: SHAKE로 X-H 결합을 고정하면 시간 스텝을 2.0 fs까지 늘릴 수 있다.
3. **Langevin damp 너무 짧음**: damp가 너무 작으면 (예: 10 fs) 무리한 에너지 펌핑으로 폭주 발생.
4. **PPPM accuracy 너무 낮음**: 1.0e-3 정도면 슬랩 보정과 결합 시 큰 정전기 오차 누적.

### 권장 수정 (소수 줄만 수정)

기존 입력 파일에서 다음 두 줄만 수정해도 안정성이 크게 향상된다.

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

## 6.4 정전기 처리 비교 — 본 시스템에서의 권고

본 시스템 (슬랩 기하학, ~1500-2500 원자) 에서:

| 항목 | PPPM | MSM |
|------|------|-----|
| 초기 설정 복잡도 | 중간 (`kspace_modify slab 3.0` 필요) | 낮음 (slab 보정 불필요) |
| 단일 노드 속도 | 빠름 | 약간 느림 |
| 다중 노드 확장성 | 큰 시스템에서 FFT 병목 | 더 좋음 |
| 슬랩 시스템 자연스러움 | 보정 후 자연스러움 | 본질적으로 자연스러움 |
| 본 가이드 권장 | 표준 비교군 | 슬랩 기하학에 권장 |

따라서 본 가이드의 결론적 권고는:

1. **표준 비교**: OPLS-AA + PPPM (커뮤니티 표준) 과 OPLS-AA + MSM (slab 친화) 동시 실행
2. **빠른 스크리닝**: TraPPE-UA + PPPM (저비용 표준)
3. **고품질 슬랩 분석**: TraPPE-UA + MSM (안정성 + slab 친화)

## 6.5 출판용 비교 권장

학술 출판을 목표로 하는 경우, 4가지 프레임워크를 모두 실행하여 다음을 보고하는 것이 견고하다.

- **힘장 효과**: 같은 정전기 (예: MSM) 에서 OPLS vs TraPPE 결과 비교
- **정전기 효과**: 같은 힘장 (예: TraPPE) 에서 PPPM vs MSM 결과 비교
- **상호작용 효과**: 4가지 조합의 ANOVA 또는 직접 비교

이러한 직교 실험 설계는 결과의 robustness 를 증명하는 데 효과적이며,
특정 힘장/정전기 방식의 artifact 와 진정한 물리 효과를 구별하는 데 도움이 된다.

## 6.6 사용자의 실험 진행 권고

사용자의 이전 결과 (TraPPE-UA + MSM 성공, OPLS-AA + PPPM 부분 성공) 를 고려할 때
다음 우선순위로 진행을 권한다.

1. **OPLS-AA + PPPM 안정화 우선**: 시간 스텝과 SHAKE 사용 (위 6.3절 참조).
2. **OPLS-AA + MSM 실행**: PPPM 안정화 후 동일 OPLS-AA 파라미터로 MSM 교체.
   기존 입력 파일에서 `kspace_style` 라인만 변경.
3. **TraPPE-UA + PPPM 추가**: 이미 안정한 TraPPE-UA 시스템에서 정전기만 PPPM으로 교체.
   기존 입력 파일에서 `kspace_style` 라인만 변경.
4. **결과 통합 비교**: 4가지 모두에서 SEI, 흡착 에너지, 표면 조성을 표로 정리.

각 프레임워크 간 차이를 최소화 (논문에서 "minimal change") 하기 위해 다음을 통일:

- 동일한 초기 데이터 파일 (`opls.data` 또는 `trappe.data`)
- 동일한 시간 스텝, dump 빈도, thermo 출력 빈도
- 동일한 평형화/생성 시간
- 동일한 분석 스크립트 (`integrated_analysis.py`)

## 6.7 출력 파일 명명 규칙 (권장)

여러 프레임워크의 출력 파일이 섞이지 않도록 다음 명명 규칙을 권한다.

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

여기서 `<framework>`는 `opls-pppm`, `opls-msm`, `trappe-pppm`, `trappe-msm` 중 하나이다.

## 참고문헌

1. 본 문서의 LAMMPS 명령어들은 모두 LAMMPS 공식 문서로 검증되었다:
   [https://docs.lammps.org/](https://docs.lammps.org/)

2. LAMMPS 공식 문서, `fix shake`:
   [https://docs.lammps.org/fix_shake.html](https://docs.lammps.org/fix_shake.html)

3. M. P. Allen, D. J. Tildesley,
   "Computer Simulation of Liquids", 2nd ed., Oxford University Press (2017).

4. 사용자의 사전 시뮬레이션 결과는 본 가이드 작성의 baseline 으로 활용되었다.

---

[← 이전: 5. 5단계 프로토콜](05-protocol) ｜ [다음: 7. 분석 방법 →](07-analysis)
