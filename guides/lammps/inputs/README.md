# inputs/ — 모듈식 LAMMPS 입력 파일

본 디렉토리는 5단계 시뮬레이션 프로토콜과 4개 프레임워크 (OPLS-AA / TraPPE-UA × PPPM / MSM)
를 모두 지원하는 모듈식 입력 파일을 제공한다.

## 파일 구조

| 파일 | 용도 | 비고 |
|------|------|------|
| `common.in`        | 단위, atom_style, neighbor, comm | 모든 stage 에서 include |
| `kspace_pppm.in`   | PPPM 정전기 + `lj/cut/coul/long` pair_style | 슬랩 보정 포함 |
| `kspace_msm.in`    | MSM 정전기 + `lj/cut/coul/msm` pair_style | 슬랩 보정 불필요 |
| `ff_opls_aa.in`    | OPLS-AA 결합/각도/이면각/pair_modify/coeffs | 12 atom types |
| `ff_trappe_ua.in`  | TraPPE-UA 결합/각도/pair_modify/coeffs | 6 atom types |
| `01_soft.in`       | Stage 1 : Soft relaxation (nve/limit) | 50~100 ps |
| `02_min.in`        | Stage 2 : Energy minimization (CG) | ~10000 iter |
| `03_heat.in`       | Stage 3 : 4단계 가열 0.1 → 300 K | 약 700 ps |
| `04_eq.in`         | Stage 4 : NVT 평형 | OPLS-AA 7.5 ns / TraPPE 3 ns |
| `05_prod.in`       | Stage 5 : Production + 분석 | 10 ~ 20 ns |

## 프레임워크 전환 방법

각 stage 파일 (`01_soft.in` ~ `05_prod.in`) 의 상단 `include` 블록 두 줄만 수정한다.

```lammps
# 예: OPLS-AA + PPPM (기본)
include kspace_pppm.in
include ff_opls_aa.in

# OPLS-AA + MSM 으로 전환
include kspace_msm.in
include ff_opls_aa.in

# TraPPE-UA + PPPM
include kspace_pppm.in
include ff_trappe_ua.in

# TraPPE-UA + MSM
include kspace_msm.in
include ff_trappe_ua.in
```

추가로 stage 파일 내 `read_data ../opls.data` 또는 `../trappe.data` 도 데이터 파일에
맞춰 변경한다. `group cu type 12` (OPLS-AA) 또는 `group cu type 6` (TraPPE-UA) 의
Cu 타입 번호도 함께 점검한다.

## 실행 순서

```bash
# 단일 코어
lmp_serial -in 01_soft.in
lmp_serial -in 02_min.in
lmp_serial -in 03_heat.in
lmp_serial -in 04_eq.in
lmp_serial -in 05_prod.in

# 병렬 (40 코어 예시)
mpirun -np 40 lmp_mpi -in 01_soft.in
mpirun -np 40 lmp_mpi -in 02_min.in
mpirun -np 40 lmp_mpi -in 03_heat.in
mpirun -np 40 lmp_mpi -in 04_eq.in
mpirun -np 40 lmp_mpi -in 05_prod.in
```

각 stage 는 직전 stage 의 `stageN.restart` 파일을 자동으로 읽으므로 순서대로
실행해야 한다.

## 주의 사항

1. **Atom type 번호** : 본 템플릿은 OPLS-AA Cu = type 12, TraPPE-UA Cu = type 6
   가정. 실제 데이터 파일의 타입 번호를 확인하고 `group cu type N` 라인을
   수정해야 한다.
2. **Pair coefficient** : 데이터 파일에 `Pair Coeffs` 섹션이 포함된 경우, `ff_*.in`
   의 `pair_coeff` 라인은 주석 처리할 수 있다. 데이터 파일이 우선한다.
3. **Wall 위치** : `wall/lj93 zhi EDGE` 는 박스 상단 z 면에 벽을 설치한다.
   Cu 슬랩이 하단에 있고 진공이 상단이라는 본 가이드의 좌표 규약과 일치해야 한다.
4. **Timestep** : 본 파일들은 0.5 fs (OPLS-AA 적정). SHAKE 사용 또는 TraPPE-UA
   에서는 2.0 fs 까지 늘릴 수 있고, 그 경우 `run` 카운트도 그에 맞춰 줄여야 한다.

자세한 설명은 [docs/05-protocol](../docs/05-protocol.md) 와
[docs/08-troubleshooting](../docs/08-troubleshooting.md) 를 참조한다.
