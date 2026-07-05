---
layout: default
title: "1. Si SCF"
---

# 1. Si SCF — 첫 SCF와 수렴 확인
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 무엇을 하는 예제인가

다이아몬드 구조 실리콘의 원시 셀(원자 2개)로 전체 에너지를 SCF로 구하고,
파동함수 컷오프(`ecutwfc`)와 k점 격자를 바꿔 가며 에너지가 어떻게 수렴하는지
확인합니다. QE의 가장 기본 흐름과 "수렴은 시험으로 정한다"는 감각을 익히는
예제입니다.

관련 개념은 [01 시작하기](01-getting-started.html),
[03 유사퍼텐셜](03-pseudopotentials.html), [04 k점 샘플링](04-kpoints.html)에서
다룹니다.

## 준비 — 유사퍼텐셜

PBE 초연질 유사퍼텐셜을 `pseudo/` 에 둡니다. 본 예제는
`Si.pbe-n-rrkjus_psl.1.0.0.UPF`(pslibrary 1.0.0, SSSP efficiency 계열)를 씁니다.

## 전체 입력 스크립트 — `si.scf.in`

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

## 실행

```bash
export OMP_NUM_THREADS=1
mpirun -np 8 pw.x -nk 8 -in si.scf.in > si.scf.out
```

작은 계라 스레드를 끄고 k점을 8개 풀로 병렬화하면 몇 초 만에 끝납니다.

## 출력 — 전체 에너지

`si.scf.out` 끝부분(QE 7.5, PBE US 실제 실행):

```text
!    total energy              =     -22.83941780 Ry
     estimated scf accuracy    <          2.8E-09 Ry

     one-electron contribution =       5.17095299 Ry
     hartree contribution      =       1.10074142 Ry
     xc contribution           =     -12.31018265 Ry
     ewald contribution        =     -16.80092957 Ry

     highest occupied level (ev):     6.2117
```

느낌표가 붙은 −22.8394 Ry 가 수렴한 전체 에너지입니다. 반도체라 페르미 준위 대신
최고 점유 준위(6.21 eV)가 찍힙니다.

## 수렴 확인 — ecutwfc와 k점

`ecutwfc`(그리고 US이므로 `ecutrho = 8×ecutwfc`)를 15→50 Ry, k점을 2→12로 바꿔
가며 전체 에너지를 모았습니다.

<figure>
  <img src="assets/images/qe-si-conv.png" alt="실리콘 전체 에너지의 ecutwfc·k점 수렴 그래프" style="width:100%;max-width:940px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    세로축은 가장 촘촘한 값과의 차이(원자당 meV, 로그 눈금). 왼쪽 ecutwfc는 30~35 Ry,
    오른쪽 k점은 8×8×8 부근에서 1 meV/atom(주황 점선) 아래로 수렴합니다.
    2×2×2 k점은 오차가 1 eV/atom을 넘습니다.
  </figcaption>
</figure>

| ecutwfc (Ry) | E (Ry) | | k-grid | E (Ry) |
|---|---|---|---|---|
| 15 | −22.83468 | | 2×2×2 | −22.65178 |
| 25 | −22.83880 | | 4×4×4 | −22.82587 |
| 35 | −22.83937 | | 6×6×6 | −22.83794 |
| 45 | −22.83947 | | 8×8×8 | −22.83942 |

## 요점

- 느낌표(`!`) 줄이 수렴 전체 에너지입니다.
- `ecutwfc`·k점 모두 "관심 물리량이 수렴할 때까지" 시험으로 정합니다.
- US 유사퍼텐셜은 `ecutrho` 를 `ecutwfc` 의 8~12배로 함께 올립니다.
- 성긴 k점은 오차가 매우 크므로(2×2×2 → 1 eV/atom 이상) 조심합니다.

## 관련 개념 챕터

- [01 시작하기](01-getting-started.html) · [03 유사퍼텐셜](03-pseudopotentials.html) · [04 k점 샘플링](04-kpoints.html)

다음 예제 [E2 — Si 밴드 + DOS](ex-02-si-bands.html) 에서는 이 SCF 결과를 이어받아
밴드구조와 상태밀도를 구합니다.
