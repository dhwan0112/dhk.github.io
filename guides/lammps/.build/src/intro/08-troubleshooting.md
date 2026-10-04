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

<p class="amm-id">NOTE 31-08-00 · 트러블슈팅과 운영</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 LAMMPS 실행 중 발생하는 오류와 의심스러운 결과의 결함 분리 절차를 다룬다.
2. 이 노트는 병렬 실행, 디스크 관리, 운영 습관을 함께 다룬다.

### B. 적용 범위

1. 자주 만나는 오류 메시지 일곱 가지를 다룬다(3.A–3.G).
2. 오류 없이 끝났지만 결과가 의심스러운 경우를 다룬다(3.H).
3. 병렬 실행 성능과 디스크 사용량 문제를 다룬다(3.I, 3.J).

### C. 결과 요약

1. "Lost atoms" 는 가장 흔한 오류다. 발생 시점에 따라 원인과 조치가 다르다.
2. 결과가 의심스러우면 NVE 보존 → 온도 → 압력·밀도 → RDF → 시각화 순서로 점검한다.
3. timing breakdown에서 `Comm` 비중이 30% 이상이면 코어를 너무 많이 쓴 것이다.

## 2. 준비 정보

### A. 참조 자료

| 자료 | 내용 |
|------|------|
| [docs.lammps.org](https://docs.lammps.org/) | 공식 매뉴얼. 명령어별 상세 옵션과 예제 |
| [lammps.org/forum.html](https://www.lammps.org/forum.html) | 사용자 포럼. 실전 질문/답변 검색에 좋음 |
| [lammpstutorials.github.io](https://lammpstutorials.github.io/) | Gravelle 외(저자 다수)의 단계별 튜토리얼. LJ 액체, 나노튜브 변형, GCMC 등 실전 예제 풍부 |
| `examples/` 폴더 | LAMMPS 소스 트리에 포함된 공식 예제. 작은 단위로 학습하기 좋음 |
| `bench/` 폴더 | 성능 벤치마크 입력들 |
| Mark Tuckerman, *Statistical Mechanics: Theory and Molecular Simulation* | MD 이론 교과서 표준 |
| Daan Frenkel, Berend Smit, *Understanding Molecular Simulation* | MD 알고리즘 교과서 표준 |

### B. 공구 및 장비

| 항목 | 용도 |
|---|---|
| MPI (`mpirun`) | 병렬 실행 (3.I) |
| OpenMP (`-sf omp`) | 코어당 쓰레드 병렬 (3.I) |
| KOKKOS (`-k on g 1 -sf kk`) | GPU 가속 (3.I) |
| OVITO, VMD | trajectory 시각화 (3.H, 4.A) |

## 3. 결함 분리 절차

### A. 증상: "ERROR: Lost atoms" 또는 "lost atom" 경고

1. 가능한 원인: 원자가 박스 밖으로 나갔거나, 너무 큰 힘을 받아 폭주했다.
2. 점검: 오류가 처음 나는 시점과 경계 조건을 확인한다.
    1. 첫 timestep에 바로 나면 초기 구조에 너무 가까운 원자 쌍이 있을 가능성이 높다.
    1. 수천~수만 스텝 뒤에 나면 timestep 이 너무 크다.
    1. 비주기 경계(`f`)에서 나면 원자가 박스 밖으로 나가는 경우다.
3. 조치: 점검 결과에 따라 아래 중 하나를 수행한다.
    1. 첫 timestep: `minimize` 를 먼저 돌린다. 또는 첫 1000 스텝은 `fix nve/limit`(한 스텝당 최대 변위 제한)을 건다.
    1. 수천~수만 스텝 뒤: timestep 을 절반으로 줄여 다시 돌린다.
    1. 비주기 경계: `fix wall/lj93` 같은 벽을 명시적으로 둘러 원자가 박스 밖으로 나가지 못하게 한다.

### B. 증상: "ERROR: Bond/Angle atoms missing"

1. 가능한 원인: 분자 시스템에서 한 분자의 원자가 박스 경계 양쪽에 걸쳐 있다. MPI 통신 buffer가 그 분자를 한 번에 보지 못하면 이 오류가 난다.
2. 점검: 박스가 가장 큰 분자보다 두 배 이상 큰지 확인한다.
3. 조치: `neighbor` skin 을 늘린다(`neighbor 5.0 bin`).
4. 조치: 그래도 안 되면 `comm_modify cutoff 15.0` 으로 통신 cutoff 를 강제로 늘린다.

### C. 증상: "ERROR: Neighbor list overflow"

1. 가능한 원인: 이웃 리스트가 미리 잡아 둔 메모리를 넘었다.
2. 조치: 이웃 리스트 메모리 한도를 늘린다.

```lammps
neigh_modify    one 5000 page 100000
```

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
`one` 은 한 원자가 가질 수 있는 최대 이웃 수, `page` 는 메모리 페이지 크기다.
</div>

### D. 증상: "ERROR: Could not find pair_coeff for type X-Y"

1. 가능한 원인: 일부 type 조합의 `pair_coeff` 가 정의되지 않았다.
2. 점검: `pair_coeff` 로 모든 type 조합을 정의했는지 확인한다.
3. 조치: 누락된 조합을 정의한다. 또는 아래 명령으로 i-j (i ≠ j) 조합을 자동으로 만들게 둔다.

```lammps
pair_modify     mix arithmetic
```

### E. 증상: "ERROR: Out of range atoms - cannot compute PPPM"

1. 가능한 원인: PPPM이 격자 바깥의 전하를 처리하지 못했다. 보통은 슬랩 시스템에서 정전기 보정을 빠뜨린 경우다.
2. 점검: 슬랩 시스템인지, 정전기 보정이 들어 있는지 확인한다.
3. 조치: 슬랩 보정을 더한다.

```lammps
kspace_modify   slab 3.0
```

### F. 증상: "WARNING: Inconsistent image flags"

1. 가능한 원인: 분자가 박스 경계를 잘못 넘으면서 image flag(어느 주기 셀에 속하는지)가 어긋났다.
2. 점검: 현재 평형화 단계인지 분석 단계인지 확인한다. 평형화 중에는 무시해도 된다.
3. 조치: 분석 단계에서는 데이터를 한 번 썼다가 다시 읽어 정리하기도 한다.

```lammps
write_data      check.data
read_data       check.data
```

### G. 증상: "ERROR: Energy was not tallied on neighbor sublist"

1. 가능한 원인: 대개 `pair_modify shift yes` 나 `tail yes` 와 호환되지 않는 pair_style 을 쓴 경우다.
2. 조치: pair_style을 바꾸거나 해당 옵션을 뺀다.

### H. 증상: 오류 없이 끝났지만 결과가 의심스럽다

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
오류 없이 끝난 실행도 결과가 틀릴 수 있다. 아래 순서로 점검하기 전에는 결과를 쓰지 않는다.
</div>

1. NVE 보존을 점검한다. 짧게 NVE로 돌렸을 때 총 에너지가 거의 일정해야 한다.
2. 총 에너지 변동이 ±0.01% 이상이면 timestep 이 크다. timestep 을 줄인다.
3. 온도 안정성을 점검한다. NVT의 setpoint 와 실제 평균 온도가 ±1 K 이내인지 본다.
4. 압력 분포를 점검한다. NPT 라면 밀도가 안정된 값에 수렴하는지 본다.
5. RDF 첫 피크 위치를 점검한다. 첫 g(r) 피크가 알려진 결합 길이/접근 거리와 맞는지 본다.
6. OVITO/VMD로 trajectory를 직접 한 번 재생한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
시각화하면 숫자만으로는 안 보이는 이상 거동(클러스터링, 표면 누출 등)이 한눈에 들어온다.
</div>

### I. 증상: 코어 수를 늘려도 기대만큼 빨라지지 않는다

1. 가능한 원인: LAMMPS는 MPI 기반이라 코어 수를 늘리면 거의 선형으로 빨라진다. 다만 통신 비용 때문에 늘 그렇지는 않다.
2. 점검: 실행 방식을 확인한다.

```bash
# MPI 4 코어
mpirun -np 4 lmp -in in.run

# 8 코어 + OpenMP 2 쓰레드/코어
export OMP_NUM_THREADS=2
mpirun -np 8 lmp -sf omp -pk omp 2 -in in.run

# GPU 가속 (KOKKOS)
mpirun -np 4 lmp -k on g 1 -sf kk -in in.run
```

3. 점검: 시스템 크기에 맞는 코어 수인지 아래 표와 비교한다.

| 시스템 크기 | 추천 코어 수 |
|-------------|--------------|
| ~수천 원자 | 1~4 |
| ~수만 원자 | 8~32 |
| ~수십만 원자 | 64~256 |
| 수백만 원자 이상 | 수백~수천 |

4. 점검: 원자 수가 코어 수의 100배 아래인지 확인한다. 이 경우 통신 오버헤드가 커진다.
5. 점검: 의심스러우면 `thermo` 의 `cpu` 컬럼을 보면서 짧게 비교 실행한다.
6. 점검: 시뮬레이션이 끝나면 LAMMPS가 자동으로 출력하는 timing breakdown을 확인한다.

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

7. 판정: `Pair` 나 `Kspace` 가 대부분을 차지하는 게 정상이다.
8. 조치: `Comm` 비중이 30% 이상이면 코어를 너무 많이 쓴 것이다. 코어 수를 줄인다.
9. 조치: `Neigh` 가 지나치게 크면 `neigh_modify every` 를 늘려 재구성 횟수를 줄인다.

### J. 증상: dump 파일로 디스크가 금방 찬다

1. 가능한 원인: 긴 시뮬레이션에서 dump 주기가 짧거나 텍스트 형식을 쓴다.
2. 조치: `dump custom 5000 ...` 처럼 주기를 늘린다.
3. 조치: 좌표만 필요하면 `dump dcd` 나 `dump netcdf` (바이너리)를 쓴다. 텍스트보다 훨씬 작다.
4. 조치: `dump_modify ... pad 8` 로 파일명을 정렬되게 만든다. 후처리 도구가 알아서 인식한다.
5. 조치: restart 파일도 쌓이면 무거우니 오래된 것은 주기적으로 지운다.

## 4. 시험 및 검사

### A. 운영 습관 점검

1. `thermo` 컬럼은 넉넉하게 둔다. `step temp pe ke etotal press density vol` 정도는 늘 켜 둔다.
2. 입력은 변수로 매개변수화한다. 온도, 시드, run 길이를 `variable` + `${...}` 로 빼 둔다.
3. `include` 로 입력을 잘게 나눈다. 힘장 정의, 시스템 정의, run 절차를 분리한다.
4. `restart` 는 반드시 켠다. 4시간 넘게 걸리는 시뮬레이션이라면 예외가 없다.
5. 결과는 꼭 한 번 시각화한다. OVITO/VMD에서 trajectory를 한 번 재생한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
`thermo` 컬럼은 나중에 무엇이 이상했는지 추적할 때 가장 먼저 보는 정보다. 변수로 매개변수화하면 여러 조건을 입력 파일 하나로 비교할 수 있다. 입력을 나눠 두면 한 부분만 갈아 끼우기 쉽다. 숫자만 보면 놓치는 실수가 자주 있으므로, trajectory 재생이 가장 빠른 sanity check 다.
</div>

## 5. 종료

### B. 후속 작업

1. 이 입문 가이드는 LAMMPS 매뉴얼의 4-part 구조를 따라 한 번 훑어보는 데 목적이 있다.
2. 같은 주제를 다른 관점, 다른 예제로 다시 본다. 이해가 훨씬 단단해진다.
3. 영문 자료 [lammpstutorials.github.io](https://lammpstutorials.github.io/)를 이 가이드와 짝지어 읽는다.
4. 같은 LJ 액체를 어떻게 다르게 풀어 가는지, 어떤 진단 명령을 끼워 넣는지 비교한다.
5. 실제 연구 문제에 LAMMPS를 적용한 사례는 [Cu 표면 흡착 시리즈](cu-overview.html)에서 다룬다.
