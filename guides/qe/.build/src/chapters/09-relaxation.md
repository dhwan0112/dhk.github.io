---
title: "09. 구조 최적화"
---

# 09. 구조 최적화

## 목차
{:.toc-title}

1. TOC
{:toc}

구조 최적화는 힘(원자 위치에 대한 에너지 기울기)과 응력(셀에 대한 기울기)을
0으로 만드는 과정입니다. `relax`는 원자만, `vc-relax`(variable-cell)는
셀까지 함께 풉니다.

## 입력 골격

```fortran
&CONTROL
  calculation   = 'vc-relax'
  etot_conv_thr = 1.0d-5      ! Ry — 이온 스텝 간 에너지 변화
  forc_conv_thr = 1.0d-4      ! Ry/bohr — 힘 수렴
  nstep         = 100         ! 최대 이온 스텝
/
&ELECTRONS
  conv_thr = 1.0d-10          ! vc-relax는 SCF를 더 엄격하게
/
&IONS
  ion_dynamics  = 'bfgs'
/
&CELL
  cell_dynamics  = 'bfgs'
  press_conv_thr = 0.1        ! kbar
  cell_dofree    = 'ibrav'    ! 대칭 유지
/
```

- 힘·응력을 쓰는 계산이므로 SCF `conv_thr`를 평소보다 엄격하게 잡습니다.
  느슨한 밀도에서 나온 힘은 잡음이라 BFGS가 헤맵니다.
- `cell_dofree`로 셀 자유도를 제약할 수 있습니다 — `'all'`, `'ibrav'`(브라베
  격자 유지), `'2Dxy'`(슬랩: z 고정), `'volume'`, `'shape'` 등.
- 원자별 구속은 `ATOMIC_POSITIONS`의 `if_pos` 플래그로 겁니다
  ([03장](03-units-coordinates.html)).

## vc-relax 후 반드시 해야 할 일 — Pulay stress

`vc-relax`가 끝나면 출력 끝의 `Begin final coordinates` /
`End final coordinates` 블록에 최종 구조가 나옵니다. 이 구조로 **`scf`를
새로 한 번 더 돌리세요.**

평면파 기저는 셀에 묶여 있습니다. 셀이 변하면 기저 집합 자체가 변하므로
(Pulay stress), `vc-relax` 마지막 스텝의 에너지·응력은 **옛 기저로 계산된
값**이라 신뢰할 수 없습니다. QE도 출력에 이 경고를 명시합니다. 실측
확인은 [예제 E6](ex-06-si-vcrelax.html)에 있습니다.

## 대칭과 최적화 경로

QE는 초기 구조의 대칭을 찾아 최적화 내내 유지합니다. 이것은 양날의 검입니다.

- 대칭 위치의 원자는 힘이 정확히 0이므로 **대칭이 허용하지 않는 방향으로는
  절대 움직이지 않습니다**. 대칭이 깨진 저에너지 구조를 찾으려면 초기 구조를
  살짝 비틀거나 `nosym=.true.`로 대칭을 꺼야 합니다.
- 반대로 대칭 유지는 계산을 크게 아낍니다. 목적에 맞게 선택하세요.

## BFGS가 헤맬 때

| 증상 | 대처 |
|---|---|
| 에너지가 진동하며 수렴 안 함 | SCF `conv_thr` 강화, `upscale` 확인 |
| 셀이 크게 변하다 실패 | `cell_factor` 증가 (기본 2.0) |
| 첫 스텝부터 발산 | 초기 구조 점검 — 원자 겹침, 비물리적 거리 |
| 힘은 작은데 응력이 안 떨어짐 | `press_conv_thr` 확인, 컷오프 부족 의심 (응력은 에너지보다 컷오프에 민감) |

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>vc-relax</code>로 얻은 격자상수를 그대로 쓰면서 마지막 스텝의
    에너지까지 그대로 인용하는 것. 격자상수는 맞지만 에너지는 Pulay 오염이
    있습니다. 반드시 최종 구조로 <code>scf</code>를 재실행한 값을 쓰세요.
    또, 응력은 에너지·힘보다 컷오프 요구가 높으므로 <code>vc-relax</code>
    전에 <a href="05-convergence.html">응력 기준 수렴</a>을 확인해야 합니다.
  </p>
</div>

## 관련 예제

- [E6 · Si vc-relax](ex-06-si-vcrelax.html) — 일부러 틀린 격자상수에서 출발해
  평형 격자상수를 찾고, PBE의 전형적 과대평가를 실측으로 확인합니다.
- [E13 · 슬랩과 AIMD](ex-13-slab-md.html) — `if_pos`로 하단 층을 고정한
  슬랩 relax.
