---
layout: default
title: 홈
nav_order: 1
description: "구리 계면 벤젠-에탄올 혼합물 분자동역학 시뮬레이션 가이드"
permalink: /
---

# 구리 계면 벤젠-에탄올 혼합물 LAMMPS 시뮬레이션 가이드
{: .fs-9 }

Cu(100) 및 Cu(111) 표면 위 벤젠-에탄올 경쟁 흡착 거동에 대한
분자동역학 시뮬레이션 프로토콜과 입력 파일을 정리한 문서.
{: .fs-6 .fw-300 }

---

## 본 가이드의 목적

본 가이드는 다음 네 가지 시뮬레이션 프레임워크를 체계적으로 비교하기 위해 작성되었다.

| 힘장 (Force field) | 정전기 방법 | 약칭         |
|--------------------|-------------|--------------|
| OPLS-AA            | PPPM        | OPLS+PPPM    |
| OPLS-AA            | MSM         | OPLS+MSM     |
| TraPPE-UA          | PPPM        | TraPPE+PPPM  |
| TraPPE-UA          | MSM         | TraPPE+MSM   |

각 조합이 동일한 다섯 단계 프로토콜 (소프트 완화 → 에너지 최소화 → 단계적 가열 → 평형화 → 생성 동역학)을
따르도록 구성되어 있으며, 이를 통해 힘장과 정전기 처리 방식이 계면 흡착 거동에 미치는 영향을
분리하여 분석할 수 있다.

## 빠른 둘러보기

- [시스템 개요](docs/01-overview) — 화학적 배경과 시뮬레이션 셀 구성
- [데이터 파일 구조](docs/02-data-files) — `opls.data`, `trappe.data` 비교
- [힘장 비교](docs/03-force-fields) — OPLS-AA vs TraPPE-UA의 화학적 의미
- [정전기 방법](docs/04-electrostatics) — PPPM과 MSM, 그리고 슬랩 보정
- [5단계 프로토콜](docs/05-protocol) — 단계별 화학적 정당화와 입력 명령어
- [4가지 프레임워크 비교](docs/06-frameworks) — 조합별 차이와 선택 가이드
- [분석 방법](docs/07-analysis) — RDF, 밀도 프로파일, SEI, 계면 장력
- [트러블슈팅](docs/08-troubleshooting) — 빈번한 오류와 화학적 진단

## 실행 환경

- **LAMMPS**: 23 Jun 2022 이후 안정 버전 권장 (KSPACE, MANYBODY, EXTRA-PAIR 패키지 포함)
- **MPI**: 40코어 워크스테이션 기준으로 `mpirun -np 40` 권장
- **세션 관리**: 장시간 실행에는 `tmux` 사용

## 인용 시 참고문헌

본 가이드의 구성은 다음 핵심 문헌에 기반한다.

- W. L. Jorgensen, D. S. Maxwell, J. Tirado-Rives,
  "Development and Testing of the OPLS All-Atom Force Field on Conformational
  Energetics and Properties of Organic Liquids",
  *J. Am. Chem. Soc.* **118**, 11225-11236 (1996). DOI: [10.1021/ja9621760](https://doi.org/10.1021/ja9621760)

- B. Chen, J. J. Potoff, J. I. Siepmann,
  "Monte Carlo Calculations for Alcohols and Their Mixtures with Alkanes.
  Transferable Potentials for Phase Equilibria. 5. United-Atom Description of
  Primary, Secondary, and Tertiary Alcohols",
  *J. Phys. Chem. B* **105**, 3093-3104 (2001). DOI: [10.1021/jp003882x](https://doi.org/10.1021/jp003882x)

- N. Rai, J. I. Siepmann,
  "Transferable Potentials for Phase Equilibria. 9. Explicit Hydrogen Description
  of Benzene and Five-Membered and Six-Membered Heterocyclic Aromatic Compounds",
  *J. Phys. Chem. B* **111**, 10790-10799 (2007). DOI: [10.1021/jp073586l](https://doi.org/10.1021/jp073586l)

- H. Heinz, R. A. Vaia, B. L. Farmer, R. R. Naik,
  "Accurate Simulation of Surfaces and Interfaces of Face-Centered Cubic Metals
  Using 12-6 and 9-6 Lennard-Jones Potentials",
  *J. Phys. Chem. C* **112**, 17281-17290 (2008). DOI: [10.1021/jp801931d](https://doi.org/10.1021/jp801931d)

- A. P. Thompson 외, "LAMMPS - a flexible simulation tool for particle-based
  materials modeling at the atomic, meso, and continuum scales",
  *Comput. Phys. Commun.* **271**, 108171 (2022). DOI: [10.1016/j.cpc.2021.108171](https://doi.org/10.1016/j.cpc.2021.108171)
