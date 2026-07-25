---
title: "E8. Si 밴드 구조"
---

# E8. Si 밴드 구조

## 목적

고대칭 경로(L–Γ–X–W–K–Γ)를 따라 실리콘 밴드 구조를 계산하고, 간접 밴드갭을
직접 읽습니다. `tpiba_b` 경로 지정과 `bands.x` 후처리를 익힙니다.

```
scf ─→ calculation='bands' (K_POINTS tpiba_b) ─→ bands.x ─→ 플롯
```

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `calculation='bands'` | 고정 밀도에서 임의 k-경로 고유값 |
| `K_POINTS (tpiba_b)` | 2π/a 직교 좌표의 밴드 경로 |
| `bands.x` (`&BANDS`) | 밴드 재정렬, `.gnu` 파일과 대칭 라벨 |

## 입력 파일

[si.bands.in](files/E08-si-bands/si.bands.in) ·
[si.bandspp.in](files/E08-si-bands/si.bandspp.in)
(선행 scf는 [E1의 si.scf.in](files/E01-si-scf/si.scf.in))

경로 카드:

```fortran
K_POINTS (tpiba_b)
6
  0.500 0.500 0.500  30   ! L
  0.000 0.000 0.000  30   ! Gamma
  0.000 1.000 0.000  20   ! X
  0.500 1.000 0.000  20   ! W
  0.750 0.750 0.000  30   ! K
  0.000 0.000 0.000   0   ! Gamma
```

`tpiba_b`는 2π/a 단위의 직교 좌표입니다. QE의 `ibrav=2` 원시벡터 관례가
문헌의 fcc 정의와 다를 수 있어, 문헌의 분수좌표를 `crystal_b`에 그대로
넣으면 틀린 경로가 됩니다 — **헷갈리면 `tpiba_b`가 안전합니다**
([10장](10-dos-bands.html)).

## 실행

```bash
pw.x    -in si.scf.in     > si.scf.out      # 선행 scf (prefix='si')
pw.x    -in si.bands.in   > si.bands.out
bands.x -in si.bandspp.in > si.bandspp.out
```

`si.bandspp.out`의 `high-symmetry point` 줄들이 경로 위 눈금 위치(x 좌표)를
알려 줍니다 — 실측: 0.000(L), 0.866(Γ), 1.866(X), 2.366(W), 2.720(K),
3.780(Γ).

## 출력·그림 — 실측

<figure>
  <img src="assets/images/qe-e08-bands.png"
       alt="Si band structure along L-Gamma-X-W-K-Gamma" />
  <figcaption>
    실리콘 밴드 구조 실측 (QE 7.5, PBE). 가전자대 꼭대기(VBM)는 Γ, 전도대
    바닥(CBM)은 Γ–X 경로 위(~0.85X)에 있는 <strong>간접갭</strong>
    반도체입니다.
  </figcaption>
</figure>

- VBM(= scf의 `highest occupied level`, 실측 6.212 eV)을 0으로 놓고
  그렸습니다.
- **실측 간접갭 0.57 eV** (VBM Γ → CBM은 Γ–X 경로의 0.83 지점),
  **Γ 직접갭 2.56 eV**. 실험 간접갭은 1.12 eV — PBE의 체계적 갭
  과소평가가 그대로 보입니다.

## 직접 써보기

1. Γ에서의 직접갭과 간접갭을 각각 읽어 비교하세요.
2. 경로 마지막 점의 분할 개수를 `0`이 아닌 값으로 두면 어떤 경고가 나오나요?
3. 같은 경로를 `crystal_b`로 다시 써서 결과가 달라지는지(또는 같은지) 직접
   확인하세요. QE의 fcc 관례에서 L점의 `crystal_b` 좌표는 무엇인가요?
4. `nbnd`를 20으로 늘려 높은 전도대까지 그려 보세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>calculation='bands'</code>를 scf 없이 바로 돌리는 것 — bands는
    밀도를 만들지 않으므로 반드시 같은 <code>prefix</code>/<code>outdir</code>의
    scf가 선행되어야 합니다. 그리고 PBE 갭이 실험보다 작다고 계산이 틀린
    것이 아닙니다 — <strong>범함수의 알려진 한계</strong>이며, 갭이 중요하면
    하이브리드·GW로 가야 합니다.
  </p>
</div>

## 관련 챕터

[10 상태밀도와 밴드](10-dos-bands.html) ·
[08 SCF와 NSCF](08-scf-nscf.html)
