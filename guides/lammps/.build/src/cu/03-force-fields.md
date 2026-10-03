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

## 3.1 두 힘장의 설계 차이

| 항목 | OPLS-AA | TraPPE-UA |
|------|---------|-----------|
| 풀네임 | Optimized Potentials for Liquid Simulations - All-Atom | Transferable Potentials for Phase Equilibria - United Atom |
| 원전 | Jorgensen, Maxwell, Tirado-Rives (1996) | Martin & Siepmann (1998), Chen et al. (2001) |
| 적합 (fit) 데이터 | 액체상 밀도, 기화열, 토션 에너지 프로파일 | 기-액 상 평형 (vapor-liquid coexistence) |
| 적합 방법 | Monte Carlo 시뮬레이션 + ab initio (RHF/6-31G*) | Gibbs-ensemble Monte Carlo |
| 표현 정확도 | 미세한 형태론적 차이 가능 (수소 결합 협동성 등) | 거시 상태 함수에 최적화 |

OPLS-AA는 단량체의 형태(conformation)와 분자 내 상호작용을 자세히 모형화하므로
수소 결합 네트워크의 협동성(cooperativity) 같은 미세한 효과를 더 정확히 잡아낸다.
TraPPE-UA는 수소를 따로 다루지 않아 계산이 빠르고, 상 평형 같은
거시 열역학량을 잘 예측한다.

## 3.2 함수형 (Functional form)

두 힘장은 다음과 같은 함수형을 공유한다.

$$
U = \underbrace{\sum_{\text{bonds}} K_b (r - r_0)^2}_{\text{결합}} + \underbrace{\sum_{\text{angles}} K_\theta (\theta - \theta_0)^2}_{\text{각도}} + \underbrace{\sum_{\text{dihedrals}} \sum_{n=1}^{4} \frac{V_n}{2} [1 + (-1)^{n+1} \cos(n\phi)]}_{\text{이면각 (OPLS)}}
+ U_{\text{nb}}
$$

비결합 (non-bonded) 항은 다음과 같다.

$$
U_{\text{nb}} = \sum_{i<j} \left[ 4\varepsilon_{ij}\left(\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{12} - \left(\frac{\sigma_{ij}}{r_{ij}}\right)^6\right) + \frac{q_i q_j}{4\pi\varepsilon_0 r_{ij}} \right]
$$

### 1-4 비결합 스케일링

같은 분자 안에서 1-4 관계인 원자 쌍의 비결합 상호작용은 일부만 반영한다.

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

서로 다른 원자 타입 사이의 LJ 파라미터는 다음 규칙으로 만든다.

- **OPLS-AA**: 기하 평균 (geometric mean), $\sigma_{ij} = \sqrt{\sigma_i \sigma_j}$, $\varepsilon_{ij} = \sqrt{\varepsilon_i \varepsilon_j}$
- **TraPPE-UA**: Lorentz-Berthelot, $\sigma_{ij} = (\sigma_i + \sigma_j)/2$, $\varepsilon_{ij} = \sqrt{\varepsilon_i \varepsilon_j}$

LAMMPS에서는 다음 명령어로 설정한다.

```bash
# OPLS-AA
pair_modify mix geometric

# TraPPE-UA
pair_modify mix arithmetic
```

## 3.3 LAMMPS pair_style 설정

이 시스템에는 유기 분자(LJ + Coulomb)와 Cu 슬랩이 함께 있다. 설정 방법은 두 가지다.

- **UROPS run 의 방식**: `pair_style hybrid eam/alloy lj/cut/coul/long 14.0`.
  Cu-Cu 는 EAM (`Cu_mishin1.eam.alloy`), 유기-유기와 Cu-유기는 LJ + Coulomb 이다.
  Cu-유기 쌍은 `pair_coeff i 12 lj/cut/coul/long ε σ` 로 하나씩 직접 줬다.
- **이 가이드의 `inputs/` 방식**: Cu 를 전부 고정하므로 Cu-Cu 상호작용은 궤적에 영향이 없다.
  그래서 `lj/cut/coul/long` 하나로 쓰고 `neigh_modify exclude type 12 12` 로 Cu-Cu 쌍을 뺐다.
  EAM 파일이 필요 없고, Cu-유기 쌍은 UROPS run 과 같은 값을 쓴다.

Cu 를 움직이게 하려면(가열, 응력 계산 등) Cu-Cu 에는 EAM 이 필요하다.
LJ 하나로 Cu-Cu 를 기술하면 fcc 금속의 탄성과 표면 이완이 맞지 않는다.

### pair_style 설정 (PPPM 사용 시)

```bash
units real
atom_style full

pair_style lj/cut/coul/long 12.0
pair_modify mix geometric tail no   # 슬랩에서는 tail correction 사용 금지
kspace_style pppm 1.0e-4
```

`tail no` 로 두는 이유는, tail correction이 균일한 밀도를 가정해서 슬랩 시스템에서는 틀린 값을 주기 때문이다.
[LAMMPS pair_modify 문서](https://docs.lammps.org/pair_modify.html) 참조.

### pair_style 설정 (MSM 사용 시)

```bash
pair_style lj/cut/coul/msm 12.0
pair_modify mix geometric tail no
kspace_style msm 1.0e-4
```

MSM 은 실공간 항도 MSM 의 분할 함수로 계산해야 하므로 `coul/msm` 변종을 쓴다.
`lj/cut/coul/long` 과 `kspace_style msm` 을 함께 쓰면 LAMMPS 가
"KSpace style is incompatible with Pair style" 오류를 낸다
([LAMMPS pair_lj_cut_coul 문서](https://docs.lammps.org/pair_lj_cut_coul.html)).

## 3.4 OPLS-AA 결합 항 설정

OPLS-AA의 결합 항은 모두 조화 진동자(harmonic) 형태다.

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

| 결합/각도 | 표준값 | UROPS 입력 |
|-----------|-----|-----|
| C-C 결합 ($K_b$, $r_0$) | 469 kcal/mol·Å², 1.400 Å | 같음 |
| C-H 결합 ($K_b$, $r_0$) | 367 kcal/mol·Å², 1.080 Å | 340, 1.080 |
| C-C-C 각도 ($K_\theta$, $\theta_0$) | 63.0 kcal/mol·rad², 120° | 같음 |
| C-C-H 각도 ($K_\theta$, $\theta_0$) | 35.0 kcal/mol·rad², 120° | 같음 |
| X-C-C-X 이면각 | $V_2$ = 7.250 kcal/mol, 나머지 0 | C-C-C-C 만 $V_3$ = 2.935, 나머지 0 |

### OPLS-AA 에탄올 LJ 파라미터 (Jorgensen 외 1996)

| 원자 | ε (kcal/mol) | σ (Å) | UROPS 입력 |
|------|--------------|--------|-----|
| HO (수산기 H) | 0.000 | 0.000 | 같음 |
| OH (수산기 O) | 0.170 | 3.120 | σ = 3.070 |
| CH₂-OH의 C (α-C) | 0.066 | 3.500 | 같음 |
| CH₃의 C | 0.066 | 3.500 | 같음 |
| 지방족 H | 0.030 | 2.500 | 같음 |

### UROPS 입력이 표준값과 다른 곳

`inputs/ff_opls_aa.in` 은 UROPS run 의 계수를 그대로 옮기고, 표준값과 다른 줄마다 `[표준: …]` 을 붙여 두었다.
요약하면 다음과 같다.

- **전하**: 에탄올 전하가 표준과 다르다 ([2장](02-data-files)의 표).
- **에탄올 각도**: C-O-H 가 63.0 / 120° (표준 55.0 / 108.5°) 로, 벤젠 C-C-C 값이 들어가 있다.
  H-C-H, C-C-H 각도도 같은 종류인데 타입마다 상수가 제각각이다.
- **이면각**: 벤젠 고리 이면각은 $V_2$ 대신 $V_3$ 에 2.935 가 들어가 있고 나머지 고리 이면각은 0 이다.
  평면성은 improper 항(10.5 kcal/mol, 180°) 하나로만 유지된다.
  에탄올의 H-C-C-H, H-C-C-O, H-C-O-H 이면각은 대부분 0 이다.
- **Cu-유기 LJ**: 아래 3.6절.

에탄올 각도와 이면각은 데이터 파일을 만들 때 타입 번호가 어긋난 것으로 보인다.
이 계수로 얻은 결과는 OPLS-AA 의 결과라고 부르기 어렵다. 새로 돌린다면 LigParGen 이나 moltemplate 의 `oplsaa.lt` 처럼
타입을 자동으로 붙여 주는 도구로 데이터 파일을 다시 만드는 편이 낫다.

## 3.5 TraPPE-UA 결합 항 설정

TraPPE-UA는 원래 Monte Carlo용이라 결합 길이를 rigid로 고정하는 게 보통이고,
MD에서 쓸 때는 아주 강한 조화 진동자로 바꿔 넣는다.

```bash
bond_style harmonic
angle_style harmonic
dihedral_style harmonic   # TraPPE는 OPLS의 4-cosine을 쓰지 않음
```

결합 길이를 SHAKE 알고리즘으로 고정하는 방법도 있지만, `fix shake` 는 중심 원자 하나와
거기 붙은 원자 최대 3개로 이루어진 클러스터만 다룬다. 그래서 모든 결합을 한꺼번에 묶을 수는 없다.

- 벤젠 UA 고리(CH 6개가 고리로 연결)는 클러스터가 아니므로 SHAKE 로 묶을 수 없다. `fix rigid/small` 을 쓴다.
- UA 에탄올 CH₃–CH₂–O–H 에서 세 결합을 모두 묶으면 CH₂ 중심 클러스터와 O 중심 클러스터가 이어져
  "Shake clusters are connected" 오류가 난다. O 중심의 CH₂–O, O–H 두 결합만 묶을 수 있다.

```bash
# 결합 타입 번호는 trappe.data 의 Bonds 섹션에서 확인한다 (아래는 CH2-O = 3, O-H = 4 인 경우)
fix shake_oh  ethanol shake 1.0e-4 20 0 b 3 4
fix rigid_bz  benzene rigid/small molecule
```

`fix rigid/small` 은 그 자체가 적분기라 벤젠 그룹에 `fix nve`/`nvt` 를 따로 걸지 않는다.
온도 조절이 필요하면 `rigid/nvt/small` 을 쓴다.

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

이 시스템의 벤젠 UA 파라미터는 일반적인 aromatic CH 값을 따랐다
(예: Wick et al. 2000, J. Phys. Chem. B 104, 8008-8016, DOI: 10.1021/jp001044x 참고).
공식 TraPPE-EH 벤젠 (Rai & Siepmann 2007) 과는 다르므로,
논문에 쓸 때는 파라미터 출처를 정확히 밝혀야 한다.

## 3.6 Cu 슬랩 파라미터 (Heinz 외 2008)

Heinz et al. (2008) 의 12-6 LJ 파라미터는 다음과 같다.

| 원자 | ε (kcal/mol) | σ (Å) | $r_0 = 2^{1/6}\sigma$ (Å) |
|------|--------------|--------|--------|
| Cu | 4.72 | 2.330 | 2.616 |

LAMMPS `lj/cut` 의 두 번째 계수는 σ 이므로 2.616 이 아니라 2.330 을 넣는다.
이 값은 fcc Cu 의 밀도와 표면 에너지에 맞춘 것이고, 유기 분자와의 cross 항을 일반적인 혼합 규칙으로
만들 수 있다는 게 INTERFACE 힘장의 장점이다.

```bash
# OPLS-AA 시스템에서 Cu는 type 12, TraPPE-UA 시스템에서는 type 6
pair_coeff 12 12 4.72 2.330
```

### UROPS run 의 Cu-유기 파라미터

UROPS run 은 이 값을 혼합하지 않고 Cu-유기 쌍을 하나씩 직접 넣었다.

| 쌍 | UROPS 입력 ε (kcal/mol) | Heinz 값을 기하 평균했을 때 ε (kcal/mol) |
|----|-----|-----|
| 벤젠 C - Cu | 0.0187 | 0.575 |
| 에탄올 C - Cu | 0.0182 | 0.558 |
| 에탄올 O - Cu | 0.0292 | 0.896 |
| H - Cu | 0.0122 | 0.376 |

UROPS 입력의 ε 는 Cu 의 ε 를 약 0.005 kcal/mol 로 두고 기하 평균한 값과 같다. Heinz 값보다 약 30배 약하다.
보고서에는 "INTERFACE 힘장의 Cu 파라미터와 기하 평균"이라고 적혀 있지만 입력 파일은 그렇지 않다.
Cu-유기 인력이 이 정도로 약하면 첫 흡착층의 구조는 Cu 와의 인력보다 벽 근처의 충전 효과에 가까울 수 있으니,
이 run 의 흡착 결과를 실제 Cu 표면에 대한 값으로 읽지 않는다.

## 3.7 힘장 선택 기준

| 연구 목적 | 알맞은 힘장 |
|-----------|-----------|
| 수소 결합 네트워크의 미세 구조 분석 | OPLS-AA (수소 명시) |
| 표면 위 분자 배향 (orientation) 의 자세한 분석 | OPLS-AA |
| 대규모 시스템에서 상 평형 (액-액, 기-액) | TraPPE-UA |
| 계산 비용이 제약 요인일 때 | TraPPE-UA |
| 분리 효율 지수 (SEI) 의 빠른 스크리닝 | TraPPE-UA |
| 흡착 에너지의 정량적 검증 | OPLS-AA 권장, TraPPE-UA로 확인 |

4가지 프레임워크 비교의 목표는 두 힘장이 같은 시스템에서 얼마나 다른 예측을 내놓는지
살펴보는 것이다.

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

