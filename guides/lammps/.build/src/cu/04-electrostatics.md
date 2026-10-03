---
layout: default
title: "4. 정전기 방법: PPPM vs MSM"
nav_order: 5
---

# 4. 정전기 방법: PPPM vs MSM
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 4.1 왜 장거리 정전기 처리가 필요한가

쿨롱 상호작용은 거리에 반비례($1/r$)해서 천천히 줄어들기 때문에, 단순히 cutoff로 자르면 오차가 크다.
에탄올 수산기처럼 부분 전하가 큰(q_O = -0.7e, q_H = +0.435e) 분자가 있으면
장거리 기여가 시스템 에너지에서 차지하는 몫이 커진다.

장거리 정전기는 크게 두 가지 방법으로 처리한다.

- **Particle-Particle Particle-Mesh (PPPM, Hockney & Eastwood 1988)**:
  FFT 기반. 분자동역학에서 가장 널리 쓰인다.
- **Multilevel Summation Method (MSM, Hardy et al. 2009)**:
  다중격자(multigrid) 기반. 슬랩 기하에 그대로 적용할 수 있다.

## 4.2 PPPM의 작동 원리와 한계

PPPM은 전하를 격자에 옮긴 뒤 FFT(Fast Fourier Transform)로
역공간에서 장거리 부분을 계산한다.

- **계산 복잡도**: O(N log N)
- **요구 조건**: 모든 방향에서 주기 경계 (`boundary p p p`)
- **장점**: 매우 빠르며 정확도 제어가 쉬움
- **한계**: 슬랩 시스템 (z 방향 비주기) 에는 직접 사용 불가

### 슬랩 보정 (PPPM Slab correction)

이 시스템은 `boundary p p f` (z 비주기) 다.
이런 슬랩 시스템에 PPPM을 쓰려면 보정을 더해야 한다.

```bash
kspace_style pppm 1.0e-4
kspace_modify slab 3.0
```

`kspace_modify slab 3.0`은 다음 일을 한다 ([LAMMPS kspace_modify 문서](https://docs.lammps.org/kspace_modify.html)).

1. 시뮬레이션 박스의 z 방향으로 빈 공간 (vacuum) 을 추가하여
   시스템을 인공적으로 3배 큰 박스 (volfactor = 3.0) 로 만든다.
2. 인접 슬랩과의 쌍극자-쌍극자 상호작용을 제거한다 (Yeh & Berkowitz 1999의 방법).

여기서는 `volfactor = 3.0`을 썼다. 값을 키우면 계산만 늘고, 줄이면 슬랩-슬랩 상호작용이 남는다.
3.0은 [LAMMPS kspace_modify 공식 문서](https://docs.lammps.org/kspace_modify.html)가 권하는 값이기도 하다.

### PPPM 슬랩 사용 시 주의사항

z 방향이 비주기이므로 원자가 z-경계 밖으로 빠져나가지 않게 벽(wall)을 둬야 한다.

```bash
# z-상단에 LJ 9-3 형태의 부드러운 벽 (atoms cannot escape)
fix wall_top organic wall/lj93 zhi EDGE 0.1 3.0 10.0 units box

# UROPS run 이 쓴 벽 (12-6 형태, epsilon 1.0 kcal/mol, sigma 3.0 A, cutoff 2.5 A)
# fix wall_top organic wall/lj126 zhi EDGE 1.0 3.0 2.5

# 또는 단순 반사 벽
fix wall_top_reflect all wall/reflect zhi EDGE
```

[LAMMPS fix wall/lj93 문서](https://docs.lammps.org/fix_wall.html)에 따르면
9-3 형태는 Cu 슬랩 같은 평면 표면에서 유도되는 LJ 벽 포텐셜이다.

### kspace_modify의 그 외 설정

- `kspace_modify pressure/scalar`: MSM 전용 키워드다. `yes` 로 두면 MSM 이 스칼라 압력만 빠르게 계산하고,
  압력 텐서와 원자별 virial(`compute stress/atom`)은 나오지 않는다. 기본값은 `no` 다.
  PPPM 에서는 아무 효과가 없으므로 PPPM 입력에는 넣지 않는다.
  ([LAMMPS 공식 문서](https://docs.lammps.org/kspace_modify.html))

## 4.3 MSM의 작동 원리와 장점

MSM은 다중격자 기법으로, FFT 없이 여러 층의 격자 사이를 보간하며 계산한다.

- **계산 복잡도**: O(N)
- **요구 조건**: 3차원이면 주기/비주기/shrink-wrap 모두 가능
- **장점**: 슬랩 시스템에 추가 보정 없이 자연스럽게 적용 가능
- **한계**: 정확도가 같은 수준일 때 PPPM보다 느릴 수 있음 (특히 작은 시스템에서)

### MSM의 LAMMPS 설정

```bash
kspace_style msm 1.0e-4
# slab 보정 명령어 불필요
```

`kspace_modify slab` 은 MSM과 함께 쓸 수 없다([LAMMPS 공식 문서](https://docs.lammps.org/kspace_modify.html)).
MSM은 애초에 비주기 경계를 지원하기 때문이다.

### MSM 설정 예

```bash
pair_style lj/cut/coul/msm 12.0
kspace_style msm 1.0e-4
kspace_modify order 10 pressure/scalar no
```

MSM 의 `order` 기본값은 10 이고(PPPM 은 5), 4, 6, 8, 10 중에서 고른다.
MSM 은 정확도 목표를 맞추려고 실공간 Coulomb cutoff 를 스스로 바꾼다. 위 설정을 `opls.data` 에 걸면
"Adjusting Coulombic cutoff for MSM, new cutoff = 9.373041" 경고와 함께 cutoff 가 12 Å 에서 9.37 Å 으로 줄어든다.
이걸 막으려면 `kspace_modify cutoff/adjust no` 를 쓴다. 정확도를 위해 `pair_modify table 0` 을 권하는 경고도 함께 나온다.
[LAMMPS kspace_modify 문서](https://docs.lammps.org/kspace_modify.html) 참조.

## 4.4 PPPM vs MSM 직접 비교

| 항목 | PPPM | MSM |
|------|------|-----|
| 계산 복잡도 | O(N log N) | O(N) |
| 슬랩 처리 | `slab 3.0` 필요 | 자연스럽게 지원 |
| 경계 조건 | p p p (또는 slab으로 p p f) | 모든 조합 가능 |
| 정확도 제어 | accuracy 인자 (여기서는 1.0e-4) | accuracy 인자 (여기서는 1.0e-4) |
| 실공간 pair style | `lj/cut/coul/long` | `lj/cut/coul/msm` (`coul/long` 은 오류) |
| `compute group/group ... kspace yes` | 지원 | 지원 안 함 |
| FFT 사용 | 사용 | 사용 안 함 |
| 병렬 확장성 | 큰 시스템에서 FFT가 병목 가능 | 좋음 |
| 메모리 사용 | 중간 | 다소 큼 |
| 정확도 차이 | 매우 비슷 (slab 보정 후) | 매우 비슷 |

이 규모에서는 MSM 이 확실히 느렸다. UROPS run 두 개(2,471원자, 40 MPI 랭크, 정확도 1e-5, 4,000,000 스텝)의 루프 시간은
PPPM + slab 19,647 s, MSM 31,988 s 로 MSM 이 1.63배였고, kspace 비중은 22 % 대 65 % 였다.
첫 흡착층 구조는 두 방법이 통계 오차 안에서 같았다
([PPPM vs MSM 글](../../blog/2026/08/22/pppm-vs-msm-cu-benzene-ethanol/)).
MSM 의 O(N) 이점은 수만 원자 이상에서나 기대할 수 있다.

PPPM이 분자동역학에서 가장 널리 쓰이는 방법이니, 두 방법으로 모두 돌려
결과를 서로 대조해 보는 편이 좋다.

## 4.5 cutoff 거리 선택

장거리 정전기(PPPM/MSM)를 쓸 때 실공간(real-space) 부분의 cutoff는 보통 LJ cutoff와 맞춘다.

| 힘장 | 권장 cutoff |
|------|-------------|
| OPLS-AA | 10.0 Å (또는 12.0 Å) |
| TraPPE-UA | 14.0 Å (TraPPE 공식 권장) |

`inputs/` 는 통일성을 위해 12.0 Å 을 쓴다(UROPS run 은 14.0 Å). TraPPE-UA 에서 cutoff 를 더 짧게 쓰면
파라미터 fit 의 정확도가 조금 떨어질 수 있다. MSM 에서는 위에 적었듯 Coulomb cutoff 가 자동으로 바뀔 수 있다.

```bash
pair_style lj/cut/coul/long 12.0
```

## 4.6 정확도 (accuracy) 매개변수

`kspace_style {pppm|msm}`의 두 번째 인자는 상대 정확도다.

```bash
kspace_style pppm 1.0e-4   # 1.0e-4 = 0.01% 상대 정확도
```

- 1.0e-3: 빠른 스크리닝용. 계면 시뮬레이션에는 부족하다.
- 1.0e-4: `inputs/` 의 값.
- 1.0e-5: UROPS run 의 값. 더 정확하지만 비용이 크다.

## 4.7 네 가지 정전기/힘장 조합

네 프레임워크의 핵심 kspace 설정은 다음과 같다.

### OPLS-AA + PPPM

```bash
pair_style lj/cut/coul/long 12.0
pair_modify mix geometric tail no
kspace_style pppm 1.0e-4
kspace_modify slab 3.0
```

### OPLS-AA + MSM

```bash
pair_style lj/cut/coul/msm 12.0
pair_modify mix geometric tail no
kspace_style msm 1.0e-4
kspace_modify pressure/scalar no
```

### TraPPE-UA + PPPM

```bash
pair_style lj/cut/coul/long 12.0
pair_modify mix arithmetic tail no
kspace_style pppm 1.0e-4
kspace_modify slab 3.0
```

### TraPPE-UA + MSM

```bash
pair_style lj/cut/coul/msm 12.0
pair_modify mix arithmetic tail no
kspace_style msm 1.0e-4
kspace_modify pressure/scalar no
```

힘장(mix rule)과 정전기(kspace_style)만 바꾸면 같은 프로토콜로 네 조합을 모두 돌릴 수 있다.
그래서 힘장과 정전기의 영향을 따로 떼어 보는 2×2 비교가 된다.

## 참고문헌

1. R. W. Hockney, J. W. Eastwood,
   "Computer Simulation Using Particles",
   Adam Hilger (1988). ISBN: 0-85274-392-0.

2. I.-C. Yeh, M. L. Berkowitz,
   "Ewald summation for systems with slab geometry",
   *J. Chem. Phys.* **111**, 3155-3162 (1999).
   DOI: [10.1063/1.479595](https://doi.org/10.1063/1.479595)

3. D. J. Hardy, J. E. Stone, K. Schulten,
   "Multilevel Summation of Electrostatic Potentials Using Graphics Processing Units",
   *Parallel Comput.* **35**, 164-177 (2009).
   DOI: [10.1016/j.parco.2008.12.005](https://doi.org/10.1016/j.parco.2008.12.005)

4. LAMMPS 공식 문서, `kspace_style`:
   [https://docs.lammps.org/kspace_style.html](https://docs.lammps.org/kspace_style.html)

5. LAMMPS 공식 문서, `kspace_modify`:
   [https://docs.lammps.org/kspace_modify.html](https://docs.lammps.org/kspace_modify.html)

6. LAMMPS 공식 문서, `fix wall/lj93`:
   [https://docs.lammps.org/fix_wall.html](https://docs.lammps.org/fix_wall.html)

