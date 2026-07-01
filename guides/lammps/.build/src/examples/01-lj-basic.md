---
layout: default
title: "1. LJ 액체 (NVE) 첫 실행"
---

# 1. LJ 액체 — 가장 단순한 첫 실행
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 무엇을 하는 예제인가

외부 데이터 파일이나 힘장 라이브러리 없이, 환원 단위(`lj`)로 fcc 격자 위에
Lennard-Jones 입자 4000개를 만들고 NVE 앙상블에서 250 step 적분합니다.
원자 종류도 하나, 상호작용도 LJ 하나뿐이라 LAMMPS 입력의 4단계 구조를 가장
작은 형태로 보여 줍니다. 처음 설치를 확인하고 "돌아가는지" 감을 잡는 데
적합합니다.

관련 개념은 [01 시작하기](01-getting-started.html)와
[03 단위계와 atom_style](03-units-atomstyle.html)에서 다룹니다.

## 전체 입력 스크립트 — `in.lj`

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

`region ... 0 10 0 10 0 10` 은 격자 단위로 10 × 10 × 10 셀, fcc 이므로 원자
4000개입니다. `velocity ... create 1.44` 로 초기 온도를 부여하고, `fix nve` 로
에너지·부피·입자수가 보존되는 미시정준 앙상블을 적분합니다.

## 실행

```bash
# 직렬 (1 코어)
lmp -in in.lj > out.lj

# 병렬 (4 코어)
mpirun -np 4 lmp -in in.lj > out.lj
```

실행이 끝나면 `out.lj` 와 `log.lammps` 가 생깁니다. 둘 다 텍스트 파일입니다.

## 출력과 결과

`out.lj` 끝부분의 thermo 표입니다(LAMMPS 22 Jul 2025 직렬 실행).

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

초기 1.44 였던 온도가 첫 50 step 만에 0.75 부근으로 떨어집니다. 이는 무작위
초기 속도로 시작한 격자가 풀리며 운동 에너지가 포텐셜로 재분배되는 자연스러운
현상입니다. 동시에 `TotEng` 은 −4.6231 부근에서 거의 일정하게 유지되어, NVE
적분이 에너지를 잘 보존함을 보여 줍니다. NVE를 첫 실험으로 자주 돌리는 이유가
바로 이 보존성 점검입니다.

<figure>
  <img src="assets/images/lj-thermo.png" alt="LJ 액체 첫 시뮬레이션의 온도와 총 에너지 추이" style="width:100%;max-width:880px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    왼쪽: 온도가 1.44 → 0.75 부근으로 평형화. 오른쪽: 총 에너지(녹색)는 거의
    일정(NVE 보존), 보라색은 포텐셜 에너지(E_pair). 위 입력을 실제 실행해 얻은 값입니다.
  </figcaption>
</figure>

## 요점

- `units lj` 는 모든 양을 무차원 환원 단위로 다루므로 외부 힘장 파일이 필요 없습니다.
- 초기 온도는 계의 절반이 포텐셜로 넘어가며 대략 절반 수준으로 떨어집니다(등분배).
- NVE에서 `TotEng` 이 일정한지 보는 것이 가장 단순한 정확도·timestep 점검입니다.
- `Loop time` 은 성능 감각의 출발점입니다. 코어 수나 계 크기를 바꿔 보십시오.

## 관련 개념 챕터

- [01 시작하기](01-getting-started.html) — 설치 확인과 첫 실행
- [02 입력 스크립트 구조](02-input-structure.html) — 4단계 표준 구조
- [03 단위계와 atom_style](03-units-atomstyle.html) — `lj` 단위의 의미
- [06 셋업과 실행](06-fix-run.html) — `velocity` · `fix` · `run`

다음 예제 [E2 — LJ 5단계](ex-02-lj-demo.html) 에서는 여기에 최소화·NVT·NPT·분석을
더한 완전한 워크플로를 다룹니다.
