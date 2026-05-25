---
layout: default
title: "2. 데이터 파일 구조"
nav_order: 3
---

# 2. 데이터 파일 구조
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

LAMMPS의 `read_data` 명령어가 읽어들이는 데이터 파일은 시스템의 원자 위치, 결합 토폴로지, 부분 전하를 모두 포함한다.
본 가이드의 두 데이터 파일 `opls.data`와 `trappe.data`는 동일한 물리계를 표현하지만,
힘장의 분자 표현 방식이 다르기 때문에 원자 수와 토폴로지가 크게 다르다.

## 2.1 두 데이터 파일의 헤더 비교

다음은 각 데이터 파일의 헤더 (전역 정보) 부분이다.

### opls.data (OPLS-AA, all-atom)

```text
LAMMPS data file from PDB (v7.2 - Angle Format Fix)

2471 atoms
2000 bonds
3100 angles
3600 dihedrals
600 impropers

12 atom types
10 bond types
15 angle types
16 dihedral types
1 improper types

0.000000 30.000000 xlo xhi
0.000000 30.000000 ylo yhi
0.000000 41.895000 zlo zhi
```

### trappe.data (TraPPE-UA, united-atom)

```text
LAMMPS data file for TraPPE-UA (converted from OPLS-AA)

1371 atoms
900 bonds
800 angles
700 dihedrals

6 atom types
4 bond types
3 angle types
2 dihedral types

0.000000 30.000000 xlo xhi
0.000000 30.000000 ylo yhi
0.000000 41.895000 zlo zhi
```

## 2.2 원자 수가 다른 이유 — 화학적 해석

두 데이터 파일은 박스 크기가 동일하나, 원자 수는 약 1.8배 차이가 난다.
이는 united-atom (UA) 모형이 메틸기와 메틸렌기를 단일 사이트로 흡수하기 때문이다.

### 벤젠 (C₆H₆)

| 표현 | 사이트 수 | 사이트 종류 |
|------|-----------|-------------|
| OPLS-AA (all-atom) | 12 사이트 | 6 × C + 6 × H |
| TraPPE-UA | 6 사이트 | 6 × CH (C-H를 묶음) |

벤젠은 TraPPE-EH (explicit hydrogen) 버전이 일반적으로 사용되지만,
본 시스템은 통일성을 위해 UA 6-site 모형 (CH를 단일 사이트로) 으로 단순화되어 있다.
이때 벤젠 평면성은 SHAKE 또는 rigid 알고리즘으로 유지하거나 강한 dihedral 항을 통해 부과한다.

### 에탄올 (CH₃-CH₂-OH)

| 표현 | 사이트 수 | 사이트 종류 |
|------|-----------|-------------|
| OPLS-AA (all-atom) | 9 사이트 | CH₃(C+3H) + CH₂(C+2H) + O + H |
| TraPPE-UA | 4 사이트 | CH₃ + CH₂ + O + H |

UA 표현에서는 메틸과 메틸렌의 수소 원자가 명시적으로 다뤄지지 않으며,
하나의 CH₃ 또는 CH₂ 사이트로 흡수된다 (Chen, Potoff, Siepmann 2001).
다만 수산기 (-OH)의 H는 수소 결합을 형성하므로 명시적으로 유지된다.

### 시스템별 분자 수

| 항목 | OPLS-AA | TraPPE-UA |
|------|---------|------------|
| 벤젠 분자 수 | 33 (× 12 = 396) | 100 (× 6 = 600) |
| 에탄올 분자 수 | 33 (× 9 = 297) | 100 (× 4 = 400) |
| Cu 원자 수 | 2471 - 693 = 1778 | 1371 - 1000 = 371 |
| 총합 | 2471 | 1371 |

OPLS-AA 시스템의 Cu 슬랩이 더 두꺼운 이유는 모든 H를 명시하기 위한 계산 비용 균형을 맞추기 위함으로 추측되며,
계면 비교 시 슬랩 두께 차이를 인지하고 분석해야 한다.

## 2.3 Atoms 섹션의 컬럼 구조

OPLS-AA, TraPPE-UA 모두 `atom_style full` 형식을 사용한다.
각 행은 다음과 같은 컬럼을 갖는다 ([LAMMPS atom_style 문서](https://docs.lammps.org/atom_style.html) 참조).

```
atom-ID  molecule-ID  atom-type  q  x  y  z
```

### OPLS-AA의 12가지 원자 타입

`opls.data` 헤더의 Masses 섹션:

```text
Masses

1 12.0110 # benzene_C
2 1.0080  # benzene_H
3 12.0110 # ethanol_C00
4 12.0110 # ethanol_C01
5 15.9990 # ethanol_O02
6 1.0080  # ethanol_H03
7 1.0080  # ethanol_H04
8 1.0080  # ethanol_H05
9 1.0080  # ethanol_H06
10 1.0080 # ethanol_H07
11 1.0080 # ethanol_H08
12 63.5460 # Cu
```

타입 6-11이 모두 수소이지만 OPLS-AA에서는 화학적 환경에 따라 다른 부분 전하를 부여하므로
별개의 타입으로 구분하는 것이 권장된다 (Jorgensen 외 1996의 화학 단위별 전하 할당 관례).

### TraPPE-UA의 6가지 원자 타입

`trappe.data` 헤더의 Masses 섹션:

```text
Masses

1 13.0190  # benzene CH (12.011 + 1.008)
2 15.0350  # ethanol CH3 (12.011 + 3 × 1.008)
3 14.0270  # ethanol CH2 (12.011 + 2 × 1.008)
4 15.9990  # ethanol O
5 1.0080   # ethanol H (수산기)
6 63.5460  # Cu
```

UA 사이트의 질량은 묶인 그룹 전체의 질량의 합이다.
예를 들어 CH₂는 14.027 = 12.011 + 2 × 1.008 g/mol.

## 2.4 부분 전하 (Atoms 섹션의 q 열)

### TraPPE-UA 에탄올의 부분 전하

`trappe.data`의 Atoms 섹션 (앞 몇 줄):

```text
1 1 2 0.0000 2.903313 17.497132 21.087920   # CH3, q = 0
2 1 3 0.2650 2.948696 18.272399 19.631332   # CH2, q = +0.265
3 1 4 -0.7000 4.248000 17.888000 19.055000  # O,   q = -0.700
4 1 5 0.4350 4.959000 18.191999 19.643999   # H,   q = +0.435
```

벤젠 CH는 모두 중성 (q = 0).
에탄올의 전하 분포는 Chen, Potoff, Siepmann (2001) 의 OPLS-UA 유래 전하 분포를 따른다:
CH₂ +0.265, O -0.700, H(수산기) +0.435.
이 전하 분포는 메탄올부터 옥탄올까지의 1차/2차/3차 알코올 전 시리즈에서 공통으로 사용된다.

### OPLS-AA 에탄올의 부분 전하

OPLS-AA에서는 모든 원자가 명시적이므로 전하가 분산된다 (Jorgensen 외 1996, Table 4 참조).
대표적인 OPLS-AA 에탄올 전하:

| 원자 | OPLS atom type (OPLS DB) | 부분 전하 (e) |
|------|--------------------------|---------------|
| HO (수산기 H) | 155 | +0.435 |
| OH (수산기 O) | 154 | -0.683 |
| CH₂-OH의 C | 157 | +0.145 |
| CH₂-OH의 H | 140 | +0.040 |
| CH₃의 C | 158 | -0.180 |
| CH₃의 H | 140 | +0.060 |

총 전하의 합은 0 (에탄올 분자는 중성).
이 값들은 OPLS-AA 공식 파라미터 (oplsaa.lt 또는 OPLS 데이터베이스)에서 확인 가능하며,
연구자에 따라 다소 변형된 값을 사용하기도 한다.

## 2.5 데이터 파일 검증 체크리스트

데이터 파일이 LAMMPS에 의해 올바르게 읽히는지 확인하기 위한 체크리스트:

1. **전하 합 검증**: `awk '{sum+=$4} END {print sum}' atoms_section.txt`
   결과가 0에 매우 가까워야 한다 (반올림 오차 ~ 1e-6).
2. **원자 ID 연속성**: ID가 1부터 N까지 연속해야 한다.
3. **분자 ID 일관성**: 같은 분자의 원자는 같은 molecule-ID를 공유해야 한다.
4. **결합/각도 토폴로지 일치**: 결합 수 = (벤젠 분자 × 6) + (에탄올 분자 × 4) 등이 맞아야 한다.
5. **박스 경계 내부**: 모든 원자 좌표가 박스 한계 내에 있어야 한다.

LAMMPS에서 `read_data` 시 자동으로 검증되는 항목도 있지만,
"Bond atoms missing" 오류를 회피하려면 사전 검증이 권장된다.
이 오류의 트러블슈팅은 [트러블슈팅](08-troubleshooting) 문서를 참조.

## 참고문헌

1. W. L. Jorgensen, D. S. Maxwell, J. Tirado-Rives,
   "Development and Testing of the OPLS All-Atom Force Field on Conformational
   Energetics and Properties of Organic Liquids",
   *J. Am. Chem. Soc.* **118**, 11225-11236 (1996).
   DOI: [10.1021/ja9621760](https://doi.org/10.1021/ja9621760)

2. B. Chen, J. J. Potoff, J. I. Siepmann,
   "Monte Carlo Calculations for Alcohols and Their Mixtures with Alkanes.
   Transferable Potentials for Phase Equilibria. 5.",
   *J. Phys. Chem. B* **105**, 3093-3104 (2001).
   DOI: [10.1021/jp003882x](https://doi.org/10.1021/jp003882x)

3. LAMMPS 공식 문서, `atom_style` 명령어:
   [https://docs.lammps.org/atom_style.html](https://docs.lammps.org/atom_style.html)

4. LAMMPS 공식 문서, `read_data` 명령어:
   [https://docs.lammps.org/read_data.html](https://docs.lammps.org/read_data.html)

---

[← 이전: 1. 시스템 개요](01-overview) ｜ [다음: 3. 힘장 비교 →](03-force-fields)
