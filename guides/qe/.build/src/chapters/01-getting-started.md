---
title: "01. 시작하기"
---

# 01. 시작하기

## 목차
{:.toc-title}

1. TOC
{:toc}

## QE를 만지기 전에 — 최소 배경 이론

배경 이론을 전부 이해하고 코드를 만지겠다는 계획은 대부분 실패합니다.
아래 여섯 개념의 **정성적 의미**만 잡고 바로 설치로 넘어가는 편이 훨씬
빠릅니다. 각 개념이 어느 입력 변수와 연결되는지가 핵심입니다.

| 개념 | 왜 필요한가 | QE에서 대응되는 입력 |
|---|---|---|
| Kohn–Sham DFT와 SCF 루프 | 출력의 "estimated scf accuracy"를 읽으려면 필수 | `conv_thr`, `mixing_beta`, `electron_maxstep` |
| 평면파 기저와 컷오프 | 기저 크기 = 정확도 = 비용 | `ecutwfc`, `ecutrho` |
| 주기 경계조건 / Bloch 정리 / Brillouin zone | 왜 k-점을 샘플링하는가 | `K_POINTS` |
| 유사퍼텐셜 (NC / US / PAW) | 컷오프와 정확도를 동시에 지배 | `ATOMIC_SPECIES`, `pseudo_dir` |
| 교환-상관 범함수 계층 | LDA/GGA의 한계가 곧 DFT+U의 존재 이유 | 유사퍼텐셜 파일에 내장, `input_dft`로 override |
| 금속의 부분 점유와 smearing | 금속·자성계 수렴의 90% | `occupations`, `smearing`, `degauss` |

이론 자료로는 [Cottenier의 온라인 DFT 강좌](https://compmatphys.epotentia.com/)
(QE 실습이 이론과 함께 붙어 있어 입문 효율이 가장 좋습니다),
[Giannozzi의 Hands-on Tutorial](http://www.fisica.uniud.it/~giannozz/QE-Tutorial/)
(QE 개발 주역이 직접 만든 자료), MIT OCW 3.320, 그리고 책으로는
Sholl &amp; Steckel(입문용)과 R. Martin(레퍼런스용)을 권합니다.

## 설치 경로 선택

| 방법 | 장점 | 단점 | 추천 상황 |
|---|---|---|---|
| 소스 빌드 (`./configure && make all`) | MKL/ScaLAPACK 최적화, GPU 빌드 가능 | 의존성 지옥 | HPC, 성능이 중요한 경우 |
| conda (`conda install -c conda-forge qe`) | 5분 설치 | 성능 최적화 제한 | 로컬 학습·테스트 |
| deb 패키지 / 배포판 | 가장 쉬움 | 버전이 뒤처질 수 있음 | 로컬 학습 |

로컬 워크스테이션에서는 **conda로 먼저 깔고 학습을 시작**한 뒤, HPC에서
소스 빌드를 익히는 순서를 권합니다. 설치에서 며칠을 태우는 것이 가장 흔한
이탈 지점입니다. GPU 빌드(`--with-cuda`)는 NVHPC 컴파일러가 필요하고
12GB급 VRAM으로는 스핀 편극된 전이금속 산화물의 큰 셀을 담기 어려우므로,
초기 학습에는 CPU 빌드로 충분합니다.

본 가이드의 모든 실측은 conda-forge `qe 7.5` 빌드(WSL Ubuntu, 16코어)에서
실행했습니다. 작은 셀은 이 환경으로도 수 초~수 분이면 돕니다.

```bash
# micromamba/conda 어느 쪽이든 동일합니다
conda create -n qe -c conda-forge qe python numpy matplotlib
conda activate qe
pw.x -in /dev/null 2>&1 | head -5     # 버전 배너 확인
```

## 환경 변수와 디렉터리 구조

```bash
export ESPRESSO_PSEUDO=$HOME/pseudo     # 유사퍼텐셜 저장소
export ESPRESSO_TMPDIR=/scratch/$USER   # 대용량 임시파일 (반드시 빠른 디스크)
```

권장 작업 디렉터리 구조:

```
project/
├── pseudo/          # UPF 파일
├── 01_convergence/  # 수렴 테스트
├── 02_relax/
├── 03_scf/
└── scripts/
```

`outdir`(임시 파일)과 `pseudo_dir`은 입력에서 명시할 수도 있고, 위 환경
변수를 기본값으로 쓸 수도 있습니다. `outdir`은 파동함수·전하밀도가 쌓이는
곳이므로 **반드시 빠른 디스크**를 가리키게 하세요.

## 설치 검증 — 여기서 반드시 해야 할 것

먼저 배너를 확인합니다.

```bash
which pw.x
pw.x -in /dev/null 2>&1 | head -20
```

확인 포인트:

- 배너에 `Parallel version (MPI), running on N processors`가 뜨는가
- `Number of MPI processes` / `Threads/MPI process`가 의도한 값인가

QE 소스 트리가 있다면 **`PW/examples/`와 `test-suite/`**를 여세요.
이것은 단순한 테스트가 아니라 **가장 좋은 교재**입니다.

```bash
cd PW/examples/example01
./run_example
ls results/            # 생성된 입출력 파일을 전부 열어볼 것
```

`example01`부터 순서대로 입력 파일을 열어 각 예제가 무엇을 시연하는지
확인하세요. 버전 정합성 면에서 서드파티 튜토리얼보다 이쪽이 안전합니다.

## 유사퍼텐셜 확보

원소별 UPF 파일이 있어야 첫 계산이 돕니다. 어디서 받고 어떻게 고르는지는
[04장](04-pseudopotentials.html)에서 자세히 다루며, 본 가이드의 예제는
PSlibrary PAW(`*.pbe-*-kjpaw_psl.1.0.0.UPF`)를 씁니다.
[QE 공식 유사퍼텐셜 페이지](https://pseudopotentials.quantum-espresso.org/)에서
원소별로 내려받을 수 있습니다.

```bash
mkdir -p pseudo tmp
# 예: Si PAW
curl -O https://pseudopotentials.quantum-espresso.org/upf_files/Si.pbe-n-kjpaw_psl.1.0.0.UPF
mv *.UPF pseudo/
```

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    OpenMP 스레드와 MPI를 동시에 과다 설정하면 작은 계에서 오히려 수십 배
    느려집니다. 본 가이드의 2원자 Si SCF는 스레드 16개 설정에서 약 2분,
    <code>OMP_NUM_THREADS=1</code> + <code>mpirun -np 6 pw.x -nk 6</code>
    설정에서 2.8초가 걸렸습니다. 병렬 설정은
    <a href="18-parallel-hpc.html">18장</a>을 참고하세요.
  </p>
</div>

## 관련 예제

- [E1 · Si SCF](ex-01-si-scf.html) — 설치가 끝났다면 바로 첫 계산으로.
- [E3 · 수렴 테스트 자동화](ex-03-convergence.html) — 첫 계산 다음에 반드시.
