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

<p class="amm-id">NOTE 32-02-00 · 데이터 파일 구조</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 `read_data` 가 읽는 두 데이터 파일 `opls.data` 와 `trappe.data` 의 구조와 차이를 다룬다.
2. 데이터 파일에는 원자 위치, 결합 토폴로지, 부분 전하가 모두 들어 있다.

### B. 적용 범위

1. 두 파일은 같은 물리계를 나타낸다.
2. 힘장마다 분자를 표현하는 방식이 달라서 원자 수와 토폴로지가 크게 다르다.

### C. 결과 요약

1. 원자 수는 `opls.data` 2471, `trappe.data` 1371 이다. 차이는 전부 수소 표현에서 나온다.
2. `opls.data` 의 초기 좌표에는 1 Å 보다 가까운 분자 간 원자 쌍이 34개 있다.
3. `opls.data` 의 에탄올 전하는 표준 OPLS-AA 값과 다르다.

## 2. 준비 정보

### A. 필요한 개념

1. LAMMPS 데이터 파일 형식(NOTE 31-04-00).
2. `atom_style full` 의 원자 정보(NOTE 31-03-00).
3. Cu 슬랩 계의 구성(NOTE 32-01-00).

### B. 참조 자료

| 참조 | 제목 |
|------|------|
| Jorgensen 외 (1996) | W. L. Jorgensen, D. S. Maxwell, J. Tirado-Rives, "Development and Testing of the OPLS All-Atom Force Field on Conformational Energetics and Properties of Organic Liquids", *J. Am. Chem. Soc.* **118**, 11225-11236 (1996). DOI: [10.1021/ja9621760](https://doi.org/10.1021/ja9621760) |
| Chen 외 (2001) | B. Chen, J. J. Potoff, J. I. Siepmann, "Monte Carlo Calculations for Alcohols and Their Mixtures with Alkanes. Transferable Potentials for Phase Equilibria. 5.", *J. Phys. Chem. B* **105**, 3093-3104 (2001). DOI: [10.1021/jp003882x](https://doi.org/10.1021/jp003882x) |
| LAMMPS `atom_style` | LAMMPS 공식 문서, `atom_style` 명령어: [https://docs.lammps.org/atom_style.html](https://docs.lammps.org/atom_style.html) |
| LAMMPS `read_data` | LAMMPS 공식 문서, `read_data` 명령어: [https://docs.lammps.org/read_data.html](https://docs.lammps.org/read_data.html) |
| NOTE 32-01-00 | [시스템 개요](01-overview) |
| NOTE 32-05-00 | [5단계 프로토콜](05-protocol) |
| NOTE 32-08-00 | [트러블슈팅](08-troubleshooting) |

### D. 관련 파일

| 항목 | 내용 |
|------|------|
| `opls.data` | OPLS-AA, all-atom, 2471 atoms |
| `trappe.data` | TraPPE-UA, united-atom, 1371 atoms |

## 3. 절차

### A. 헤더 비교

1. 각 데이터 파일의 헤더(전역 정보) 부분을 확인한다.
2. `opls.data` (OPLS-AA, all-atom) 의 헤더는 다음과 같다.

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

3. `trappe.data` (TraPPE-UA, united-atom) 의 헤더는 다음과 같다.

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

### B. 원자 수 차이 확인

1. 두 파일은 박스 크기가 같은데도 원자 수가 약 1.8배 차이 난다.
2. united-atom (UA) 모형이 메틸기와 메틸렌기를 한 사이트로 묶기 때문이다.
3. 벤젠(C₆H₆)의 사이트 구성을 비교한다.

| 표현 | 사이트 수 | 사이트 종류 |
|------|-----------|-------------|
| OPLS-AA (all-atom) | 12 사이트 | 6 × C + 6 × H |
| TraPPE-UA | 6 사이트 | 6 × CH (C-H를 묶음) |

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
벤젠에는 보통 TraPPE-EH (explicit hydrogen) 버전을 쓴다. 이 시스템에서는 통일성을 위해 UA 6-site 모형(CH를 한 사이트로)으로 단순화했다. 이 경우 벤젠 평면성은 `fix rigid/small` 로 고리를 강체로 묶거나 강한 dihedral 항으로 부과한다.
</div>

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
`fix shake` 는 한 원자를 중심으로 한 별 모양 클러스터(최대 4원자)만 묶을 수 있어서 고리에는 쓸 수 없다.
</div>

4. 에탄올(CH₃-CH₂-OH)의 사이트 구성을 비교한다.

| 표현 | 사이트 수 | 사이트 종류 |
|------|-----------|-------------|
| OPLS-AA (all-atom) | 9 사이트 | CH₃(C+3H) + CH₂(C+2H) + O + H |
| TraPPE-UA | 4 사이트 | CH₃ + CH₂ + O + H |

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
UA 표현에서는 메틸과 메틸렌의 수소를 따로 두지 않고 CH₃ 또는 CH₂ 사이트 하나에 포함시킨다 (Chen, Potoff, Siepmann 2001). 다만 수산기(-OH)의 H는 수소 결합을 만들기 때문에 명시적으로 남겨 둔다.
</div>

5. 시스템별 분자 수를 확인한다.

| 항목 | OPLS-AA | TraPPE-UA |
|------|---------|------------|
| 벤젠 분자 수 | 100 (× 12 = 1200) | 100 (× 6 = 600) |
| 에탄올 분자 수 | 100 (× 9 = 900) | 100 (× 4 = 400) |
| Cu 원자 수 | 2471 - 2100 = 371 | 1371 - 1000 = 371 |
| 총합 | 2471 | 1371 |

6. 두 파일은 분자 수와 Cu 슬랩이 같고, 원자 수 차이는 전부 수소 표현에서 나온다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
Cu 슬랩은 fcc 가 아닌 bcc 쌓임이고, 주기 경계에서 원자가 겹친다. 상세 내용은 [1장](01-overview)의 경고에 적었다.
</div>

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
`opls.data` 의 초기 좌표에는 서로 다른 분자의 원자 쌍 34개가 1 Å 보다 가깝게 붙어 있다(가장 가까운 쌍 0.15 Å). 첫 스텝의 퍼텐셜 에너지가 약 $9 \times 10^{14}$ kcal/mol 로 나오므로, [5장](05-protocol)의 소프트 완화 단계를 건너뛸 수 없다.
</div>

### C. Atoms 섹션 컬럼 확인

1. 두 파일 모두 `atom_style full` 형식임을 확인한다.
2. 각 행의 컬럼은 다음과 같다 ([LAMMPS atom_style 문서](https://docs.lammps.org/atom_style.html) 참조).

```
atom-ID  molecule-ID  atom-type  q  x  y  z
```

3. `opls.data` 헤더의 Masses 섹션에서 OPLS-AA의 12가지 원자 타입을 확인한다.

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

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
타입 6-11은 모두 수소지만, OPLS-AA는 화학적 환경에 따라 부분 전하를 다르게 주므로 타입도 따로 나눠 두는 게 좋다 (Jorgensen 외 1996의 화학 단위별 전하 할당 관례).
</div>

4. `trappe.data` 헤더의 Masses 섹션에서 TraPPE-UA의 6가지 원자 타입을 확인한다.

```text
Masses

1 13.0190  # benzene CH (12.011 + 1.008)
2 15.0350  # ethanol CH3 (12.011 + 3 × 1.008)
3 14.0270  # ethanol CH2 (12.011 + 2 × 1.008)
4 15.9990  # ethanol O
5 1.0080   # ethanol H (수산기)
6 63.5460  # Cu
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
UA 사이트의 질량은 묶인 원자들의 질량을 더한 값이다. 예를 들어 CH₂는 14.027 = 12.011 + 2 × 1.008 g/mol.
</div>

### D. 부분 전하 확인 (Atoms 섹션의 q 열)

1. `trappe.data` 의 Atoms 섹션(앞 몇 줄)에서 TraPPE-UA 에탄올의 부분 전하를 확인한다.

```text
1 1 2 0.0000 2.903313 17.497132 21.087920   # CH3, q = 0
2 1 3 0.2650 2.948696 18.272399 19.631332   # CH2, q = +0.265
3 1 4 -0.7000 4.248000 17.888000 19.055000  # O,   q = -0.700
4 1 5 0.4350 4.959000 18.191999 19.643999   # H,   q = +0.435
```

2. 벤젠 CH는 모두 중성 (q = 0) 이다.
3. 에탄올의 전하 분포는 Chen, Potoff, Siepmann (2001) 의 OPLS-UA 유래 전하 분포를 따른다. CH₂ +0.265, O -0.700, H(수산기) +0.435 이다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
이 전하 분포는 메탄올부터 옥탄올까지 1차/2차/3차 알코올 전체에 공통으로 쓰인다.
</div>

4. OPLS-AA 에탄올의 부분 전하를 확인한다. OPLS-AA는 모든 원자를 명시하므로 전하도 여러 원자에 나뉜다 (Jorgensen 외 1996).

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
`opls.data` 의 에탄올 전하는 표준 OPLS-AA 값과 다르다. 아래 표에 표준값과 `opls.data` 에 실제로 들어 있는 값을 나란히 적었다.
</div>

5. 표준 OPLS-AA 에탄올 전하와 `opls.data` 의 값을 비교한다.

| 원자 | OPLS atom type | 표준 전하 (e) | `opls.data` (e) |
|------|----------------|---------------|-----------------|
| HO (수산기 H) | 155 | +0.418 | +0.432 |
| OH (수산기 O) | 154 | -0.683 | -0.728 |
| CH₂-OH의 C | 157 | +0.145 | +0.128 |
| CH₂-OH의 H (×2) | 140 | +0.060 | +0.0592 |
| CH₃의 C | 135 | -0.180 | -0.128 |
| CH₃의 H (×3) | 140 | +0.060 | +0.0592 |

6. 두 열 모두 합이 0 임을 확인한다.
    1. 표준값에서는 CH₃ 와 CH₂OH 가 각각 중성이다.
    2. `opls.data` 는 C 두 개에 ±0.128 을 주고 H 다섯 개에 같은 값을 줘서 분자 전체만 중성이다.
7. 벤젠은 표준값(C -0.115, H +0.115) 그대로임을 확인한다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
수산기 H 의 +0.435 는 OPLS-AA 가 아니라 OPLS-UA·TraPPE-UA 의 값이다. 섞어 쓰지 않는다.
</div>

## 4. 시험 및 검사

### A. 데이터 파일 검증

1. LAMMPS가 데이터 파일을 제대로 읽는지 다음 항목으로 점검한다.
2. 전하 합을 검증한다: `awk '{sum+=$4} END {print sum}' atoms_section.txt`
    1. 결과가 0에 매우 가까워야 한다 (반올림 오차 ~ 1e-6).
3. 원자 ID 연속성을 확인한다. ID가 1부터 N까지 연속해야 한다.
4. 분자 ID 일관성을 확인한다. 같은 분자의 원자는 같은 molecule-ID를 공유해야 한다.
5. 결합/각도 토폴로지 일치를 확인한다. 헤더의 개수가 분자 수와 맞아야 한다.
    1. OPLS-AA 는 결합이 벤젠 12개, 에탄올 8개라 100 × 12 + 100 × 8 = 2000 이다. 각도는 18 + 13 개라 3100, 이면각은 24 + 12 개라 3600 이다.
    2. TraPPE-UA 는 결합 6 + 3 개라 900, 각도 6 + 2 개라 800, 이면각 6 + 1 개라 700 이다.
6. 박스 경계 내부를 확인한다. 모든 원자 좌표가 박스 한계 내에 있어야 한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
`read_data` 가 자동으로 검사하는 항목도 있지만, "Bond atoms missing" 오류를 피하려면 미리 확인해 두는 편이 낫다. 이 오류의 해결법은 [트러블슈팅](08-troubleshooting)에 있다.
</div>
