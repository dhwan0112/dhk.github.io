---
layout: page
title: Guides
description: 직접 정리한 계산화학·연구 도구 한국어 사용자 가이드 모음
permalink: /guides/
---

<section class="blog-list">
    <div class="container">
        <div class="posts-container">
            <article class="post-preview">
                <div class="post-header">
                    <h2 class="post-title">
                        <a href="{{ '/guides/orca/' | relative_url }}">ORCA 사용자 가이드</a>
                    </h2>
                    <div class="post-meta">
                        <span class="post-category"><i class="fas fa-atom"></i> Quantum Chemistry</span>
                        <span class="post-category"><i class="fas fa-book"></i> ORCA 6.0.0</span>
                    </div>
                </div>
                <div class="post-excerpt">
                    <p>
                        양자화학 계산 프로그램 ORCA의 한국어 사용자 가이드입니다.
                        입력 파일 구조, 단일점 에너지, 구조 최적화, 진동수, 전이 상태,
                        들뜬 상태(TD-DFT), 용매 효과, DLPNO-CCSD(T), 베이시스 세트,
                        DFT 함수 선택, 운영 팁까지 14개 챕터로 구성되어 있습니다.
                    </p>
                    <a href="{{ '/guides/orca/' | relative_url }}" class="read-more">가이드 열기 →</a>
                </div>
                <div class="post-tags">
                    <span class="tag">ORCA</span>
                    <span class="tag">DFT</span>
                    <span class="tag">Coupled Cluster</span>
                    <span class="tag">NEB</span>
                    <span class="tag">TD-DFT</span>
                </div>
            </article>

            <article class="post-preview">
                <div class="post-header">
                    <h2 class="post-title">
                        <a href="{{ '/guides/lammps/' | relative_url }}">LAMMPS 한국어 입문 가이드</a>
                    </h2>
                    <div class="post-meta">
                        <span class="post-category"><i class="fas fa-cubes"></i> Molecular Dynamics</span>
                        <span class="post-category"><i class="fas fa-graduation-cap"></i> 입문 + 응용</span>
                    </div>
                </div>
                <div class="post-excerpt">
                    <p>
                        Lennard-Jones 액체 한 예제부터 시작해 LAMMPS 입력 스크립트의 4단계
                        구조와 단위계, 시스템 정의, 상호작용 모델, 시뮬레이션 셋업, 출력과
                        분석, 트러블슈팅까지 단계별로 풀어쓴 한국어 입문 가이드입니다(8장).
                        그 다음 응용 시리즈로 Cu(100)/Cu(111) 표면 위 벤젠-에탄올 경쟁 흡착
                        문제에 OPLS-AA · TraPPE-UA · PPPM · MSM 네 조합을 비교하는 9장이
                        이어집니다.
                    </p>
                    <a href="{{ '/guides/lammps/' | relative_url }}" class="read-more">가이드 열기 →</a>
                </div>
                <div class="post-tags">
                    <span class="tag">LAMMPS</span>
                    <span class="tag">Molecular Dynamics</span>
                    <span class="tag">LJ · EAM · OPLS</span>
                    <span class="tag">Cu Surface (응용)</span>
                </div>
            </article>

            <article class="post-preview">
                <div class="post-header">
                    <h2 class="post-title">
                        <a href="{{ '/guides/qe/' | relative_url }}">Quantum ESPRESSO 한국어 입문 가이드</a>
                    </h2>
                    <div class="post-meta">
                        <span class="post-category"><i class="fas fa-wave-square"></i> DFT · 제일원리</span>
                        <span class="post-category"><i class="fas fa-book"></i> QE 7.5 · 입문 + 심화</span>
                    </div>
                </div>
                <div class="post-excerpt">
                    <p>
                        실리콘 SCF 한 예제에서 출발해 입력 문법, 수렴 테스트, 구조 최적화,
                        밴드·DOS 후처리를 거쳐 스핀 편극과 반강자성, DFT+U의 HUBBARD 카드,
                        hp.x에 의한 U 계산, 슬랩·ab initio MD까지 다루는 한국어 가이드입니다
                        (본문 18장 + 레퍼런스 4). Si부터 bcc Fe, FeO(AFM)까지 예제 13종을
                        QE 7.5로 전부 실제 실행해 실측 수치·그림과 함께 정리했고, 입력
                        파일도 내려받을 수 있습니다.
                    </p>
                    <a href="{{ '/guides/qe/' | relative_url }}" class="read-more">가이드 열기 →</a>
                </div>
                <div class="post-tags">
                    <span class="tag">Quantum ESPRESSO</span>
                    <span class="tag">DFT+U</span>
                    <span class="tag">Band Structure · DOS</span>
                    <span class="tag">FeO · 자성</span>
                    <span class="tag">AIMD</span>
                </div>
            </article>
        </div>
    </div>
</section>
