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

<p class="amm-id">NOTE 32-06-00 · 4가지 프레임워크 비교</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 힘장 두 가지와 정전기 처리 두 가지를 엇갈려 조합한 4가지 프레임워크를 비교한다.
2. 이 노트는 UROPS 보고서 값 중 그대로 쓸 수 없는 값과 그 이유를 보고서 값과 함께 적는다.
3. 이 노트는 비교를 다시 할 때의 실행 순서와 출력 파일 이름 규칙을 정한다.

### B. 적용 범위

1. 슬랩 기하의 Cu 표면 벤젠-에탄올 계(~1500-2500 원자)에 적용한다.
2. 이 노트의 LAMMPS 명령어는 LAMMPS 22 Jul 2025 에서 `opls.data` 로 실행해 확인했다.

### C. 결과 요약

1. 이 가이드는 "어느 조합이 더 안정적이다"는 결론을 내리지 않는다.
2. UROPS 보고서의 SEI 와 흡착 에너지는 힘장 비교에 쓸 수 없다.
3. 같은 OPLS-AA 궤적에서 PPPM 과 MSM 의 첫 층 조성은 통계 오차 안에서 같다.
4. 이 크기에서는 PPPM + slab 을 기본으로 쓰고, MSM 은 확인용으로 돌린다.

## 2. 준비 정보

### A. 필요한 개념

1. OPLS-AA 와 TraPPE-UA 의 차이(NOTE 32-03-00).
2. PPPM 과 MSM 의 차이(NOTE 32-04-00).
3. 5단계 프로토콜(NOTE 32-05-00).

### B. 참조 자료

| 참조 | 제목 |
|------|------|
| LAMMPS 공식 문서 | [https://docs.lammps.org/](https://docs.lammps.org/) (이 노트의 명령어는 LAMMPS 22 Jul 2025 에서 `opls.data` 로 확인) |
| LAMMPS 공식 문서, `fix shake` | [https://docs.lammps.org/fix_shake.html](https://docs.lammps.org/fix_shake.html) |
| M. P. Allen, D. J. Tildesley | "Computer Simulation of Liquids", 2nd ed., Oxford University Press (2017) |
| [PPPM vs MSM 글](../../blog/2026/08/22/pppm-vs-msm-cu-benzene-ethanol/) | 같은 OPLS-AA 궤적의 블록 평균 재분석 |
| [3장](03-force-fields) | 타입이 맞는 OPLS-AA 계수, Cu-유기 LJ |
| 이전 시뮬레이션(UROPS run) 결과 | 이 가이드의 출발점 |

### C. 사용 프로그램

| 항목 | 용도 |
|------|------|
| LAMMPS 22 Jul 2025 | 4가지 프레임워크 실행, `fix shake` 구문 확인 |
| `integrated_analysis.py` | 네 조합에 공통으로 쓰는 분석 스크립트 |

### D. 관련 파일

| 항목 | 용도 |
|------|------|
| `opls.data` | OPLS-AA 초기 데이터 파일 |
| `trappe.data` | TraPPE-UA 초기 데이터 파일 |
| `kspace_pppm.in`, `kspace_msm.in` | 정전기 처리 설정을 바꾸는 include 파일 |

## 3. 절차

### A. 2×2 비교 설계

1. 힘장 두 가지와 정전기 처리 두 가지를 엇갈려 네 조합을 만든다.

|             | PPPM | MSM |
|-------------|------|-----|
| **OPLS-AA**   | OPLS+PPPM | OPLS+MSM |
| **TraPPE-UA** | TraPPE+PPPM | TraPPE+MSM |

2. 다음 세 효과를 따로 떼어 비교한다.
    1. 힘장 효과: PPPM을 고정하고 OPLS-AA와 TraPPE-UA를 비교한다.
    2. 정전기 처리 효과: 같은 힘장에서 PPPM과 MSM을 비교한다.
    3. 상호작용 효과: 두 인자를 조합했을 때만 나타나는 효과를 본다(예: TraPPE+MSM이 다른 조합보다 유독 잘/못 동작하는 경우).

### B. UROPS run 결과 확인

1. UROPS 보고서가 표로 낸 네 조합의 SEI 와 흡착 에너지를 기록과 대조한다.

| 프레임워크 | 보고서 SEI | 보고서 벤젠 흡착 에너지 | 기록에서 확인한 것 |
|-------------|--------|--------|------|
| OPLS-AA + PPPM | -0.686 | -0.271 eV | 2 ns production 완료. 첫 층 벤젠 몰분율 0.70 ± 0.05 |
| OPLS-AA + MSM | 0.809 | -0.269 eV | 2 ns production 완료. 첫 층 벤젠 몰분율 0.66 ± 0.03 |
| TraPPE-UA + PPPM | 0.867 | -0.325 eV | 초기 run 은 전하가 없었고 100→150 K 승온 중 Bond atoms missing 으로 멈춤 |
| TraPPE-UA + MSM | 0.930 | -0.321 eV | 위와 같은 입력(전하가 없어 kspace 가 없으므로 PPPM 과 같은 계산) |

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
**SEI**: 보고서의 정의는 $|x_\text{surf} - x_\text{bulk}| / (1 - x_\text{bulk})$ 이라 음수가 나올 수 없다. -0.686 은 계산이나 정의 중 하나가 틀린 것이다.
</div>

2. 보고서 SEI 의 부호를 정의와 대조한다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
**흡착 에너지**: 보고서 방법 절에 따르면 이 값은 힘장 에너지가 아니다. "최대 2.0 eV(벤젠), 1.5 eV(에탄올)의 지수형 거리 함수"로 계산한 값이다.
힘장이 주는 Cu-분자 상호작용 에너지가 아니므로 힘장 비교에 쓸 수 없다.
</div>

3. 보고서 흡착 에너지를 힘장 비교에서 뺀다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
**PPPM 과 MSM 의 차이**: 같은 OPLS-AA 궤적을 블록 평균으로 다시 분석하면 첫 층 조성은 두 방법이 통계 오차 안에서 같다
([PPPM vs MSM 글](../../blog/2026/08/22/pppm-vs-msm-cu-benzene-ethanol/)). 보고서가 말한 "정전기 방법 의존성"은 확인되지 않았다.
</div>

4. PPPM 과 MSM 의 차이는 블록 평균 오차와 함께 판단한다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
**TraPPE-UA**: 초기 TraPPE-UA run 두 개는 입력, 시드, 프로세스 수가 같아 비트 단위로 같은 계산이었고, 같은 스텝에서 멈췄다.
최종 보고서의 TraPPE-UA run 이 그 뒤 전하를 넣고 다시 돌린 것인지는 남은 입력으로 확인할 수 없다.
</div>

5. TraPPE-UA 두 행을 정전기 처리 비교에 쓰지 않는다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
그래서 이 가이드는 "어느 조합이 더 안정적이다"는 결론을 내리지 않는다. 비교를 다시 하려면 네 조합 모두 같은 데이터 파일과 같은 길이로 돌리고, 블록 평균으로 오차를 낸 뒤 비교한다(5.B).
</div>

### C. 프레임워크별 예측 비교

1. 두 힘장의 예측과 차이가 생기는 곳을 다음 표로 확인한다.

| 물리량 | OPLS-AA | TraPPE-UA | 차이가 생기는 곳 |
|--------|---------------|------------------|-------------|
| 표면 1차 흡착층 조성 | 측정 필요 | 측정 필요 | 벤젠 표현(전원자 vs UA)과 Cu-유기 LJ |
| 에탄올 O-O g(r) 첫 피크 | 약 2.8 Å 예상 | 약 2.8 Å 예상 | 두 모형 모두 수산기 H 를 명시한다 |
| 평형화 시간 | 조성 프로파일로 판단 | 조성 프로파일로 판단 | UA 는 자유도가 적어 빠를 수 있다 |

### D. 가열 단계 불안정 대처

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
가열 단계에서 계가 터지는 원인은 대개 아래 네 가지 중 하나다. 차례로 확인한다.
</div>

1. 시간 스텝을 확인한다. X-H 신축 주기가 9–11 fs 이므로 SHAKE 없이 1.0 fs 는 큰 편이다.
2. 시간 스텝을 0.5 fs 로 줄인다.
3. 초기 구조의 중첩이 덜 풀렸는지 확인한다.
    1. `opls.data` 처럼 1 Å 이내로 붙은 쌍이 있는지 본다.
    2. 그런 쌍이 있으면 1단계를 충분히 돌린다.
4. 열욕 설정을 확인한다.
    1. Langevin 은 damp 가 작을수록 열욕에 강하게 묶이므로 폭주를 일으키지 않는다.
    2. Nose-Hoover(`fix nvt`)는 damp 가 timestep 의 수십 배보다 작으면 온도가 크게 진동하므로 100 fs 정도로 둔다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
thermo 온도의 분모: 고정된 Cu 를 포함한 `thermo_temp` 를 기준으로 열욕을 걸면 유기층이 목표보다 뜨거워진다.
</div>

5. 열욕은 `organic` 그룹에 건다.

### E. SHAKE 로 시간 스텝 늘리기

1. `opls.data` 의 X-H 결합 타입을 확인한다. 2 (벤젠 C-H), 4·10 (CH₂ 의 C-H), 5·6·9 (CH₃ 의 C-H), 8 (O-H) 이다.
2. H-C-H 각도는 CH₂ 의 것(타입 15)만 묶는다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
각도 구속은 3원자 클러스터에만 걸린다. 그래서 H-C-H 각도는 CH₂ 의 것(타입 15)만 묶을 수 있다.
</div>

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
데이터 파일에 없는 타입 번호(예: 11)를 주면 "Invalid bond type 11 index for fix shake" 오류가 난다.
벤젠 C-C(타입 1)처럼 클러스터끼리 이어지는 결합을 넣으면 "Shake clusters are connected" 오류가 난다.
</div>

3. 다음 명령으로 X-H 결합과 CH₂ 각도를 묶고 시간 스텝을 2.0 fs 로 둔다.

```lammps
fix             shake_xh organic shake 1.0e-4 20 0 b 2 4 5 6 8 9 10 a 15
timestep        2.0
```

4. 잡힌 클러스터 수를 확인한다.
    1. 2원자 클러스터 700개(벤젠 C-H 600, O-H 100).
    2. 4원자 클러스터 100개(CH₃).
    3. 각도까지 묶은 3원자 클러스터 100개(CH₂).

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
UROPS run 의 `fix shake_OH ethanol shake 0.0001 20 0 b 8 a 6` 은 O-H 결합 100개만 묶는다.
각도 타입 6 은 C-C-H 라 O-H 클러스터에 속하지 않으므로 무시된다.
</div>

5. 기존 입력의 `a` 옵션 각도 타입이 묶인 클러스터에 속하는지 확인한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
`fix shake`의 b (bonds), a (angles), t (atom types), m (atom mass) 옵션은
[LAMMPS fix shake 문서](https://docs.lammps.org/fix_shake.html)에 정리되어 있다.
</div>

### F. 정전기 처리 선택

1. 이 시스템(슬랩 기하, ~1500-2500 원자)에서 두 방법을 다음 표로 비교한다.

| 항목 | PPPM | MSM |
|------|------|-----|
| 초기 설정 복잡도 | 중간 (`kspace_modify slab 3.0` 필요) | 낮음 (slab 보정 불필요) |
| 2,471원자, 40 랭크 루프 시간 | 19,647 s | 31,988 s (1.63배) |
| 다중 노드 확장성 | 큰 시스템에서 FFT 병목 | 더 좋음 |
| 슬랩 처리 | 보정하면 문제없음 | 별도 처리 없이 지원 |
| 첫 흡착층 조성 (UROPS run) | 0.70 ± 0.05 | 0.66 ± 0.03 |

2. PPPM + slab 을 기본으로 쓴다. 이 크기에서는 구조가 같고 PPPM 이 더 빠르다.
3. MSM 은 확인용으로 돌린다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
TraPPE-UA 는 원자 수가 적어 스크리닝에 유리하지만, 전하를 넣지 않으면 PPPM/MSM 비교 자체가 의미가 없다.
</div>

4. TraPPE-UA 로 정전기 처리를 비교할 때는 전하를 넣은 `trappe.data` 를 쓴다.

### G. 출력 파일 이름 규칙

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
여러 프레임워크를 같은 디렉터리에서 돌리면 출력 파일이 섞인다.
</div>

1. 프레임워크마다 디렉터리를 하나 두고 다음처럼 이름을 붙인다.

```text
<framework>/
├── 01_soft.log        stage1.restart
├── 02_min.log         stage2.restart
├── 03_heat.log        stage3.restart
├── 04_eq.log          stage4.restart
├── 05_prod.log        stage5.restart, final.data
├── dump.lammpstrj
├── profile_benzene.dat, profile_ethanol.dat, rdf.dat, stress_profile.dat
└── analysis_results/
```

2. `<framework>`는 `opls-pppm`, `opls-msm`, `trappe-pppm`, `trappe-msm` 중 하나로 정한다.
3. 로그 파일 이름은 `lmp -in 01_soft.in -log 01_soft.log` 처럼 실행할 때 정한다.

## 4. 시험 및 검사

### A. 논문용 비교 항목

1. 논문을 목표로 한다면 4가지 프레임워크를 모두 돌린다.
2. 다음 세 항목을 보고한다.
    1. 힘장 효과: 같은 정전기 처리(예: MSM)에서 OPLS와 TraPPE 결과를 비교한다.
    2. 정전기 효과: 같은 힘장(예: TraPPE)에서 PPPM과 MSM 결과를 비교한다.
    3. 상호작용 효과: 4가지 조합의 ANOVA 또는 직접 비교를 한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
네 조합을 모두 보고하는 편이 논문에서 탄탄하다. 이렇게 엇갈려 비교해 두면 결과가 특정 힘장이나 정전기 방식에 기대지 않는다는 점을 보이기 쉽다.
방법에서 생긴 artifact와 실제 물리 효과를 가려내는 데도 도움이 된다.
</div>

## 5. 종료

### B. 후속 작업

1. 3.B 를 바탕으로 비교를 다시 할 때는 데이터 파일부터 다시 만든다: fcc(100) Cu 슬랩, 타입이 맞는 OPLS-AA 계수([3장](03-force-fields)), 의도한 Cu-유기 LJ.
2. OPLS-AA + PPPM 으로 평형화 기준을 정한다. 벌크 조성 프로파일이 평평해질 때까지 돌린다.
3. OPLS-AA + MSM 은 `include kspace_pppm.in` 을 `kspace_msm.in` 으로 바꿔 돌린다(pair style 도 같이 바뀐다).
4. TraPPE-UA 두 조합은 전하를 넣은 `trappe.data` 로, 같은 길이만큼 돌린다.
5. 표면 조성과 Cu-분자 상호작용 에너지(`compute group/group`)를 블록 평균 오차와 함께 표로 비교한다.
6. 프레임워크 사이의 차이가 힘장과 정전기 처리에서만 나오도록 다음은 모두 똑같이 맞춘다.
    1. 같은 초기 데이터 파일 (`opls.data` 또는 `trappe.data`)
    2. 같은 시간 스텝, dump 빈도, thermo 출력 빈도
    3. 같은 평형화/production 시간
    4. 같은 분석 스크립트 (`integrated_analysis.py`)
