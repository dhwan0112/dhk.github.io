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
                        <a href="{{ '/guides/qe/' | relative_url }}">Quantum ESPRESSO: A Practical Guide</a>
                    </h2>
                    <div class="post-meta">
                        <span class="post-category"><i class="fas fa-wave-square"></i> DFT · First principles</span>
                        <span class="post-category"><i class="fas fa-book"></i> QE 7.5 · English</span>
                    </div>
                </div>
                <div class="post-excerpt">
                    <p>
                        An English-language guide that starts from a single silicon SCF and
                        works through input syntax, convergence testing, structure
                        optimization, and band/DOS post-processing, then continues into spin
                        polarization and antiferromagnetism, the HUBBARD card for DFT+U,
                        computing U with hp.x, and slabs with ab initio MD (18 chapters plus
                        4 reference pages). All 13 examples, from Si to bcc Fe and
                        antiferromagnetic FeO, were actually executed with QE 7.5; the pages
                        include the measured numbers, figures, and downloadable inputs.
                    </p>
                    <a href="{{ '/guides/qe/' | relative_url }}" class="read-more">Open the guide →</a>
                </div>
                <div class="post-tags">
                    <span class="tag">Quantum ESPRESSO</span>
                    <span class="tag">DFT+U</span>
                    <span class="tag">Band Structure · DOS</span>
                    <span class="tag">FeO · Magnetism</span>
                    <span class="tag">AIMD</span>
                </div>
            </article>
        </div>
    </div>
</section>
