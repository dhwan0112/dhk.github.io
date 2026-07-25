---
title: "R4. 실행 파일 목록"
---

# R4. 실행 파일 목록

QE는 하나의 프로그램이 아니라 실행 파일들의 스위트입니다. 각 파일이 무엇을
받고 무엇을 내놓는지의 지도입니다. 변수 상세는 각 코드의
`Doc/INPUT_<이름>.txt`에 있습니다.

## 목차
{:.toc-title}

1. TOC
{:toc}

## 핵심 파이프라인

| 실행파일 | 입력 네임리스트 | 선행 계산 | 산출물 | 관련 장 |
|---|---|---|---|---|
| `pw.x` | `&CONTROL`+`&SYSTEM`+`&ELECTRONS`(+`&IONS`,`&CELL`) | — | 총에너지, 힘, 응력, 밀도, 파동함수 | [02장](02-input-structure.html) |
| `dos.x` | `&DOS` | `nscf` | 총 DOS (`fildos`) | [10장](10-dos-bands.html) |
| `projwfc.x` | `&PROJWFC` | `nscf` | PDOS, Löwdin 전하 | [10장](10-dos-bands.html) |
| `bands.x` | `&BANDS` | `calculation='bands'` | 밴드 데이터(`.gnu`), 대칭 라벨 | [10장](10-dos-bands.html) |
| `pp.x` | `&INPUTPP` + `&PLOT` | `scf` | 전하밀도·퍼텐셜·ELF (cube/XSF) | [11장](11-postprocessing.html) |
| `average.x` | (직접 입력) | `pp.x` | 평면 평균 (일함수) | [15장](15-surfaces.html) |
| `hp.x` | `&INPUTHP` | `scf` + HUBBARD 카드 | Hubbard U·V (`*.Hubbard_parameters.dat`) | [14장](14-hubbard-hp.html) |
| `ph.x` | `&INPUTPH` | `scf` | 동역학 행렬 (`fildyn`) | [17장](17-phonons-neb.html) |
| `q2r.x` / `matdyn.x` | 각자 | `ph.x` | 실공간 힘상수 / 포논 분산·DOS | [17장](17-phonons-neb.html) |
| `neb.x` | `&PATH` + 엔진 입력 | 양끝 구조 최적화 | 최소 에너지 경로, 장벽 | [17장](17-phonons-neb.html) |
| `cp.x` | 별도 (CP 입력) | — | Car-Parrinello MD | [16장](16-molecular-dynamics.html) 참고 |
| `pw2wannier90.x` | `&INPUTPP` | `nscf` + Wannier90 | Wannier 함수 인터페이스 | [17장](17-phonons-neb.html) |
| `plotband.x` | 대화형 | `bands.x` | 밴드 플롯 데이터 | [10장](10-dos-bands.html) |

## 후처리 코드 네임리스트 요약

### dos.x — &DOS

`prefix`, `outdir`, `fildos`, `Emin`, `Emax`, `DeltaE`, `ngauss`, `degauss`,
`bz_sum`. 출력 파일은 1열 E(eV), 2열 DOS(스핀 계는 up/down 2열), 마지막 열
적분 DOS.

### projwfc.x — &PROJWFC

`prefix`, `outdir`, `filpdos`, `filproj`, `ngauss`, `degauss`, `Emin`,
`Emax`, `DeltaE`, `lsym`(대칭화된 원자 궤도), `pawproj`, `lwrite_overlaps`,
`kresolveddos`(k-분해 DOS). 출력은 `filpdos.pdos_atm#N(라벨)_wfc#M(궤도)`
파일들과, 표준출력의 **Löwdin charges** 블록.

### bands.x — &BANDS

`prefix`, `outdir`, `filband`, `lsym`(대칭 라벨 부여), `spin_component`,
`lp`(운동량 행렬요소). `filband.gnu`가 플롯용, 표준출력의
`high-symmetry point` 줄이 눈금 위치입니다.

### pp.x — &INPUTPP + &PLOT

`&INPUTPP`: `prefix`, `outdir`, `filplot`, `plot_num`, `spin_component`,
`sample_bias`, `kpoint`, `kband`.

| `plot_num` | 내용 |
|---|---|
| 0 | 원자가 전하밀도 |
| 1 | 총 퍼텐셜 (V_bare + V_H + V_xc) |
| 2 | 국소 이온 퍼텐셜 |
| 5 | STM 이미지 |
| 6 | 스핀 밀도 ρ↑ − ρ↓ |
| 8 | ELF |
| 11 | bare + Hartree 퍼텐셜 (**일함수**) |

`&PLOT`: `nfile`, `filepp(i)`, `weight(i)`, `iflag`(0 1D선 / 1 구면평균 /
2 2D / 3 3D / 4 2D극좌표), `output_format`(0 gnuplot / 3 XCrySDen 2D /
5 XSF 3D / 6 Gaussian cube / 7 gnuplot 2D), `fileout`, `e1,e2,e3`, `x0`,
`nx,ny,nz`. PAW 전전자 밀도 옵션은 버전별로 다르므로 `Doc/INPUT_PP.txt` 확인.

### hp.x — &INPUTHP

`prefix`, `outdir`, `nq1/nq2/nq3`, `conv_thr_chi`, `thresh_init`,
`iverbosity`, `start_q`/`last_q`(작업 분할), `perturb_only_atom(i)`,
`skip_equivalence_q`, `determine_num_pert_only`, `compute_hp`(부분 결과 취합).

### ph.x — &INPUTPH

`prefix`, `outdir`, `fildyn`, `tr2_ph`, `ldisp`, `nq1/nq2/nq3`, `epsil`,
`zeu`, `recover`, `start_q`/`last_q`, `alpha_mix(1)`.

### neb.x — &PATH

`string_method`(`'neb'`/`'smd'`), `num_of_images`, `nstep_path`,
`opt_scheme`(`'broyden'`/`'quick-min'`/`'sd'`),
`CI_scheme`(`'no-CI'`/`'auto'`/`'manual'`), `path_thr`, `ds`, `k_max`,
`k_min`, `restart_mode`. 입력 블록 구조는 [R2](ref-cards.html) 참고.

## 파일 흐름 한 장 요약

```
                    ┌─ dos.x ──────→ 총 DOS
scf ──→ nscf ───────┼─ projwfc.x ──→ PDOS, Löwdin
 │                  └─ (밀도 고정)
 ├────→ bands ──────── bands.x ────→ 밴드 (.gnu)
 ├────→ pp.x ─────────────────────→ 밀도·퍼텐셜 (cube) ──→ average.x → 일함수
 ├────→ hp.x (HUBBARD 필요) ──────→ U, V
 └────→ ph.x ──→ q2r.x ──→ matdyn.x → 포논 분산
```

모든 화살표는 **동일한 `prefix`·`outdir`**로 연결됩니다. 이 사슬이 끊기면
`cannot open file ... .save/...` 에러가 납니다 ([R3](ref-errors.html)).
