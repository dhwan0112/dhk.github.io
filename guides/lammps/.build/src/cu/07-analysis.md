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

본 가이드는 시뮬레이션 후처리에 `integrated_analysis.py` (MDAnalysis 기반) 를 사용한다.
주요 분석 항목과 각각의 화학적 의미를 정리한다.

## 7.1 방사 분포 함수 (Radial Distribution Function, RDF)

### 정의

방사 분포 함수 $g(r)$ 은 임의의 기준 입자에서 거리 $r$ 에 다른 입자가 발견될 확률을
이상 기체 (균일 분포) 와 비교하여 정규화한 양이다.

$$
g_{\alpha\beta}(r) = \frac{1}{\rho_\beta} \left\langle \sum_{i \in \alpha} \sum_{j \in \beta, j \neq i} \frac{\delta(r - r_{ij})}{4\pi r^2} \right\rangle
$$

### 분석 페어와 화학적 의미

| 페어 | 첫 피크 위치 (Å) | 화학적 의미 |
|------|------------------|-------------|
| Cu - 벤젠 C | 약 3.0-3.5 | 첫 흡착층 거리 (π-d 분산력) |
| Cu - 에탄올 O | 약 2.7-3.2 | 산소가 표면에 닿는 거리 |
| 벤젠 - 벤젠 (C-C) | 약 3.6-3.8 | π-π stacking 거리 |
| 에탄올 O - 에탄올 H | 약 1.8 (수소 결합) | 수산기 수소 결합 |
| 에탄올 O - 에탄올 O | 약 2.8 | 수산기 O-O 분리 |

벤젠-벤젠 stacking 거리 약 3.7 Å은 sandwich 또는 T-shape 배열에 해당한다.
벤젠 dimer의 ab initio 계산값은 3.4-3.9 Å (Sherrill 외) 이므로 OPLS-AA 결과는 좋은 예측을 보여야 한다.

### LAMMPS 내부 RDF 계산

LAMMPS에서 직접 RDF를 계산할 수도 있다.

```bash
compute rdf_cu_o all rdf 200 12 5 cutoff 15.0     # OPLS-AA: Cu(12)-O(5)
fix     rdf_save all ave/time 100 10 1000 c_rdf_cu_o[*] file rdf_cu_o.dat mode vector
```

[LAMMPS compute rdf 문서](https://docs.lammps.org/compute_rdf.html) 참조.

다만 본 가이드는 외부 후처리 (`integrated_analysis.py`) 가 더 유연하므로 그쪽을 권장한다.

## 7.2 밀도 프로파일 (z 방향)

### 정의

z 방향 (표면 수직) 의 분자별 밀도 분포는 슬랩 시스템에서 가장 중요한 분석량이다.

$$
\rho_\alpha(z) = \frac{\langle N_\alpha(z, z + \Delta z) \rangle}{L_x L_y \Delta z} \cdot m_\alpha
$$

여기서 $m_\alpha$ 는 종 $\alpha$ 분자의 질량이다.

### 예상되는 프로파일 형태

| 영역 | 벤젠 밀도 | 에탄올 밀도 | 화학적 의미 |
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

`bin/1d z lower 1.0 units box`: z 방향으로 박스 하단부터 1 Å 폭의 빈으로 분할.
[LAMMPS compute chunk/atom 문서](https://docs.lammps.org/compute_chunk_atom.html) 참조.

그룹별 밀도를 분리하려면 group을 먼저 정의한 뒤 chunk를 그룹에 적용한다.

```bash
compute     z_bins_benzene benzene chunk/atom bin/1d z lower 1.0 units box
fix         density_benzene benzene ave/chunk 100 10 1000 z_bins_benzene density/mass file density_benzene.dat
```

## 7.3 분리 효율 지수 (Separation Efficiency Index, SEI)

### 정의

SEI는 표면 1차 흡착층에서 두 분자 종의 분리 정도를 정량화한다.

$$
\text{SEI} = \left| x_{\text{benzene}}^{\text{surf}} - x_{\text{benzene}}^{\text{bulk}} \right|
$$

여기서

- $x_{\text{benzene}}^{\text{surf}}$: 표면 1차 흡착층에서의 벤젠 분율
- $x_{\text{benzene}}^{\text{bulk}}$: 벌크 영역에서의 벤젠 분율

값의 의미:

- **SEI = 0**: 표면 조성 = 벌크 조성 (분리 없음, 완전 혼합)
- **SEI = 1**: 표면이 한 종만 흡착 (완전 분리)

### 계산 방법

1. Cu 슬랩의 가장 상단 z 좌표 $z_{\text{Cu,max}}$ 결정.
2. 표면 영역 정의: $z_{\text{Cu,max}} < z < z_{\text{Cu,max}} + 5$ Å.
3. 벌크 영역 정의: $z > z_{\text{Cu,max}} + 10$ Å (또는 박스 상부 일정 거리).
4. 각 영역에서 각 분자의 분자 수 (또는 질량) 평균.
5. 분율 계산 및 차이 계산.

본 가이드의 사용자는 TraPPE-UA + MSM에서 SEI = 0.93-1.00 을 보고하였다.
이는 벤젠이 표면을 거의 완전히 점유한다는 것을 의미한다.

## 7.4 흡착 에너지 (Adsorption Energy)

### 정의

분자 $\alpha$ 의 흡착 에너지는 다음과 같다.

$$
\Delta E_{\text{ads}}^\alpha = E_{\text{surf+mol}} - E_{\text{surf}} - E_{\text{mol}}
$$

여기서

- $E_{\text{surf+mol}}$: 표면에 흡착된 분자가 있는 시스템의 에너지
- $E_{\text{surf}}$: 같은 표면만의 에너지
- $E_{\text{mol}}$: 같은 분자가 자유롭게 (vacuum) 있는 에너지

### MD에서의 추정

엄밀한 흡착 에너지 계산은 thermodynamic integration 등 별도 시뮬레이션이 필요하지만,
본 가이드의 production 궤적에서는 다음 양으로 근사할 수 있다.

$$
E_{\text{ads}}^\alpha \approx \langle E_{\text{Cu-}\alpha}^{\text{LJ+Coul}} \rangle_{\text{surf}} - \langle E_{\text{Cu-}\alpha}^{\text{LJ+Coul}} \rangle_{\text{far}}
$$

LAMMPS에서 group-group 상호작용 에너지를 계산:

```bash
group benzene type 1 2
group copper  type 12

# 두 그룹 간 비결합 상호작용 에너지 계산
compute     cu_benzene all group/group benzene copper kspace yes
thermo_style custom step temp c_cu_benzene
```

[LAMMPS compute group/group 문서](https://docs.lammps.org/compute_group_group.html) 참조.

이 값은 표면에 가까운 벤젠 (1차 흡착층) 과 멀리 있는 벤젠 (벌크) 의 평균을 비교하여
흡착 에너지로 변환할 수 있다.

### 본 시스템에서의 예상 값

| 분자 | 흡착 에너지 (eV) | 흡착 에너지 (kJ/mol) | 화학적 특징 |
|------|-------------------|----------------------|-------------|
| 벤젠 | -0.27 ~ -0.32 | -26 ~ -31 | π-d 분산 (강) |
| 에탄올 | -0.15 ~ -0.25 | -14 ~ -24 | 산소 + 수소 결합 (중간) |

이는 Heinz et al. (2008) 의 LJ 파라미터가 표면 장력 및 단순 분자 흡착에 fit 되었다는 점,
그리고 사용자의 사전 결과와 일치한다.

## 7.5 계면 장력 (Interfacial Tension) — Irving-Kirkwood 방법

### 정의

계면 장력 $\gamma$ 는 시스템의 응력 텐서 (stress tensor) 의 z 방향 성분과 횡방향 성분의 차이로 계산된다 (Irving & Kirkwood 1950).

$$
\gamma = \frac{1}{2} \int_{-\infty}^{+\infty} \left[ P_{zz}(z) - \frac{P_{xx}(z) + P_{yy}(z)}{2} \right] dz
$$

여기서 $P_{xx}, P_{yy}, P_{zz}$ 는 각 위치에서의 압력 텐서 성분이다.
$1/2$ 계수는 슬랩에 두 개의 계면 (위/아래) 이 있기 때문에 한 계면당 장력으로 나누는 것이다.

### LAMMPS에서 응력 텐서 계산

```bash
compute   stress_atom all stress/atom NULL pair kspace bond angle dihedral improper
compute   z_bins all chunk/atom bin/1d z lower 1.0 units box
fix       stress_save all ave/chunk 100 10 1000 z_bins &
          v_stress_xx v_stress_yy v_stress_zz file stress_profile.dat

variable  stress_xx atom -c_stress_atom[1]/vol
variable  stress_yy atom -c_stress_atom[2]/vol
variable  stress_zz atom -c_stress_atom[3]/vol
```

`stress/atom` 의 부호는 응력 (tension positive) 이고, 압력은 음의 응력이므로 변환 시 부호 주의.
[LAMMPS compute stress/atom 문서](https://docs.lammps.org/compute_stress_atom.html) 참조.

### 단위 변환

LAMMPS `real` 단위에서 응력은 bar·Å (또는 atm·Å³의 부피당) 으로 나타난다.
계면 장력 SI 단위 (mJ/m² = mN/m) 로 변환:

$$
\gamma [\text{mJ/m}^2] = \gamma [\text{atm·Å}] \times 1.01325 \times 10^{-1}
$$

또는 더 일반적으로:

$$
1 \text{ bar·Å} = 0.1 \text{ mJ/m}^2
$$

### 본 시스템에서의 예상 값

| 계면 종류 | 계면 장력 (mJ/m²) | 비고 |
|-----------|---------------------|------|
| 액체 벤젠 - 진공 (300 K) | ~28 | 실험값 |
| 액체 에탄올 - 진공 (300 K) | ~22 | 실험값 |
| Cu 표면 - 벤젠 (시뮬레이션) | 음의 값 가능 | 강한 흡착 |
| Cu 표면 - 에탄올 (시뮬레이션) | 중간 값 | |
| 벤젠/에탄올 혼합 - Cu (시뮬레이션) | 25-30 | OPLS-AA |
|  | 22-27 | TraPPE-UA |

## 7.6 통합 분석 스크립트 사용법

본 프로젝트의 `integrated_analysis.py` 는 위의 모든 분석을 한 번에 수행한다.

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

스크립트는 힘장 (OPLS-AA vs TraPPE-UA) 을 원자 수로 자동 감지하며,
RDF, 밀도 프로파일, SEI, 흡착 에너지를 모두 계산하여 PNG 및 DAT 파일로 저장한다.

## 7.7 분석 결과의 통계적 신뢰성

각 분석량의 신뢰성을 보장하려면 다음을 점검해야 한다.

1. **자기 상관 시간 확인**: $\tau_A$ 가 production 시간보다 충분히 짧아야 함.
   (Allen & Tildesley 2017, Frenkel & Smit 2002)
2. **블록 평균 (Block average) 방법**: production 을 5-10 개 블록으로 나누어 블록 간 분산 계산.
3. **수렴 그래프 표시**: 누적 평균값이 시간에 따라 수렴하는지 시각화.

이러한 신뢰성 분석은 출판 시 평가자가 요구하는 표준 절차이다.

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

---

[← 이전: 6. 4가지 프레임워크 비교](06-frameworks) ｜ [다음: 8. 트러블슈팅 →](08-troubleshooting)
