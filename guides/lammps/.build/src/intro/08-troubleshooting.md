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

## 8.1 자주 만나는 오류

### "ERROR: Lost atoms" 또는 "lost atom" 경고

가장 흔한 오류다. 원자가 박스 밖으로 나갔거나, 너무 큰 힘을 받아 폭주한
경우에 난다. 다음 순서로 진단한다.

1. 첫 timestep에 바로 난다면 초기 구조에 너무 가까운 원자 쌍이 있을
   가능성이 높다. `minimize` 를 먼저 돌리거나, 첫 1000 스텝은 `fix nve/limit`
   (한 스텝당 최대 변위 제한)을 건다.
2. 수천~수만 스텝 뒤에 난다면 timestep 이 너무 크다. 절반으로 줄여 다시 돌린다.
3. 비주기 경계(`f`)에서 난다면 `fix wall/lj93` 같은 벽을 명시적으로
   둘러 원자가 박스 밖으로 나가지 못하게 해야 한다.

### "ERROR: Bond/Angle atoms missing"

분자 시스템에서 한 분자의 원자가 박스 경계 양쪽에 걸쳐 있을 때, MPI 통신
buffer가 그 분자를 한 번에 보지 못하면 나는 오류다.

- `neighbor` skin 을 늘린다(`neighbor 5.0 bin`).
- 박스는 가장 큰 분자보다 두 배 이상 커야 한다.
- 그래도 안 되면 `comm_modify cutoff 15.0` 으로 통신 cutoff 를 강제로
  늘린다.

### "ERROR: Neighbor list overflow"

이웃 리스트가 미리 잡아 둔 메모리를 넘었다는 뜻이다.

```lammps
neigh_modify    one 5000 page 100000
```

`one` 은 한 원자가 가질 수 있는 최대 이웃 수, `page` 는 메모리 페이지 크기다.

### "ERROR: Could not find pair_coeff for type X-Y"

`pair_coeff` 로 모든 type 조합을 정의했는지 확인한다. 아니면

```lammps
pair_modify     mix arithmetic
```

로 i-j (i ≠ j) 조합을 자동으로 만들게 둘 수도 있다.

### "ERROR: Out of range atoms - cannot compute PPPM"

PPPM이 격자 바깥의 전하를 처리하지 못해서 나는 오류로, 보통은 슬랩 시스템에서
정전기 보정을 빠뜨린 경우다.

```lammps
kspace_modify   slab 3.0
```

### "WARNING: Inconsistent image flags"

분자가 박스 경계를 잘못 넘으면서 image flag(어느 주기 셀에 속하는지)가
어긋났다. 평형화 중에는 무시해도 되지만, 분석 단계에서는

```lammps
write_data      check.data
read_data       check.data
```

식으로 한 번 썼다가 다시 읽어 정리하기도 한다.

### "ERROR: Energy was not tallied on neighbor sublist"

대개 `pair_modify shift yes` 나 `tail yes` 와 호환되지 않는 pair_style
을 쓴 경우다. pair_style을 바꾸거나 해당 옵션을 빼면 해결된다.

## 8.2 결과가 의심스러울 때 점검 순서

오류 없이 끝났는데 결과가 이상하다면 다음 순서로 점검한다.

1. NVE 보존: 짧게 NVE로 돌렸을 때 총 에너지가 거의 일정해야 한다.
   변동이 ±0.01% 이상이면 timestep 이 크다.
2. 온도 안정성: NVT의 setpoint 와 실제 평균 온도가 ±1 K 이내인지 본다.
3. 압력 분포: NPT 라면 밀도가 안정된 값에 수렴하는지 본다.
4. RDF 첫 피크 위치: 첫 g(r) 피크가 알려진 결합 길이/접근 거리와 맞는지 본다.
5. 시각화: OVITO/VMD로 trajectory를 직접 한 번 돌려 본다.
   숫자만으로는 안 보이는 이상 거동(클러스터링, 표면 누출 등)이 한눈에 들어온다.

## 8.3 병렬 실행

LAMMPS는 MPI 기반이라 코어 수를 늘리면 거의 선형으로 빨라진다.
다만 통신 비용 때문에 늘 그렇지는 않다.

```bash
# MPI 4 코어
mpirun -np 4 lmp -in in.run

# 8 코어 + OpenMP 2 쓰레드/코어
export OMP_NUM_THREADS=2
mpirun -np 8 lmp -sf omp -pk omp 2 -in in.run

# GPU 가속 (KOKKOS)
mpirun -np 4 lmp -k on g 1 -sf kk -in in.run
```

### 코어 수 고르기

| 시스템 크기 | 추천 코어 수 |
|-------------|--------------|
| ~수천 원자 | 1~4 |
| ~수만 원자 | 8~32 |
| ~수십만 원자 | 64~256 |
| 수백만 원자 이상 | 수백~수천 |

원자 수가 코어 수의 100배 아래로 떨어지면 통신 오버헤드가 커진다.
의심스러우면 `thermo` 의 `cpu` 컬럼을 보면서 짧게 비교 실행해 보자.

### LAMMPS 자체 timing 진단

시뮬레이션이 끝나면 LAMMPS는 다음과 같은 timing breakdown을
자동으로 출력한다.

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

`Pair` 나 `Kspace` 가 대부분을 차지하는 게 정상이다.
`Comm` 비중이 30% 이상이면 코어를 너무 많이 쓴 것이고, `Neigh` 가 지나치게
크다면 `neigh_modify every` 를 늘려 재구성 횟수를 줄일 수 있다.

## 8.4 디스크와 메모리 관리

긴 시뮬레이션을 돌리면 dump 파일로 디스크가 금방 찬다.

- `dump custom 5000 ...` 처럼 주기를 늘린다.
- 좌표만 필요하면 `dump dcd` 나 `dump netcdf` (바이너리)가 텍스트보다
  훨씬 작다.
- `dump_modify ... pad 8` 로 파일명을 정렬되게 만들면 후처리 도구가 알아서
  인식한다.

restart 파일도 쌓이면 무거우니 오래된 것은 주기적으로 지운다.

## 8.5 운영 습관

1. `thermo` 컬럼은 넉넉하게 둔다. `step temp pe ke etotal press density vol`
   정도는 늘 켜 두자. 나중에 무엇이 이상했는지 추적할 때 가장 먼저 보는 정보다.
2. 입력은 변수로 매개변수화한다. 온도, 시드, run 길이를 `variable` +
   `${...}` 로 빼 두면 여러 조건을 입력 파일 하나로 비교할 수 있다.
3. `include` 로 입력을 잘게 나눈다. 힘장 정의, 시스템 정의, run 절차를
   분리해 두면 한 부분만 갈아 끼우기 쉽다.
4. `restart` 는 반드시 켠다. 4시간 넘게 걸리는 시뮬레이션이라면 예외 없이.
5. 결과는 꼭 한 번 시각화한다. 숫자만 보면 놓치는 실수가 자주 있다.
   OVITO/VMD에서 trajectory를 한 번 돌려 보는 게 가장 빠른 sanity check
   다.

## 8.6 더 읽어 볼 자료

| 자료 | 내용 |
|------|------|
| [docs.lammps.org](https://docs.lammps.org/) | 공식 매뉴얼. 명령어별 상세 옵션과 예제 |
| [lammps.org/forum.html](https://www.lammps.org/forum.html) | 사용자 포럼. 실전 질문/답변 검색에 좋음 |
| [lammpstutorials.github.io](https://lammpstutorials.github.io/) | Gravelle 외(저자 다수)의 단계별 튜토리얼. LJ 액체, 나노튜브 변형, GCMC 등 실전 예제 풍부 |
| `examples/` 폴더 | LAMMPS 소스 트리에 포함된 공식 예제. 작은 단위로 학습하기 좋음 |
| `bench/` 폴더 | 성능 벤치마크 입력들 |
| Mark Tuckerman, *Statistical Mechanics: Theory and Molecular Simulation* | MD 이론 교과서 표준 |
| Daan Frenkel, Berend Smit, *Understanding Molecular Simulation* | MD 알고리즘 교과서 표준 |

이 입문 가이드는 LAMMPS 매뉴얼의 4-part 구조를 따라 한 번 훑어보는 데
목적이 있다. 같은 주제를 다른 관점, 다른 예제로 다시 보면 이해가 훨씬 단단해진다.
[lammpstutorials.github.io](https://lammpstutorials.github.io/)는
이 가이드와 짝지어 읽기 좋은 영문 자료다. 같은 LJ 액체를 어떻게
다르게 풀어 가는지, 어떤 진단 명령을 끼워 넣는지 비교해 보면 좋다.

실제 연구 문제에 LAMMPS를 적용한 사례는 [Cu 표면 흡착 시리즈](cu-overview.html)에 있다.
