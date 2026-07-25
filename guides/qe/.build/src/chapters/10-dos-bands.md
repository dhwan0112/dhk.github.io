---
title: "10. 상태밀도와 밴드"
---

# 10. 상태밀도와 밴드

## 목차
{:.toc-title}

1. TOC
{:toc}

전자구조 후처리는 **파이프라인 순서와 `prefix`/`outdir` 일치가 전부**입니다.

## DOS / PDOS 파이프라인

```
scf (성긴 k) ─→ nscf (조밀한 k, occupations='tetrahedra_opt') ─┬─→ dos.x      (총 DOS)
                                                                └─→ projwfc.x  (PDOS + Löwdin)
```

- **nscf**: k-격자를 조밀하게(예: 8³ → 16³), `nbnd`를 전도대까지 넉넉하게,
  `occupations='tetrahedra'`. 사면체법은 **Γ 중심의 시프트 없는 자동
  격자**를 요구합니다. 최적화판 `'tetrahedra_opt'`는 dos.x에는 문제없지만
  **QE 7.5에서 projwfc.x의 PDOS가 0으로 나오는 문제를 실측에서
  확인**했으므로, PDOS까지 뽑을 파이프라인이라면 고전 `'tetrahedra'`를
  쓰세요 ([예제 E7](ex-07-si-dos.html)의 실측 노트).
- **`dos.x`** (`&DOS`): 총 DOS. 출력 `fildos` 파일은 1열 E(eV), 2열 DOS,
  3열 적분 DOS입니다. 적분 DOS가 Fermi 준위에서 원자가 전자 수와 일치하는지
  검산할 수 있습니다.
- **`projwfc.x`** (`&PROJWFC`): 원자·궤도별 분해 DOS(PDOS)와 **Löwdin 전하**.
  `si.pdos_atm#1(Si)_wfc#2(p)`처럼 원자·궤도별 파일이 생깁니다. Fe의 d-궤도
  점유, 스핀별 분해, d-band center가 모두 여기서 나옵니다.

<figure>
  <img src="assets/images/qe-e07-dos-pdos.png"
       alt="Si total DOS and s/p-projected DOS" />
  <figcaption>
    실리콘 총 DOS와 s/p 분해 PDOS 실측 (QE 7.5, nscf 16×16×16, tetrahedra).
    원자가띠 하단은 s, 상단은 p 성격이 지배적임이 그대로 보입니다. 절차와
    수치는 <a href="ex-07-si-dos.html">예제 E7</a>.
  </figcaption>
</figure>

## 밴드 구조 파이프라인

```
scf ─→ calculation='bands' (K_POINTS tpiba_b / crystal_b 경로) ─→ bands.x ─→ 플롯
```

`calculation='bands'`에서 k-경로를 카드로 지정합니다.

```fortran
K_POINTS (tpiba_b)
6
  0.500 0.500 0.500  30   ! L
  0.000 0.000 0.000  30   ! Gamma
  0.000 1.000 0.000  20   ! X
  0.500 1.000 0.000  20   ! W
  0.750 0.750 0.000  30   ! K
  0.000 0.000 0.000   0   ! Gamma  (마지막 점은 분할 0)
```

각 줄은 고대칭점과 "다음 점까지의 분할 수"입니다. `bands.x`(`&BANDS`)가
고유값을 밴드 순서로 재정렬해 `filband` 파일(`.gnu` 포함)로 씁니다.

<div class="tip">
  <div class="note-title">tpiba_b vs crystal_b — 경로가 이상할 때</div>
  <p>
    <code>tpiba_b</code>는 2π/a 단위의 <strong>직교 좌표</strong>,
    <code>crystal_b</code>는 <strong>역격자 기저의 분수 좌표</strong>입니다.
    QE의 <code>ibrav=2</code> 원시벡터 정의는 문헌의 표준 fcc 정의와 다를 수
    있어, 문헌의 분수좌표를 <code>crystal_b</code>에 그대로 넣으면 틀린 경로가
    됩니다. <strong>경로가 헷갈릴 때는 <code>tpiba_b</code>가 안전합니다.</strong>
    복잡한 결정계는
    <a href="https://www.materialscloud.org/work/tools/seekpath">SeeK-path</a>로
    경로를 생성하세요.
  </p>
</div>

<figure>
  <img src="assets/images/qe-e08-bands.png"
       alt="Si band structure along L-Gamma-X-W-K-Gamma" />
  <figcaption>
    실리콘 밴드 구조 실측 (QE 7.5, PBE, L–Γ–X–W–K–Γ). 가전자대 꼭대기는 Γ,
    전도대 바닥은 Γ–X 위에 있는 간접갭 반도체입니다. PBE 갭은 실험(1.12 eV)을
    체계적으로 과소평가합니다. 수치는 <a href="ex-08-si-bands.html">예제 E8</a>.
  </figcaption>
</figure>

## 갭 읽기 — 세 가지 방법

1. scf/nscf 출력의 `highest occupied, lowest unoccupied level (ev)` — 가장 간단.
2. 밴드 데이터에서 VBM/CBM을 직접 읽기 — 간접갭의 위치까지 알 수 있음.
3. DOS에서 상태가 0인 구간 — k-격자가 성기면 갭이 실제보다 넓어 보일 수 있음.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    DOS가 톱니처럼 거칠다고 <code>DeltaE</code>만 줄이는 것. 원인은 거의 항상
    <strong>nscf k-격자 부족</strong>입니다. 격자를 늘리고
    <code>tetrahedra_opt</code>를 쓰세요. 또, nscf 없이 성긴 scf 밀도에서 바로
    <code>dos.x</code>를 돌리면 돌아가긴 하지만 해상도가 형편없습니다 —
    파이프라인 순서를 지키세요.
  </p>
</div>

## 관련 예제

- [E7 · Si DOS·PDOS](ex-07-si-dos.html) — 파이프라인 전체 실측, Löwdin 전하.
- [E8 · Si 밴드 구조](ex-08-si-bands.html) — 경로 지정과 간접갭 읽기.
- [E10](ex-10-feo-afm.html)/[E11 · FeO](ex-11-feo-hubbard.html) — 스핀 분해
  DOS로 GGA 실패와 +U 갭 열림을 확인.
