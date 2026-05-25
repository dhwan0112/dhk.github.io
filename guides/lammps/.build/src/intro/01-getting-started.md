---
layout: default
title: "1. 시작하기"
nav_order: 2
---

# 1. 시작하기
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1.1 LAMMPS란

LAMMPS는 Sandia 국립연구소가 1990년대 후반부터 개발해온 범용 분자동역학
시뮬레이션 패키지입니다. 원자, 입자, 거대 분자, 메타입자 등 다양한
"점 입자" 시스템을 다룰 수 있으며, 특히 다음과 같은 점에서 강점이 있습니다.

- **확장성**: 같은 입력 스크립트를 노트북 한 대부터 수만 코어 슈퍼컴퓨터까지
  거의 그대로 사용할 수 있습니다. 코드 자체가 MPI 기반으로 설계되었습니다.
- **모델 다양성**: Lennard-Jones, EAM, Tersoff, ReaxFF, OPLS, AMBER, CHARMM,
  COMPASS, MEAM, machine learning potential 등 수십 종의 상호작용 모델을
  내장 또는 외부 패키지로 지원합니다.
- **활발한 사용자 커뮤니티**: 공식 매뉴얼은 1500쪽이 넘고,
  포럼(lammps.org/forum.html)에는 매일 새로운 질문과 답변이 올라옵니다.

본 가이드는 LAMMPS를 처음 설치하고 첫 입력 스크립트를 돌리는 단계부터
시작합니다.

## 1.2 설치 확인

LAMMPS는 다음과 같이 여러 경로로 설치할 수 있습니다.

| OS / 환경 | 가장 빠른 설치 방법 |
|-----------|---------------------|
| Linux (Ubuntu/Debian) | `sudo apt install lammps` |
| Linux (Conda) | `conda install -c conda-forge lammps` |
| macOS (Homebrew) | `brew install lammps` |
| Windows | WSL2 후 Ubuntu 방식 또는 공식 바이너리 (`lammps.org/download.html`) |
| HPC / 워크스테이션 | `module load lammps` 또는 소스 빌드 |

소스에서 직접 빌드하면 어떤 패키지를 포함할지 세밀하게 조절할 수 있지만,
입문 단계에서는 패키지 매니저 설치만으로 충분합니다.

설치가 끝나면 터미널에서 다음을 실행해 보십시오.

```bash
lmp -h
```

도움말 메시지가 출력되면서 빌드에 포함된 패키지 목록이 보이면 설치가 정상입니다.
실행 파일의 이름은 빌드 방식에 따라 `lmp`, `lmp_serial`, `lmp_mpi`,
`lmp_<machine>` 등으로 달라질 수 있으니, 설치 후 자신의 환경에서 사용 가능한
이름을 한 번 확인해 두시기를 권합니다.

<div class="tip">
  <div class="note-title">실행 파일 이름이 다를 때</div>
  <p>
    소스 빌드의 경우 보통 <code>lmp_mpi</code>(MPI 빌드)와
    <code>lmp_serial</code>(직렬 빌드)이 함께 생성됩니다.
    이후 본 가이드에서는 일관되게 <code>lmp</code> 라고 쓰지만,
    자신의 환경에 맞는 이름으로 바꿔서 읽으시면 됩니다.
  </p>
</div>

## 1.3 첫 시뮬레이션 — Lennard-Jones 액체

가장 단순한 LAMMPS 시뮬레이션은 Lennard-Jones(LJ) 입자들로 이루어진 액체입니다.
원자 종류는 한 가지, 상호작용은 LJ 한 가지뿐이고, 단위계도 환원
단위(reduced units)를 쓰기 때문에 외부 데이터 파일이나 힘장 라이브러리가
전혀 필요 없습니다.

다음 내용을 `in.lj` 라는 파일로 저장하십시오.

```lammps
# in.lj — 가장 단순한 Lennard-Jones 액체

units           lj
atom_style      atomic

lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 box

mass            1 1.0

pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5

velocity        all create 1.44 87287 loop geom

neighbor        0.3 bin
neigh_modify    every 20 delay 0 check no

fix             1 all nve

thermo          50
run             250
```

이 스크립트는 fcc 격자로 4000개 LJ 입자를 만들고, 초기 속도를 무작위로
부여한 뒤 NVE 앙상블에서 250 스텝 동안 적분합니다.

실행은 다음과 같이 합니다.

```bash
# 직렬 실행 (1 코어)
lmp -in in.lj > out.lj

# 병렬 실행 (4 코어)
mpirun -np 4 lmp -in in.lj > out.lj
```

<div class="tip">
  <div class="note-title">왜 <code>-in in.lj</code> 가 권장될까</div>
  <p>
    매뉴얼은 <code>lmp -in in.lj</code> 형태를 권장합니다.
    <code>lmp &lt; in.lj</code> 처럼 표준 입력으로 넘기는 방식도 동작하지만,
    <code>mpirun</code> 또는 <code>mpiexec</code> 로 병렬 실행할 때
    리디렉션 연산자가 일부 환경에서 제대로 동작하지 않기 때문입니다.
  </p>
</div>

## 1.4 출력 결과 살펴보기

실행이 끝나면 `out.lj` 라는 출력 파일과 `log.lammps` 라는 로그 파일이
생성됩니다. 둘 다 텍스트 파일이므로 일반 에디터로 열 수 있습니다.

`out.lj` 의 끝부분을 보면 다음과 같은 형태의 표가 있습니다.

```text
Step          Temp          E_pair         E_mol          TotEng       Press
   0          1.44         -6.7733...      0.0           -4.6133...   -5.0228
  50          0.7572       -5.7585...      0.0           -4.6240...    0.1924
 100          0.7592       -5.7625...      0.0           -4.6253...    0.2058
 ...
 250          0.7480       -5.7400...      0.0           -4.6201...    0.2330
Loop time of 0.0XX on 4 procs for 250 steps with 4000 atoms
```

`Step` 은 시뮬레이션 스텝 번호, `Temp` 는 온도, `TotEng` 은 총 에너지(kinetic + potential)
입니다. 초기에 1.44 였던 온도가 빠르게 0.75 부근으로 떨어지면서 평형에 도달하는
것을 볼 수 있는데, 이는 NVE 앙상블에서 초기 격자가 풀어지면서 운동에너지가
포텐셜에너지로 분배되는 자연스러운 현상입니다.

마지막 줄의 `Loop time` 은 시뮬레이션이 소요한 wall-clock 시간으로,
LAMMPS 성능 진단의 출발점입니다.

## 1.5 다음 단계

이번 장에서는 LAMMPS 실행 방법과 가장 단순한 입력 스크립트의 형태만
훑어보았습니다. 다음 장에서는 이 스크립트를 한 줄 한 줄 뜯어보며,
LAMMPS 매뉴얼이 정의하는 입력 스크립트의 **4단계 표준 구조**를 살펴봅니다.
