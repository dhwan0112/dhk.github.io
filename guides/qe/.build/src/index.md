---
layout: default
title: "Quantum ESPRESSO 한국어 가이드"
permalink: /
---

# Quantum ESPRESSO 한국어 가이드

Quantum ESPRESSO(QE)는 평면파(plane-wave) 기저와 유사퍼텐셜(pseudopotential)을
쓰는 오픈소스 제일원리(DFT) 계산 패키지입니다. 결정·표면·분자의 전자구조,
전체 에너지, 힘과 응력, 밴드구조·상태밀도, 포논, ab initio 분자동역학까지
다루며, 학술용으로 무료로 배포됩니다.

본 가이드는 QE를 처음 접하는 사용자가 `pw.x` 앞에서 길을 잃지 않도록 정리한
한국어 안내서입니다. 가장 단순한 실리콘 SCF에서 출발해 입력 문법, 수렴 테스트,
구조 최적화, 후처리를 거쳐, 스핀 편극과 반강자성, DFT+U의 `HUBBARD` 카드,
`hp.x`에 의한 U 계산, 슬랩과 ab initio MD까지 — 전이금속 산화물(Fe–O 계) 연구에
필요한 경로를 끝까지 다룹니다.

## 학습 전에 붙잡아야 할 원칙 세 가지

**1. QE는 프로그램이라기보다 실험 장비에 가깝습니다.** 입력 파라미터 하나하나가
물리적 근사에 대응합니다. `ecutwfc = 60`은 "60이라는 숫자"가 아니라 "평면파
기저를 어디서 자를 것인가"라는 물리적 결정입니다. 매뉴얼을 암기하는 대신
**이 값이 무엇을 근사하고 있는가**를 매번 묻는 습관이 학습 속도를 결정합니다.

**2. 수렴 테스트를 통과하지 않은 숫자는 숫자가 아닙니다.** 가장 흔한 실수는
"계산이 돌아갔다 = 결과가 맞다"는 착각입니다. QE는 물리적으로 완전히 틀린
결과도 아주 깔끔하게 출력해 줍니다. [05장](05-convergence.html)과
[예제 E3](ex-03-convergence.html)에 절차를 정리했습니다.

**3. 서드파티 튜토리얼은 버전을 확인하고 쓰세요.** 인터넷의 QE 예제 상당수가
구버전 문법입니다. 대표적으로 DFT+U는 v7.1에서 `lda_plus_u` / `Hubbard_U(i)`
방식이 **`HUBBARD` 카드** 방식으로 완전히 바뀌었습니다. 옛 예제를 그대로
복사하면 조용히 무시되거나 에러가 납니다. 본 가이드는 신문법만 씁니다.

## 이 가이드에 관하여

- **기준 버전은 QE 7.5**(2025년 8월 릴리스)입니다. 예제 13종은 모두 QE 7.5
  (conda-forge 빌드, WSL Ubuntu)에서 **실제로 실행해 실측 수치·그림과 함께**
  정리했습니다. 각 예제 페이지 하단에서 입력 파일을 내려받을 수 있고,
  [전체 묶음](files/qe-examples.tar.gz)도 제공합니다.
- 본문(01–18장)은 개념축, [예제(E1–E13)](ex-01-si-scf.html)는 계(system)축입니다.
  "이 변수가 무엇인가"는 본문에서, "이 계를 어떻게 돌리는가"는 예제에서 찾고,
  서로 교차 링크를 따라가시면 됩니다.
- [레퍼런스(R1–R4)](ref-keywords.html)는 읽는 문서가 아니라 **찾는 문서**입니다.
  키워드·카드·오류 메시지를 사전처럼 검색하세요.
- 입력 변수의 최종 근거는 항상 설치 버전의 `Doc/INPUT_PW.txt`
  ([온라인판](https://www.quantum-espresso.org/Doc/INPUT_PW.html))입니다.

## 주제별로 들어가기

### 입문 · 시작

<div class="cards">
  <a class="card" href="01-getting-started.html">
    <div class="card-num">01 · START</div>
    <div class="card-title">시작하기</div>
    <div class="card-desc">평면파 DFT의 최소 배경, 설치 경로 선택, 설치 검증.</div>
  </a>
  <a class="card" href="02-input-structure.html">
    <div class="card-num">02 · INPUT</div>
    <div class="card-title">입력 파일 구조</div>
    <div class="card-desc">네임리스트와 카드, 최소 입력 해부, 실행 명령.</div>
  </a>
  <a class="card" href="03-units-coordinates.html">
    <div class="card-num">03 · UNITS</div>
    <div class="card-title">단위계와 좌표계</div>
    <div class="card-desc">Ry·bohr 규약, ibrav와 celldm, alat/crystal/angstrom.</div>
  </a>
</div>

### 입문 · 핵심 개념

<div class="cards">
  <a class="card" href="04-pseudopotentials.html">
    <div class="card-num">04 · PSEUDO</div>
    <div class="card-title">유사퍼텐셜</div>
    <div class="card-desc">NC/US/PAW, SSSP·PSlibrary, 파일명 해독법.</div>
  </a>
  <a class="card" href="05-convergence.html">
    <div class="card-num">05 · CONV</div>
    <div class="card-title">컷오프와 k-점 수렴</div>
    <div class="card-desc">표준 수렴 절차, meV/atom 환산, 흔한 오해.</div>
  </a>
  <a class="card" href="06-occupations.html">
    <div class="card-num">06 · SMEARING</div>
    <div class="card-title">점유수와 smearing</div>
    <div class="card-desc">절연체/금속의 occupations, smearing 종류와 degauss.</div>
  </a>
  <a class="card" href="07-scf-control.html">
    <div class="card-num">07 · SCF</div>
    <div class="card-title">SCF 수렴 제어</div>
    <div class="card-desc">mixing·diagonalization, 수렴 실패 시 진단 순서.</div>
  </a>
</div>

### 입문 · 계산 종류

<div class="cards">
  <a class="card" href="08-scf-nscf.html">
    <div class="card-num">08 · SCF/NSCF</div>
    <div class="card-title">SCF와 NSCF</div>
    <div class="card-desc">자기일관/비자기일관 계산의 역할, 출력 읽는 법.</div>
  </a>
  <a class="card" href="09-relaxation.html">
    <div class="card-num">09 · RELAX</div>
    <div class="card-title">구조 최적화</div>
    <div class="card-desc">relax/vc-relax, BFGS, if_pos, Pulay stress.</div>
  </a>
  <a class="card" href="10-dos-bands.html">
    <div class="card-num">10 · DOS·BANDS</div>
    <div class="card-title">상태밀도와 밴드</div>
    <div class="card-desc">dos.x·projwfc.x·bands.x 후처리 파이프라인.</div>
  </a>
  <a class="card" href="11-postprocessing.html">
    <div class="card-num">11 · PP</div>
    <div class="card-title">전하밀도와 퍼텐셜</div>
    <div class="card-desc">pp.x plot_num, 큐브 파일, Bader, 시각화 도구.</div>
  </a>
</div>

### 심화 · 자성과 강상관

<div class="cards">
  <a class="card" href="12-magnetism.html">
    <div class="card-num">12 · SPIN</div>
    <div class="card-title">스핀 편극과 자성</div>
    <div class="card-desc">nspin·starting_magnetization, AFM 라벨 분리, bcc Fe.</div>
  </a>
  <a class="card" href="13-dft-plus-u.html">
    <div class="card-num">13 · DFT+U</div>
    <div class="card-title">DFT+U와 HUBBARD 카드</div>
    <div class="card-desc">v7.1+ 신문법, 투영자 선택, FeO에서 갭 열기.</div>
  </a>
  <a class="card" href="14-hubbard-hp.html">
    <div class="card-num">14 · HP.X</div>
    <div class="card-title">hp.x 로 U 계산하기</div>
    <div class="card-desc">선형 응답 U, nq 수렴, self-consistent U 절차.</div>
  </a>
</div>

### 심화 · 응용과 운영

<div class="cards">
  <a class="card" href="15-surfaces.html">
    <div class="card-num">15 · SLAB</div>
    <div class="card-title">표면·슬랩과 일함수</div>
    <div class="card-desc">슬랩 생성, 쌍극자 보정, 평면평균 퍼텐셜.</div>
  </a>
  <a class="card" href="16-molecular-dynamics.html">
    <div class="card-num">16 · AIMD</div>
    <div class="card-title">분자동역학</div>
    <div class="card-desc">Born-Oppenheimer MD, SVR 온도조절, ML 데이터 샘플링.</div>
  </a>
  <a class="card" href="17-phonons-neb.html">
    <div class="card-num">17 · PH·NEB</div>
    <div class="card-title">포논과 반응 경로</div>
    <div class="card-desc">ph.x와 neb.x — 언제 필요하고 어디서 시작하는지.</div>
  </a>
  <a class="card" href="18-parallel-hpc.html">
    <div class="card-num">18 · HPC</div>
    <div class="card-title">병렬 실행과 HPC 운영</div>
    <div class="card-desc">-nk/-nd/-ni 병렬화, 스케일링 감각, 운영 습관.</div>
  </a>
</div>

### 레퍼런스

<div class="cards">
  <a class="card" href="ref-keywords.html">
    <div class="card-num">R1 · KEYWORDS</div>
    <div class="card-title">키워드 사전</div>
    <div class="card-desc">네임리스트별 주요 변수와 기본값.</div>
  </a>
  <a class="card" href="ref-cards.html">
    <div class="card-num">R2 · CARDS</div>
    <div class="card-title">카드 레퍼런스</div>
    <div class="card-desc">ATOMIC_*, K_POINTS, HUBBARD 카드 문법.</div>
  </a>
  <a class="card" href="ref-errors.html">
    <div class="card-num">R3 · ERRORS</div>
    <div class="card-title">오류 메시지 사전</div>
    <div class="card-desc">증상 → 원인 → 해결. 에러 없이 틀리는 경우 포함.</div>
  </a>
  <a class="card" href="ref-executables.html">
    <div class="card-num">R4 · BINARIES</div>
    <div class="card-title">실행 파일 목록</div>
    <div class="card-desc">pw.x부터 hp.x까지, 입력 네임리스트와 산출물.</div>
  </a>
</div>

### 예제 · 따라 하기

각 예제는 목적 → 새로 나오는 카드·변수 → 입력 파일(다운로드) → 실행 →
출력에서 확인할 것 → 직접 써보기 → 흔한 실수 순서의 자체완결 페이지입니다.
모든 수치는 QE 7.5로 실제 실행한 실측값입니다.

<div class="cards">
  <a class="card" href="ex-01-si-scf.html">
    <div class="card-num">E1</div>
    <div class="card-title">Si SCF</div>
    <div class="card-desc">가장 단순한 SCF와 출력 읽기.</div>
  </a>
  <a class="card" href="ex-02-si-ibrav0.html">
    <div class="card-num">E2</div>
    <div class="card-title">ibrav=0 다시 쓰기</div>
    <div class="card-desc">CELL_PARAMETERS로 같은 결정 재정의.</div>
  </a>
  <a class="card" href="ex-03-convergence.html">
    <div class="card-num">E3</div>
    <div class="card-title">수렴 테스트 자동화</div>
    <div class="card-desc">ecut·k점·힘 수렴 스크립트.</div>
  </a>
  <a class="card" href="ex-04-o2-molecule.html">
    <div class="card-num">E4</div>
    <div class="card-title">O₂ 분자 (삼중항)</div>
    <div class="card-desc">고립계 보정과 스핀 고정, 결합 에너지.</div>
  </a>
  <a class="card" href="ex-05-al-metal.html">
    <div class="card-num">E5</div>
    <div class="card-title">fcc Al 금속</div>
    <div class="card-desc">smearing SCF와 페르미 준위.</div>
  </a>
  <a class="card" href="ex-06-si-vcrelax.html">
    <div class="card-num">E6</div>
    <div class="card-title">Si vc-relax</div>
    <div class="card-desc">셀까지 푸는 최적화, 평형 격자상수.</div>
  </a>
  <a class="card" href="ex-07-si-dos.html">
    <div class="card-num">E7</div>
    <div class="card-title">Si DOS·PDOS</div>
    <div class="card-desc">nscf → dos.x → projwfc.x 파이프라인.</div>
  </a>
  <a class="card" href="ex-08-si-bands.html">
    <div class="card-num">E8</div>
    <div class="card-title">Si 밴드 구조</div>
    <div class="card-desc">고대칭 경로 밴드와 간접 갭.</div>
  </a>
  <a class="card" href="ex-09-fe-bcc.html">
    <div class="card-num">E9</div>
    <div class="card-title">bcc Fe 강자성</div>
    <div class="card-desc">스핀 편극 SCF와 자기모멘트 2.2 μB.</div>
  </a>
  <a class="card" href="ex-10-feo-afm.html">
    <div class="card-num">E10</div>
    <div class="card-title">FeO AFM (GGA 실패)</div>
    <div class="card-desc">GGA가 FeO를 금속으로 예측하는 것을 확인.</div>
  </a>
  <a class="card" href="ex-11-feo-hubbard.html">
    <div class="card-num">E11</div>
    <div class="card-title">FeO DFT+U</div>
    <div class="card-desc">HUBBARD 카드와 Hubbard 분리, 그리고 유명한 함정.</div>
  </a>
  <a class="card" href="ex-12-feo-hp.html">
    <div class="card-num">E12</div>
    <div class="card-title">hp.x 로 U 계산</div>
    <div class="card-desc">선형 응답으로 U를 제일원리 계산.</div>
  </a>
  <a class="card" href="ex-13-slab-md.html">
    <div class="card-num">E13</div>
    <div class="card-title">슬랩과 AIMD</div>
    <div class="card-desc">슬랩 생성·일함수·BOMD 샘플링.</div>
  </a>
</div>

<div class="divider"></div>

## Fe–O 계로 가는 최단 경로

전이금속 산화물(예: 철 산화)이 최종 목표라면, 예제를 다음 순서로 축약해
따라가실 수 있습니다.

1. **Si (E1–E3, E6–E8)** — 문법·수렴·최적화 감각. 2~3일이면 충분합니다.
2. **bcc Fe (E9)** — 금속 + 강자성. smearing과 자화 수렴의 어려움을 여기서
   미리 겪어 둡니다.
3. **FeO AFM (E10)** — DFT+U 없이는 금속으로 나오는 것을 **직접 확인**합니다.
4. **FeO + U (E11–E12)** — `HUBBARD` 카드로 U를 켜 Hubbard 분리를 확인하고
   (그리고 이상적 큐빅 셀의 유명한 함정까지 겪고), `hp.x`로 U를 제일원리
   계산합니다. 이 한 사이클이 전체 학습의 핵심입니다.
5. **슬랩 + AIMD (E13)** — ML 퍼텐셜 학습 데이터 생성의 출발점입니다.

ML 퍼텐셜 학습 데이터가 목표라면 기준이 하나 달라집니다. 에너지가 아니라
**힘(force)에 대해 수렴**을 잡아야 하고, 모든 구조에서 컷오프·k-점·smearing·U를
완전히 동일하게 고정해야 합니다. 설정이 섞인 데이터셋은 학습 단계에서 복구가
불가능합니다.

## 자기 점검 체크리스트

각 구간을 마친 뒤 아래에 답할 수 있어야 다음으로 넘어가세요.

- **기초 (E1–E3)** — `ecutwfc`와 `ecutrho`의 차이를 물리적으로 설명할 수 있다.
  `alat`/`crystal`/`angstrom` 좌표를 서로 변환할 수 있다. 총에너지의 절대값을
  왜 비교하면 안 되는지 설명할 수 있다.
- **계의 종류 (E4–E6)** — 금속·반도체·분자에 각각 어떤 `occupations`를 쓰는지
  안다. `starting_magnetization`과 `tot_magnetization`의 차이를 안다.
  `vc-relax` 후 `scf`를 다시 돌려야 하는 이유(Pulay stress)를 설명할 수 있다.
- **후처리 (E7–E8)** — scf → nscf → dos.x 파이프라인에서 `prefix`/`outdir`의
  역할을 안다. `tetrahedra_opt`가 왜 Γ 중심 그리드를 요구하는지 안다.
- **자성·강상관 (E9–E12)** — 같은 원소를 다른 라벨로 나눠야 AFM을 만들 수 있는
  이유를 안다. total/absolute magnetization으로 자기 배열을 판별할 수 있다.
  `HUBBARD` 카드의 투영자 선택이 U 값의 의미를 바꾼다는 것을 안다.
  GGA가 FeO를 금속으로 예측하는 것을 직접 확인했다.

## 인용에 관하여

Quantum ESPRESSO를 사용한 연구를 발표할 때는 다음 논문들을 인용하는 것이
관례입니다. 실제 사용한 모듈의 원저 논문(예: `hp.x`)과 유사퍼텐셜의 출처도
함께 밝히는 것이 좋습니다.

- P. Giannozzi 외. *J. Phys.: Condens. Matter* **2009**, *21*, 395502.
- P. Giannozzi 외. *J. Phys.: Condens. Matter* **2017**, *29*, 465901.
- P. Giannozzi 외. *J. Chem. Phys.* **2020**, *152*, 154105.
- (`hp.x` 사용 시) I. Timrov, N. Marzari, M. Cococcioni.
  *Comput. Phys. Commun.* **2022**, *279*, 108455.

<div class="note">
  <div class="note-title">참고 자료</div>
  <p>
    1차 출처는 항상 설치 버전의 <code>Doc/</code> 폴더
    (<code>INPUT_PW.txt</code>, <code>user_guide.pdf</code>,
    <code>Hubbard_input.pdf</code>)와
    <a href="https://www.quantum-espresso.org/documentation/input-data-description/">공식 입력 변수 문서</a>,
    그리고 소스 트리의 <code>PW/examples/</code>·<code>test-suite/</code>입니다.
    학습 자료로는 <a href="https://compmatphys.epotentia.com/">Cottenier의 온라인 DFT 강좌</a>,
    <a href="http://www.fisica.uniud.it/~giannozz/QE-Tutorial/">Giannozzi의 Hands-on Tutorial</a>,
    MIT OCW 3.320, 그리고 책으로 Sholl &amp; Steckel(입문)과 R. Martin(레퍼런스)을
    권합니다. 막히면 <a href="https://www.mail-archive.com/users@lists.quantum-espresso.org/">QE users
    메일링 리스트 아카이브</a>를 먼저 검색하세요 — 대부분의 문제가 이미 답변되어
    있습니다.
  </p>
</div>
