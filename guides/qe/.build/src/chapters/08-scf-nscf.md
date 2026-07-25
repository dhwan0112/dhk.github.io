---
title: "08. SCF와 NSCF"
---

# 08. SCF와 NSCF

## 목차
{:.toc-title}

1. TOC
{:toc}

QE는 하나의 프로그램이 아니라 **실행 파일들의 모음**이고, 그 사이를
`prefix`/`outdir`로 연결된 파이프라인이 흐릅니다. 그 출발점이 `scf`와
`nscf`의 역할 분담입니다.

## 역할 분담

| calculation | 무엇을 하나 | 밀도 | 용도 |
|---|---|---|---|
| `'scf'` | 전하밀도를 자기일관적으로 수렴 | 만든다 | 모든 것의 출발점. 에너지·힘·응력 |
| `'nscf'` | **고정된 밀도** 위에서 고유값만 계산 | scf 것을 읽음 | 조밀한 k-격자의 DOS, 페르미 면 |
| `'bands'` | nscf의 변형 — 임의의 k-경로에서 고유값 | scf 것을 읽음 | 밴드 구조 |

nscf/bands는 SCF가 만들어 둔 `outdir/prefix.save/`의 전하밀도를 읽으므로,
**`prefix`와 `outdir`이 scf와 정확히 일치**해야 하고, 같은 디렉터리에서
실행해야 합니다. 불일치하면
`cannot open file ... .save/charge-density.dat` 에러가 납니다.

```
scf (성긴 k, 밀도 수렴) ─→ nscf (조밀한 k, tetrahedra_opt) ─→ dos.x / projwfc.x
                        └→ bands (k-경로)                  ─→ bands.x
```

nscf에서 흔히 바꾸는 것: k-격자를 조밀하게, `occupations='tetrahedra_opt'`,
`nbnd`를 전도대까지 넉넉하게.

## 출력 파일 읽는 법 — 이 절을 건너뛰지 마세요

`.out` 파일에서 매번 확인해야 할 항목:

```
!    total energy              =     -93.45 Ry      ← "!" 가 붙은 줄이 최종 수렴값
     estimated scf accuracy    <       1.0E-09 Ry   ← conv_thr 아래로 내려갔는가
     the Fermi energy is       6.2 ev               ← 금속인 경우
     highest occupied, lowest unoccupied level (ev):← 절연체인 경우 (밴드갭 추정)
     total magnetization       =     4.00 Bohr mag/cell  ← 스핀 계산 시
     absolute magnetization    =     4.12 Bohr mag/cell  ← 위와 크게 다르면 AFM 성분
     Total force               =     0.001 Ry/au
     convergence has been achieved in  12 iterations
```

- `!` 표시가 붙은 총에너지 줄만 수렴된 값입니다. SCF 도중의 `total energy`
  줄은 중간값입니다.
- **total vs absolute magnetization의 차이는 자기 배열 정보입니다.**
  FM이면 두 값이 거의 같고, AFM이면 total ≈ 0인데 absolute는 큽니다
  ([12장](12-magnetism.html)).
- 절연체는 `highest occupied, lowest unoccupied level`에서 갭을 추정할 수
  있고, 금속은 대신 `the Fermi energy is`가 출력됩니다. **이 둘 중 무엇이
  나오는지 자체가 계의 진단**입니다 — [예제 E10](ex-10-feo-afm.html)에서
  FeO가 GGA로 "금속"이 되는 것을 이 줄로 확인합니다.
- 에너지 분해 블록(`one-electron contribution`, `hartree contribution`,
  `xc contribution`, `ewald contribution`)은 이상값 진단에 유용합니다.

출력 맨 아래의 **timing 분해**(`init_run`, `electrons`, `c_bands`,
`sum_band`)는 어디서 시간을 쓰는지 알려 주므로, 병렬화 전략을 세울 때 첫
번째로 보는 곳입니다([18장](18-parallel-hpc.html)).

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    nscf를 scf와 <strong>다른 디렉터리</strong>에서 돌리거나, 사이에
    <code>outdir</code>을 지우는 것. nscf는 밀도를 새로 만들지 않으므로 scf의
    산출물이 없으면 시작조차 못 합니다. 또 하나 — verbosity를
    <code>'low'</code>로 두고 학습하는 것. <code>'high'</code>여야 대칭 연산
    목록, k-점 목록, (DFT+U라면) ns 행렬까지 출력에 남습니다.
  </p>
</div>

## 관련 예제

- [E1 · Si SCF](ex-01-si-scf.html) — 출력의 모든 블록을 실측으로 읽습니다.
- [E7 · Si DOS·PDOS](ex-07-si-dos.html) — scf → nscf 연결의 실전.
- [E8 · Si 밴드 구조](ex-08-si-bands.html) — scf → bands 연결의 실전.
