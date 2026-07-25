---
title: "03. 단위계와 좌표계"
---

# 03. 단위계와 좌표계

## 목차
{:.toc-title}

1. TOC
{:toc}

QE 입문자가 겪는 오류의 상당 부분이 단위 혼동에서 옵니다. 이 장의 표 하나만
외워도 며칠을 아낄 수 있습니다.

## 반드시 외워야 할 단위 규약

QE는 **Rydberg 원자단위**를 씁니다.

| 물리량 | QE 단위 | 비고 |
|---|---|---|
| 에너지 (입력/출력) | **Ry** | 1 Ry = 13.6057 eV. `ecutwfc`, `conv_thr`, `degauss` 모두 Ry |
| 길이 (`celldm`) | **bohr** | 1 bohr = 0.5292 Å. `CELL_PARAMETERS angstrom`으로 명시 가능 |
| 힘 | Ry/bohr | `forc_conv_thr` 기본값 1.0d-3. 1 Ry/bohr = 25.711 eV/Å |
| 응력 | kbar (출력 시 Ry/bohr³ 병기) | |
| MD 시간 (`dt`) | Rydberg 원자단위 | 20.0 a.u. ≈ 0.968 fs |
| `starting_magnetization` | **−1 ~ 1의 무차원 비율** | Bohr magneton이 아님 (매우 흔한 실수) |
| DOS/밴드 출력 | eV | 후처리 코드는 eV로 나옴 — 혼동 주의 |

`&SYSTEM`의 격자 파라미터는 `celldm(1..6)`(bohr) 또는 `A, B, C, cosAB, ...`
(**Å 단위**) 중 한 벌만 씁니다. 같은 길이인데 한쪽은 bohr, 한쪽은 Å라는 점이
함정입니다.

## ibrav — 브라베 격자를 고르는 스위치

`ibrav`는 셀을 정의하는 방식을 결정합니다.

| `ibrav` | 격자 | 필요한 `celldm` |
|---|---|---|
| 0 | `CELL_PARAMETERS` 카드로 직접 지정 | (`celldm(1)`을 `alat` 스케일로 쓸 수 있음) |
| 1 | 단순입방 (sc) | `celldm(1)` |
| 2 | 면심입방 (fcc) | `celldm(1)` |
| 3 | 체심입방 (bcc) | `celldm(1)` |
| 4 | 육방 (hex) | `celldm(1)`, `celldm(3)=c/a` |
| 5 | 능면체 | `celldm(1)`, `celldm(4)=cos α` |
| 6, 7 | 정방 | `celldm(1)`, `celldm(3)` |
| 8~11 | 사방 | `celldm(1..3)` |
| 12~13 | 단사 | `celldm(1..4)` |
| 14 | 삼사 | `celldm(1..6)` |

`ibrav > 0`이면 QE가 **관례에 따라 원시벡터를 스스로 정의**합니다. 이 관례가
문헌의 정의와 다를 수 있다는 점이 뒤에서(특히 밴드 경로) 문제를 일으킵니다 —
[10장](10-dos-bands.html)의 `tpiba_b` 항목을 참고하세요.

`ibrav = 0`은 유연하지만 **대칭성 자동 탐지가 약해질 수 있습니다**. 출력의
`Sym. Ops.` 개수를 확인하세요. 대칭 연산이 줄면 기약 k-점이 늘어나 그만큼
느려집니다. 실측 비교는 [예제 E2](ex-02-si-ibrav0.html)에 있습니다.

## 좌표계 — ATOMIC_POSITIONS의 네 가지 단위

```fortran
ATOMIC_POSITIONS (crystal)
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25
```

| 옵션 | 의미 |
|---|---|
| `alat` | 셀의 `celldm(1)`(= `A`) 단위의 **직교 좌표** |
| `bohr` / `angstrom` | 절대 직교 좌표 |
| `crystal` | 셀 벡터를 기저로 한 **분수 좌표** — 구조를 셀 크기와 분리할 수 있어 실무에서 가장 안전 |

`CELL_PARAMETERS` 카드도 `alat` / `bohr` / `angstrom` 단위를 받습니다.
`alat`로 쓰면 `celldm(1)` 하나로 셀 크기를 조절할 수 있어 vc-relax나 부피
스캔에서 편리합니다.

## if_pos — 좌표 뒤의 고정 플래그

`ATOMIC_POSITIONS`의 각 줄 끝에 정수 3개를 붙이면 해당 방향의 움직임을
구속합니다(1 = 자유, 0 = 고정). 구조 최적화·MD에서만 의미가 있습니다.

```fortran
ATOMIC_POSITIONS (crystal)
  Fe  0.000  0.000  0.000   0 0 0    ! 완전 고정
  Fe  0.500  0.500  0.250   0 0 1    ! z 방향만 자유 (슬랩 하단 고정에 사용)
  O   0.500  0.000  0.375   1 1 1    ! 완전 자유 (기본값, 생략 가능)
```

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>starting_magnetization = 2.2</code>처럼 자기모멘트를 μB 단위로 넣는
    실수가 대단히 흔합니다. 이 변수는 <strong>−1~1의 무차원 비율</strong>(원자가
    전자의 스핀 편극 비율)입니다. 범위를 벗어나면 QE가 잘라내거나 에러를 내며,
    의도한 초기 자화가 걸리지 않습니다. 자성 계산은
    <a href="12-magnetism.html">12장</a>을 보세요.
  </p>
</div>

## 관련 예제

- [E2 · ibrav=0 다시 쓰기](ex-02-si-ibrav0.html) — 같은 결정을 `ibrav=2`와
  `ibrav=0 + CELL_PARAMETERS`로 두 번 정의해 등가성과 대칭 탐지를 확인합니다.
