---
layout: default
title: "8. 트러블슈팅과 운영 팁"
nav_order: 9
---

# 8. 트러블슈팅과 운영 팁
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 8.1 가장 자주 마주치는 오류 일곱 가지

### "ERROR: Lost atoms" 또는 "lost atom" 경고

가장 흔한 오류입니다. 원자가 박스 밖으로 나갔거나, 너무 큰 힘을 받아 폭주한
경우입니다. 진단 순서:

1. **첫 timestep에 바로 발생** → 초기 구조가 너무 가까운 원자 쌍을 갖고 있을
   확률이 높음. `minimize` 를 먼저 돌리거나, 첫 1000 스텝은 `fix nve/limit`
   (한 스텝당 최대 변위 제한)을 적용.
2. **수천~수만 스텝 후 발생** → timestep 이 너무 큼. 절반으로 줄여서 재시도.
3. **비주기 경계(`f`)에서 발생** → `fix wall/lj93` 같은 벽을 명시적으로
   둘러서 원자가 박스 밖으로 나가지 못하게 해야 함.

### "ERROR: Bond/Angle atoms missing"

분자 시스템에서 한 분자의 원자가 박스 경계 양쪽에 걸쳐 있을 때, MPI 통신
buffer가 그 분자를 한 번에 못 보면 나는 오류입니다.

- `neighbor` skin 을 늘리세요 (`neighbor 5.0 bin`).
- 가장 큰 분자보다 박스가 두 배 이상 커야 합니다.
- 그래도 해결이 안 되면 `comm_modify cutoff 15.0` 으로 통신 cutoff 를 강제로
  늘리세요.

### "ERROR: Neighbor list overflow"

이웃 리스트가 미리 잡아둔 메모리를 넘었습니다.

```lammps
neigh_modify    one 5000 page 100000
```

`one` 은 한 원자가 가질 수 있는 이웃 최대 수, `page` 는 메모리 페이지 크기입니다.

### "ERROR: Could not find pair_coeff for type X-Y"

`pair_coeff` 에 모든 type 조합을 정의했는지 확인. 또는

```lammps
pair_modify     mix arithmetic
```

로 i-j (i ≠ j) 조합을 자동 생성하게 두는 방법도 있습니다.

### "ERROR: Out of range atoms - cannot compute PPPM"

PPPM이 격자 외부의 전하를 처리 못 함. 원인은 보통 슬랩 시스템에서 정전기
보정을 안 한 경우입니다.

```lammps
kspace_modify   slab 3.0
```

### "WARNING: Inconsistent image flags"

분자가 박스 경계를 잘못 넘으면서 image flag(어느 주기 셀에 속하는지)가
어긋났습니다. 평형화 중에는 무시해도 되지만, 분석 단계에서는

```lammps
write_data      check.data
read_data       check.data
```

식으로 한 번 cycle을 돌려 정리하기도 합니다.

### "ERROR: Energy was not tallied on neighbor sublist"

대부분 `pair_modify shift yes` 또는 `tail yes` 와 호환 안 되는 pair_style
을 쓴 경우. pair_style을 바꾸거나 옵션을 제거하면 해결됩니다.

## 8.2 결과가 의심스러울 때 점검 순서

오류 없이 끝났더라도 결과가 이상하면 다음 순서로 점검하시기를 권합니다.

1. **NVE 보존** — 짧게 NVE로 돌렸을 때 총 에너지가 거의 일정해야 함.
   변동이 ±0.01% 이상이면 timestep 이 큼.
2. **온도 안정성** — NVT의 setpoint 와 실제 평균 온도가 ±1 K 이내인지.
3. **압력 분포** — NPT 라면 밀도가 안정 값에 수렴하는지.
4. **RDF 첫 피크 위치** — 첫 g(r) 피크가 알려진 결합 길이/접근 거리와 일치하는지.
5. **시각화** — OVITO/VMD로 trajectory를 직접 한 번 보십시오.
   숫자만 봐서는 보이지 않는 비정상 행동(클러스터링, 표면 누출 등)이 한눈에 보입니다.

## 8.3 병렬 실행

LAMMPS는 MPI 기반이므로 코어 수가 늘어날수록 거의 선형으로 빨라집니다.
다만 통신 비용이 있어 항상 그런 것은 아닙니다.

```bash
# MPI 4 코어
mpirun -np 4 lmp -in in.run

# 8 코어 + OpenMP 2 쓰레드/코어
export OMP_NUM_THREADS=2
mpirun -np 8 lmp -sf omp -pk omp 2 -in in.run

# GPU 가속 (KOKKOS)
mpirun -np 4 lmp -k on g 1 -sf kk -in in.run
```

### 코어 수 선택 가이드

| 시스템 크기 | 추천 코어 수 |
|-------------|--------------|
| ~수천 원자 | 1~4 |
| ~수만 원자 | 8~32 |
| ~수십만 원자 | 64~256 |
| 수백만 원자 이상 | 수백~수천 |

원자 수가 코어 수의 100배 이하로 떨어지면 통신 오버헤드가 커집니다.
의심되면 `thermo` 의 `cpu` 컬럼을 보면서 짧게 비교 실행해 보십시오.

### LAMMPS 자체 timing 진단

시뮬레이션이 끝나면 LAMMPS는 자동으로 다음과 같은 timing breakdown을
출력합니다.

```text
MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    |  12.5      |  12.7      |  12.9      |   1.2 |  61.0
Bond    |   0.3      |   0.3      |   0.4      |   0.1 |   1.7
Kspace  |   3.4      |   3.5      |   3.6      |   0.5 |  16.7
Neigh   |   1.1      |   1.1      |   1.2      |   0.2 |   5.3
Comm    |   2.0      |   2.1      |   2.3      |   1.8 |  10.0
...
```

`Pair` 또는 `Kspace` 가 압도적으로 큰 비중을 차지하는 것이 정상입니다.
`Comm` 비중이 30% 이상이면 코어를 너무 많이 쓴 것이고, `Neigh` 가 너무
크다면 `neigh_modify every` 를 늘려 재구성을 줄일 수 있습니다.

## 8.4 디스크와 메모리 관리

긴 시뮬레이션은 dump 파일로 디스크가 빠르게 찹니다.

- `dump custom 5000 ...` 처럼 주기를 늘리세요.
- 좌표만 필요하면 `dump dcd` 또는 `dump netcdf` (바이너리)가 텍스트보다
  훨씬 작습니다.
- `dump_modify ... pad 8` 로 정렬된 파일명을 쓰면 후처리 도구가 자동
  인식합니다.

restart 파일도 누적되면 무거우므로 오래된 것은 주기적으로 정리하시기 바랍니다.

## 8.5 좋은 습관 다섯 가지

1. **`thermo` 컬럼을 충분히 늘려라**. `step temp pe ke etotal press density vol`
   정도는 항상 켜 두세요. 사후에 무엇이 이상했는지 추적하는 1차 정보원입니다.
2. **변수로 입력을 매개변수화하라**. 온도, 시드, run 길이는 `variable` +
   `${...}` 로. 여러 조건 비교 실험이 한 입력 파일로 처리됩니다.
3. **`include` 로 입력을 잘게 쪼개라**. 힘장 정의, 시스템 정의, run 절차를
   분리해 두면 한 부분만 갈아 끼우기 쉽습니다.
4. **반드시 `restart` 를 켜라**. 4시간 이상 걸리는 모든 시뮬레이션은 그렇게
   하세요.
5. **결과는 항상 한 번 시각화하라**. 숫자만 보면 놓치는 실수가 자주 있습니다.
   OVITO/VMD에서 trajectory를 한 번 돌려보는 것이 가장 빠른 sanity check
   입니다.

## 8.6 더 읽어 볼 자료

| 자료 | 내용 |
|------|------|
| [docs.lammps.org](https://docs.lammps.org/) | 공식 매뉴얼. 명령어별 상세 옵션과 예제 |
| [lammps.org/forum.html](https://www.lammps.org/forum.html) | 사용자 포럼. 실전 질문/답변 검색에 좋음 |
| `examples/` 폴더 | 소스 트리에 포함된 예제. 작은 단위로 학습하기 좋음 |
| `bench/` 폴더 | 성능 벤치마크 입력들 |
| Mark Tuckerman, *Statistical Mechanics: Theory and Molecular Simulation* | MD 이론 교과서 표준 |
| Daan Frenkel, Berend Smit, *Understanding Molecular Simulation* | MD 알고리즘 교과서 표준 |

본 입문 가이드는 여기서 끝납니다. 실제 연구 문제에 LAMMPS를 적용하는
구체적 사례는 [Cu 표면 흡착 시리즈](cu-overview.html)에서 이어집니다.
