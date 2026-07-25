---
title: "18. 병렬 실행과 HPC 운영"
---

# 18. 병렬 실행과 HPC 운영

## 목차
{:.toc-title}

1. TOC
{:toc}

## 병렬화 레벨 치트시트

```bash
mpirun -np 32 pw.x -nk 8 -in input.in > output.out
```

| 플래그 | 별칭 | 의미 | 실무 지침 |
|---|---|---|---|
| `-nk` | `-npool` | k-점 풀 분할 | **가장 효율이 좋음.** k-점 수를 나누어떨어지게 잡되, `nproc/nk`가 FFT 분할에 충분해야 함 |
| `-nb` | `-nband` | 밴드 그룹 | 하이브리드·EXX에서 유효 |
| `-nt` | `-ntg` | FFT task group | 밴드가 많고 코어가 많을 때 |
| `-nd` | `-ndiag` | 대각화 그룹 | **제곱수여야 함.** 큰 계에서만 |
| `-ni` | `-nimage` | 이미지 병렬 | NEB, 포논, hp.x |

기본 분할(플래그 없음)은 평면파(G-벡터) 분산입니다. 작은 셀 + 많은 k-점이면
`-nk`가 압도적이고, 큰 셀 + 적은 k-점이면 G-벡터 분산과 `-nd`가 주력이
됩니다. **메모리가 부족하면 `-nk`를 줄이세요** — 풀마다 전하밀도 사본을
가집니다.

## 실측 — 작은 계에서 스레드의 함정

본 가이드의 2원자 Si SCF 실측 (16코어 WSL, conda-forge 빌드):

| 설정 | WALL |
|---|---|
| `OMP_NUM_THREADS=16` (스레드만) | 약 2분 |
| `OMP_NUM_THREADS=1` + `mpirun -np 6 pw.x -nk 6` | **2.8초** |

conda 빌드는 OpenMP가 켜져 있어, 그대로 두면 작은 계에서 스레드 스핀으로
수십 배 느려질 수 있습니다. **로컬 학습 환경에서는 `OMP_NUM_THREADS=1`을
명시하고 MPI + `-nk`로 병렬화**하는 것이 안전합니다. HPC에서 MPI×OpenMP
하이브리드를 쓸 때는 노드당 랭크 수 × 스레드 수 = 물리 코어 수를 지키세요.

## 어디에 시간을 쓰는지 먼저 봅니다

출력 맨 아래 timing 분해가 병렬화 전략의 출발점입니다.

```
     init_run     :    ...
     electrons    :    ...      ← SCF 전체
     c_bands      :    ...      ← 대각화 (크면 -nd, diagonalization 조정)
     sum_band     :    ...
     fft + ffts   :    ...      ← FFT (크면 G-벡터 분산/-nt)
```

`PWSCF : ... CPU ... WALL`에서 CPU ≫ WALL이면 스레드가, WALL ≫ CPU이면
I/O나 통신이 병목입니다.

## HPC 운영 습관

- **`max_seconds`를 걸어 두세요.** 큐 시간 초과 직전에 안전하게 저장하고
  종료합니다. `restart_mode='restart'`로 이어받습니다.
- `outdir`은 스크래치(고속 병렬 파일시스템)로. 홈 디렉터리에 파동함수를
  쓰면 본인도 시스템도 느려집니다.
- 배치 스크립트에 **QE 버전, 유사퍼텐셜 경로·이름, 커밋 로그**를 함께
  기록하세요. "이 데이터가 어떤 설정으로 계산됐는가"는 몇 달 뒤의 자신이
  가장 자주 묻는 질문입니다.
- 큰 스캔(수렴 테스트, U 스캔, MD 프레임 재계산)은 셸 루프보다 AiiDA·ASE
  같은 워크플로 도구가 재현성 면에서 안전합니다.

전형적인 PBS/Slurm 한 줄:

```bash
mpirun -np $SLURM_NTASKS pw.x -nk 8 -nd 4 -in feo.scf.in > feo.scf.out
```

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>npool must divide nproc</code> — <code>-nk</code>가 전체 랭크 수의
    약수가 아닐 때. <code>some processors have no planes</code> — 랭크가 FFT
    격자 z-평면 수보다 많을 때(작은 셀에 랭크 과다). 이런 병렬 설정 오류는
    <a href="ref-errors.html">R3 · 오류 사전</a> 4절에 모아 두었습니다.
  </p>
</div>

## 관련 예제

- 모든 예제 페이지의 "실행" 절에 이 장의 규칙으로 정한 실측 명령이 있습니다.
  hp.x의 q-점 분할은 [예제 E12](ex-12-feo-hp.html)를 참고하세요.
