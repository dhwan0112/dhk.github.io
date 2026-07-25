---
title: "04. 유사퍼텐셜"
---

# 04. 유사퍼텐셜

## 목차
{:.toc-title}

1. TOC
{:toc}

유사퍼텐셜(pseudopotential)은 원자핵 근처의 빠르게 진동하는 전전자(all-electron)
파동함수를 부드러운 유사파동함수로 대체해, 평면파 기저로 다룰 수 있게 만드는
장치입니다. **어떤 유사퍼텐셜을 고르느냐가 필요한 컷오프와 정확도를 동시에
지배**합니다.

## NC / US / PAW — 세 계열

| 계열 | 특징 | 컷오프 요구 | `ecutrho` 배수 |
|---|---|---|---|
| NC (norm-conserving) | 단순, 이론적으로 깔끔. GW 등 고급 방법과 호환 좋음 | 높음 | 4배(기본값)로 충분 |
| US (ultrasoft) | 컷오프를 크게 낮춤. augmentation 전하 도입 | 낮음 | **8~12배 필요** |
| PAW (projector augmented wave) | US의 장점 + 전전자 정보 복원 가능 | 낮음 | **8~12배 필요** |

본 가이드의 예제는 PSlibrary **PAW**를 씁니다. Fe처럼 요구가 큰 원소는
`ecutrho`를 `ecutwfc`의 10배로 잡았습니다.

<div class="warning">
  <div class="note-title">흔한 실수 — ecutrho의 함정</div>
  <p>
    <code>ecutrho</code>의 기본값은 <code>4 × ecutwfc</code>인데, 이것은
    <strong>norm-conserving 기준</strong>입니다. US/PAW에서 이 기본값을 그대로
    두면 <code>negative rho</code> 경고나 <code>charge is wrong</code> 에러가
    나거나, 더 나쁘게는 <strong>에러 없이 조용히 틀린 에너지</strong>가 나옵니다.
    US/PAW는 반드시 8~12배로 명시하세요.
  </p>
</div>

## 어디서 받는가

- **[SSSP](https://www.materialscloud.org/discover/sssp/)** (Standard Solid State
  Pseudopotentials) — 원소별로 검증된 유사퍼텐셜 모음. *efficiency* 라이브러리는
  정밀도를 합리적으로 유지하면서 컷오프를 낮게 잡아 일상 계산과 스크리닝에,
  *precision* 라이브러리는 전전자 계산에 가장 가까운 고정밀 모델링에 적합합니다.
  **초보자에게 SSSP의 진짜 가치는 원소별 권장 컷오프 표**입니다. 수렴 테스트의
  출발점을 여기서 얻으세요.
- **[PSlibrary](https://pseudopotentials.quantum-espresso.org/)** — QE 개발진이
  만든 NC/US/PAW 라이브러리. QE 공식 사이트에서 원소별로 내려받습니다.
- **[PseudoDojo](http://www.pseudo-dojo.org/)** — ONCVPSP 기반 norm-conserving.
  컷오프는 높지만 검증이 잘 되어 있습니다.

## 파일명 해독법

PSlibrary 명명 규칙을 읽을 줄 알면 유사퍼텐셜 선택이 훨씬 쉬워집니다.

```
Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
│   │   │    │        └─ PSlibrary 버전
│   │   │    └─ kjpaw = Kresse-Joubert PAW (rrkjus = ultrasoft)
│   │   └─ s = semicore s 포함, p = semicore p 포함, n = nonlinear core correction
│   └─ 교환-상관 범함수 (pbe / pbesol / pz ...)
└─ 원소
```

전이금속은 semicore 상태(`s`, `p`)를 원자가에 포함한 것을 쓰는 편이
안전합니다. DFT+U에서 Hubbard 매니폴드를 인식하려면 해당 채널이 유사퍼텐셜에
있어야 하며, 없으면 `set_hubbard_l: pseudopotential not yet inserted` 에러가
납니다.

`ATOMIC_SPECIES` 카드에서 파일명을 지정합니다. 파일명이 본 가이드와 다르면
이 카드만 바꾸면 됩니다.

```fortran
ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-kjpaw_psl.1.0.0.UPF
```

## 범함수는 유사퍼텐셜에 내장되어 있습니다

교환-상관 범함수는 유사퍼텐셜 파일이 만들어질 때 결정되며, `pw.x`는 그것을
읽어 씁니다. `input_dft`로 강제로 바꿀 수 있지만 **유사퍼텐셜 생성 조건과
어긋나므로 되도록 쓰지 마세요**. PBE 계산에는 PBE 유사퍼텐셜을 쓰는 것이
원칙입니다.

<div class="tip">
  <div class="note-title">총에너지 절대값은 비교 대상이 아닙니다</div>
  <p>
    유사퍼텐셜마다 에너지 기준점이 다르므로, 서로 다른 유사퍼텐셜(또는 다른
    컷오프)로 얻은 총에너지의 절대값 비교는 무의미합니다. 같은 조건에서 얻은
    에너지끼리의 <strong>차이</strong>만 물리적 의미가 있습니다. 문헌의
    총에너지와 내 계산이 다르다고 당황할 필요가 없습니다.
  </p>
</div>

## 관련 예제

- [E1 · Si SCF](ex-01-si-scf.html) — PAW 유사퍼텐셜로 첫 계산.
- [E3 · 수렴 테스트 자동화](ex-03-convergence.html) — 유사퍼텐셜이 요구하는
  컷오프를 실측으로 확인.
