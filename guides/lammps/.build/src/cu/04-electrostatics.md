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

쿨롱 상호작용은 거리에 반비례 ($1/r$) 하므로 단순한 cutoff 방식은 큰 오차를 만든다.
특히 에탄올의 수산기와 같이 큰 부분 전하 (q_O = -0.7e, q_H = +0.435e) 가 있는 분자에서는
장거리 효과가 시스템 에너지의 비중을 크게 차지한다.

장거리 정전기 처리 방법은 크게 두 가지가 있다.

- **Particle-Particle Particle-Mesh (PPPM, Hockney & Eastwood 1988)**:
  FFT 기반. 거의 모든 분자동역학 시스템의 표준.
- **Multilevel Summation Method (MSM, Hardy et al. 2009)**:
  다중격자 (multigrid) 기반. 슬랩 기하학에 자연스럽게 적용 가능.

## 4.2 PPPM의 작동 원리와 한계

PPPM은 전하를 격자에 매핑하고 FFT (Fast Fourier Transform) 를 사용해
역공간에서 장거리 부분을 계산한다.

- **계산 복잡도**: O(N log N)
- **요구 조건**: 모든 방향에서 주기 경계 (`boundary p p p`)
- **장점**: 매우 빠르며 정확도 제어가 쉬움
- **한계**: 슬랩 시스템 (z 방향 비주기) 에는 직접 사용 불가

### 슬랩 보정 (PPPM Slab correction)

본 가이드의 시스템은 `boundary p p f` (z 비주기) 이다.
PPPM을 이러한 슬랩 시스템에 적용하려면 추가 보정이 필요하다.

```bash
kspace_style pppm 1.0e-4
kspace_modify slab 3.0
```

`kspace_modify slab 3.0`은 다음을 수행한다 ([LAMMPS kspace_modify 문서](https://docs.lammps.org/kspace_modify.html)).

1. 시뮬레이션 박스의 z 방향으로 빈 공간 (vacuum) 을 추가하여
   시스템을 인공적으로 3배 큰 박스 (volfactor = 3.0) 로 만든다.
2. 인접 슬랩과의 쌍극자-쌍극자 상호작용을 제거한다 (Yeh & Berkowitz 1999의 방법).

`volfactor = 3.0`은 권장값이다. 더 큰 값은 비효율적이고, 더 작은 값은 슬랩-슬랩 상호작용을 남긴다.
[LAMMPS kspace_modify 공식 문서](https://docs.lammps.org/kspace_modify.html)에 명시되어 있다.

### PPPM 슬랩 사용 시 주의사항

z 방향이 비주기이므로 원자가 z-경계 밖으로 이탈하지 않도록 벽 (wall) 을 두어야 한다.
LAMMPS 명령어:

```bash
# z-상단에 LJ 9-3 형태의 부드러운 벽 (atoms cannot escape)
fix wall_top all wall/lj93 zhi EDGE 0.1 3.0 10.0 units box

# 또는 단순 반사 벽
fix wall_top_reflect all wall/reflect zhi EDGE
```

[LAMMPS fix wall/lj93 문서](https://docs.lammps.org/fix_wall.html)에 따르면
9-3 형태는 Cu 슬랩 같은 평면 표면에서 유도되는 자연스러운 LJ 벽 포텐셜이다.

### kspace_modify의 그 외 설정

- `kspace_modify pressure/scalar no`: 슬랩에서 압력 텐서 계산 시 권장.
  스칼라 압력만 계산하지 않고 텐서로 계산하면 정확도 향상.
  ([LAMMPS 공식 문서](https://docs.lammps.org/kspace_modify.html))

## 4.3 MSM의 작동 원리와 장점

MSM은 다중격자 보정 기법으로, FFT를 사용하지 않고 격자 간 계층적 보간을 수행한다.

- **계산 복잡도**: O(N)
- **요구 조건**: 3차원이면 주기/비주기/shrink-wrap 모두 가능
- **장점**: 슬랩 시스템에 추가 보정 없이 자연스럽게 적용 가능
- **한계**: 정확도가 같은 수준일 때 PPPM보다 느릴 수 있음 (특히 작은 시스템에서)

### MSM의 LAMMPS 설정

```bash
kspace_style msm 1.0e-4
# slab 보정 명령어 불필요
```

`kspace_modify slab` 명령어는 MSM과 사용할 수 없다 ([LAMMPS 공식 문서](https://docs.lammps.org/kspace_modify.html)에 명시).
MSM은 본질적으로 비주기 경계를 지원하기 때문이다.

### MSM의 권장 설정

```bash
kspace_style msm 1.0e-4
kspace_modify order 8 pressure/scalar no
```

`order 8`은 MSM의 기본값이다 (PPPM은 5).
주의: MSM의 `order`는 짝수만 가능하며, 4-10 범위이다.
[LAMMPS kspace_modify 문서](https://docs.lammps.org/kspace_modify.html) 참조.

## 4.4 PPPM vs MSM 직접 비교

| 항목 | PPPM | MSM |
|------|------|-----|
| 계산 복잡도 | O(N log N) | O(N) |
| 슬랩 처리 | `slab 3.0` 필요 | 자연스럽게 지원 |
| 경계 조건 | p p p (또는 slab으로 p p f) | 모든 조합 가능 |
| 정확도 제어 | accuracy 인자 (1.0e-4 권장) | accuracy 인자 (1.0e-4 권장) |
| FFT 사용 | 사용 | 사용 안 함 |
| 병렬 확장성 | 큰 시스템에서 FFT가 병목 가능 | 좋음 |
| 메모리 사용 | 중간 | 다소 큼 |
| 정확도 차이 | 매우 비슷 (slab 보정 후) | 매우 비슷 |

본 시스템 (~1000-2500 원자) 의 규모에서 PPPM과 MSM의 절대 계산 시간 차이는
크지 않으나, MSM은 슬랩 기하학을 명시적인 보정 없이 처리할 수 있다는 점에서
계면 시뮬레이션에 더 적합하다는 의견이 있다 (Hardy et al. 2009).

다만 PPPM은 분자동역학 커뮤니티의 사실상 표준이므로, 두 방법으로 시뮬레이션하여
결과를 교차 검증하는 것이 권장된다.

## 4.5 cutoff 거리 선택

장거리 정전기 (PPPM/MSM) 사용 시 실공간 (real-space) 부분의 cutoff는 LJ cutoff와 통일하는 것이 일반적이다.

| 힘장 | 권장 cutoff |
|------|-------------|
| OPLS-AA | 10.0 Å (또는 12.0 Å) |
| TraPPE-UA | 14.0 Å (TraPPE 공식 권장) |

본 가이드에서는 통일성을 위해 12.0 Å을 사용한다. TraPPE-UA에서 더 짧은 cutoff를 쓰면
파라미터 fit의 정확도가 약간 떨어질 수 있다.

```bash
pair_style lj/cut/coul/long 12.0
```

## 4.6 정확도 (accuracy) 매개변수

`kspace_style {pppm|msm}`의 두 번째 인자는 상대 정확도이다.

```bash
kspace_style pppm 1.0e-4   # 1.0e-4 = 0.01% 상대 정확도
```

- **1.0e-3**: 빠른 스크리닝용, 계면 시뮬레이션에는 비권장
- **1.0e-4**: 표준 (본 가이드의 권장값)
- **1.0e-5**: 매우 정확하지만 비용 큼, 자유에너지 계산용

## 4.7 본 가이드의 네 가지 정전기/힘장 조합

다음은 네 가지 프레임워크 각각의 핵심 kspace 설정 라인이다.

### OPLS-AA + PPPM

```bash
pair_style lj/cut/coul/long 12.0
pair_modify mix geometric tail no
kspace_style pppm 1.0e-4
kspace_modify slab 3.0 pressure/scalar no
```

### OPLS-AA + MSM

```bash
pair_style lj/cut/coul/long 12.0
pair_modify mix geometric tail no
kspace_style msm 1.0e-4
kspace_modify pressure/scalar no
```

### TraPPE-UA + PPPM

```bash
pair_style lj/cut/coul/long 12.0
pair_modify mix arithmetic tail no
kspace_style pppm 1.0e-4
kspace_modify slab 3.0 pressure/scalar no
```

### TraPPE-UA + MSM

```bash
pair_style lj/cut/coul/long 12.0
pair_modify mix arithmetic tail no
kspace_style msm 1.0e-4
kspace_modify pressure/scalar no
```

힘장 (mix rule) 과 정전기 (kspace_style) 만 바꾸면 동일한 프로토콜로 네 가지 조합을 모두 실행할 수 있다.
이를 통해 두 인자의 영향을 분리 분석할 수 있는 직교 (orthogonal) 실험 설계가 완성된다.

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

---

[← 이전: 3. 힘장 비교](03-force-fields) ｜ [다음: 5. 5단계 프로토콜 →](05-protocol)
