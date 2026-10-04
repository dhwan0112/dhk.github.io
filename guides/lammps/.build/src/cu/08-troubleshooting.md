---
layout: default
title: "8. 트러블슈팅"
nav_order: 9
---

# 8. 트러블슈팅
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<p class="amm-id">NOTE 32-08-00 · 응용 트러블슈팅</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 이 시스템을 돌리면서 실제로 만난 오류와 해결 방법을 다룬다.
2. 증상마다 가능한 원인, 점검, 조치 순으로 적는다.

### B. 적용 범위

1. Cu 슬랩 위 벤젠-에탄올 계(`opls.data` 2471 원자, `trappe.data` 1371 원자)에 적용한다.
2. LAMMPS 오류 전반은 공식 문서 [Errors](https://docs.lammps.org/Errors.html) 에 정리되어 있다.

## 2. 준비 정보

### A. 필요한 개념

1. Cu 응용 시리즈 NOTE 32-01-00 ~ 32-07-00 의 내용.
2. 일반 오류 진단 절차(NOTE 31-08-00).

### B. 참조 자료

| 참조 | 제목 |
|------|------|
| LAMMPS 공식 문서 | [Errors](https://docs.lammps.org/Errors.html) |
| LAMMPS Documentation, Common Errors | <https://docs.lammps.org/Errors_common.html> |
| Plimpton, S. | *J. Comput. Phys.* **117**, 1 (1995). DOI: [10.1006/jcph.1995.1039](https://doi.org/10.1006/jcph.1995.1039) |
| Frenkel, D.; Smit, B. | *Understanding Molecular Simulation: From Algorithms to Applications*, 2nd ed.; Academic Press, 2002. Chapter 4. |
| Allen, M. P.; Tildesley, D. J. | *Computer Simulation of Liquids*, 2nd ed.; Oxford University Press, 2017. Section 3.5. |
| [6장](06-frameworks) | SHAKE 결합 타입 번호를 고르는 법 |
| [7장](07-analysis) | 원자별 응력의 빈별 합 계산 |

### C. 사용 프로그램

| 항목 | 용도 |
|------|------|
| LAMMPS | 시뮬레이션 실행, 오류 재현 |
| `awk` | 데이터 파일의 원자 수와 전하 합 검증 |

### D. 관련 파일

| 항목 | 용도 |
|------|------|
| `opls.data`, `trappe.data` | 검증할 데이터 파일 |
| `common.in` | 공통 설정 (`comm_modify`, `neighbor`) |
| `inputs/04_eq.in` | 평형화 입력 |

## 3. 결함 분리 절차

### A. 증상: "Bond atoms missing on proc N at step M"

1. 다음 오류로 run 이 멈춘다.

```
ERROR: Bond atoms missing on proc 3 at step 12450 (../ntopo_bond_all.cpp:62)
```

#### 가능한 원인

2. 결합된 두 원자 중 하나가 인접 프로세서의 통신 영역(ghost atom region)을 벗어났다.
3. 분자가 비정상적으로 늘어났다(bond stretching).
4. 통신 차단 거리가 너무 짧다.

#### 점검

5. 마지막으로 출력된 온도와 압력을 가장 먼저 본다.
6. 온도가 비정상적으로 높은 값(예: 10000 K 이상)으로 폭주했다면 원인은 결합 자체가 아니라 적분 불안정이다. 3.B 로 간다.

#### 조치

7. Communication cutoff 를 확장한다. `common.in` 이나 입력 시작 부분에 다음을 넣는다.

```lammps
comm_modify cutoff 14.0   # pair cutoff 12 Å + skin 2 Å 이상으로
neighbor    2.0 bin       # neighbor skin 증가
neigh_modify every 1 delay 0 check yes
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
ghost 원자 범위의 기본값은 pair cutoff + neighbor skin 이다. 분자가 크거나 결합이 늘어난 상태에서는 이 값이 모자랄 수 있다.
</div>

8. Soft potential 초기 단계를 확인한다.
    1. 데이터 파일에서 분자가 비현실적으로 가깝게 놓여 있는지 본다(특히 packmol 출력의 경계 부분).
    2. 그렇다면 첫 단계 `fix nve/limit` 의 변위 제한을 더 줄인다.

```lammps
fix relax organic nve/limit 0.01   # inputs/ 의 0.05 에서 축소
run 50000
```

9. 데이터 파일을 검증한다. Atoms 섹션의 줄 수와 전하 합을 구한다.

```bash
# Atoms 섹션의 줄 수와 전하 합
awk '/^Atoms/{f=1; getline; next} f&&NF==0{exit} f{n++; q+=$4} END{print n, q}' opls.data
```

10. 줄 수가 기대값(OPLS-AA 2471, TraPPE-UA 1371)과 맞는지, 전하 합이 0 인지 본다.
11. 분자 ID, 원자 타입, 전하 컬럼이 모두 채워져 있는지도 직접 확인한다.

### B. 증상: 가열 단계의 온도 폭주

1. 가열 단계(특히 0.1 K → 10 K 또는 100 K → 200 K 로 넘어가는 구간)에서 온도가 설정값을 크게 넘어 발산하거나 "Bond atoms missing" 으로 멈춘다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
UROPS 초기 TraPPE-UA run 두 개가 100 → 150 K 구간에서 이렇게 멈췄다.
</div>

#### 가능한 원인

2. 타임스텝이 너무 크다.
3. Langevin damping 이 부족하다.
4. 초기 속도를 주지 않았다.
5. 초기 구조에 원자가 겹쳐 있다. 단단한 LJ 코어 때문에 적분이 불안정해진다.

#### 점검

6. 앞의 세 가지 가능성(타임스텝, damping, 초기 속도)을 차례로 확인한다.
7. 타임스텝을 확인한다. 수소 진동 주기는 약 10 fs 이고, OPLS-AA 전원자 모델은 C-H 결합까지 그대로 적분한다.
8. Langevin damping 값을 확인한다. 저온에서 damping 파라미터가 너무 크면(즉 마찰이 약하면) 열욕과의 결합이 느려져 국소적으로 뜨거운 곳(핫스팟)이 생긴다.
9. 데이터 파일에 Velocities 섹션이 있는지 확인한다. 없으면 모든 원자가 멈춘 상태에서 시작한다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
같은 입력, 같은 시드, 같은 MPI 프로세스 수로 돌린 두 run 은 비트 단위로 같은 궤적을 낸다.
두 run 이 같은 스텝에서 멈췄다는 사실은 그래서 아무것도 알려 주지 않는다.
</div>

10. 재현성을 확인한다. 원인을 찾으려면 `velocity ... create` 와 `fix langevin` 의 시드를 바꿔 다시 돌린다.

#### 조치

11. SHAKE 를 쓰지 않으면 타임스텝을 0.5 fs 이하로 둔다.

```lammps
timestep 0.5
```

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
벤젠 C-C(결합 타입 1)를 넣으면 고리 전체가 하나로 이어져 "Shake clusters are connected" 오류가 난다.
</div>

12. X-H 결합을 SHAKE 로 묶으면 1.0~2.0 fs 까지 늘릴 수 있다. `opls.data` 기준 타입 번호는 다음과 같다
(번호를 고르는 법은 [6장](06-frameworks)).

```lammps
fix shake_xh organic shake 1.0e-4 20 0 b 2 4 5 6 8 9 10 a 15
timestep 2.0
```

13. Langevin damping 값은 [5장](05-protocol) 3.C 를 따른다.

```lammps
fix lang organic langevin 0.1 10.0 50.0 12345     # damp = 50 fs (저온)
fix lang organic langevin 100.0 200.0 100.0 12347 # damp = 100 fs (중온 이후)
```

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
열욕을 `all` 에 걸면 Cu 자유도까지 온도 계산에 들어가 유기층이 목표보다 뜨거워진다.
</div>

14. 열욕은 고정된 Cu 를 뺀 `organic` 그룹에 건다.
15. 초기 속도를 직접 준다. 0.1 K 에서 가열을 시작하려는 경우에도 필요하다.

```lammps
velocity organic create 0.1 87287 dist gaussian mom yes rot yes
```

16. 초기 중첩을 해소한다. 1 단계 소프트 완화를 충분히 길게(≥ 50 ps) 돌린 뒤 넘어간다.

### C. 증상: 도메인 분해 (Domain Decomposition) 문제

1. 다음 오류가 난다. 또는 병렬로 돌릴 때 특정 프로세서 수에서만 충돌이 나거나, 코어를 늘려도 빨라지지 않는다.

```
ERROR: Out of range atoms - cannot compute PPPM
```

#### 가능한 원인

2. "Out of range atoms" 는 원자가 한 번의 재이웃(reneighbor) 사이에 PPPM 격자의 허용 범위 밖으로 움직였다는 뜻이다.
3. 이 오류는 거의 항상 계가 터지는 중이라는 신호다. 병렬 분할 자체가 원인인 경우는 드물다.
4. 성능 쪽 문제는 원자 밀도가 z 방향으로 고르지 않아 생긴다. Cu 가 아래 7 Å, 액체가 그 위 약 30 Å 를 채운다.
5. z 로 나누면 프로세서마다 원자 수가 크게 달라진다.
6. 랭크당 원자가 너무 적다. 2,471원자를 40 랭크로 나누면 랭크당 62원자라 UROPS run 의 통신 비중이 13–26 % 였다.

#### 점검

7. "Out of range atoms" 가 나면 3.B 를 먼저 본다.

#### 조치

8. Processor 그리드를 직접 지정한다. z 방향은 1로 고정하고 xy 평면에서만 나눈다.

```lammps
processors * * 1
```

9. 이 크기라면 코어 수 자체를 줄인다. 랭크당 원자 200개 이상이 되도록 8–16 코어면 충분하다.

```lammps
processors 4 4 1    # 16 코어
```

10. PPPM 차수를 조정한다.

```lammps
kspace_style pppm 1.0e-5
kspace_modify slab 3.0
kspace_modify order 4    # 기본 5. 낮추면 ghost 격자가 줄어든다
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
MSM 으로 바꾸는 것은 이 크기에서는 해결책이 아니다. 같은 정확도에서 MSM 이 1.63배 느렸다([4장](04-electrostatics) 4.B).
</div>

### D. 증상: 평형화가 너무 오래 걸림 (OPLS-AA)

1. NVT 평형 단계에서 4~5 ns 가 지나도 에탄올 OH 그룹의 RDF 첫 피크 위치가 계속 움직인다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
에너지는 평형에 이른 것처럼 보여도 구조는 아직 평형이 아니다.
</div>

#### 가능한 원인

2. 에탄올의 수소 결합 네트워크가 재배열되는 데 시간이 걸린다.
3. 슬랩 계에서는 그보다 느린 과정이 하나 더 있다. 두 성분이 막의 두께 방향으로 재분배되는 확산이다.
4. 30 Å 두께의 막에서 액체 확산 계수가 $10^{-9}$ m²/s 정도면 $L^2/D \approx 1$ ns 이고, 첫 흡착층의 분자 교환은 이보다 느리다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
TraPPE-UA 도 수산기 H 를 명시하므로 수소 결합 자체는 두 모형 모두 있다.
</div>

#### 점검

5. 평형은 에너지가 아니라 조성으로 판단한다. 다음을 모두 만족해야 평형으로 본다.
    1. z 방향 벤젠·에탄올 밀도 프로파일을 앞뒤 절반으로 나눠 그렸을 때 차이가 블록 오차 안에 든다.
    2. 첫 층 벤젠 몰분율의 누적 평균이 더 이상 한쪽으로 움직이지 않는다.
    3. 에탄올 O-O RDF 첫 피크가 앞뒤 절반에서 같다.

#### 조치

6. 평형화를 1 ns + 6.5 ns 로 돌린다. `inputs/04_eq.in` 은 이 길이로 잡아 두었다(0.5 fs).

```lammps
# 04_eq.in, dt = 0.5 fs
fix tstat organic nvt temp 300.0 300.0 100.0
run 2000000       # 4a) 1 ns
run 13000000      # 4b) 6.5 ns
```

7. SHAKE 로 2 fs 를 쓴다면 스텝 수를 1/4 로 줄인다.

### E. 증상: Stress 계산에서 NaN 또는 발산

1. 압력 프로파일이 비현실적으로 크거나, 빈마다 들쭉날쭉하거나, 액체 한가운데서 $P_{zz}$ 가 일정하지 않다.

#### 가능한 원인

2. **합 대신 평균을 냈다**: `fix ave/chunk` 에 `c_stress[1]` 을 넣으면 빈 안 원자의 평균이 나온다.
3. **부호**: `stress/atom` 은 압력의 반대 부호다. $P = -\sum s / V$.
4. **빠진 항**: 키워드를 일부만 적어 `kspace`, `improper`, `fix` 가 빠졌다. 벽과 `setforce` 의 기여는 `fix` 키워드로 들어간다.
5. **MSM**: `kspace_modify pressure/scalar yes` 면 원자별 virial 이 나오지 않는다.
6. **SHAKE**: 구속력의 virial 은 `fix` 항으로 들어가므로 SHAKE 를 쓸 때 `fix` 를 빼면 압력이 틀린다.

#### 점검

7. 액체 영역에서 $P_{zz}$ 가 평평한지 본다. $P_{zz}(z)$ 는 역학적 평형에서 z 에 상관없이 일정해야 하므로 가장 쉬운 검산이다.
8. `stress/atom` 키워드를 확인한다. 키워드를 생략하면 모든 항이 들어가지만, 일부만 적었다면 `kspace`, `improper`, `fix` 가 빠졌는지 본다.

#### 조치

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
합 대신 평균, 부호, 빠진 항, SHAKE 의 `fix` 누락은 모두 틀린 압력 프로파일을 낸다.
</div>

9. 빈별 합을 `compute reduce/chunk ... sum` 으로 구하고 빈 부피로 나눈다([7장](07-analysis) 3.E).
10. 압력은 $P = -\sum s / V$ 로 부호를 바꿔 구한다.
11. 벽과 `setforce` 를 쓰면 `fix` 키워드를 포함한다.
12. MSM 에서는 `pressure/scalar` 를 기본값 `no` 로 둔다.
13. SHAKE 를 쓸 때는 `fix` 키워드를 빼지 않는다.

## 4. 시험 및 검사

### A. 진단 체크리스트

1. 문제가 생기면 다음 순서로 확인한다.
    1. 로그 파일 마지막 50줄: 온도, 압력, 에너지의 거동
    2. 데이터 파일 무결성: 원자 수, 결합 수, 전하 합
    3. 타임스텝: SHAKE 유무에 따라 0.5 / 2.0 fs
    4. K-space 설정: PPPM 은 slab 보정 필요, MSM 은 불필요
    5. Communication cutoff: `comm_modify cutoff` 가 충분한지
    6. Processor 분할: 슬랩이면 `processors * * 1`
    7. Soft potential 단계: 충분한 시간 (≥ 50 ps)
    8. 재현성: 다른 random seed 로도 같은 오류가 나는가 (같은 시드면 당연히 같은 곳에서 멈춘다)
