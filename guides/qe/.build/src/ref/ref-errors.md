---
title: "R3. 오류 메시지 사전"
---

# R3. 오류 메시지 사전

QE의 에러는 대부분 `Error in routine <루틴명> (<코드>)` 형태로 나오며,
**루틴 이름이 원인의 가장 강한 단서**입니다.

## 목차
{:.toc-title}

1. TOC
{:toc}

## 에러를 읽는 법

```
     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
     Error in routine  cdiaghg (2):
      problems computing cholesky
     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
```

| 루틴 이름 | 문제 영역 |
|---|---|
| `read_*`, `card_*`, `iosys` | 입력 파일 문법 |
| `c_bands`, `cdiaghg`, `regterg`, `cegterg` | 대각화 |
| `sum_band`, `v_of_rho` | 전하밀도 (컷오프, 유사퍼텐셜) |
| `electrons` | SCF 수렴 |
| `punch`, `openfil`, `davcio` | 파일 I/O (경로, 디스크, `prefix` 불일치) |

에러가 없는데 결과가 이상한 경우가 더 위험합니다 — 아래
[에러 없이 틀리는 경우](#에러-없이-틀리는-경우--가장-위험한-범주)를 보세요.

## 입력 파일 문법 오류

| 메시지 | 원인 | 해결 |
|---|---|---|
| `Error in routine card_xxx` | 카드 이름 오타 또는 필드 수 불일치 | 카드명 대문자 확인, 열 개수 확인 |
| `too many atomic species` / `nat is wrong` | `nat`·`ntyp`이 실제 줄 수와 다름 | 카드 내용과 대조 |
| `Unknown label of the Hubbard parameter` | `HUBBARD` 카드의 파라미터 문자 오타 | `U`, `J0`, `J`, `V`, `alpha` 중 하나여야 함 |
| `namelist not found` | 네임리스트 이름 오타 또는 `/` 누락 | 모든 네임리스트는 `/`로 종료 |
| `input_dft not allowed` | 유사퍼텐셜 범함수와 충돌 | `input_dft`를 지우고 PP 내장 범함수 사용 |
| `reading namelist ...` | Fortran 파싱 실패 (대개 쉼표·따옴표) | 문자열은 작은따옴표, 논리값은 `.true.`/`.false.` |

## 유사퍼텐셜·전하밀도 문제

| 메시지 | 원인 | 해결 |
|---|---|---|
| `charge is wrong: smearing is needed` | 절연체로 가정했는데 금속 | `occupations = 'smearing'` |
| `charge is wrong` (적분 전하 불일치) | k-격자 대비 과소한 `degauss`, 또는 `ecutrho` 부족 | degauss·k-격자 함께 수렴, US/PAW는 `ecutrho` 8~12배 |
| `negative rho (up, down)` (경고) | `ecutrho` 부족 | US/PAW라면 8~12배로 |
| `Error in routine readpp` / `upf_read` | UPF 손상, 경로 오류, 버전 비호환 | `pseudo_dir` 확인, PP 재다운로드 |
| `wrong number of valence electrons` | PP와 원자 종류 불일치 | `ATOMIC_SPECIES` 재확인 |
| `set_hubbard_l: pseudopotential not yet inserted` | Hubbard 매니폴드를 PP가 지원 안 함 | 반코어(semicore) 포함 PP 사용 |

실측 사례 — 본 가이드 [예제 E5](ex-05-al-metal.html)의 degauss 스캔에서
`mv` smearing에 `degauss=0.005`를 주자 12×12×12 격자로는 적분 전하가
3.003으로 어긋나며 `charge is wrong`으로 정지했습니다. smearing 폭과
k-격자는 함께 수렴시켜야 한다는 실제 사례입니다.

## SCF·대각화 수렴 실패

### convergence NOT achieved after N iterations

가장 흔한 문제입니다. **순서대로** 시도하세요.

1. `mixing_beta` 0.7 → 0.3 → 0.1
2. `mixing_mode = 'local-TF'` (금속, 슬랩, 자성계에 효과적)
3. `electron_maxstep` 증가 (200~500)
4. `mixing_ndim` 증가 (8 → 12~16, 메모리 여유가 있을 때)
5. `degauss`를 일시적으로 키워 수렴시킨 뒤 `startingpot='file'`로 재시작하며 줄이기
6. `diagonalization = 'cg'` 또는 `'ppcg'` (느리지만 안정)
7. 초기 구조 점검 (원자 간 거리가 너무 가깝지 않은가)

### c_bands: N eigenvalues not converged

- 경고 수준이면 무시 가능한 경우가 많지만, 반복되면 대각화 실패입니다.
- `diagonalization`을 바꾸고 `nbnd`를 늘리세요 (특히 금속·자성계).
- `diago_david_ndim` 2 → 4도 개선책입니다 (메모리 증가).

### cdiaghg: problems computing cholesky / S matrix not positive definite

- 겹침 행렬이 특이해진 경우. 대개 **원자가 너무 가깝거나, 초기 파동함수가
  나쁘거나, 기저가 선형종속**.
- `startingwfc = 'random'`으로 바꿔 보세요.
- 구조를 다시 확인하세요 — 원자 두 개가 겹쳐 있는 경우가 의외로 많습니다.

### Not enough space allocated for radial FFT

- 셀이 매우 크거나 원자가 셀 경계에 걸친 경우.
- `cell_factor`를 늘리거나 원자를 셀 안쪽으로 옮기세요.

### checkallsym: some of the original symmetry operations not satisfied

- 초기 구조에서 잡힌 대칭을 이후의 원자 이동이 깨뜨린 경우. **MD에서 거의
  반드시 만납니다** (열운동이 대칭 위치를 즉시 무너뜨림).
- MD는 `&SYSTEM`에 `nosym = .true.`를 넣으세요 ([16장](16-molecular-dynamics.html)).
  구조 최적화에서 나온다면 초기 구조의 대칭이 수치 잡음 수준으로만 성립했던
  것이니 구조를 정밀화하거나 역시 `nosym`을 고려하세요.

## 병렬·메모리·I/O 문제

| 메시지 | 원인 | 해결 |
|---|---|---|
| `some processors have no planes` | MPI 랭크가 FFT 격자보다 많음 | 랭크 축소 또는 `-nk` 증가 |
| `npool must divide nproc` | `-nk` 설정 오류 | `nproc`을 `-nk`로 나누어떨어지게 |
| `ndiag must be a square number` | `-nd` 설정 오류 | 1, 4, 9, 16, ... |
| `Error in routine davcio` | 디스크 부족, 권한, `outdir` 불일치 | 용량·경로 확인 |
| `cannot open file ... .save/charge-density.dat` | `prefix`/`outdir`이 선행 계산과 다름 | 전 단계와 동일하게 |
| 메모리 부족(OOM) | `-nk` 과다 (풀마다 밀도 사본) | `-nk` 감소, `diago_david_ndim` 감소 |

## 에러 없이 틀리는 경우 — 가장 위험한 범주

QE는 물리적으로 틀린 결과도 깔끔하게 출력합니다. 다음을 습관적으로
점검하세요.

| 증상 | 숨은 원인 | 점검 방법 |
|---|---|---|
| 총에너지가 문헌과 크게 다름 | 유사퍼텐셜이 다름 | 총에너지 **절대값은 비교 대상이 아님**. 같은 조건의 차이만 의미 있음 |
| 자기모멘트가 0으로 붕괴 | 초기 자화 부족, smearing 과다 | `starting_magnetization` 증가, `degauss` 감소 |
| AFM인데 `total magnetization` ≠ 0 | 라벨 분리 실패, 대칭이 배열을 강제 | `ntyp` 늘려 라벨 분리, `Sym. Ops.` 확인 |
| FeO가 금속으로 나옴 | GGA의 자기상호작용 오차 | DFT+U 적용. U만으로 부족하면 `starting_ns_eigenvalue` |
| U를 켰는데도 금속 | d 궤도 점유가 잘못된 극소값에 갇힘 | `starting_ns_eigenvalue`로 점유 유도 |
| `vc-relax` 결과가 재현 안 됨 | Pulay stress | 최종 구조로 `scf` 재실행 |
| DOS가 톱니처럼 거침 | nscf k-점 부족 | 격자 증가 + `tetrahedra_opt` |
| 밴드 경로가 이상함 | `crystal_b` 좌표계 혼동 | `tpiba_b` 사용 또는 SeeK-path |
| 슬랩 에너지가 진공 두께에 민감 | 쌍극자 상호작용 | `dipfield` 활성화, 진공 증가 |
| 힘이 수렴하지 않음 | 에너지 기준으로만 수렴을 봤음 | 힘 기준 수렴 테스트 별도 수행 |

## 자성 전이금속 산화물 전용 체크리스트

FeO, Fe₂O₃, Fe₃O₄ 같은 계에서 반복적으로 겪는 문제들입니다.

- `ecutrho`가 `ecutwfc`의 최소 10배인가 (Fe PAW는 특히 요구가 큼)
- 스핀 up/down 라벨을 다른 원자종으로 분리했는가
- `mixing_beta` 0.3 이하 + `mixing_mode='local-TF'`인가
- 여러 초기 자화에서 출발해 **에너지가 가장 낮은 해**를 골랐는가
- `HUBBARD` 카드가 **신문법**인가 (`lda_plus_u`가 남아 있지 않은가)
- 투영자(`ortho-atomic` 등)를 U 값과 세트로 기록해 두었는가
- `starting_ns_eigenvalue`로 올바른 궤도 점유를 유도했는가
- `hp.x`를 쓴다면 `nq` 수렴을 확인했는가
- 데이터셋 전체에서 컷오프·k-점·smearing·U가 완전히 동일한가

## 도움을 구할 때

[QE users 메일링 리스트 아카이브](https://www.mail-archive.com/users@lists.quantum-espresso.org/)에서
먼저 검색하세요. 대부분의 문제가 이미 답변되어 있고, 개발자(Giannozzi,
Timrov 등)가 직접 답한 스레드는 사실상 공식 문서에 준합니다.

질문할 때 반드시 포함할 것:

1. QE 버전과 빌드 방식
2. **입력 파일 전문**
3. 출력의 에러 부분 **앞뒤 30줄**
4. 이미 시도해 본 것
