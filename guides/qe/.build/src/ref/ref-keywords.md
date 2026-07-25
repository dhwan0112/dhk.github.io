---
title: "R1. 키워드 사전"
---

# R1. 키워드 사전

`pw.x` 입력 변수를 네임리스트별로 찾아보는 사전입니다. 기본값은 QE 7.5
기준이며, **최종 근거는 항상 설치 버전의 `Doc/INPUT_PW.txt`**
([온라인판](https://www.quantum-espresso.org/Doc/INPUT_PW.html))입니다.
카드 문법은 [R2](ref-cards.html), 후처리 코드 변수는
[R4](ref-executables.html)에 있습니다.

## 목차
{:.toc-title}

1. TOC
{:toc}

## &CONTROL

| 변수 | 기본값 | 설명 |
|---|---|---|
| `calculation` | `'scf'` | `scf` / `nscf` / `bands` / `relax` / `md` / `vc-relax` / `vc-md` |
| `title` | 없음 | 출력에 찍히는 설명. 배치 작업 관리에 유용 |
| `verbosity` | `'low'` | `'high'`면 대칭 연산, ns 행렬, k-점 목록까지 출력. **학습 중에는 항상 high** |
| `restart_mode` | `'from_scratch'` | `'restart'`로 중단된 계산 재개 |
| `nstep` | scf 1, relax/md 50 | 이온 스텝 수 |
| `dt` | 20.0 | MD 시간 간격. **Rydberg 원자단위** (20 a.u. ≈ 0.968 fs) |
| `outdir` | `./` 또는 `$ESPRESSO_TMPDIR` | 대용량 임시 파일 위치. **빠른 디스크로 지정할 것** |
| `wfcdir` | `outdir` | 파동함수만 따로 둘 때 |
| `prefix` | `'pwscf'` | 후속 계산과 **반드시 일치**해야 함 |
| `pseudo_dir` | `$ESPRESSO_PSEUDO` 또는 `~/espresso/pseudo` | UPF 파일 위치 |
| `disk_io` | 계산 종류에 따름 | `'none'` / `'low'` / `'medium'` / `'high'` / `'nowf'`. MD에서는 `'none'` |
| `tprnfor` | scf에서 `.false.` | 힘 출력. **ML 학습 데이터라면 반드시 `.true.`** |
| `tstress` | `.false.` | 응력 출력 |
| `etot_conv_thr` | 1.0d-4 Ry | 이온 최적화의 에너지 수렴 기준 |
| `forc_conv_thr` | 1.0d-3 Ry/bohr | 이온 최적화의 힘 수렴 기준 |
| `max_seconds` | 1.0d7 | 시간 초과 시 안전 저장 후 종료. **HPC 배치에서 필수** |
| `tefield`, `dipfield` | `.false.` | 톱니 전기장 / 쌍극자 보정 스위치. **&CONTROL 소속** (위치 파라미터 `edir` 등은 &SYSTEM) |
| `lelfield`, `gate`, `trism` | `.false.` | 특수 기능 (유한 전기장 / 게이트 / RISM) |

## &SYSTEM — 격자와 원자

| 변수 | 설명 |
|---|---|
| `ibrav` | 0 = `CELL_PARAMETERS`로 직접 지정 / 1 단순입방 / 2 fcc / 3 bcc / 4 육방 / 5 능면체 / 6·7 정방 / 8~11 사방 / 12·13 단사 / 14 삼사 |
| `celldm(1..6)` | `ibrav`에 따른 격자 파라미터. **`celldm(1)`은 bohr** |
| `A, B, C, cosAB, cosAC, cosBC` | `celldm`의 대안. **`A`는 Å 단위** (혼동 주의) |
| `nat`, `ntyp` | 원자 수 / 원자 종류 수. 카드의 줄 수와 일치해야 함 |
| `nosym`, `noinv` | 대칭/반전 사용 억제. 특수한 자기 배열이나 디버깅용 |

`ibrav=0`은 유연하지만 대칭 자동 탐지가 약해질 수 있습니다. 출력의
`Sym. Ops.` 개수를 확인하세요.

## &SYSTEM — 기저와 컷오프

| 변수 | 기본값 | 설명 |
|---|---|---|
| `ecutwfc` | **필수** | 파동함수 컷오프 (Ry) |
| `ecutrho` | `4*ecutwfc` | 전하밀도 컷오프 (Ry). **US/PAW는 8~12배 필요** |
| `nbnd` | 절연체 `nelec/2`, 금속은 그보다 여유 | 밴드 수. DOS/밴드 계산에서는 넉넉히 |

## &SYSTEM — 점유수와 smearing

| 변수 | 설명 |
|---|---|
| `occupations` | `'fixed'`(절연체) / `'smearing'`(금속) / `'tetrahedra'` / `'tetrahedra_lin'` / `'tetrahedra_opt'`(DOS·밴드용 nscf) / `'from_input'` |
| `smearing` | `'gaussian'` / `'methfessel-paxton'`(`'mp'`) / `'marzari-vanderbilt'`(`'mv'`, `'cold'`) / `'fermi-dirac'`(`'fd'`) |
| `degauss` | smearing 폭 (Ry). 금속은 보통 0.01~0.02 |

사면체법(`tetrahedra*`)은 **Γ 중심의 shift 없는 자동 그리드**를 요구하며
`nscf`에서 씁니다.

## &SYSTEM — 스핀과 자성

| 변수 | 설명 |
|---|---|
| `nspin` | 1 비편극 / 2 공선 스핀 편극 / 4 비공선(`noncolin` 사용 권장) |
| `starting_magnetization(i)` | 원자종 `i`의 **초기 자화 비율 (−1~1)**. Bohr magneton 아님 |
| `tot_magnetization` | 셀 전체 자화를 구속. up/down에 별도 Fermi 준위 |
| `noncolin` | `.true.`면 비공선 자성 |
| `lspinorb` | 스핀궤도결합. 완전상대론적 유사퍼텐셜 필요 |
| `angle1(i)`, `angle2(i)` | 비공선일 때 자화 방향 (도) |
| `constrained_magnetization` | `'atomic'`, `'total'` 등. `lambda`로 구속 강도 조절 |

## &SYSTEM — DFT+U 관련 (v7.1+ 신문법)

U 파라미터는 **`&SYSTEM`이 아니라 `HUBBARD` 카드**([R2](ref-cards.html))에
씁니다. `&SYSTEM`에 남아 있는 관련 변수:

| 변수 | 설명 |
|---|---|
| `starting_ns_eigenvalue(m, ispin, ityp)` | 초기 d/f 궤도 점유 고유값을 강제. **FeO처럼 잘못된 극소값에 갇히는 계에 필수** |
| `Hubbard_occ(ityp, i)` | Hubbard 매니폴드의 초기 점유수 override |

**폐기된 문법**: `lda_plus_u`, `lda_plus_u_kind`, `Hubbard_U(i)`,
`U_projection_type` — v7.1 이후 `HUBBARD` 카드로 대체되었습니다.

## &SYSTEM — 범함수·분산·고립계·전기장

| 변수 | 설명 |
|---|---|
| `input_dft` | 유사퍼텐셜에 내장된 범함수 override. 되도록 쓰지 말 것 |
| `vdw_corr` | `'grimme-d2'` / `'grimme-d3'` / `'ts-vdw'` / `'xdm'` / `'mbd'` |
| `assume_isolated` | `'none'` / `'makov-payne'` / `'martyna-tuckerman'`(`'mt'`) / `'esm'` / `'2D'` |
| `edir`, `emaxpos`, `eopreg`, `eamp` | 전기장 방향(1/2/3), 위치, 폭, 세기 (스위치 `tefield`/`dipfield`는 &CONTROL) |
| `exx_fraction`, `screening_parameter`, `nqx1..3` | 하이브리드 범함수 파라미터 |

## &ELECTRONS

| 변수 | 기본값 | 설명 |
|---|---|---|
| `electron_maxstep` | 100 | SCF 최대 반복 |
| `conv_thr` | 1.0d-6 | SCF 수렴 임계값 (Ry). `hp.x` 선행 계산은 1.0d-12 권장 |
| `mixing_mode` | `'plain'` | `'plain'`(Broyden) / `'TF'` / `'local-TF'`. **금속·슬랩·자성계는 `'local-TF'`** |
| `mixing_beta` | 0.7 | 혼합 계수. 자성·금속은 0.1~0.3 |
| `mixing_ndim` | 8 | 혼합에 쓰는 이전 반복 수. 늘리면 메모리 증가 |
| `mixing_fixed_ns` | 0 | DFT+U: 초기 N회 반복 동안 점유행렬 ns 동결. **nosym+U 조합(MD 등)의 SCF 정체를 풂** ([E13](ex-13-slab-md.html) 실측) |
| `diagonalization` | `'david'` | `'david'` / `'cg'` / `'ppcg'` / `'paro'` / `'rmm-davidson'`. 실패 시 `'cg'`가 느리지만 안정 |
| `diago_david_ndim` | 2 | Davidson 작업공간. 메모리 부족 시 감소 |
| `startingwfc` | `'atomic+random'` | `'atomic'` / `'random'` / `'file'` |
| `startingpot` | `'atomic'` | `'atomic'` / `'file'` |
| `adaptive_thr` | `.false.` | 초기 반복에서 임계값 완화 (하이브리드용) |

## &IONS

| 변수 | 설명 |
|---|---|
| `ion_dynamics` | `relax`: `'bfgs'`(기본), `'damp'` / `md`: `'verlet'`, `'langevin'` |
| `ion_temperature` | `'not_controlled'` / `'rescaling'` / `'rescale-v'` / `'berendsen'` / `'andersen'` / `'svr'` / `'initial'` |
| `tempw` | 목표 온도 (K) |
| `nraise` | 온도 제어 주기 |
| `pot_extrapolation`, `wfc_extrapolation` | `'none'` / `'atomic'` / `'first_order'` / `'second_order'`. MD 속도에 큰 영향 |
| `upscale` | BFGS에서 SCF 임계값 자동 강화 배수 |
| `bfgs_ndim` | 1 (기본). 2 이상이면 준뉴턴 |

## &CELL

| 변수 | 설명 |
|---|---|
| `cell_dynamics` | `vc-relax`: `'bfgs'` / `vc-md`: `'pr'`, `'w'` |
| `press` | 목표 압력 (kbar) |
| `press_conv_thr` | 0.5 kbar (기본) |
| `cell_dofree` | `'all'` / `'ibrav'` / `'x'`,`'y'`,`'z'` / `'xy'` 등 / `'2Dxy'` / `'2Dshape'` / `'volume'` / `'shape'`. **슬랩은 `'2Dxy'`** |
| `cell_factor` | 2.0 (vc-relax). 셀이 크게 변할 때 늘림 |
| `wmass` | 셀 관성 질량 (vc-md) |

## 명령행 병렬화 플래그

| 플래그 | 별칭 | 의미 | 지침 |
|---|---|---|---|
| `-nk` | `-npool` | k-점 풀 분할 | **효율 최고.** k-점 수를 나누어떨어지게. 메모리 부족 시 줄임 |
| `-nb` | `-nband` | 밴드 그룹 | 하이브리드·EXX에서 유효 |
| `-nt` | `-ntg` | FFT task group | 밴드·코어가 많을 때 |
| `-nd` | `-ndiag` | 대각화 그룹 | **제곱수여야 함.** 큰 계에서만 |
| `-ni` | `-nimage` | 이미지 병렬 | NEB, 포논, hp.x |
| `-i` / `-in` / `-inp` | | 입력 파일 지정 | |

## 환경 변수

| 변수 | 용도 |
|---|---|
| `ESPRESSO_PSEUDO` | 유사퍼텐셜 기본 경로 (`pseudo_dir` 미지정 시) |
| `ESPRESSO_TMPDIR` | `outdir` 기본값 |
| `OMP_NUM_THREADS` | OpenMP 스레드. MPI와 함께 쓸 때 과다 설정 주의 ([18장](18-parallel-hpc.html)) |
| `ESPRESSO_ROOT` | 소스 트리 경로 |
