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

본 장에서는 본 시뮬레이션 시스템에서 실제로 관측된 오류 사례와 그 해결 방법을 정리한다.
일반적인 LAMMPS 오류 일람은 공식 문서 [Errors](https://docs.lammps.org/Errors.html) 를 참조한다.

---

## 8.1 "Bond atoms missing on proc N at step M"

### 증상

```
ERROR: Bond atoms missing on proc 3 at step 12450 (../ntopo_bond_all.cpp:62)
```

본 오류는 결합으로 연결된 두 원자 중 한쪽이 인접 프로세서의 통신 영역 (ghost atom region) 을
벗어났을 때 발생한다. 분자가 비정상적으로 늘어났거나 (bond stretching), 통신 차단 거리가
너무 짧을 때 나타난다.

### 진단

가장 먼저 확인할 사항은 마지막 출력된 온도와 압력 값이다. 온도가 비정상적으로 높은
값 (예: 10000 K 이상) 으로 폭주했다면 원인은 결합 자체가 아니라 적분 불안정이다.
8.2 절을 참조한다.

### 해결책

**1) Communication cutoff 확장**

기본값은 force cutoff 와 동일하나, 결합 길이가 커진 상태에서는 충분치 않다.
`common.in` 또는 시작부에 다음을 추가한다.

```lammps
comm_modify cutoff 14.0   # force cutoff 의 1.3~1.4 배 권장
neighbor    2.0 bin       # neighbor skin 증가
neigh_modify every 1 delay 0 check yes
```

**2) Soft potential 초기 단계 확인**

데이터 파일에서 분자 구조가 비현실적으로 가까이 배치된 경우 (특히 packmol 출력의
경계 영역), 첫 단계 `fix nve/limit` 의 변위 제한을 더 작게 한다.

```lammps
fix relax all nve/limit 0.01   # 기본 0.05 에서 축소
run 50000
```

**3) 데이터 파일 검증**

```bash
grep -c "^[[:space:]]*[0-9]" opls.data    # 원자 수 카운트
```

기대값 (OPLS-AA 2471, TraPPE-UA 1371) 과 일치하는지 확인한다. 분자 ID, 원자 타입,
전하 컬럼이 모두 채워져 있는지 직접 확인한다.

---

## 8.2 가열 단계에서의 온도 폭주

### 증상

가열 단계 (특히 0.1 K → 10 K 또는 100 K → 200 K 전환부) 에서 온도가
지정 값을 크게 초과하여 발산한다. OPLS-AA + PPPM 조합에서 빈번히 관측되었다.

### 원인 분석

세 가지 가능성을 차례로 점검한다.

**1) 타임스텝 과대**

수소 진동 주기는 약 10 fs 이며, OPLS-AA 전 원자 모델은 C-H 결합을 명시적으로 적분한다.
SHAKE 미사용 시 0.5 fs 이하가 안전하다.

```lammps
timestep 0.5
```

SHAKE 를 사용하면 1.0~2.0 fs 까지 허용된다.

```lammps
fix shake all shake 0.0001 20 0 b 1 2 3 a 1 2
timestep 2.0
```

**2) Langevin damping 부족**

저온 영역에서 damping 파라미터가 너무 크면 (즉 마찰이 약하면) 열욕과의 결합이
느려져 국소 핫스팟이 형성된다. 4.2 절 권장값을 따른다.

```lammps
fix lang all langevin 0.1 10.0 50.0 12345   # damp = 50 fs (저온)
fix lang all langevin 100.0 200.0 100.0 12345  # damp = 100 fs (중온 이후)
```

**3) 초기 속도 미설정**

데이터 파일에 Velocities 섹션이 없으면 모든 원자가 정지 상태에서 시작한다.
0.1 K 가열을 의도했다 하더라도 초기 속도를 명시적으로 부여해야 한다.

```lammps
velocity organic create 0.1 87287 dist gaussian mom yes rot yes
```

### 추가 조치: 에너지 등가화

극저온 단계에서 단단한 LJ 코어가 활성화되면 적분이 불안정해진다.
1 단계에서 soft potential 을 충분히 길게 (≥ 50 ps) 돌린 뒤 진행한다.

---

## 8.3 도메인 분해 (Domain Decomposition) 문제

### 증상

```
ERROR: Out of range atoms - cannot compute PPPM
ERROR: Domain too small for processor sub-domains
```

또는 병렬 처리 시 특정 프로세서 수에서만 발생하는 충돌.

### 원인

PPPM 은 도메인 분해 기반의 FFT 를 사용하므로, 슬랩 형상 (z 방향이 짧고 진공이 큰 경우)
에서 z 축 분할이 비효율적이다. 본 시스템 박스 (30 × 30 × 41.9 Å) 는 z 분할이
4 이상이 되면 한 서브도메인의 두께가 PPPM 격자 간격보다 작아진다.

### 해결책

**1) Processor 그리드 수동 지정**

z 방향 분할을 1로 고정하고 xy 평면에서만 분할한다.

```lammps
processors * * 1
```

40 코어 환경에서는 다음을 고려한다.

```lammps
processors 8 5 1
```

**2) PPPM 차수 및 격자 조정**

```lammps
kspace_style pppm 1.0e-5
kspace_modify slab 3.0 pressure/scalar no
kspace_modify order 5    # 기본 5, 4까지 낮춰 도메인 요구 완화 가능
```

**3) MSM 으로 전환**

MSM 은 격자 기반 멀티그리드 방법으로, FFT 가 필요 없으며 슬랩 형상에서
도메인 분해 제약이 훨씬 약하다. 4.3 절 참조.

```lammps
kspace_style msm 1.0e-4
```

본 프로젝트에서 TraPPE-UA + MSM 조합이 안정적이었던 이유 중 하나가 이것이다.

---

## 8.4 평형 시간이 지나치게 길어짐 (OPLS-AA)

### 증상

NVT 평형 단계에서 4~5 ns 가 지나도 에탄올 OH 그룹의 RDF 첫 피크 위치가 계속
이동한다. 에너지는 평형으로 보이나 구조는 미평형 상태.

### 원인

OPLS-AA 전 원자 모델은 에탄올의 협력적 수소결합 (cooperative H-bonding)
재구성을 정확히 기술하며, 이 과정의 특성 시간은 수 ns 이다. United-atom 모델
(TraPPE-UA) 에서는 명시적 OH 수소가 없어 이 효과가 약화되므로 평형이 빠르다.

### 권장 절차

총 평형 시간 7.5 ns 권장 (1 단계 평형 + 6.5 ns 재평형).

```lammps
# Stage 4a: 초기 평형
fix eq1 organic nvt temp 300.0 300.0 100.0
run 500000        # 1 ns @ dt=2fs

# Stage 4b: 본 평형
unfix eq1
fix eq2 organic nvt temp 300.0 300.0 100.0
run 3250000       # 6.5 ns
```

평형 판정은 다음 두 가지를 모두 충족할 때만 인정한다.

1. 마지막 500 ps 의 총 에너지 표준편차 / 평균 < 0.1%
2. 마지막 500 ps 와 그 이전 500 ps 의 O-H 첫 피크 RDF 변화 < 5%

---

## 8.5 Stress 계산 시 NaN 또는 발산

### 증상

```
WARNING: Inconsistent image flags
```

또는 압력 텐서 일부 성분이 비현실적으로 큰 값.

### 원인

`compute stress/atom` 사용 시 K-space 기여가 분자별로 잘 정의되지 않으면
잘못된 응력이 누적된다. 특히 슬랩 보정이 있는 PPPM 에서 빈번하다.

### 해결책

```lammps
compute stress all stress/atom NULL pair bond angle dihedral
```

K-space 항을 명시적으로 제외하고 pair, bond, angle, dihedral 만 포함한다.
Irving-Kirkwood 적분 시 K-space 의 장거리 기여는 별도로 계산하거나,
짧은 cutoff 영역에서의 응력만 의미있게 해석한다.

`kspace_modify pressure/scalar no` 옵션도 함께 설정해야 응력 텐서가
정상적으로 출력된다.

---

## 8.6 진단 체크리스트

문제 발생 시 다음 순서로 점검한다.

1. **로그 파일 마지막 50줄 확인** — 온도, 압력, 에너지의 거동
2. **데이터 파일 무결성** — 원자 수, 결합 수, 전하 합
3. **타임스텝 적정성** — SHAKE 유무에 따라 0.5 / 2.0 fs
4. **K-space 설정** — PPPM 은 slab 보정 필요, MSM 은 불필요
5. **Communication cutoff** — `comm_modify cutoff` 적정성
6. **Processor 분할** — `processors * * 1` 슬랩 권장
7. **Soft potential 단계** — 충분한 시간 (≥ 50 ps)
8. **재현성** — 다른 random seed 로 같은 오류가 재현되는가

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
