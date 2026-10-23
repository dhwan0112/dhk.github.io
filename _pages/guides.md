---
layout: page
title: Guides
description: 계산화학을 시작하는 사람을 위해 쓴 프로그램 사용 가이드입니다. 대부분 한국어로 썼고 일부는 영어판이 있습니다. Quantum ESPRESSO 가이드는 영어로 썼습니다.
permalink: /guides/
---

<div class="prose-page">

<article class="guide" id="orca">
    <h2><a href="{{ '/guides/orca/' | relative_url }}">ORCA 사용자 가이드</a></h2>
    <p class="guide-meta">양자화학. ORCA 6.0.0 기준, 한국어와 영어. 17장.</p>
    <p>입력 파일 구조에서 시작해 단일점 에너지, 구조 최적화, 진동수, 전이 상태, TD-DFT, 용매 효과, DLPNO-CCSD(T), 베이시스 세트와 범함수 선택, CASSCF, GFN-xTB와 분자동역학까지 다룹니다.</p>
</article>

<article class="guide" id="xtb">
    <h2><a href="{{ '/guides/xtb/' | relative_url }}">xtb와 CREST 사용자 가이드</a></h2>
    <p class="guide-meta">반경험 방법과 컨포머 탐색. xtb 6.7, CREST 3. 6장.</p>
    <p>알라닌 다이펩타이드 한 분자로 처음부터 끝까지 진행합니다. 최적화와 진동수, 용매 모델, 분자동역학과 메타다이내믹스, CREST 컨포머 앙상블을 거쳐 r2SCAN-3c로 순위를 다시 매기는 데까지 갑니다. 궤적 애니메이션과 그림은 NUS HPC에서 돌린 계산에서 나온 것입니다.</p>
</article>

<article class="guide" id="lammps">
    <h2><a href="{{ '/guides/lammps/' | relative_url }}">LAMMPS 입문 가이드</a></h2>
    <p class="guide-meta">고전 분자동역학. LAMMPS 22 Jul 2024 기준. 입문 8장, 응용 9장.</p>
    <p>Lennard-Jones 액체 예제 하나로 입력 스크립트의 네 단계 구조, 단위계, 시스템 정의, 상호작용 모델, 실행 설정, 출력과 분석, 문제 해결을 차례로 설명합니다. 응용 편에서는 구리 표면 위 벤젠–에탄올 경쟁 흡착에 OPLS-AA, TraPPE-UA, PPPM, MSM 네 조합을 적용해 비교합니다.</p>
</article>

<article class="guide" id="qe">
    <h2><a href="{{ '/guides/qe/' | relative_url }}">Quantum ESPRESSO: a practical guide</a></h2>
    <p class="guide-meta">Plane-wave DFT. QE 7.5, in English. 18 chapters and 4 reference pages.</p>
    <p>Starts from a single silicon SCF calculation and goes through input syntax, convergence tests, structure optimisation, and bands and DOS. Later chapters cover spin polarisation and antiferromagnetism, the HUBBARD card for DFT+U, computing U with hp.x, and slabs with ab initio MD. Each of the 13 examples, from Si to bcc Fe and antiferromagnetic FeO, comes with its input files, figures and the numbers QE 7.5 printed.</p>
</article>

<article class="guide" id="linux">
    <h2><a href="{{ '/guides/linux/' | relative_url }}">Linux 스타터팩</a></h2>
    <p class="guide-meta">Linux와 HPC 입문. 한국어와 영어. 11장.</p>
    <p>WSL이나 macOS 터미널을 준비하는 데서 시작해 파일과 권한, 프로세스와 환경 변수, ssh 키와 파일 전송, tmux, 클러스터에 첫 작업을 제출하는 방법까지 다룹니다. 마지막에 쓸 만한 프로그램 목록과 치트시트를 붙였습니다. 명령 아래의 출력은 실제 실행 결과입니다.</p>
</article>

<article class="guide" id="shell">
    <h2><a href="{{ '/guides/shell/' | relative_url }}">셸 스크립팅 가이드</a></h2>
    <p class="guide-meta">bash. 한국어와 영어. 9장.</p>
    <p>변수와 반복문, 함수와 getopts, <code>set -euo pipefail</code>과 trap, grep, sed, awk로 ORCA, QE, LAMMPS, xtb 출력에서 값을 뽑는 법, PBS와 Slurm 작업 스크립트와 작업 배열, 파라미터 스윕을 다룹니다. 예제 스크립트는 ShellCheck 검사를 통과했습니다.</p>
</article>

</div>
