---
title: "13. DFT+U와 HUBBARD 카드"
---

# 13. DFT+U와 HUBBARD 카드

## 목차
{:.toc-title}

1. TOC
{:toc}

## 왜 필요한가

GGA는 국소화된 3d 전자의 자기상호작용(self-interaction) 오차를 제대로 다루지
못합니다. 전자가 자기 자신과 상호작용하는 가짜 항이 국소화된 궤도를
비물리적으로 퍼뜨리고, 그 결과 FeO 같은 계에서 **실험적으로는 절연체(갭
~2.4 eV)인데 계산은 금속**으로 나옵니다. [예제 E10](ex-10-feo-afm.html)에서
이 실패를 직접 확인할 수 있습니다.

DFT+U는 선택한 궤도 매니폴드(예: Fe-3d)에 Hubbard 보정 항을 더해 이 오차를
바로잡는, 비용이 거의 들지 않는 처방입니다.

## 신문법 — HUBBARD 카드 (v7.1+)

U 파라미터는 `&SYSTEM`이 아니라 **입력 맨 끝의 `HUBBARD` 카드**에 씁니다.

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 4.6
U Fe2-3d 4.6
```

문법 구조:

```
HUBBARD (<투영자>)
<파라미터> <원자라벨>-<매니폴드> <값(eV)>
```

| 항목 | 선택지 | 비고 |
|---|---|---|
| 투영자 | `atomic`, `ortho-atomic`, `norm-atomic`, `wf`, `pseudo` | **`ortho-atomic` 권장** — `atomic`은 궤도 겹침 영역에서 보정이 두 번 적용되는 문제가 있음 |
| 파라미터 | `U`, `J0`, `J`, `B`, `E2`, `E3`, `V`, `alpha` | |
| 매니폴드 | `3d`, `2p`, `4f` ... | 원자 타입당 최대 3개 채널 |

사이트 간 상호작용(DFT+U+V)은 이웃 원자 인덱스까지 지정합니다
(인덱스는 `ATOMIC_POSITIONS`에서의 순서).

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 4.6
U Fe2-3d 4.6
V Fe1-3d O-2p  1 3  0.8
```

정본 문서는 `Doc/Hubbard_input.pdf`
([온라인판](https://www.quantum-espresso.org/Doc/user_guide_PDF/Hubbard_input.pdf))입니다.

<div class="warning">
  <div class="note-title">구버전 문법은 쓰지 마세요</div>
  <p>
    <code>lda_plus_u = .true.</code> / <code>Hubbard_U(1) = 4.6</code> /
    <code>U_projection_type</code> 방식은 v7.1 이후 폐기되었습니다. 인터넷 예제
    상당수가 아직 옛 문법이며, 그대로 쓰면 조용히 무시되거나 에러가 납니다.
    <code>&amp;SYSTEM</code>에 남아 있는 DFT+U 관련 변수는
    <code>starting_ns_eigenvalue</code>와 <code>Hubbard_occ</code> 정도입니다.
  </p>
</div>

## 실측 — FeO에서 U가 하는 일 (그리고 다 못 하는 일)

같은 FeO AFM-II 셀에 `HUBBARD` 카드 세 줄만 추가한 것이
[예제 E11](ex-11-feo-hubbard.html)입니다.

<figure>
  <img src="assets/images/qe-e10-e11-feo-dos.png"
       alt="FeO DOS: GGA (metallic) vs GGA+U (Hubbard splitting)" />
  <figcaption>
    FeO 스핀 분해 DOS 실측 (QE 7.5, PBE, AFM-II). 왼쪽: GGA — Fermi 준위에
    Fe-3d 상태가 걸려 금속으로 나옵니다(실험은 절연체). 오른쪽: GGA+U
    (U = 4.6 eV, ortho-atomic) — Hubbard 분리로 위아래에 갭이 열리지만,
    이상적 큐빅 셀에서는 소수 스핀 t2g 유래의 좁은 띠가 Fermi 준위에
    남습니다. 이 마지막 함정은 아래와 E11에서 다룹니다.
  </figcaption>
</figure>

## U를 켰는데도 금속이라면 — 점유 패턴 함정

U를 켜고도 금속으로 수렴하는 경우가 많습니다. 원인은 d 궤도의 **점유
패턴**입니다. QE 7.1부터 Fe-3d의 초기 점유수를 유사퍼텐셜에서 읽도록
바뀌었고(이전에는 코드에 하드코딩), 그 결과 같은 입력이 버전에 따라 서로
다른 금속 해로 수렴할 수 있습니다. **둘 다 틀린 바닥상태입니다.**

올바른 절연체 상태로 유도하려면 `starting_ns_eigenvalue`로 점유를 명시적으로
지정합니다.

```fortran
&SYSTEM
  ...
  starting_ns_eigenvalue(5, 2, 1) = 0.0d0   ! (궤도 index, 스핀, 원자타입)
/
```

이 변수는 첫 몇 번의 SCF 반복 동안만 강제되고 이후 풀립니다 — "올바른
극소값의 유역(basin)으로 밀어 넣는" 장치입니다. 수렴 후에는 출력의
`Tr[ns(na)]`와 ns 고유값 블록에서 점유 패턴을 확인하세요
(`verbosity='high'` 필요). "계산이 수렴했다 ≠ 물리적으로 맞다"의 전형적인
사례입니다.

## U 값은 투영자와 세트입니다

같은 U = 4.6 eV라도 투영자가 `atomic`이냐 `ortho-atomic`이냐에 따라 결과가
달라집니다. **U 값은 투영자(그리고 유사퍼텐셜)와 세트로만 의미가 있으므로**,
문헌의 U를 빌릴 때는 그 문헌의 투영자 설정까지 확인해야 하고, 논문에 쓸 때는
자신의 설정을 함께 기록해야 합니다. 문헌값 대신 자기 계에 맞는 U를 직접
계산하는 방법이 [14장 hp.x](14-hubbard-hp.html)입니다.

QE 7.5에는 **궤도 분해(orbital-resolved) DFT+U**가 새로 들어갔습니다
(Macke &amp; Timrov, *JCTC* 2024). 같은 3d 매니폴드 안에서 t2g/eg를 구분해
U를 다르게 주는 방식으로, 팔면체 배위의 전이금속 산화물에서 유용할 수
있습니다.

## 관련 예제

- [E10 · FeO AFM (GGA 실패)](ex-10-feo-afm.html) — U 없이 금속으로 나오는 것 확인.
- [E11 · FeO DFT+U](ex-11-feo-hubbard.html) — HUBBARD 카드로 갭 열기.
- [E12 · hp.x 로 U 계산](ex-12-feo-hp.html) — U를 제일원리로 결정.
