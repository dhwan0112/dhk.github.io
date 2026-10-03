---
layout: default
title: 홈
nav_order: 1
description: "구리 계면 벤젠-에탄올 혼합물 분자동역학 시뮬레이션 가이드"
permalink: /
---

# 구리 계면 벤젠-에탄올 혼합물 LAMMPS 시뮬레이션 가이드

Cu 표면 위 벤젠-에탄올 경쟁 흡착을 분자동역학으로 계산할 때 쓴
프로토콜과 입력 파일을 정리했다. `inputs/` 의 다섯 단계 입력은 공개된
[`opls.data`](../../files/blog/pppm-vs-msm/opls.data) 로 끝까지 돌아가는 것을 확인했다.
다만 이 데이터 파일은 Cu 슬랩 구조와 일부 OPLS-AA 계수가 틀려 있어서, 각 장에 그 내용을 함께 적었다
([1장](docs/01-overview), [3장](docs/03-force-fields)).

---

## 무엇을 비교하나

이 시리즈는 다음 네 가지 조합을 비교한다.

| 힘장 (Force field) | 정전기 방법 | 약칭         |
|--------------------|-------------|--------------|
| OPLS-AA            | PPPM        | OPLS+PPPM    |
| OPLS-AA            | MSM         | OPLS+MSM     |
| TraPPE-UA          | PPPM        | TraPPE+PPPM  |
| TraPPE-UA          | MSM         | TraPPE+MSM   |

네 조합 모두 같은 다섯 단계 프로토콜(소프트 완화 → 에너지 최소화 → 단계적 가열 → 평형화 → production)을
따른다. 그래서 힘장과 정전기 처리 방식이 계면 흡착에 주는 영향을 따로 떼어 볼 수 있다.

## 빠른 둘러보기

- [시스템 개요](docs/01-overview): 화학적 배경과 시뮬레이션 셀 구성
- [데이터 파일 구조](docs/02-data-files): `opls.data`, `trappe.data` 비교
- [힘장 비교](docs/03-force-fields): OPLS-AA와 TraPPE-UA의 차이
- [정전기 방법](docs/04-electrostatics): PPPM과 MSM, 슬랩 보정
- [5단계 프로토콜](docs/05-protocol): 단계별 이유와 입력 명령어
- [4가지 프레임워크 비교](docs/06-frameworks): 조합별 차이와 선택 기준
- [분석 방법](docs/07-analysis): RDF, 밀도 프로파일, SEI, 계면 장력
- [트러블슈팅](docs/08-troubleshooting): 자주 나는 오류와 원인 진단

## 실행 환경

- LAMMPS: 23 Jun 2022 이후 안정 버전 (MOLECULE, KSPACE, RIGID 패키지. UROPS run 처럼 Cu-Cu 에 EAM 을 쓰면 MANYBODY 도)
- 입력 확인에 쓴 버전: LAMMPS 22 Jul 2025
- MPI: 40코어 워크스테이션에서 `mpirun -np 40`
- 세션 관리: 오래 걸리는 실행은 `tmux` 안에서

## 인용 시 참고문헌

이 시리즈는 주로 다음 문헌을 바탕으로 한다.

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
