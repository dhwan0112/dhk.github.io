---
layout: default
title: "1. LJ 액체 (NVE) 첫 실행"
---

# 1. LJ 액체: 가장 단순한 첫 실행
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<p class="amm-id">NOTE 33-01-00 · LJ 액체 (NVE) 첫 실행</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 환원 단위(`lj`)로 fcc 격자 위에 Lennard-Jones 입자 4000개를 만든다.
2. 이 노트는 NVE 앙상블에서 250 step 적분한다.
3. 설치 직후 LAMMPS 가 제대로 실행되는지 확인하는 용도로 쓴다.

### B. 적용 범위

1. 외부 데이터 파일이나 힘장 라이브러리가 필요 없다.
2. 원자 종류와 상호작용이 하나뿐이다.
3. LAMMPS 입력의 4단계 구조를 가장 작은 형태로 다룬다.

### C. 결과 요약

1. 온도는 첫 50 step 만에 1.44 에서 0.75 부근으로 떨어진다.
2. `TotEng` 은 −4.6231 부근에서 거의 일정하다.

## 2. 준비 정보

### A. 필요한 개념

1. LAMMPS 가 설치되어 있어야 한다([01 시작하기](01-getting-started.html)).

### B. 참조 자료

| 참조 | 제목 |
|---|---|
| [01 시작하기](01-getting-started.html) | 설치 확인과 첫 실행 |
| [02 입력 스크립트 구조](02-input-structure.html) | 4단계 구조 |
| [03 단위계와 atom_style](03-units-atomstyle.html) | `lj` 단위의 의미 |
| [06 셋업과 실행](06-fix-run.html) | `velocity` · `fix` · `run` |
| [E2 — LJ 5단계](ex-02-lj-demo.html) | 최소화·NVT·NPT·분석을 더한 전체 흐름 |

### C. 사용 프로그램

| 항목 | 용도 |
|---|---|
| LAMMPS (`lmp`) | 시뮬레이션 실행. 4.A 의 결과는 LAMMPS 22 Jul 2025 직렬 실행 기준이다. |
| MPI (`mpirun`) | 병렬 실행 (4 코어 예시) |

### D. 관련 파일

| 항목 | 내용 |
|---|---|
| `in.lj` | 입력 스크립트 (3.A 에서 작성) |
| 데이터·포텐셜 파일 | 없음. `units lj` 는 모든 양을 무차원 환원 단위로 다룬다. |

## 3. 절차

### A. 입력 작성: `in.lj`

1. 아래 내용으로 `in.lj` 를 작성한다.

```lammps
# in.lj — 가장 단순한 Lennard-Jones 액체
units           lj
atom_style      atomic

lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 box

mass            1 1.0

pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5

velocity        all create 1.44 87287 loop geom

neighbor        0.3 bin
neigh_modify    every 20 delay 0 check no

fix             1 all nve

thermo          50
run             250
```

2. 계 크기를 확인한다. `region ... 0 10 0 10 0 10` 은 격자 단위로 10 × 10 × 10 셀이다.
3. 원자 수를 확인한다. fcc 이므로 원자는 4000개다.
4. `velocity ... create 1.44` 가 초기 온도를 주는지 확인한다.
5. `fix nve` 가 미시정준 앙상블을 적분하는지 확인한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
미시정준(NVE) 앙상블에서는 에너지·부피·입자수가 보존된다.
</div>

### B. 실행

1. 직렬(1 코어) 또는 병렬(4 코어)로 실행한다.

```bash
# 직렬 (1 코어)
lmp -in in.lj > out.lj

# 병렬 (4 코어)
mpirun -np 4 lmp -in in.lj > out.lj
```

### C. 출력 확인

1. 텍스트 파일 `out.lj` 와 `log.lammps` 가 생겼는지 확인한다.
2. `out.lj` 끝부분의 thermo 표를 연다.

## 4. 시험 및 검사

### A. 온도 평형과 에너지 보존

1. thermo 표를 아래 기준값과 비교한다(LAMMPS 22 Jul 2025, 직렬 실행).

```text
   Step          Temp          E_pair         E_mol          TotEng         Press
         0   1.44          -6.7733681      0             -4.6139081     -5.0199732
        50   0.74368149    -5.7370606      0             -4.6218173      0.30804835
       100   0.75715334    -5.7581426      0             -4.6226965      0.20850222
       150   0.7518449     -5.7510464      0             -4.623561       0.22707058
       200   0.75139921    -5.7500924      0             -4.6232753      0.25362795
       250   0.75954471    -5.7621762      0             -4.623144       0.21729981
Loop time of 0.350699 on 1 procs for 250 steps with 4000 atoms
```

2. 온도를 확인한다. 처음 1.44 였던 온도가 첫 50 step 만에 0.75 부근으로 떨어지면 정상이다.
3. 총 에너지를 확인한다. `TotEng` 이 −4.6231 부근에서 거의 일정하면 합격이다.

<figure>
  <img src="assets/images/lj-thermo.png" alt="LJ 액체 첫 시뮬레이션의 온도와 총 에너지 추이" style="width:100%;max-width:880px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    왼쪽: 온도가 1.44 → 0.75 부근으로 평형화. 오른쪽: 총 에너지(녹색)는 거의
    일정(NVE 보존), 보라색은 포텐셜 에너지(E_pair).
  </figcaption>
</figure>

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
온도가 떨어지는 이유는 무작위 초기 속도로 출발한 격자가 풀리면서 운동 에너지가 포텐셜로 나뉘어 들어가기 때문이다. 운동 에너지의 절반가량이 포텐셜로 넘어가므로 온도는 대략 절반 수준이 된다(등분배). `TotEng` 이 일정하다는 것은 NVE 적분이 에너지를 잘 보존한다는 뜻이다. 첫 실험으로 NVE 를 자주 돌리는 이유도 이 보존성을 확인하기 위해서다.
</div>

## 5. 종료

### A. 결과 정리

1. `units lj` 는 모든 양을 무차원 환원 단위로 다루므로 외부 힘장 파일이 필요 없다.
2. 초기 온도는 운동 에너지의 절반가량이 포텐셜로 넘어가면서 대략 절반 수준으로 떨어진다(등분배).
3. NVE 에서 `TotEng` 이 일정한지 확인하는 것이 가장 단순한 정확도·timestep 점검이다.

### B. 후속 작업

1. 성능은 `Loop time` 을 기준으로 판단한다. 코어 수나 계 크기를 바꿔 `Loop time` 을 비교한다.
2. 최소화·NVT·NPT·분석을 더한 전체 흐름은 [E2 — LJ 5단계](ex-02-lj-demo.html)에서 다룬다.
