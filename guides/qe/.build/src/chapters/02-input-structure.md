---
title: "02. 입력 파일 구조"
---

# 02. 입력 파일 구조

## 목차
{:.toc-title}

1. TOC
{:toc}

## 입력은 네임리스트와 카드, 두 층입니다

`pw.x` 입력 파일은 두 종류의 블록으로 구성됩니다.

- **네임리스트(namelist)** — `&CONTROL`, `&SYSTEM`, `&ELECTRONS`처럼 `&이름`으로
  시작해 `/`로 닫는 Fortran 네임리스트. `변수 = 값` 형태이며 순서는
  `&CONTROL → &SYSTEM → &ELECTRONS → (&IONS) → (&CELL)` 로 고정입니다.
- **카드(card)** — `ATOMIC_SPECIES`, `ATOMIC_POSITIONS`, `K_POINTS`,
  `CELL_PARAMETERS`, `HUBBARD`처럼 대문자 제목 아래 표 형태의 데이터가 오는
  블록. 네임리스트 뒤에 옵니다. 일부 카드는 괄호로 단위/옵션을 받습니다
  (예: `ATOMIC_POSITIONS (crystal)`).

문자열은 작은따옴표(`'scf'`), 논리값은 `.true.`/`.false.`, 주석은 `!`입니다.

## 최소 입력 해부 — 실리콘 SCF

첫 계산은 **반드시 실리콘 같은 단순 반도체**로 하세요. Fe 계로 바로 뛰어들면
수렴 실패의 원인이 물리 문제인지 설정 문제인지 구별할 수 없습니다.

```fortran
&CONTROL
  calculation  = 'scf'        ! scf / nscf / bands / relax / vc-relax / md
  prefix       = 'si'         ! 출력 파일 접두어 (후속 계산과 반드시 일치)
  outdir       = './tmp/'
  pseudo_dir   = './pseudo/'
  verbosity    = 'high'       ! 학습 단계에서는 무조건 high
  tprnfor      = .true.       ! 힘 출력
  tstress      = .true.       ! 응력 출력
/
&SYSTEM
  ibrav        = 2            ! fcc. 0이면 CELL_PARAMETERS로 직접 지정
  celldm(1)    = 10.26        ! bohr 단위 (= 5.43 Å)
  nat          = 2
  ntyp         = 1
  ecutwfc      = 30           ! Ry — 파동함수 컷오프
  ecutrho      = 240          ! Ry — 전하밀도 컷오프 (PAW/US는 8배)
  occupations  = 'fixed'      ! 절연체/반도체
/
&ELECTRONS
  conv_thr     = 1.0d-8       ! Ry
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

각 블록의 역할:

| 블록 | 담당 | 자세히 |
|---|---|---|
| `&CONTROL` | 무엇을 계산하고 어디에 쓸 것인가 | 계산 종류는 [08장](08-scf-nscf.html)·[09장](09-relaxation.html) |
| `&SYSTEM` | 계가 무엇인가 (셀, 원자 수, 기저, 점유) | 단위·좌표는 [03장](03-units-coordinates.html), 점유는 [06장](06-occupations.html) |
| `&ELECTRONS` | SCF를 어떻게 수렴시킬 것인가 | [07장](07-scf-control.html) |
| `ATOMIC_SPECIES` | 라벨·질량·유사퍼텐셜 파일 | [04장](04-pseudopotentials.html) |
| `ATOMIC_POSITIONS` | 원자 좌표 (+선택적 `if_pos` 고정 플래그) | [03장](03-units-coordinates.html) |
| `K_POINTS` | Brillouin zone 샘플링 | [05장](05-convergence.html) |

카드별 전체 문법은 [R2 · 카드 레퍼런스](ref-cards.html)에 정리했습니다.

## 실행 명령

```bash
pw.x -in si.scf.in > si.scf.out                       # 직렬
mpirun -np 8 pw.x -nk 4 -in si.scf.in > si.scf.out    # 병렬 (k-점 풀 4개)
```

출력은 표준출력으로 나오므로 리다이렉트(`>`)로 저장합니다. 계산 중간 파일은
`outdir/prefix.save/`에 쌓이고, 후속 계산(nscf, 후처리)은 **같은 `prefix`와
`outdir`**로 이 디렉터리를 찾아갑니다.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    네임리스트를 <code>/</code>로 닫지 않으면
    <code>namelist not found</code> 에러가 납니다. 문자열을 큰따옴표로 쓰거나
    논리값을 <code>true</code>로 쓰는 것도 파싱 실패의 단골 원인입니다.
    카드 이름 오타는 <code>Error in routine card_xxx</code>로 나타납니다.
    입력 문법 오류 전반은 <a href="ref-errors.html">R3 · 오류 사전</a>을
    참고하세요.
  </p>
</div>

## 관련 예제

- [E1 · Si SCF](ex-01-si-scf.html) — 이 입력을 그대로 실행하고 출력을 읽습니다.
- [E2 · ibrav=0 다시 쓰기](ex-02-si-ibrav0.html) — 같은 계를 다른 문법으로.
