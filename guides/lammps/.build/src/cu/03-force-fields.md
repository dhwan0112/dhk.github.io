---
layout: default
title: "3. 힘장 비교: OPLS-AA vs TraPPE-UA"
nav_order: 4
---

# 3. 힘장 비교: OPLS-AA vs TraPPE-UA
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 3.1 두 힘장의 철학적 차이

| 항목 | OPLS-AA | TraPPE-UA |
|------|---------|-----------|
| 풀네임 | Optimized Potentials for Liquid Simulations - All-Atom | Transferable Potentials for Phase Equilibria - United Atom |
| 원전 | Jorgensen, Maxwell, Tirado-Rives (1996) | Martin & Siepmann (1998), Chen et al. (2001) |
| 적합 (fit) 데이터 | 액체상 밀도, 기화열, 토션 에너지 프로파일 | 기-액 상 평형 (vapor-liquid coexistence) |
| 적합 방법 | Monte Carlo 시뮬레이션 + ab initio (RHF/6-31G*) | Gibbs-ensemble Monte Carlo |
| 표현 정확도 | 미세한 형태론적 차이 가능 (수소 결합 협동성 등) | 거시 상태 함수에 최적화 |

OPLS-AA는 단량체의 형태 (conformation) 와 분자 내 상호작용을 자세히 모형화하므로,
수소 결합 네트워크의 협동성 (cooperativity) 과 같은 미세 효과를 더 정확히 포착할 수 있다.
반면 TraPPE-UA는 수소를 음으로 다루지 않으므로 계산이 빠르고, 상 평형과 같은
거시 열역학량의 예측에 강하다.

## 3.2 함수형 (Functional form)

두 힘장 모두 다음과 같은 동일한 표준 함수형을 사용한다.

$$
U = \underbrace{\sum_{\text{bonds}} K_b (r - r_0)^2}_{\text{결합}} + \underbrace{\sum_{\text{angles}} K_\theta (\theta - \theta_0)^2}_{\text{각도}} + \underbrace{\sum_{\text{dihedrals}} \sum_{n=1}^{4} \frac{V_n}{2} [1 + (-1)^{n+1} \cos(n\phi)]}_{\text{이면각 (OPLS)}}
+ U_{\text{nb}}
$$

비결합 (non-bonded) 항은 다음과 같다.

$$
U_{\text{nb}} = \sum_{i<j} \left[ 4\varepsilon_{ij}\left(\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{12} - \left(\frac{\sigma_{ij}}{r_{ij}}\right)^6\right) + \frac{q_i q_j}{4\pi\varepsilon_0 r_{ij}} \right]
$$

### 1-4 비결합 스케일링

같은 분자 내 1-4 떨어진 원자 쌍의 비결합 상호작용은 부분적으로 스케일링된다.

- **OPLS-AA**: LJ × 0.5, Coulomb × 0.5 (Jorgensen 외 1996의 표준)
- **TraPPE-UA**: LJ × 0 (완전 제외), Coulomb × 0 (TraPPE 표준)

LAMMPS에서는 다음 명령어로 설정한다.

```bash
# OPLS-AA
special_bonds lj/coul 0.0 0.0 0.5

# TraPPE-UA
special_bonds lj/coul 0.0 0.0 0.0
```

### LJ 혼합 규칙 (Mixing rule)

서로 다른 원자 타입 간 LJ 파라미터 결합:

- **OPLS-AA**: 기하 평균 (geometric mean) — $\sigma_{ij} = \sqrt{\sigma_i \sigma_j}$, $\varepsilon_{ij} = \sqrt{\varepsilon_i \varepsilon_j}$
- **TraPPE-UA**: Lorentz-Berthelot — $\sigma_{ij} = (\sigma_i + \sigma_j)/2$, $\varepsilon_{ij} = \sqrt{\varepsilon_i \varepsilon_j}$

LAMMPS에서는 다음 명령어로 설정한다.

```bash
# OPLS-AA
pair_modify mix geometric

# TraPPE-UA
pair_modify mix arithmetic
```

## 3.3 LAMMPS pair_style 설정

본 시스템은 유기 분자 (LJ + Coulomb) 와 Cu 슬랩 (EAM) 을 모두 포함하므로
`pair_style hybrid`를 사용한다. EAM은 전통적인 fcc 금속 모형화에 적합하나,
본 가이드는 Heinz et al. (2008) 의 12-6 LJ 파라미터를 채택하여 Cu 슬랩도 LJ로 통일한다.
이렇게 하면 hybrid의 복잡성을 피하고, Cu-유기 분자 간 cross 항을 명확하게 정의할 수 있다.

### 권장 pair_style (PPPM 사용 시)

```bash
units real
atom_style full

pair_style lj/cut/coul/long 12.0
pair_modify mix geometric tail no   # 슬랩에서는 tail correction 사용 금지
kspace_style pppm 1.0e-4
```

`tail no`인 이유: tail correction은 균일한 밀도를 가정하므로 슬랩 시스템에는 부정확하다.
[LAMMPS pair_modify 문서](https://docs.lammps.org/pair_modify.html) 참조.

### 권장 pair_style (MSM 사용 시)

```bash
pair_style lj/cut/coul/long 12.0
pair_modify mix geometric tail no
kspace_style msm 1.0e-4
```

`lj/cut/coul/long`은 MSM과도 호환된다 ([LAMMPS pair_lj_cut_coul 문서](https://docs.lammps.org/pair_lj_cut_coul.html)).
또는 `lj/cut/coul/msm`을 사용할 수도 있다.

## 3.4 OPLS-AA 결합 항 설정

OPLS-AA의 결합 항은 모두 조화 진동자 (harmonic) 형태이다.

```bash
bond_style harmonic
angle_style harmonic
dihedral_style opls       # OPLS 4-cosine 형태
improper_style harmonic   # 평면성 부과 (벤젠 등)
```

`dihedral_style opls`는 다음 형태를 따른다.

$$
U_\phi = \frac{V_1}{2}(1 + \cos\phi) + \frac{V_2}{2}(1 - \cos 2\phi) + \frac{V_3}{2}(1 + \cos 3\phi) + \frac{V_4}{2}(1 - \cos 4\phi)
$$

[LAMMPS dihedral_opls 문서](https://docs.lammps.org/dihedral_opls.html) 참조.

### OPLS-AA 벤젠 파라미터 (요약)

| 결합/각도 | 값 |
|-----------|-----|
| C-C 결합 ($K_b$, $r_0$) | 469 kcal/mol·Å², 1.400 Å |
| C-H 결합 ($K_b$, $r_0$) | 367 kcal/mol·Å², 1.080 Å |
| C-C-C 각도 ($K_\theta$, $\theta_0$) | 63.0 kcal/mol·rad², 120° |
| C-C-H 각도 ($K_\theta$, $\theta_0$) | 35.0 kcal/mol·rad², 120° |
| C-C-C-C 이면각 (V₂) | 7.250 kcal/mol (V_1 = V_3 = V_4 = 0) |

### OPLS-AA 에탄올 LJ 파라미터 (Jorgensen 외 1996, Table 4)

| 원자 | ε (kcal/mol) | σ (Å) |
|------|--------------|--------|
| HO (수산기 H) | 0.000 | 0.000 |
| OH (수산기 O) | 0.170 | 3.120 |
| CH₂-OH의 C (α-C) | 0.066 | 3.500 |
| CH₃의 C | 0.066 | 3.500 |
| 지방족 H | 0.030 | 2.500 |

## 3.5 TraPPE-UA 결합 항 설정

TraPPE-UA에서는 결합 길이가 일반적으로 rigid로 고정되거나 (Monte Carlo 원본),
MD로 사용 시 매우 강한 조화 진동자로 대체된다.

```bash
bond_style harmonic
angle_style harmonic
dihedral_style harmonic   # TraPPE는 OPLS의 4-cosine을 쓰지 않음
```

대안으로 결합 길이를 SHAKE 알고리즘으로 고정할 수 있다.

```bash
# 결합 타입 1, 2, 3, 4를 모두 SHAKE로 고정 (예시)
fix shake_bonds all shake 1.0e-4 20 0 b 1 2 3 4
```

### TraPPE-UA 에탄올 LJ 파라미터 (Chen 외 2001, Table 1)

| 사이트 | ε/k_B (K) | σ (Å) | q (e) |
|--------|------------|--------|-------|
| CH₃ (메틸) | 98.0 | 3.75 | 0.000 |
| CH₂ (메틸렌, α-C) | 46.0 | 3.95 | +0.265 |
| O (수산기 산소) | 93.0 | 3.02 | -0.700 |
| H (수산기 수소) | 0.0 | 0.000 | +0.435 |

ε/k_B 값을 kcal/mol로 변환할 때: ε [kcal/mol] = ε/k_B [K] × 1.987 × 10⁻³.
예: CH₃의 ε = 98.0 × 1.987e-3 = 0.1948 kcal/mol.

### TraPPE-UA 벤젠 파라미터 (UA 6-site, ε/k_B = 50.5 K, σ = 3.695 Å)

본 시스템에서 사용된 벤젠 UA 표현의 파라미터는 일반적인 aromatic CH의 값을 따른다
(예: Wick et al. 2000, J. Phys. Chem. B 104, 8008-8016, DOI: 10.1021/jp001044x 참고).
공식 TraPPE-EH 벤젠 (Rai & Siepmann 2007) 과는 다르므로,
연구 출판 시 정확한 파라미터 출처를 명시해야 한다.

## 3.6 Cu 슬랩 파라미터 (Heinz 외 2008)

본 가이드는 Heinz et al. (2008) 의 12-6 INTERFACE-FF Cu LJ 파라미터를 사용한다.

| 원자 | ε (kcal/mol) | σ (Å) |
|------|--------------|--------|
| Cu | 4.72 | 2.616 |

이 값들은 fcc Cu의 격자 상수, 표면 장력, 표면 에너지에 동시에 fit된 결과이다.
EAM 포텐셜보다 단순하지만, 유기 분자와의 cross-term을 표준 LJ 혼합 규칙으로 정의할 수 있어
INTERFACE 힘장과 자연스럽게 통합된다.

LAMMPS 명령어:

```bash
# OPLS-AA 시스템에서 Cu는 type 12
pair_coeff 12 12 4.72 2.616
```

```bash
# TraPPE-UA 시스템에서 Cu는 type 6
pair_coeff 6 6 4.72 2.616
```

## 3.7 힘장 선택 기준 — 화학적 가이드

| 연구 목적 | 권장 힘장 |
|-----------|-----------|
| 수소 결합 네트워크의 미세 구조 분석 | OPLS-AA (수소 명시) |
| 표면 위 분자 배향 (orientation) 의 자세한 분석 | OPLS-AA |
| 대규모 시스템에서 상 평형 (액-액, 기-액) | TraPPE-UA |
| 계산 비용이 제약 요인일 때 | TraPPE-UA |
| 분리 효율 지수 (SEI) 의 빠른 스크리닝 | TraPPE-UA |
| 흡착 에너지의 정량적 검증 | OPLS-AA 권장, TraPPE-UA로 확인 |

본 가이드의 4가지 프레임워크 비교는 두 힘장이 동일 시스템에서 어떻게 다른 예측을 내놓는지
체계적으로 평가하는 것이 목표이다.

## 참고문헌

1. W. L. Jorgensen, D. S. Maxwell, J. Tirado-Rives,
   "Development and Testing of the OPLS All-Atom Force Field on Conformational
   Energetics and Properties of Organic Liquids",
   *J. Am. Chem. Soc.* **118**, 11225-11236 (1996).
   DOI: [10.1021/ja9621760](https://doi.org/10.1021/ja9621760)

2. M. G. Martin, J. I. Siepmann,
   "Transferable Potentials for Phase Equilibria. 1. United-Atom Description of n-Alkanes",
   *J. Phys. Chem. B* **102**, 2569-2577 (1998).
   DOI: [10.1021/jp972543+](https://doi.org/10.1021/jp972543+)

3. B. Chen, J. J. Potoff, J. I. Siepmann,
   "Monte Carlo Calculations for Alcohols and Their Mixtures with Alkanes.
   Transferable Potentials for Phase Equilibria. 5.",
   *J. Phys. Chem. B* **105**, 3093-3104 (2001).
   DOI: [10.1021/jp003882x](https://doi.org/10.1021/jp003882x)

4. C. D. Wick, M. G. Martin, J. I. Siepmann,
   "Transferable Potentials for Phase Equilibria. 4. United-Atom Description of
   Linear and Branched Alkenes and Alkylbenzenes",
   *J. Phys. Chem. B* **104**, 8008-8016 (2000).
   DOI: [10.1021/jp001044x](https://doi.org/10.1021/jp001044x)

5. N. Rai, J. I. Siepmann,
   "Transferable Potentials for Phase Equilibria. 9. Explicit Hydrogen Description
   of Benzene and Five-Membered and Six-Membered Heterocyclic Aromatic Compounds",
   *J. Phys. Chem. B* **111**, 10790-10799 (2007).
   DOI: [10.1021/jp073586l](https://doi.org/10.1021/jp073586l)

6. H. Heinz, R. A. Vaia, B. L. Farmer, R. R. Naik,
   "Accurate Simulation of Surfaces and Interfaces of Face-Centered Cubic Metals
   Using 12-6 and 9-6 Lennard-Jones Potentials",
   *J. Phys. Chem. C* **112**, 17281-17290 (2008).
   DOI: [10.1021/jp801931d](https://doi.org/10.1021/jp801931d)

7. LAMMPS 공식 문서, `pair_modify`:
   [https://docs.lammps.org/pair_modify.html](https://docs.lammps.org/pair_modify.html)

8. LAMMPS 공식 문서, `dihedral_opls`:
   [https://docs.lammps.org/dihedral_opls.html](https://docs.lammps.org/dihedral_opls.html)

---

[← 이전: 2. 데이터 파일 구조](02-data-files) ｜ [다음: 4. 정전기 방법 →](04-electrostatics)
