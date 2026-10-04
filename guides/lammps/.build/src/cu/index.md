---
layout: default
title: 홈
nav_order: 1
description: "구리 계면 벤젠-에탄올 혼합물 분자동역학 시뮬레이션 가이드"
permalink: /
---

# 구리 계면 벤젠-에탄올 혼합물 LAMMPS 시뮬레이션 가이드

<p class="amm-id">NOTE 32-00-00 · Cu 표면 경쟁 흡착 시리즈 개요</p>

## 1. 일반 사항

### A. 목적

1. 이 시리즈는 Cu 표면 위 벤젠-에탄올 경쟁 흡착을 분자동역학으로 계산하는 프로토콜과 입력 파일을 다룬다.
2. 이 시리즈는 힘장과 정전기 처리 방식이 계면 흡착에 주는 영향을 따로 떼어 비교한다.

### B. 적용 범위

1. 다음 네 가지 조합을 비교한다.

| 힘장 (Force field) | 정전기 방법 | 약칭         |
|--------------------|-------------|--------------|
| OPLS-AA            | PPPM        | OPLS+PPPM    |
| OPLS-AA            | MSM         | OPLS+MSM     |
| TraPPE-UA          | PPPM        | TraPPE+PPPM  |
| TraPPE-UA          | MSM         | TraPPE+MSM   |

2. 네 조합 모두 같은 다섯 단계 프로토콜을 따른다. 순서는 소프트 완화 → 에너지 최소화 → 단계적 가열 → 평형화 → production 이다.

### C. 결과 요약

1. `inputs/` 의 다섯 단계 입력은 공개된 [`opls.data`](../../files/blog/pppm-vs-msm/opls.data) 로 끝까지 실행된다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
`opls.data` 는 Cu 슬랩 구조와 일부 OPLS-AA 계수가 틀려 있다. 실행은 오류 없이 끝나지만 결과는 표준 힘장의 결과가 아니다. 각 장에 해당 내용을 함께 적었다([1장](docs/01-overview), [3장](docs/03-force-fields)).
</div>

## 2. 준비 정보

### A. 필요한 개념

1. LAMMPS 기초(NOTE 31-01-00 ~ 31-08-00).
2. 고전 힘장, 부분 전하, 장거리 정전기의 기본 개념.

### B. 참조 자료

이 시리즈는 주로 다음 문헌을 바탕으로 한다. 인용 시 아래 문헌을 참고한다.

| 참조 | 제목 |
|------|------|
| Jorgensen 외 (1996) | W. L. Jorgensen, D. S. Maxwell, J. Tirado-Rives, "Development and Testing of the OPLS All-Atom Force Field on Conformational Energetics and Properties of Organic Liquids", *J. Am. Chem. Soc.* **118**, 11225-11236 (1996). DOI: [10.1021/ja9621760](https://doi.org/10.1021/ja9621760) |
| Chen 외 (2001) | B. Chen, J. J. Potoff, J. I. Siepmann, "Monte Carlo Calculations for Alcohols and Their Mixtures with Alkanes. Transferable Potentials for Phase Equilibria. 5. United-Atom Description of Primary, Secondary, and Tertiary Alcohols", *J. Phys. Chem. B* **105**, 3093-3104 (2001). DOI: [10.1021/jp003882x](https://doi.org/10.1021/jp003882x) |
| Rai, Siepmann (2007) | N. Rai, J. I. Siepmann, "Transferable Potentials for Phase Equilibria. 9. Explicit Hydrogen Description of Benzene and Five-Membered and Six-Membered Heterocyclic Aromatic Compounds", *J. Phys. Chem. B* **111**, 10790-10799 (2007). DOI: [10.1021/jp073586l](https://doi.org/10.1021/jp073586l) |
| Heinz 외 (2008) | H. Heinz, R. A. Vaia, B. L. Farmer, R. R. Naik, "Accurate Simulation of Surfaces and Interfaces of Face-Centered Cubic Metals Using 12-6 and 9-6 Lennard-Jones Potentials", *J. Phys. Chem. C* **112**, 17281-17290 (2008). DOI: [10.1021/jp801931d](https://doi.org/10.1021/jp801931d) |
| Thompson 외 (2022) | A. P. Thompson 외, "LAMMPS - a flexible simulation tool for particle-based materials modeling at the atomic, meso, and continuum scales", *Comput. Phys. Commun.* **271**, 108171 (2022). DOI: [10.1016/j.cpc.2021.108171](https://doi.org/10.1016/j.cpc.2021.108171) |

### C. 사용 프로그램

| 항목 | 내용 |
|------|------|
| LAMMPS | 23 Jun 2022 이후 안정 버전 (MOLECULE, KSPACE, RIGID 패키지. UROPS run 처럼 Cu-Cu 에 EAM 을 쓰면 MANYBODY 도) |
| 입력 확인에 쓴 버전 | LAMMPS 22 Jul 2025 |
| MPI | 40코어 워크스테이션에서 `mpirun -np 40` |
| 세션 관리 | 오래 걸리는 실행은 `tmux` 안에서 |

### D. 관련 파일

| 항목 | 용도 |
|------|------|
| [`opls.data`](../../files/blog/pppm-vs-msm/opls.data) | OPLS-AA 데이터 파일 (공개) |
| `inputs/` | 다섯 단계 입력 |

## 3. 노트 목록

| 노트 번호 | 제목 | 내용 |
|-----------|------|------|
| NOTE 32-01-00 | [시스템 개요](docs/01-overview) | 화학적 배경과 시뮬레이션 셀 구성 |
| NOTE 32-02-00 | [데이터 파일 구조](docs/02-data-files) | `opls.data`, `trappe.data` 비교 |
| NOTE 32-03-00 | [힘장 비교](docs/03-force-fields) | OPLS-AA와 TraPPE-UA의 차이 |
| NOTE 32-04-00 | [정전기 방법](docs/04-electrostatics) | PPPM과 MSM, 슬랩 보정 |
| NOTE 32-05-00 | [5단계 프로토콜](docs/05-protocol) | 단계별 이유와 입력 명령어 |
| NOTE 32-06-00 | [4가지 프레임워크 비교](docs/06-frameworks) | 조합별 차이와 선택 기준 |
| NOTE 32-07-00 | [분석 방법](docs/07-analysis) | RDF, 밀도 프로파일, SEI, 계면 장력 |
| NOTE 32-08-00 | [트러블슈팅](docs/08-troubleshooting) | 자주 나는 오류와 원인 진단 |
