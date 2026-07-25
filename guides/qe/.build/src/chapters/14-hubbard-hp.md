---
title: "14. hp.x 로 U 계산하기"
---

# 14. hp.x 로 U 계산하기

## 목차
{:.toc-title}

1. TOC
{:toc}

문헌의 U 값을 베끼는 것보다, **선형 응답(DFPT)으로 자기 계에 맞는 U를 직접
계산**하는 것이 방법론적으로 훨씬 방어 가능합니다. `hp.x`가 그 도구입니다
(Timrov, Cococcioni, Marzari, *Comput. Phys. Commun.* **2022**, *279*, 108455).

## 원리 한 줄

Hubbard U는 국소화된 매니폴드의 점유수를 살짝 흔들었을 때(섭동) 계가
얼마나 되받아치는지(응답 행렬 χ)로 정의됩니다. `hp.x`는 이 응답을
밀도범함수 섭동이론으로 계산해, 스크리닝된 상호작용

$$U = (\chi_0^{-1} - \chi^{-1})$$

을 돌려줍니다. 경험 파라미터가 들어가지 않습니다.

## 워크플로

```
pw.x (작은 초기 U를 넣은 scf, conv_thr 1.0d-12) → hp.x → prefix.Hubbard_parameters.dat
```

**Step 1** — [예제 E11](ex-11-feo-hubbard.html)의 입력을 그대로 쓰되 U를
아주 작은 값으로 넣고 `scf`를 돌립니다. `hp.x`가 "어떤 원자를 섭동할지"
인식하려면 **HUBBARD 카드가 있어야** 합니다.

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 1.0d-8
U Fe2-3d 1.0d-8
```

`&ELECTRONS`의 `conv_thr`는 `1.0d-12` 수준으로 엄격하게 둡니다 — 선형 응답은
바닥상태 밀도의 품질에 민감합니다.

**Step 2** — `hp.x` 입력(`&INPUTHP`):

```fortran
&INPUTHP
  prefix       = 'FeO'
  outdir       = './tmp/'
  nq1 = 2, nq2 = 2, nq3 = 2
  conv_thr_chi = 1.0d-6
  iverbosity   = 2
/
```

`conv_thr_chi`는 응답 함수 χ의 수렴 임계값입니다. GGA 바닥상태가 금속성인
계(FeO가 그렇습니다)에서는 χ의 수치 노이즈 플로어가 10⁻⁷ 수준이라
1.0d-8은 도달하지 못할 수 있습니다 — 실측 근거는
[예제 E12](ex-12-feo-hp.html)에 있습니다.

```bash
pw.x -in feo_hp_scf.in > feo_hp_scf.out
hp.x -in feo.hp.in     > feo.hp.out
cat FeO.Hubbard_parameters.dat
```

결과 파일에 원자별 U가 정리되어 나옵니다. 실측 수치는
[예제 E12](ex-12-feo-hp.html)에 있습니다.

## 주의점

- **`nq` 그리드 수렴 테스트가 필수입니다.** 1×1×1로 얻은 U는 신뢰할 수
  없습니다. scf의 k-그리드도 함께 수렴시켜야 합니다.
- `hp.x`는 계산량이 큽니다. 섭동 횟수는 비등가 Hubbard 원자 수에 비례하고,
  각 섭동마다 q-점 격자만큼의 선형 응답 계산이 돕니다. `-nk` 풀 병렬이
  그대로 적용되고, q-점은 `start_q`/`last_q`로 나눠 돌릴 수 있습니다.
- 얻은 U를 다시 HUBBARD 카드에 넣어 scf → hp.x를 반복하는
  **self-consistent U** 절차가 정석입니다. 보통 1~2회 반복이면 안정됩니다.
- 라벨 분리(`Fe1`/`Fe2`)를 해 두었다면 hp.x가 대칭 등가성을 인식해 등가
  원자의 섭동을 건너뜁니다(`skip_equivalence_q` 등 옵션 참조).

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>hp.x</code>로 얻은 U를 <strong>다른 투영자·다른 유사퍼텐셜</strong>
    설정에 이식하는 것. U는 계산된 조건(투영자, PP, 자기 배열)과 세트로만
    의미가 있습니다. 또, 선행 scf의 <code>conv_thr</code>가 느슨하면 응답
    행렬에 잡음이 들어가 U가 수 eV씩 흔들립니다 — 1.0d-12를 지키세요.
  </p>
</div>

## 관련 예제

- [E12 · hp.x 로 U 계산](ex-12-feo-hp.html) — FeO에서 U를 실측으로 계산.
- [E11 · FeO DFT+U](ex-11-feo-hubbard.html) — 얻은 U를 넣어 갭 확인.
