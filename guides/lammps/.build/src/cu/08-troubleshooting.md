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

기본값은 force cutoff 와 같은데, 결합이 늘어난 상태에서는 모자란다.
`common.in` 이나 입력 시작 부분에 다음을 넣는다.

```lammps
comm_modify cutoff 14.0   # force cutoff 의 1.3~1.4 배 권장
neighbor    2.0 bin       # neighbor skin 증가
neigh_modify every 1 delay 0 check yes
```

**2) Soft potential 초기 단계 확인**

데이터 파일에서 분자가 비현실적으로 가깝게 놓여 있으면(특히 packmol 출력의
경계 부분) 첫 단계 `fix nve/limit` 의 변위 제한을 더 줄인다.

```lammps
fix relax all nve/limit 0.01   # 기본 0.05 에서 축소
run 50000
```

**3) 데이터 파일 검증**

```bash
grep -c "^[[:space:]]*[0-9]" opls.data    # 원자 수 카운트
```

기대값(OPLS-AA 2471, TraPPE-UA 1371)과 맞는지 보고, 분자 ID, 원자 타입,
전하 컬럼이 모두 채워져 있는지도 직접 확인한다.

---

## 8.2 가열 단계의 온도 폭주

### 증상

가열 단계(특히 0.1 K → 10 K 또는 100 K → 200 K 로 넘어가는 구간)에서 온도가
설정값을 크게 넘어 발산한다. 내 run에서는 OPLS-AA + PPPM 조합에서 자주 나왔다.

### 원인 분석

세 가지 가능성을 차례로 확인한다.

**1) 타임스텝이 너무 큼**

수소 진동 주기는 약 10 fs 이고, OPLS-AA 전원자 모델은 C-H 결합까지 그대로 적분한다.
SHAKE 를 쓰지 않으면 0.5 fs 이하가 안전하다.

```lammps
timestep 0.5
```

SHAKE 를 쓰면 1.0~2.0 fs 까지 늘릴 수 있다.

```lammps
fix shake all shake 0.0001 20 0 b 1 2 3 a 1 2
timestep 2.0
```

**2) Langevin damping 부족**

저온에서 damping 파라미터가 너무 크면(즉 마찰이 약하면) 열욕과의 결합이
느려져 국소적으로 뜨거운 곳(핫스팟)이 생긴다. 값은 4.2 절을 따른다.

```lammps
fix lang all langevin 0.1 10.0 50.0 12345   # damp = 50 fs (저온)
fix lang all langevin 100.0 200.0 100.0 12345  # damp = 100 fs (중온 이후)
```

**3) 초기 속도를 주지 않음**

데이터 파일에 Velocities 섹션이 없으면 모든 원자가 멈춘 상태에서 시작한다.
0.1 K 에서 가열을 시작하려는 경우에도 초기 속도는 직접 줘야 한다.

```lammps
velocity organic create 0.1 87287 dist gaussian mom yes rot yes
```

### 추가 조치: 에너지 등가화

극저온 단계에서 단단한 LJ 코어가 켜지면 적분이 불안정해진다.
1 단계 soft potential 을 충분히 길게(≥ 50 ps) 돌린 뒤 넘어간다.

---

## 8.3 도메인 분해 (Domain Decomposition) 문제

### 증상

```
ERROR: Out of range atoms - cannot compute PPPM
ERROR: Domain too small for processor sub-domains
```

또는 병렬로 돌릴 때 특정 프로세서 수에서만 나는 충돌.

### 원인

PPPM 은 도메인 분해에 기반한 FFT 를 쓰기 때문에 슬랩 형상(z 방향이 짧고 진공이 큰 경우)
에서는 z 축 분할이 비효율적이다. 이 시스템 박스(30 × 30 × 41.9 Å)는 z 분할이
4 이상이면 서브도메인 하나의 두께가 PPPM 격자 간격보다 작아진다.

### 해결책

**1) Processor 그리드 직접 지정**

z 방향은 1로 고정하고 xy 평면에서만 나눈다.

```lammps
processors * * 1
```

40 코어라면 이렇게 나눌 수 있다.

```lammps
processors 8 5 1
```

**2) PPPM 차수와 격자 조정**

```lammps
kspace_style pppm 1.0e-5
kspace_modify slab 3.0 pressure/scalar no
kspace_modify order 5    # 기본 5, 4까지 낮춰 도메인 요구 완화 가능
```

**3) MSM 으로 전환**

MSM 은 격자 기반 멀티그리드 방법이라 FFT 가 필요 없고, 슬랩 형상에서도
도메인 분해 제약이 훨씬 덜하다. 4.3 절 참조.

```lammps
kspace_style msm 1.0e-4
```

내 run에서 TraPPE-UA + MSM 조합이 안정적이었던 이유 중 하나도 이것이다.

---

## 8.4 평형화가 너무 오래 걸림 (OPLS-AA)

### 증상

NVT 평형 단계에서 4~5 ns 가 지나도 에탄올 OH 그룹의 RDF 첫 피크 위치가 계속
움직인다. 에너지는 평형에 이른 것처럼 보여도 구조는 아직 평형이 아니다.

### 원인

OPLS-AA 전원자 모델은 에탄올의 협동적 수소 결합(cooperative H-bonding)이
재배열되는 과정을 정확히 기술하는데, 이 과정의 특성 시간이 수 ns 다. United-atom 모델
(TraPPE-UA)에는 OH 수소가 따로 없어 이 효과가 약하고, 그래서 평형에 빨리 도달한다.

### 평형화 절차

평형화는 총 7.5 ns 로 잡는다 (1 단계 평형 + 6.5 ns 재평형).

```lammps
# Stage 4a: 초기 평형
fix eq1 organic nvt temp 300.0 300.0 100.0
run 500000        # 1 ns @ dt=2fs

# Stage 4b: 본 평형
unfix eq1
fix eq2 organic nvt temp 300.0 300.0 100.0
run 3250000       # 6.5 ns
```

다음 두 조건을 모두 만족해야 평형으로 본다.

1. 마지막 500 ps 의 총 에너지 표준편차 / 평균 < 0.1%
2. 마지막 500 ps 와 그 이전 500 ps 의 O-H 첫 피크 RDF 변화 < 5%

---

## 8.5 Stress 계산에서 NaN 또는 발산

### 증상

```
WARNING: Inconsistent image flags
```

또는 압력 텐서 일부 성분이 비현실적으로 크게 나온다.

### 원인

`compute stress/atom` 을 쓸 때 K-space 기여가 분자별로 제대로 정의되지 않으면
잘못된 응력이 쌓인다. 슬랩 보정을 건 PPPM 에서 특히 자주 생긴다.

### 해결책

```lammps
compute stress all stress/atom NULL pair bond angle dihedral
```

K-space 항은 빼고 pair, bond, angle, dihedral 만 넣는다.
Irving-Kirkwood 적분에서 K-space 의 장거리 기여는 따로 계산하거나,
짧은 cutoff 범위의 응력만 해석에 쓴다.

`kspace_modify pressure/scalar no` 옵션도 같이 줘야 응력 텐서가
제대로 출력된다.

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
8. 재현성: 다른 random seed 로도 같은 오류가 나는가

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
