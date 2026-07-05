---
layout: default
title: "Quantum ESPRESSO 한국어 입문 가이드"
permalink: /
---

# Quantum ESPRESSO 한국어 입문 가이드

Quantum ESPRESSO(QE)는 평면파(plane-wave) 기저와 유사퍼텐셜(pseudopotential)을
쓰는 오픈소스 제일원리(DFT) 계산 패키지입니다. 결정·표면·분자의 전자구조,
전체 에너지, 힘과 응력, 밴드구조·상태밀도, 포논 등을 계산할 수 있으며,
학술용으로 무료로 배포됩니다.

본 가이드는 QE를 처음 접하는 사용자가 `pw.x` 앞에서 길을 잃지 않도록 정리한
한국어 입문서입니다. 가장 단순한 실리콘(Si) SCF 예제부터 시작해 입력 파일의
네임리스트 구조, 유사퍼텐셜과 컷오프, k점 샘플링, SCF 수렴, 구조 최적화,
밴드구조와 상태밀도까지 차근차근 다룹니다.

## 이 가이드에 관하여

모든 예제는 **Quantum ESPRESSO 7.5**(2025년 8월 릴리스, conda-forge 빌드)를
기준으로 실제 실행해 작성했습니다. 명령·입력 변수 이름은 공식 매뉴얼의 원어
표기를 그대로 쓰며, 상세 옵션은 각 프로그램의 입력 설명서
([INPUT_PW](https://www.quantum-espresso.org/Doc/INPUT_PW.html) 등)를 직접
참조하시기를 권합니다.

## 주제별로 들어가기

### 처음 시작한다면

<div class="cards">
  <a class="card" href="01-getting-started.html">
    <div class="card-num">01 · GETTING STARTED</div>
    <div class="card-title">시작하기</div>
    <div class="card-desc">설치 확인, pw.x 첫 실행, 실리콘 SCF, 출력 읽기.</div>
  </a>
  <a class="card" href="02-input-structure.html">
    <div class="card-num">02 · INPUT</div>
    <div class="card-title">입력 파일 구조</div>
    <div class="card-desc">네임리스트(&control/&system/&electrons)와 카드.</div>
  </a>
</div>

### 계산 준비하기

<div class="cards">
  <a class="card" href="03-pseudopotentials.html">
    <div class="card-num">03 · PSEUDO</div>
    <div class="card-title">유사퍼텐셜</div>
    <div class="card-desc">NC/US/PAW, SSSP, ecutwfc·ecutrho 컷오프.</div>
  </a>
  <a class="card" href="04-kpoints.html">
    <div class="card-num">04 · K-POINTS</div>
    <div class="card-title">k점 샘플링</div>
    <div class="card-desc">Monkhorst-Pack 격자, 자동/명시, 수렴 점검.</div>
  </a>
</div>

### 계산하고 최적화하기

<div class="cards">
  <a class="card" href="05-scf-convergence.html">
    <div class="card-num">05 · SCF</div>
    <div class="card-title">SCF와 수렴</div>
    <div class="card-desc">SCF 순환, mixing_beta·conv_thr, 금속 smearing.</div>
  </a>
  <a class="card" href="06-relax.html">
    <div class="card-num">06 · RELAX</div>
    <div class="card-title">구조 최적화</div>
    <div class="card-desc">힘과 응력, relax·vc-relax, &ions/&cell.</div>
  </a>
</div>

### 결과 보기와 운영

<div class="cards">
  <a class="card" href="07-bands-dos.html">
    <div class="card-num">07 · BANDS · DOS</div>
    <div class="card-title">밴드와 DOS</div>
    <div class="card-desc">scf→nscf→bands.x, dos.x, projwfc.x.</div>
  </a>
  <a class="card" href="08-troubleshooting.html">
    <div class="card-num">08 · TIPS</div>
    <div class="card-title">트러블슈팅과 운영</div>
    <div class="card-desc">자주 나는 오류, 병렬(-nk), 성능 감각.</div>
  </a>
</div>

### 예제 따라 하기

각 예제는 목적 → 입력 파일 → 실행 → 출력·그림 순으로 자체완결 페이지에
정리돼 있습니다.

<div class="cards">
  <a class="card" href="ex-01-si-scf.html">
    <div class="card-num">예제 · E1</div>
    <div class="card-title">Si SCF</div>
    <div class="card-desc">실리콘 SCF 전체 에너지와 ecutwfc·k점 수렴.</div>
  </a>
  <a class="card" href="ex-02-si-bands.html">
    <div class="card-num">예제 · E2</div>
    <div class="card-title">Si 밴드 + DOS</div>
    <div class="card-desc">scf → nscf → bands.x 밴드구조와 dos.x 상태밀도.</div>
  </a>
  <a class="card" href="ex-03-metal-smearing.html">
    <div class="card-num">예제 · E3</div>
    <div class="card-title">금속 smearing</div>
    <div class="card-desc">알루미늄을 smearing 으로 SCF, 페르미 준위 확인.</div>
  </a>
  <a class="card" href="ex-04-relax.html">
    <div class="card-num">예제 · E4</div>
    <div class="card-title">구조 최적화</div>
    <div class="card-desc">힘·응력 기반 relax/vc-relax 를 실제로 실행.</div>
  </a>
</div>

<div class="divider"></div>

## 인용에 관하여

Quantum ESPRESSO를 사용한 연구를 발표할 때는 다음 두 논문을 함께 인용하는 것이
관례입니다. 여기에 더해, 실제로 사용한 유사퍼텐셜의 출처도 함께 밝히는 것이
좋습니다.

- P. Giannozzi 외. *J. Phys.: Condens. Matter* **2009**, *21*, 395502.
- P. Giannozzi 외. *J. Phys.: Condens. Matter* **2017**, *29*, 465901.

<div class="note">
  <div class="note-title">참고 자료</div>
  <p>
    본 가이드의 내용은 QE 공식 문서
    (<a href="https://www.quantum-espresso.org/documentation/">quantum-espresso.org</a>)를
    기반으로 합니다. 각 프로그램의 입력 변수는 <code>INPUT_PW.html</code> 등
    입력 설명서에 변수별로 정리돼 있으니, 더 깊이 알고 싶은 변수가 나오면 함께
    보시기를 권합니다.
  </p>
</div>
