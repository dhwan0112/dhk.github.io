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

이 장에는 이 시스템을 돌리면서 실제로 만난 오류와 해결 방법을 정리했다.
LAMMPS 오류 전반은 공식 문서 [Errors](https://docs.lammps.org/Errors.html) 에 정리되어 있다.

---

## 8.1 "Bond atoms missing on proc N at step M"

### 증상

```
ERROR: Bond atoms missing on proc 3 at step 12450 (../ntopo_bond_all.cpp:62)
```

이 오류는 결합된 두 원자 중 하나가 인접 프로세서의 통신 영역(ghost atom region)을
벗어나면 난다. 분자가 비정상적으로 늘어났거나(bond stretching) 통신 차단 거리가
너무 짧을 때 생긴다.

### 진단

가장 먼저 볼 것은 마지막으로 출력된 온도와 압력이다. 온도가 비정상적으로 높은
값(예: 10000 K 이상)으로 폭주했다면 원인은 결합 자체가 아니라 적분 불안정이다.
8.2 절 참조.

### 해결책

**1) Communication cutoff 확장**

ghost 원자 범위의 기본값은 pair cutoff + neighbor skin 인데, 분자가 크거나 결합이 늘어난 상태에서는 모자랄 수 있다.
`common.in` 이나 입력 시작 부분에 다음을 넣는다.

```lammps
comm_modify cutoff 14.0   # pair cutoff 12 Å + skin 2 Å 이상으로
neighbor    2.0 bin       # neighbor skin 증가
neigh_modify every 1 delay 0 check yes
```

**2) Soft potential 초기 단계 확인**

데이터 파일에서 분자가 비현실적으로 가깝게 놓여 있으면(특히 packmol 출력의
경계 부분) 첫 단계 `fix nve/limit` 의 변위 제한을 더 줄인다.

```lammps
fix relax organic nve/limit 0.01   # inputs/ 의 0.05 에서 축소
run 50000
```

**3) 데이터 파일 검증**

```bash
# Atoms 섹션의 줄 수와 전하 합
awk '/^Atoms/{f=1; getline; next} f&&NF==0{exit} f{n++; q+=$4} END{print n, q}' opls.data
```

기대값(OPLS-AA 2471, TraPPE-UA 1371)과 맞는지, 전하 합이 0 인지 본다. 분자 ID, 원자 타입,
전하 컬럼이 모두 채워져 있는지도 직접 확인한다.

---

## 8.2 가열 단계의 온도 폭주

### 증상

가열 단계(특히 0.1 K → 10 K 또는 100 K → 200 K 로 넘어가는 구간)에서 온도가
설정값을 크게 넘어 발산하거나 "Bond atoms missing" 으로 멈춘다. UROPS 초기 TraPPE-UA run 두 개가
100 → 150 K 구간에서 이렇게 멈췄다.

### 원인 분석

세 가지 가능성을 차례로 확인한다.

**1) 타임스텝이 너무 큼**

수소 진동 주기는 약 10 fs 이고, OPLS-AA 전원자 모델은 C-H 결합까지 그대로 적분한다.
SHAKE 를 쓰지 않으면 0.5 fs 이하가 안전하다.

```lammps
timestep 0.5
```

X-H 결합을 SHAKE 로 묶으면 1.0~2.0 fs 까지 늘릴 수 있다. `opls.data` 기준 타입 번호는 다음과 같다
(번호를 고르는 법은 [6장](06-frameworks)).

```lammps
fix shake_xh organic shake 1.0e-4 20 0 b 2 4 5 6 8 9 10 a 15
timestep 2.0
```

벤젠 C-C(결합 타입 1)를 넣으면 고리 전체가 하나로 이어져 "Shake clusters are connected" 오류가 난다.

**2) Langevin damping 부족**

저온에서 damping 파라미터가 너무 크면(즉 마찰이 약하면) 열욕과의 결합이
느려져 국소적으로 뜨거운 곳(핫스팟)이 생긴다. 값은 5.3 절을 따른다.

```lammps
fix lang organic langevin 0.1 10.0 50.0 12345     # damp = 50 fs (저온)
fix lang organic langevin 100.0 200.0 100.0 12347 # damp = 100 fs (중온 이후)
```

열욕은 고정된 Cu 를 뺀 `organic` 그룹에 건다. `all` 에 걸면 Cu 자유도까지 온도 계산에 들어가
유기층이 목표보다 뜨거워진다.

**3) 초기 속도를 주지 않음**

데이터 파일에 Velocities 섹션이 없으면 모든 원자가 멈춘 상태에서 시작한다.
0.1 K 에서 가열을 시작하려는 경우에도 초기 속도는 직접 줘야 한다.

```lammps
velocity organic create 0.1 87287 dist gaussian mom yes rot yes
```

### 추가 조치: 초기 중첩 해소

초기 구조에 원자가 겹쳐 있으면 단단한 LJ 코어 때문에 적분이 불안정해진다.
1 단계 소프트 완화를 충분히 길게(≥ 50 ps) 돌린 뒤 넘어간다.

### 재현성 확인

같은 입력, 같은 시드, 같은 MPI 프로세스 수로 돌린 두 run 은 비트 단위로 같은 궤적을 낸다.
두 run 이 같은 스텝에서 멈췄다는 사실은 그래서 아무것도 알려 주지 않는다.
원인을 찾으려면 `velocity ... create` 와 `fix langevin` 의 시드를 바꿔 다시 돌린다.

---

## 8.3 도메인 분해 (Domain Decomposition) 문제

### 증상

```
ERROR: Out of range atoms - cannot compute PPPM
```

또는 병렬로 돌릴 때 특정 프로세서 수에서만 나는 충돌, 코어를 늘려도 빨라지지 않는 현상.

### 원인

"Out of range atoms" 는 원자가 한 번의 재이웃(reneighbor) 사이에 PPPM 격자의 허용 범위 밖으로 움직였다는 뜻이다.
거의 항상 계가 터지는 중이라는 신호이므로 8.2 절을 먼저 본다. 병렬 분할 자체가 원인인 경우는 드물다.

성능 쪽 문제는 따로 있다. 이 계는 Cu 가 아래 7 Å, 액체가 그 위 약 30 Å 를 채우고 있어 z 방향으로 원자 밀도가 고르지 않다.
z 로 나누면 프로세서마다 원자 수가 크게 달라진다. 또 2,471원자를 40 랭크로 나누면 랭크당 62원자라
UROPS run 의 통신 비중이 13–26 % 였다.

### 해결책

**1) Processor 그리드 직접 지정**

z 방향은 1로 고정하고 xy 평면에서만 나눈다.

```lammps
processors * * 1
```

이 크기라면 코어 수 자체를 줄인다. 랭크당 원자 200개 이상이 되도록 8–16 코어면 충분하다.

```lammps
processors 4 4 1    # 16 코어
```

**2) PPPM 차수 조정**

```lammps
kspace_style pppm 1.0e-5
kspace_modify slab 3.0
kspace_modify order 4    # 기본 5. 낮추면 ghost 격자가 줄어든다
```

MSM 으로 바꾸는 것은 이 크기에서는 해결책이 아니다. 같은 정확도에서 MSM 이 1.63배 느렸다(4.4 절).

---

## 8.4 평형화가 너무 오래 걸림 (OPLS-AA)

### 증상

NVT 평형 단계에서 4~5 ns 가 지나도 에탄올 OH 그룹의 RDF 첫 피크 위치가 계속
움직인다. 에너지는 평형에 이른 것처럼 보여도 구조는 아직 평형이 아니다.

### 원인

에탄올의 수소 결합 네트워크가 재배열되는 데 시간이 걸리고, 슬랩 계에서는 그보다 느린 과정이 하나 더 있다.
두 성분이 막의 두께 방향으로 재분배되는 확산이다. 30 Å 두께의 막에서 액체 확산 계수가 $10^{-9}$ m²/s 정도면
$L^2/D \approx 1$ ns 이고, 첫 흡착층의 분자 교환은 이보다 느리다.
TraPPE-UA 도 수산기 H 를 명시하므로 수소 결합 자체는 두 모형 모두 있다.

### 평형화 절차

평형은 에너지가 아니라 조성으로 판단한다. `inputs/04_eq.in` 은 1 ns + 6.5 ns 로 잡아 두었다(0.5 fs).
SHAKE 로 2 fs 를 쓴다면 스텝 수는 1/4 이다.

```lammps
# 04_eq.in, dt = 0.5 fs
fix tstat organic nvt temp 300.0 300.0 100.0
run 2000000       # 4a) 1 ns
run 13000000      # 4b) 6.5 ns
```

다음을 모두 만족해야 평형으로 본다.

1. z 방향 벤젠·에탄올 밀도 프로파일을 앞뒤 절반으로 나눠 그렸을 때 차이가 블록 오차 안에 든다.
2. 첫 층 벤젠 몰분율의 누적 평균이 더 이상 한쪽으로 움직이지 않는다.
3. 에탄올 O-O RDF 첫 피크가 앞뒤 절반에서 같다.

---

## 8.5 Stress 계산에서 NaN 또는 발산

### 증상

압력 프로파일이 비현실적으로 크거나, 빈마다 들쭉날쭉하거나, 액체 한가운데서 $P_{zz}$ 가 일정하지 않다.

### 원인과 해결책

1. **합 대신 평균을 냈다**: `fix ave/chunk` 에 `c_stress[1]` 을 넣으면 빈 안 원자의 평균이 나온다.
   빈별 합을 `compute reduce/chunk ... sum` 으로 구하고 빈 부피로 나눈다([7장](07-analysis) 7.5절).
2. **부호**: `stress/atom` 은 압력의 반대 부호다. $P = -\sum s / V$.
3. **빠진 항**: 키워드를 생략하면 모든 항이 들어가지만, 일부만 적었다면 `kspace`, `improper`, `fix` 가 빠졌는지 본다.
   벽과 `setforce` 의 기여는 `fix` 키워드로 들어간다.
4. **MSM**: `kspace_modify pressure/scalar yes` 면 원자별 virial 이 나오지 않는다. 기본값 `no` 로 둔다.
5. **SHAKE**: 구속력의 virial 은 `fix` 항으로 들어가므로 SHAKE 를 쓸 때 `fix` 를 빼면 압력이 틀린다.

$P_{zz}(z)$ 는 역학적 평형에서 z 에 상관없이 일정해야 하므로, 액체 영역에서 $P_{zz}$ 가 평평한지가 가장 쉬운 검산이다.

---

## 8.6 진단 체크리스트

문제가 생기면 다음 순서로 확인한다.

1. 로그 파일 마지막 50줄: 온도, 압력, 에너지의 거동
2. 데이터 파일 무결성: 원자 수, 결합 수, 전하 합
3. 타임스텝: SHAKE 유무에 따라 0.5 / 2.0 fs
4. K-space 설정: PPPM 은 slab 보정 필요, MSM 은 불필요
5. Communication cutoff: `comm_modify cutoff` 가 충분한지
6. Processor 분할: 슬랩이면 `processors * * 1`
7. Soft potential 단계: 충분한 시간 (≥ 50 ps)
8. 재현성: 다른 random seed 로도 같은 오류가 나는가 (같은 시드면 당연히 같은 곳에서 멈춘다)

---

## 참고문헌

1. LAMMPS Documentation, Common Errors.
   <https://docs.lammps.org/Errors_common.html>
2. Plimpton, S. *J. Comput. Phys.* **117**, 1 (1995).
   DOI: [10.1006/jcph.1995.1039](https://doi.org/10.1006/jcph.1995.1039)
3. Frenkel, D.; Smit, B. *Understanding Molecular Simulation: From
   Algorithms to Applications*, 2nd ed.; Academic Press, 2002. Chapter 4.
4. Allen, M. P.; Tildesley, D. J. *Computer Simulation of Liquids*,
   2nd ed.; Oxford University Press, 2017. Section 3.5.
