---
layout: default
title: "6. 구조 최적화"
---

# 6. 구조 최적화
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

SCF는 주어진 구조의 에너지를 구합니다. 그런데 대개는 **에너지가 가장 낮은 구조**
자체를 알고 싶습니다. 구조 최적화는 원자에 걸리는 힘과 셀에 걸리는 응력을 이용해
그 구조를 찾습니다.

## 6.1 힘과 응력

`pw.x` 는 SCF가 끝나면 각 원자에 걸리는 힘(force)과, 원하면 셀 전체의 응력
텐서(stress)를 계산합니다. 최적 구조에서는 모든 힘과 (셀까지 풀 때는) 응력이
0에 가까워집니다.

```fortran
&control
  tprnfor = .true.   ! 힘 출력
  tstress = .true.   ! 응력 출력
/
```

`calculation` 이 `relax` / `vc-relax` 이면 이 둘은 자동으로 켜집니다.

## 6.2 원자만 움직이기 — relax

원자 위치만 최적화하고 셀은 고정합니다. `&ions` 블록이 추가됩니다.

```fortran
&control
  calculation    = 'relax'
  forc_conv_thr  = 1.0d-4   ! 힘 수렴 임계 (Ry/bohr)
  etot_conv_thr  = 1.0d-5   ! 에너지 수렴 임계 (Ry)
  nstep          = 100      ! 최대 최적화 스텝
/
&ions
  ion_dynamics = 'bfgs'     ! 준-뉴턴 BFGS (기본, 대개 최선)
/
```

분자·결함·표면 흡착처럼 셀은 고정하고 원자만 이완할 때 씁니다.

## 6.3 셀까지 움직이기 — vc-relax

격자 상수·모양까지 최적화하려면 `vc-relax`(variable-cell)를 쓰고 `&cell` 을
추가합니다.

```fortran
&control
  calculation = 'vc-relax'
/
&ions
  ion_dynamics = 'bfgs'
/
&cell
  cell_dynamics = 'bfgs'
  press         = 0.0        ! 목표 압력 (kbar)
  cell_dofree   = 'all'      ! 'all' | 'ibrav'(대칭 유지) | 'volume' ...
/
```

- 격자 상수·부피·평형 결정 구조를 찾을 때 씁니다.
- `cell_dofree = 'ibrav'` 로 두면 브라베 격자의 대칭을 유지한 채 크기만 이완합니다.
- 셀을 바꾸면 평면파 기저도 바뀌므로, vc-relax는 **넉넉한 `ecutwfc`** 가
  중요합니다(작으면 Pulay 응력으로 부피가 부정확해집니다).

실제로 실리콘을 압축된 격자에서 출발해 vc-relax하면 압력이 100 kbar대에서 0으로
줄며 평형 격자 상수 a = 5.47 Å(PBE)로 수렴합니다. 스텝별 에너지·압력 추이는
[예제 E4](ex-04-relax.html)에 그래프로 있습니다.

## 6.4 최적화가 흔들릴 때

- `mixing_beta` 를 낮춰 각 스텝의 SCF부터 안정화합니다.
- `forc_conv_thr` 을 너무 빡빡하게 잡지 않습니다(SCF 노이즈보다 작으면 못 멈춥니다).
  그래서 최적화용 SCF `conv_thr` 은 보통 10⁻⁹ 처럼 더 엄격히 잡습니다.
- 대칭을 유지하고 싶으면 초기 구조의 대칭을 정확히 주고 `cell_dofree='ibrav'`
  를 씁니다.
- 최종 구조는 출력의 `Begin final coordinates` 블록(또는 새 `CELL_PARAMETERS`)에
  있습니다.

## 6.5 요점

- `relax` 는 원자만, `vc-relax` 는 셀까지 최적화합니다.
- 수렴은 힘(`forc_conv_thr`)과 에너지(`etot_conv_thr`)로 판정합니다.
- vc-relax는 `ecutwfc` 를 넉넉히 잡아야 부피가 정확합니다.
- 최적화용 SCF `conv_thr` 은 힘 임계보다 충분히 작게 둡니다.
