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
| `04_eq.in`         | Stage 4 : NVT 평형 | 1 + 6.5 ns (조성 프로파일로 판단) |
| `05_prod.in`       | Stage 5 : Production + 분석 | 10 ns |

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
3. **Wall 위치** : `wall/lj93 zhi EDGE` 는 박스 상단 z 면에 벽을 설치하고, `organic`
   그룹(유기 분자)에만 작용한다. Cu 슬랩이 하단에 있고 진공이 상단이라는 본 가이드의
   좌표 규약과 일치해야 한다.
4. **Timestep** : 본 파일들은 0.5 fs. 제약 없이 C–H, O–H 를 그대로 두면 이 값을 유지한다.
   TraPPE-UA 에서도 에탄올 O–H 를 SHAKE 로 묶지 않으면 1 fs 이상은 위험하다
   ([3.5절](../cu-03-force-fields.html) 참고). `run` 카운트는 timestep 에 맞춰 바꾼다.
5. **Cu–Cu 상호작용** : 이 템플릿은 Cu 를 `setforce 0` 으로 고정하고
   `neigh_modify exclude type 12 12` 로 Cu–Cu 쌍을 계산에서 뺀다. 이 때문에
   "Neighbor exclusions used with KSpace solver" 경고가 나오지만 Cu 전하가 0 이라 무해하다.

## 확인한 것

`opls.data` ([다운로드](/files/blog/pppm-vs-msm/opls.data)) 를 이 디렉토리 한 단계 위에 두고
`run` 길이만 줄여 LAMMPS 22 Jul 2025 로 다섯 stage 를 PPPM, MSM 각각 끝까지 돌렸다.
MSM 에서는 Coulomb cutoff 를 자동 조정했다는 경고가 나온다 ([4장](../cu-04-electrostatics.html)).
`opls.data` 자체의 문제(초기 겹침, 비표준 전하 등)는 [2장](../cu-02-data-files.html) 에 정리했다.

자세한 설명은 [5장](../cu-05-protocol.html) 과
[8장](../cu-08-troubleshooting.html) 을 참조한다.
