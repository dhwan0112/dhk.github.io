---
title: "06. 점유수와 smearing"
---

# 06. 점유수와 smearing

## 목차
{:.toc-title}

1. TOC
{:toc}

금속·자성계 수렴 문제의 90%가 점유수 처리에서 옵니다. `occupations` 선택은
"이 계가 절연체인가 금속인가"라는 물리적 판단입니다.

## occupations — 계의 종류에 따라

| 값 | 의미 | 용도 |
|---|---|---|
| `'fixed'` | 정수 점유. 갭이 있어야 함 | 절연체/반도체 |
| `'smearing'` | Fermi 준위 주변을 부드럽게 부분 점유 | **금속**, 갭 유무가 불확실한 계 |
| `'tetrahedra'` / `'tetrahedra_lin'` / `'tetrahedra_opt'` | smearing 없는 정밀 BZ 적분 | **DOS·밴드용 nscf 전용** |
| `'from_input'` | `OCCUPATIONS` 카드로 밴드별 점유 직접 지정 | 특수 |

절연체에 `'fixed'` 대신 smearing을 쓰면 갭 근처 상태가 미세하게 부분 점유되어
에너지가 오염됩니다. 반대로 금속에 `'fixed'`를 쓰면
`the system is metallic, specify occupations` 에러로 멈춥니다.

## smearing 종류와 degauss

`occupations='smearing'`일 때 두 변수가 따라옵니다 — 어떤 함수로 뭉갤 것인가
(`smearing`)와 얼마나 넓게 뭉갤 것인가(`degauss`, Ry).

| 값 | 특징 | 용도 |
|---|---|---|
| `'gaussian'` | 단순, 안전, 느린 수렴 | 범용 |
| `'mv'` (Marzari-Vanderbilt, cold) | 자유에너지 ≈ E(σ→0), 외삽 불필요 | **금속 기본 선택** |
| `'mp'` (Methfessel-Paxton) | 고차 전개, 점유수가 음수가 될 수 있음 | 금속 |
| `'fd'` (Fermi-Dirac) | 물리적 전자온도에 대응 | 유한온도 계산 |

smearing은 수치 안정화 장치이면서 동시에 근사입니다. `degauss`가 크면 수렴은
쉬워지지만 결과가 σ = 0 극한에서 멀어집니다. 출력의 `smearing contrib. (-TS)`
항이 그 오염의 크기입니다 — 이 값이 크면 `degauss`가 과하다는 뜻입니다.

## 실측 — Al에서 smearing 종류별 degauss 의존성

[예제 E5](ex-05-al-metal.html)의 fcc Al(12×12×12 k)에서 smearing 종류별로
`degauss`를 스캔한 실측입니다.

<figure>
  <img src="assets/images/qe-e05-smearing.png"
       alt="Al total energy vs degauss for gaussian / mv / fd smearing" />
  <figcaption>
    fcc Al의 전체 에너지 vs degauss (QE 7.5 실측). cold smearing(mv)은
    degauss에 거의 무감해 외삽 없이 σ→0 값을 주는 반면, gaussian과
    Fermi-Dirac은 degauss에 따라 에너지가 흘러갑니다. 금속에 mv가 기본
    선택인 이유입니다.
  </figcaption>
</figure>

## 사면체법 — 후처리 전용

`'tetrahedra_opt'`(최적화 사면체법)는 smearing 없이 BZ 적분을 수행해 DOS가
가장 깨끗하게 나옵니다. 단, 제약이 있습니다.

- **Γ 중심, 시프트 없는 자동 격자**(`K_POINTS automatic`의 시프트 0 0 0)를
  요구합니다.
- SCF 자체보다는 **DOS/밴드용 nscf**에서 쓰는 것이 정석입니다
  ([10장](10-dos-bands.html)).
- 실측 주의: `'tetrahedra_opt'` nscf 위에서 QE 7.5의 projwfc.x가 PDOS를
  0으로 쓰는 문제를 확인했습니다. PDOS가 필요하면 고전 `'tetrahedra'`를
  쓰세요 ([예제 E7](ex-07-si-dos.html)).

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    degauss를 "수렴이 잘 되는 큰 값"으로 올려 두고 잊는 것. smearing 폭은
    결과에 남는 근사이므로, 목표 물성이 degauss에 둔감한지 반드시 확인해야
    합니다. 특히 자성계에서 과한 degauss는 <strong>자기모멘트를 0으로
    붕괴</strong>시키는 단골 원인입니다(<a href="12-magnetism.html">12장</a>).
    금속 k-점 수렴과 degauss 수렴은 결합되어 있으므로 함께 스캔하세요.
  </p>
</div>

## 관련 예제

- [E5 · fcc Al 금속](ex-05-al-metal.html) — smearing SCF, 페르미 준위,
  degauss 스캔 실측.
- [E4 · O₂ 분자](ex-04-o2-molecule.html) — 분자인데 smearing을 쓰는 이유
  (부분 점유 안정화)와 `tot_magnetization`.
