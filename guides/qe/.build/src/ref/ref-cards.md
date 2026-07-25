---
title: "R2. 카드 레퍼런스"
---

# R2. 카드 레퍼런스

`pw.x` 입력에서 네임리스트 뒤에 오는 카드들의 문법 정리입니다. 네임리스트
변수는 [R1](ref-keywords.html)을 보세요.

## 목차
{:.toc-title}

1. TOC
{:toc}

## 카드 한눈에 보기

| 카드 | 필수 | 옵션 | 설명 |
|---|---|---|---|
| `ATOMIC_SPECIES` | ○ | — | 라벨, 질량, UPF 파일명 |
| `ATOMIC_POSITIONS` | ○ | `alat` / `bohr` / `angstrom` / `crystal` / `crystal_sg` | 끝에 `if_pos` 3개 플래그 추가 가능 |
| `K_POINTS` | ○ | `automatic` / `gamma` / `tpiba` / `crystal` / `tpiba_b` / `crystal_b` / `tpiba_c` / `crystal_c` | `_b`는 밴드 경로용 |
| `CELL_PARAMETERS` | `ibrav=0`일 때 | `alat` / `bohr` / `angstrom` | 3×3 행렬 |
| `HUBBARD` | DFT+U 시 | `atomic` / `ortho-atomic` / `norm-atomic` / `wf` / `pseudo` | v7.1+ 신문법 |
| `OCCUPATIONS` | `occupations='from_input'` | — | 밴드별 점유수 직접 지정 |
| `CONSTRAINTS` | 구속 최적화/MD | — | 결합길이·각도 구속 |
| `ATOMIC_VELOCITIES` | MD 재시작 | `a.u.` | |
| `ATOMIC_FORCES` | 외력 인가 | — | |
| `ADDITIONAL_K_POINTS` | 특수 | — | |
| `SOLVENTS` | RISM | — | |

## ATOMIC_SPECIES

```fortran
ATOMIC_SPECIES
  Fe1  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
  Fe2  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF   ! 같은 PP, 다른 라벨 — AFM용
  O    15.999  O.pbe-n-kjpaw_psl.1.0.0.UPF
```

줄 수는 `ntyp`과 일치해야 합니다. **같은 유사퍼텐셜을 다른 라벨로 여러 번
등록할 수 있으며**, 반강자성 배열([12장](12-magnetism.html))과 원자별
U([13장](13-dft-plus-u.html))가 이 라벨 분리를 이용합니다. 질량은 MD·포논에서만
물리적으로 쓰입니다.

## ATOMIC_POSITIONS

```fortran
ATOMIC_POSITIONS (crystal)
  Fe  0.000  0.000  0.000   0 0 0    ! if_pos: 완전 고정
  Fe  0.500  0.500  0.250   0 0 1    ! z만 자유
  O   0.500  0.000  0.375              ! 생략 시 1 1 1 (완전 자유)
```

| 옵션 | 의미 |
|---|---|
| `alat` | `celldm(1)` 단위의 직교 좌표 |
| `bohr` / `angstrom` | 절대 직교 좌표 |
| `crystal` | 셀 벡터 기저의 분수 좌표 (실무에서 가장 안전) |
| `crystal_sg` | 공간군 대칭 기준 좌표 (`space_group` 지정 시) |

`if_pos`(0/1 셋)는 구조 최적화·MD에서 해당 성분의 힘을 0으로 만들어 그
방향 움직임을 막습니다.

## K_POINTS

```fortran
K_POINTS (automatic)      ! Monkhorst-Pack 자동 격자
  8 8 8  0 0 0            ! nk1 nk2 nk3  s1 s2 s3 (시프트 0/1)

K_POINTS gamma            ! Γ 한 점 (고립 분자) — 실수 파동함수 최적화

K_POINTS (tpiba_b)        ! 밴드 경로: 2π/a 단위 직교 좌표
6
  0.500 0.500 0.500  30   ! 고대칭점 + 다음 점까지 분할 수
  ...
  0.000 0.000 0.000   0   ! 마지막 점은 0

K_POINTS (crystal)        ! 명시적 k-점 목록 (가중치 포함)
```

- `tpiba_b`(2π/a 직교)와 `crystal_b`(역격자 분수)의 구분은
  [10장](10-dos-bands.html)에 정리했습니다. 헷갈리면 `tpiba_b`가 안전합니다.
- 사면체법을 쓸 nscf는 **시프트 없는 Γ 중심 automatic 격자**여야 합니다.

## CELL_PARAMETERS

```fortran
CELL_PARAMETERS (angstrom)
  -2.715   0.000   2.715
   0.000   2.715   2.715
  -2.715   2.715   0.000
```

`ibrav=0`일 때 셀 벡터 3개를 행으로 씁니다. `alat` 옵션이면 `celldm(1)`
(또는 `A`)을 스케일로 쓰므로, 부피 스캔·vc-relax 재시작에서 편리합니다.

## HUBBARD (v7.1+)

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 4.6
U Fe2-3d 4.6
V Fe1-3d O-2p  1 3  0.8    ! DFT+U+V: 사이트 인덱스는 ATOMIC_POSITIONS 순서
```

문법: `HUBBARD (<투영자>)` 아래 `<파라미터> <라벨>-<매니폴드> <값(eV)>`.

| 항목 | 선택지 |
|---|---|
| 투영자 | `atomic` / `ortho-atomic`(**권장**) / `norm-atomic` / `wf` / `pseudo` |
| 파라미터 | `U`, `J0`, `J`, `B`, `E2`, `E3`, `V`, `alpha` |
| 매니폴드 | `3d`, `2p`, `4f`, ... (원자 타입당 최대 3채널) |

구버전 문법(`lda_plus_u`, `Hubbard_U(i)`)은 폐기되었습니다. 상세는
[13장](13-dft-plus-u.html)과 `Doc/Hubbard_input.pdf`.

## OCCUPATIONS

`occupations='from_input'`일 때 밴드별 점유수를 직접 나열합니다. 스핀 편극
계산이면 up 블록 다음에 down 블록이 옵니다. 특수한 들뜬 상태·구속 계산
외에는 쓸 일이 드뭅니다.

## CONSTRAINTS

```fortran
CONSTRAINTS
1
'distance' 1 2 2.40      ! 원자 1-2 거리를 2.40 bohr로 구속
```

구속 MD·최적화용. 첫 줄은 구속 개수, 이후 한 줄에 하나씩
(`'distance'`, `'planar_angle'`, `'torsional_angle'` 등).

## neb.x 입력 구조 (참고)

`neb.x`는 카드가 아니라 **블록 구조**의 입력을 씁니다.

```
BEGIN
BEGIN_PATH_INPUT
&PATH
  string_method = 'neb'
  num_of_images = 7
  nstep_path    = 100
  opt_scheme    = 'broyden'
  path_thr      = 0.05
/
END_PATH_INPUT
BEGIN_ENGINE_INPUT
&CONTROL
 ... (pw.x 입력과 동일)
/
BEGIN_POSITIONS
FIRST_IMAGE
ATOMIC_POSITIONS (crystal)
 ...
LAST_IMAGE
ATOMIC_POSITIONS (crystal)
 ...
END_POSITIONS
END_ENGINE_INPUT
END
```

배경은 [17장](17-phonons-neb.html)을 보세요.
