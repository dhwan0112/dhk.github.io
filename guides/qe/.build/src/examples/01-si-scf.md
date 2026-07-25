---
title: "E1. Si SCF"
---

# E1. Si SCF

## 목적

가장 단순한 계(다이아몬드 구조 실리콘, 2원자)로 SCF를 한 번 돌리고, 출력의
모든 블록을 읽어봅니다. 이 예제의 입력이 이후 모든 예제의 뼈대입니다.

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `&CONTROL` / `&SYSTEM` / `&ELECTRONS` | 필수 네임리스트 3종 ([02장](02-input-structure.html)) |
| `ibrav=2` + `celldm(1)` | fcc 격자를 관례로 정의 ([03장](03-units-coordinates.html)) |
| `ATOMIC_SPECIES` / `ATOMIC_POSITIONS` / `K_POINTS` | 필수 카드 3종 |
| `verbosity='high'`, `tprnfor`, `tstress` | 학습용 상세 출력 + 힘·응력 |

## 입력 파일

[si.scf.in 내려받기](files/E01-si-scf/si.scf.in)

```fortran
&CONTROL
  calculation  = 'scf'
  prefix       = 'si'
  outdir       = './tmp/'
  pseudo_dir   = './pseudo/'
  verbosity    = 'high'
  tprnfor      = .true.
  tstress      = .true.
/
&SYSTEM
  ibrav        = 2
  celldm(1)    = 10.26
  nat          = 2
  ntyp         = 1
  ecutwfc      = 30
  ecutrho      = 240
  occupations  = 'fixed'
/
&ELECTRONS
  conv_thr     = 1.0d-8
  mixing_beta  = 0.7
/

ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (alat)
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25

K_POINTS (automatic)
  8 8 8  0 0 0
```

## 실행

```bash
mkdir -p pseudo tmp        # pseudo/ 에 Si PAW UPF를 받아 두세요 (01장)
pw.x -in si.scf.in > si.scf.out                     # 직렬
mpirun -np 6 pw.x -nk 6 -in si.scf.in > si.scf.out  # 실측에 쓴 병렬 설정
```

## 출력에서 확인할 것

| 찾을 것 | 검색어 | 실측값 (QE 7.5, PAW) |
|---|---|---|
| 최종 총에너지 | `!    total` | **−93.45273690 Ry** |
| 수렴 | `convergence has been achieved` | 6회 반복 |
| 기약 k-점 수 | `number of k points` | 29 (8×8×8에서 대칭으로 축소) |
| 대칭 연산 | `Sym. Ops.` | 48 (반전 포함) |
| 최고 점유 준위 | `highest occupied level` | 6.2124 eV |
| 힘 | `Total force` | 0.000000 (대칭 위치이므로 정확히 0) |
| 응력 | `total   stress` | P = 20.28 kbar |
| 소요 시간 | `PWSCF ... WALL` | 2.75 s (6랭크) |

읽는 법 몇 가지 —

- `!`가 붙은 총에너지 줄만 수렴된 최종값입니다. PAW라 절대값이 US
  유사퍼텐셜과 크게 다른데, [총에너지 절대값은 원래 비교 대상이
  아닙니다](04-pseudopotentials.html).
- `occupations='fixed'`에 기본 `nbnd`(점유 밴드만)라서
  `highest occupied level`만 나오고 갭 추정(`lowest unoccupied`)은 나오지
  않습니다. 갭까지 보려면 `nbnd`를 늘리세요 (직접 써보기 3).
- P = +20 kbar는 이 격자상수(5.43 Å, 실험값)가 PBE 평형보다 압축되어
  있다는 뜻입니다. PBE 평형 격자상수는 [E6](ex-06-si-vcrelax.html)에서
  구합니다.

## 직접 써보기

1. `verbosity`를 `'low'`로 바꿔 출력이 얼마나 줄어드는지 확인하고, 학습
   중에는 왜 `'high'`를 써야 하는지 설명해 보세요.
2. `occupations`를 `'smearing'`으로 바꾸면 에너지가 어떻게 변하나요? 왜
   반도체에 smearing을 쓰면 안 되는지 서술해 보세요.
3. `nbnd = 8`을 추가해 `highest occupied, lowest unoccupied level`이
   출력되게 하고, 그 차이(갭 추정)를 읽어 보세요.
4. `ecutrho`를 지우면(기본값 = 4×`ecutwfc`) 어떤 일이 생기는지 확인하세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>pseudo_dir</code>에 UPF 파일이 없거나 파일명이
    <code>ATOMIC_SPECIES</code>와 다르면 <code>Error in routine readpp</code>로
    멈춥니다. 그리고 이 계산의 <code>outdir</code>(<code>./tmp/</code>)을
    지우면 후속 예제(E7·E8)의 nscf가 시작하지 못합니다 —
    <a href="08-scf-nscf.html">08장</a>.
  </p>
</div>

## 관련 챕터

[02 입력 파일 구조](02-input-structure.html) ·
[03 단위계와 좌표계](03-units-coordinates.html) ·
[08 SCF와 NSCF](08-scf-nscf.html)
