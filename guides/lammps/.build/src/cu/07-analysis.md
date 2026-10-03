---
layout: default
title: "7. 분석 방법"
nav_order: 8
---

# 7. 분석 방법
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

UROPS 때 후처리에는 `integrated_analysis.py` (MDAnalysis 기반) 를 썼다. 이 스크립트는 공개하지 않았다.
밀도 프로파일과 첫 층 조성, 블록 평균은 [PPPM vs MSM 글](../../blog/2026/08/22/pppm-vs-msm-cu-benzene-ethanol/)의
`profiles.py`, `blocks.py` 로 덤프에서 다시 계산할 수 있다.
아래에 주요 분석 항목과 각 항목이 무엇을 알려 주는지 정리한다.

## 7.1 동경 분포 함수 (Radial Distribution Function, RDF)

### 정의

동경 분포 함수 $g(r)$ 은 기준 입자에서 거리 $r$ 만큼 떨어진 곳에 다른 입자가 있을 확률을
이상 기체(균일 분포)와 비교해 정규화한 양이다.

$$
g_{\alpha\beta}(r) = \frac{1}{\rho_\beta} \left\langle \sum_{i \in \alpha} \sum_{j \in \beta, j \neq i} \frac{\delta(r - r_{ij})}{4\pi r^2} \right\rangle
$$

### 분석하는 원자 쌍

| 페어 | 첫 피크 위치 (Å) | 해석 |
|------|------------------|-------------|
| Cu - 벤젠 C | 약 3.0-3.5 | 첫 흡착층 거리 (π-d 분산력) |
| Cu - 에탄올 O | 약 2.7-3.2 | 산소가 표면에 닿는 거리 |
| 벤젠 - 벤젠 (C-C) | 약 3.6-3.8 | π-π stacking 거리 |
| 에탄올 O - 에탄올 H | 약 1.8 (수소 결합) | 수산기 수소 결합 |
| 에탄올 O - 에탄올 O | 약 2.8 | 수산기 O-O 분리 |

벤젠-벤젠 stacking 거리 약 3.7 Å은 sandwich 또는 T-shape 배열에 해당한다.
벤젠 dimer의 ab initio 계산값이 3.4-3.9 Å (Sherrill 외) 이므로 OPLS-AA도 이 범위를 잘 맞춰야 한다.

### LAMMPS 내부 RDF 계산

RDF는 LAMMPS 안에서 바로 계산할 수도 있다.

```bash
compute rdf_cu_o all rdf 200 12 5 cutoff 12.0     # OPLS-AA: Cu(12)-O(5)
fix     rdf_save all ave/time 100 10 1000 c_rdf_cu_o[*] file rdf_cu_o.dat mode vector
```

`cutoff` 에 skin(2 Å)을 더한 값이 ghost 원자 범위(여기서는 `comm_modify cutoff 14.0`)를 넘으면
"Compute rdf cutoff plus skin 17 exceeds ghost atom range 14" 오류가 난다. 15 Å 까지 보려면 `comm_modify cutoff 17.0` 이 필요하다.
[LAMMPS compute rdf 문서](https://docs.lammps.org/compute_rdf.html) 참조.

다만 여기서는 더 유연한 외부 후처리(`integrated_analysis.py`)를 썼다.

## 7.2 밀도 프로파일 (z 방향)

### 정의

슬랩 시스템에서 가장 중요한 분석량은 z 방향(표면 수직)의 분자별 밀도 분포다.

$$
\rho_\alpha(z) = \frac{\langle N_\alpha(z, z + \Delta z) \rangle}{L_x L_y \Delta z} \cdot m_\alpha
$$

여기서 $m_\alpha$ 는 종 $\alpha$ 분자의 질량이다.

### 예상되는 프로파일 모양

| 영역 | 벤젠 밀도 | 에탄올 밀도 | 해석 |
|------|-----------|--------------|-------------|
| z < 0 (슬랩 내부) | 0 | 0 | 진공 또는 슬랩 |
| z = 슬랩 표면 ~ +5 Å | 큰 봉우리 | 작은 봉우리 | 1차 흡착층 |
| +5 Å ~ +10 Å | 작은 봉우리 | 봉우리 | 2차 층 |
| +10 Å 이상 | 일정값 (벌크) | 일정값 (벌크) | 액체상 |
| z > 박스 상한 | 0 | 0 | 진공 |

### LAMMPS 내부 밀도 프로파일 계산

```bash
compute     z_bins all chunk/atom bin/1d z lower 1.0 units box
fix         density_save all ave/chunk 100 10 1000 z_bins density/mass file density.dat
```

`bin/1d z lower 1.0 units box`: 박스 아래쪽부터 z 방향으로 1 Å 폭의 빈으로 나눈다.
[LAMMPS compute chunk/atom 문서](https://docs.lammps.org/compute_chunk_atom.html) 참조.

그룹별 밀도를 따로 보려면 group을 먼저 정의하고 chunk를 그 그룹에 적용한다.

```bash
compute     z_bins_benzene benzene chunk/atom bin/1d z lower 1.0 units box
fix         density_benzene benzene ave/chunk 100 10 1000 z_bins_benzene density/mass file density_benzene.dat
```

## 7.3 분리 효율 지수 (Separation Efficiency Index, SEI)

### 정의

SEI는 표면 1차 흡착층에서 두 분자 종이 얼마나 갈라져 있는지를 수치로 나타낸다.

$$
\text{SEI} = \frac{\left| x_{\text{benzene}}^{\text{surf}} - x_{\text{benzene}}^{\text{bulk}} \right|}{1 - x_{\text{benzene}}^{\text{bulk}}}
$$

여기서

- $x_{\text{benzene}}^{\text{surf}}$: 표면 1차 흡착층의 벤젠 분율
- $x_{\text{benzene}}^{\text{bulk}}$: 벌크 영역의 벤젠 분율

값은 다음처럼 읽는다.

- SEI = 0: 표면 조성 = 벌크 조성 (분리 없음, 완전 혼합)
- SEI = 1: 표면에 벤젠만 흡착 (완전 분리)

분모 $1 - x^\text{bulk}$ 로 나눠 벤젠이 표면을 다 차지했을 때 1 이 되게 맞춘 것이다.
절댓값이 있으므로 SEI 는 음수가 될 수 없고, 에탄올이 표면에 더 많은 경우에도 양수로 나온다.
방향을 보려면 절댓값 없이 $x^\text{surf} - x^\text{bulk}$ 를 같이 보고한다.

### 계산 방법

1. Cu 슬랩 맨 위의 z 좌표 $z_{\text{Cu,max}}$ 를 구한다.
2. 표면 영역: $z_{\text{Cu,max}} < z < z_{\text{Cu,max}} + 5$ Å.
3. 벌크 영역: $z > z_{\text{Cu,max}} + 10$ Å (또는 박스 위쪽의 일정 거리).
4. 각 영역에서 분자 종별 분자 수(또는 질량)를 평균한다.
5. 분율을 구하고 그 차이를 계산한다.

첫 층 분자가 20개 남짓이면 한두 개만 드나들어도 $x^\text{surf}$ 가 0.04 씩 움직인다.
UROPS OPLS-AA run 의 첫 층 벤젠 몰분율은 2 ns 동안 0.83 에서 0.57 까지 표류했으므로,
SEI 는 블록 평균과 그 표준오차를 함께 낸다(아래 7.7절).

## 7.4 흡착 에너지 (Adsorption Energy)

### 정의

분자 $\alpha$ 의 흡착 에너지는 다음과 같다.

$$
\Delta E_{\text{ads}}^\alpha = E_{\text{surf+mol}} - E_{\text{surf}} - E_{\text{mol}}
$$

여기서

- $E_{\text{surf+mol}}$: 분자가 표면에 흡착된 시스템의 에너지
- $E_{\text{surf}}$: 같은 표면만 있을 때의 에너지
- $E_{\text{mol}}$: 같은 분자가 진공(vacuum)에 홀로 있을 때의 에너지

### MD에서의 추정

흡착 에너지를 엄밀히 구하려면 thermodynamic integration 같은 별도 시뮬레이션이 필요하다.
여기서는 production 궤적에서 다음 양으로 근사했다.

$$
E_{\text{ads}}^\alpha \approx \langle E_{\text{Cu-}\alpha}^{\text{LJ+Coul}} \rangle_{\text{surf}} - \langle E_{\text{Cu-}\alpha}^{\text{LJ+Coul}} \rangle_{\text{far}}
$$

LAMMPS에서 group-group 상호작용 에너지는 이렇게 계산한다.

```bash
group benzene type 1 2
group copper  type 12

# 두 그룹 간 비결합 상호작용 에너지: compute ID 그룹1 group/group 그룹2
compute     cu_benzene copper group/group benzene kspace yes
thermo_style custom step temp c_cu_benzene
```

`compute ID group-ID group/group group2-ID` 형식이라 그룹 두 개를 나란히 쓰면 "Illegal compute group/group command" 오류가 난다.
`kspace yes` 는 PPPM/Ewald 에서만 되고 MSM 에서는 "Kspace style does not support compute group/group" 오류가 난다.
Cu 의 전하가 0 이면 Cu-분자 쌍에는 Coulomb 항이 없으므로 `kspace` 키워드를 빼도 값이 같다.
[LAMMPS compute group/group 문서](https://docs.lammps.org/compute_group_group.html) 참조.

표면 가까이 있는 벤젠(1차 흡착층)과 멀리 있는 벤젠(벌크)의 평균값을 비교하면
이 값을 흡착 에너지로 바꿀 수 있다. 결과는 분자 하나당으로 나눠 보고한다.

### UROPS 보고서의 흡착 에너지에 대해

UROPS 보고서는 벤젠 -0.27 ~ -0.32 eV, 에탄올 -0.19 ~ -0.21 eV 를 흡착 에너지로 냈다.
그런데 방법 절을 보면 이 값은 힘장에서 나온 것이 아니라 "최대 2.0 eV(벤젠), 1.5 eV(에탄올)인 지수형 거리 함수"에
분자의 높이를 넣어 계산한 것이다. 최댓값을 정해 둔 함수라 힘장이나 정전기 방법을 바꿔도 값이 크게 달라질 수 없고,
힘장 비교에 쓸 수 없다. 위의 `compute group/group` 으로 다시 재야 한다.
참고로 UROPS 입력의 Cu-유기 LJ ε 는 0.012–0.029 kcal/mol 로 매우 작아서([3장](03-force-fields)),
다시 재면 보고서가 인용한 실험값(벤젠/Cu(111) TPD, 약 0.7–0.9 eV)보다 훨씬 약하게 나올 가능성이 크다.

## 7.5 계면 장력 (Interfacial Tension): Irving-Kirkwood 방법

### 정의

계면 장력 $\gamma$ 는 응력 텐서(stress tensor)의 z 방향 성분과 가로 방향 성분의 차이로 구한다 (Irving & Kirkwood 1950).

$$
\gamma = \frac{1}{2} \int_{-\infty}^{+\infty} \left[ P_{zz}(z) - \frac{P_{xx}(z) + P_{yy}(z)}{2} \right] dz
$$

여기서 $P_{xx}, P_{yy}, P_{zz}$ 는 각 위치의 압력 텐서 성분이다.
$1/2$ 계수는 자유 액체막처럼 같은 계면이 위아래로 두 개 있을 때 계면 하나당 장력으로 나누는 것이다.
이 계는 아래가 Cu-액체, 위가 액체-벽이라 두 계면이 다르다. 그래서 적분 전체를 반으로 나눈 값은 어느 계면의 장력도 아니고,
적분 구간을 계면 하나만 포함하도록 잘라야 한다. 고정된 Cu 와 벽이 주는 힘도 응력에 들어가므로 해석이 더 까다롭다.

### LAMMPS에서 응력 텐서 계산

```bash
compute   stress_atom all stress/atom NULL pair bond angle dihedral improper kspace fix
compute   z_bins all chunk/atom bin/1d z lower 1.0 units box
compute   stress_sum all reduce/chunk z_bins sum c_stress_atom[1] c_stress_atom[2] c_stress_atom[3]
fix       stress_save all ave/time 100 10 1000 c_stress_sum[*] file stress_profile.dat mode vector
```

`stress/atom` 의 값은 원자별 (압력 × 부피) 이고 부호는 압력의 반대다. 빈 $k$ 의 압력 성분은
$P_{\alpha\alpha}(z_k) = -\sum_{i \in k} s_{i,\alpha\alpha} / (L_x L_y \Delta z)$ 로 후처리에서 계산한다.
`fix ave/chunk` 는 빈 안의 원자 평균을 내므로 여기서는 합을 주는 `reduce/chunk` 를 쓴다.
PPPM 슬랩 보정과 MSM 모두 `kspace` 원자별 virial 을 낸다(MSM 은 `pressure/scalar no` 일 때).
[LAMMPS compute stress/atom 문서](https://docs.lammps.org/compute_stress_atom.html) 참조.

### 단위 변환

LAMMPS `real` 단위에서 압력은 atm, 길이는 Å 이므로 $\gamma$ 는 atm·Å 로 나온다.
1 atm·Å = 101325 Pa × 10⁻¹⁰ m = 1.01325 × 10⁻⁵ N/m 이므로

$$
\gamma\,[\text{mJ/m}^2] = \gamma\,[\text{atm·Å}] \times 1.01325 \times 10^{-2}
$$

`metal` 단위(압력 bar)라면 1 bar·Å = 10⁻⁵ N/m = 0.01 mJ/m² 이다.

### 이 시스템에서 예상되는 값

| 계면 종류 | 표면 장력 (mJ/m²) | 비고 |
|-----------|---------------------|------|
| 액체 벤젠 - 증기 (25 °C) | 28.2 | 실험값 |
| 액체 에탄올 - 증기 (25 °C) | 22.0 | 실험값 |

Cu-액체 계면 장력은 이 계에서 아직 재지 않았다. 힘장의 표면 장력을 먼저 검증하려면
벤젠, 에탄올 각각의 자유 액체막(위아래 진공)을 돌려 위 실험값과 비교하는 것이 순서다.

## 7.6 통합 분석 스크립트 사용법

`integrated_analysis.py` 하나로 위의 분석을 모두 돌린다.

```bash
# Production 단계 분석
python integrated_analysis.py \
    --topology trappe.data \
    --trajectories 05_production.lammpstrj \
    --stages production \
    --log lammps_run.log \
    --output analysis_trappe_msm
```

```bash
# 다단계 분석 (heating, equilibration, production 모두)
python integrated_analysis.py \
    --topology trappe.data \
    --trajectories 03_heat.lammpstrj 04_eq.lammpstrj 05_production.lammpstrj \
    --stages heating equilibration production \
    --log lammps_run.log \
    --output analysis_trappe_msm
```

스크립트는 원자 수를 보고 힘장(OPLS-AA vs TraPPE-UA)을 알아서 판별하고,
RDF, 밀도 프로파일, SEI, 흡착 에너지를 모두 계산해 PNG와 DAT 파일로 저장한다.
다만 여기서 나오는 흡착 에너지는 7.4절에 적은 지수형 모형 값이라 쓰지 않는다.

## 7.7 분석 결과의 통계적 신뢰성

분석값을 믿으려면 다음을 확인한다.

1. 자기 상관 시간: $\tau_A$ 가 production 시간보다 충분히 짧아야 한다.
   (Allen & Tildesley 2017, Frenkel & Smit 2002)
2. 블록 평균(Block average): production 을 5-10 개 블록으로 나눠 블록 사이의 분산을 계산한다.
3. 수렴 그래프: 누적 평균이 시간에 따라 수렴하는지 그려 본다.

논문 심사에서도 이런 신뢰성 분석을 흔히 요구한다.

## 참고문헌

1. J. H. Irving, J. G. Kirkwood,
   "The Statistical Mechanical Theory of Transport Processes. IV.",
   *J. Chem. Phys.* **18**, 817-829 (1950).
   DOI: [10.1063/1.1747782](https://doi.org/10.1063/1.1747782)

2. N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, O. Beckstein,
   "MDAnalysis: A toolkit for the analysis of molecular dynamics simulations",
   *J. Comput. Chem.* **32**, 2319-2327 (2011).
   DOI: [10.1002/jcc.21787](https://doi.org/10.1002/jcc.21787)

3. M. P. Allen, D. J. Tildesley,
   "Computer Simulation of Liquids", 2nd ed., Oxford University Press (2017).
   ISBN: 9780198803195.

4. D. Frenkel, B. Smit,
   "Understanding Molecular Simulation", 2nd ed., Academic Press (2002).
   ISBN: 9780122673511.

5. LAMMPS 공식 문서, `compute rdf`:
   [https://docs.lammps.org/compute_rdf.html](https://docs.lammps.org/compute_rdf.html)

6. LAMMPS 공식 문서, `compute chunk/atom`:
   [https://docs.lammps.org/compute_chunk_atom.html](https://docs.lammps.org/compute_chunk_atom.html)

7. LAMMPS 공식 문서, `compute stress/atom`:
   [https://docs.lammps.org/compute_stress_atom.html](https://docs.lammps.org/compute_stress_atom.html)

8. LAMMPS 공식 문서, `compute group/group`:
   [https://docs.lammps.org/compute_group_group.html](https://docs.lammps.org/compute_group_group.html)
