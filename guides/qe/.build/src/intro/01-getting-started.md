---
layout: default
title: "1. 시작하기"
---

# 1. 시작하기
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1.1 Quantum ESPRESSO란

Quantum ESPRESSO는 평면파 기저와 유사퍼텐셜을 쓰는 밀도범함수이론(DFT) 계산
패키지입니다. 핵심 프로그램은 자체무결(self-consistent) 전자구조와 전체 에너지,
힘·응력을 계산하는 `pw.x`(PWscf)이고, 그 결과를 받아 밴드구조(`bands.x`),
상태밀도(`dos.x`, `projwfc.x`), 포논(`ph.x`) 등을 계산하는 후처리 프로그램들이
함께 배포됩니다.

본 가이드는 **Quantum ESPRESSO 7.5**(2025년 8월 릴리스)를 기준으로 하며, 모든
출력은 conda-forge 빌드로 실제 실행해 얻은 값입니다.

## 1.2 설치 확인

가장 간편한 설치는 conda(또는 mamba/micromamba)입니다.

| 환경 | 설치 방법 |
|------|-----------|
| Conda / Mamba | `conda install -c conda-forge qe` |
| Ubuntu/Debian | `sudo apt install quantum-espresso` |
| macOS (Homebrew) | `brew install quantum-espresso` |
| HPC | `module load quantum-espresso` 또는 소스 빌드 |

설치되면 프로그램들이 `pw.x`, `dos.x`, `bands.x`, `projwfc.x`, `pp.x`, `ph.x`
등의 이름으로 생깁니다. 다음으로 버전을 확인합니다.

```bash
pw.x -h | head        # 사용법
echo | pw.x | head -3 # 배너에서 버전 확인
```

출력 첫 줄에 `Program PWSCF v.7.5 ...` 처럼 버전이 보이면 정상입니다.

## 1.3 첫 계산 — 실리콘 SCF

QE의 가장 단순한 예제는 실리콘 결정의 전체 에너지를 구하는 SCF 계산입니다.
다이아몬드 구조 실리콘의 원시 셀(원자 2개)을 다음과 같이 `si.scf.in` 으로
저장합니다.

```fortran
&control
  calculation = 'scf'
  prefix      = 'si'
  outdir      = './out'
  pseudo_dir  = './pseudo'
/
&system
  ibrav     = 2
  celldm(1) = 10.26
  nat       = 2
  ntyp      = 1
  ecutwfc   = 40.0
  ecutrho   = 320.0
/
&electrons
  conv_thr    = 1.0d-8
  mixing_beta = 0.7
/
ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-rrkjus_psl.1.0.0.UPF
ATOMIC_POSITIONS (alat)
  Si  0.00 0.00 0.00
  Si  0.25 0.25 0.25
K_POINTS (automatic)
  8 8 8  0 0 0
```

`ibrav = 2` 는 면심입방(FCC) 브라베 격자, `celldm(1) = 10.26` 은 격자 상수
(bohr 단위, 5.43 Å에 해당)입니다. 원자 두 개를 (0,0,0)과 (¼,¼,¼)에 두면
다이아몬드 구조가 됩니다. `ecutwfc`(파동함수 컷오프)와 `ecutrho`(전하밀도 컷오프)는
[03장](03-pseudopotentials.html)에서, `K_POINTS`는 [04장](04-kpoints.html)에서
자세히 다룹니다.

유사퍼텐셜 파일(`Si.pbe-n-rrkjus_psl.1.0.0.UPF`)은 `pseudo_dir` 로 지정한
디렉토리에 있어야 합니다. 이 파일은 [SSSP](https://www.materialscloud.org/discover/sssp)
같은 라이브러리에서 받습니다([03장](03-pseudopotentials.html) 참고).

실행은 다음과 같이 합니다.

```bash
# 직렬
pw.x -in si.scf.in > si.scf.out

# 병렬 (예: 8 프로세스, k점을 8개 풀로 분할)
mpirun -np 8 pw.x -nk 8 -in si.scf.in > si.scf.out
```

<div class="tip">
  <div class="note-title">작은 계는 스레드보다 MPI가 빠릅니다</div>
  <p>
    OpenMP 스레드를 잔뜩 띄우면 원자 몇 개짜리 계는 오히려 느려집니다.
    <code>export OMP_NUM_THREADS=1</code> 로 스레드를 끄고 <code>mpirun -np N</code>
    로 k점을 병렬화(<code>-nk</code>)하는 편이 보통 훨씬 빠릅니다. 위 예제는
    이렇게 하면 몇 초 만에 끝납니다.
  </p>
</div>

## 1.4 출력 결과 살펴보기

`si.scf.out` 을 보면 SCF 순환이 한 줄씩 찍힙니다. 아래는 본 가이드를 작성하며
QE 7.5로 실제 실행해 얻은 값입니다.

```text
     iteration #  1     ecut=    40.00 Ry     beta= 0.70
     total energy              =     -22.83676466 Ry
     estimated scf accuracy    <       0.05408644 Ry
     ...
     iteration #  5     ecut=    40.00 Ry     beta= 0.70
     total energy              =     -22.83941737 Ry
     estimated scf accuracy    <       0.00000047 Ry
     End of self-consistent calculation

!    total energy              =     -22.83941780 Ry
     estimated scf accuracy    <          2.8E-09 Ry

     The total energy is the sum of the following terms:
     one-electron contribution =       5.17095299 Ry
     hartree contribution      =       1.10074142 Ry
     xc contribution           =     -12.31018265 Ry
     ewald contribution        =     -16.80092957 Ry

     highest occupied level (ev):     6.2117
```

- `estimated scf accuracy` 가 매 반복 줄어들다 `conv_thr`(여기서는 10⁻⁸ Ry)
  아래로 내려가면 수렴한 것입니다.
- **느낌표(`!`)가 붙은 `total energy`** 가 최종 수렴 전체 에너지입니다. 실리콘
  원시 셀 기준 −22.8394 Ry 가 나왔습니다.
- 그 아래 에너지 분해(one-electron / hartree / xc / ewald)는 전체 에너지가
  어떤 항들의 합인지 보여 줍니다.
- 반도체라 페르미 준위 대신 `highest occupied level`(최고 점유 준위, 6.21 eV)이
  찍힙니다. 금속이면 `the Fermi energy is ...` 로 나옵니다([05장](05-scf-convergence.html)).

파일 끝에 `JOB DONE.` 가 있으면 정상 종료입니다.

<div class="tip">
  <div class="note-title">전체 예제로 보기</div>
  <p>
    이 SCF 예제의 전체 입력·실행과 컷오프·k점 수렴 그래프는
    <a href="ex-01-si-scf.html">예제 E1 — Si SCF</a> 에 정리돼 있습니다.
  </p>
</div>

## 1.5 다음 단계

다음 장에서는 이 입력 파일을 한 줄씩 뜯어보며, `pw.x` 입력이 어떤
**네임리스트와 카드**로 이루어지는지 살펴봅니다.
