---
title: "12. 스핀 편극과 자성"
---

# 12. 스핀 편극과 자성

## 목차
{:.toc-title}

1. TOC
{:toc}

전이금속 산화물로 가는 관문입니다. 공선(collinear) 스핀 편극은 `nspin = 2`
하나로 켜지지만, **어떤 자성 해로 수렴시킬 것인가**가 진짜 문제입니다.

## 기본 설정

```fortran
&SYSTEM
  nspin = 2
  starting_magnetization(1) =  0.6   ! Fe1 (up)
  starting_magnetization(2) = -0.6   ! Fe2 (down) — AFM
  starting_magnetization(3) =  0.0   ! O
  occupations = 'smearing'
  smearing    = 'mv'
  degauss     = 0.01
/
&ELECTRONS
  mixing_beta = 0.2                  ! 자성계는 낮게
  mixing_mode = 'local-TF'
/

ATOMIC_SPECIES
  Fe1  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
  Fe2  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF   ! 같은 파일, 다른 라벨
  O    15.999  O.pbe-n-kjpaw_psl.1.0.0.UPF
```

- `starting_magnetization`은 **−1~1의 무차원 비율**(μB 아님)이고, 어디까지나
  **초기 추측**입니다. SCF가 자유롭게 바꿉니다.
- 특정 총 자화를 **구속**하고 싶으면 `tot_magnetization`을 씁니다 (up/down에
  별도 Fermi 준위 사용). [예제 E4](ex-04-o2-molecule.html)의 O₂ 삼중항이
  그 예입니다.

## AFM은 라벨 분리로 만듭니다

반강자성 배열의 핵심 요령: **같은 유사퍼텐셜을 서로 다른 라벨(`Fe1`,
`Fe2`)로 등록**하고 각각 반대 부호의 초기 자화를 줍니다. 라벨 분리 없이는
QE가 두 Fe를 대칭 등가로 보고 **AFM 배열을 만들 수 없습니다**. 이 라벨
분리는 뒤의 DFT+U와 `hp.x`에서도 그대로 필요합니다.

수렴 후 판별은 출력의 두 줄로 합니다.

| 배열 | total magnetization | absolute magnetization |
|---|---|---|
| FM | 큰 값 | total과 거의 같음 |
| AFM | **≈ 0** | **큰 값** |
| 비자성 붕괴 | ≈ 0 | ≈ 0 |

## 실측 — bcc Fe와 FeO

[예제 E9](ex-09-fe-bcc.html)의 bcc Fe(강자성 금속)와
[예제 E10](ex-10-feo-afm.html)의 FeO(반강자성 산화물)가 이 장의 실전입니다.

<figure>
  <img src="assets/images/qe-e09-fe-dos.png"
       alt="bcc Fe spin-resolved DOS" />
  <figcaption>
    bcc Fe의 스핀 분해 DOS 실측 (QE 7.5, PBE). 교환 상호작용이 up/down
    d-밴드를 분리시켜 강자성 모멘트(실측 2.2 μB/원자, 실험 2.22)가 생기는
    것이 그대로 보입니다.
  </figcaption>
</figure>

## 수렴 요령 — 자성계가 말을 안 들을 때

`starting_magnetization`이 SCF 도중 0으로 붕괴하는 일이 흔합니다. 순서대로:

1. `mixing_beta` 0.7 → 0.3 → 0.1
2. `mixing_mode = 'local-TF'`
3. `starting_magnetization`을 더 크게 (0.4~0.9)
4. `degauss`를 줄이기 (과한 smearing이 모멘트를 지웁니다). 반대로 수렴 자체가
   안 되면 일시적으로 키워 수렴시킨 뒤 `startingpot='file'`로 재시작하며 줄이기
5. `diagonalization = 'cg'` 또는 `'ppcg'`

그리고 근본적인 주의 —

<div class="warning">
  <div class="note-title">자성계는 국소 최소가 여러 개입니다</div>
  <p>
    자성계는 서로 다른 자기 배열마다 <strong>준안정 해(metastable state)</strong>가
    존재합니다. 한 번 수렴했다고 그것이 바닥상태라는 보장이 없습니다. 서로
    다른 초기 자화(FM, AFM, 비자성)에서 출발해 여러 해를 얻은 뒤
    <strong>에너지를 비교해 가장 낮은 것을 고르는 것</strong>이 정석입니다.
  </p>
</div>

비공선(noncollinear) 자성과 스핀궤도결합은 `noncolin=.true.`,
`lspinorb=.true.`로 켜지만 비용이 크게 뜁니다(완전상대론적 유사퍼텐셜 필요).
필요해질 때 배우면 됩니다.

## 관련 예제

- [E9 · bcc Fe 강자성](ex-09-fe-bcc.html) — FM 금속, 모멘트 2.2 μB 실측.
- [E10 · FeO AFM](ex-10-feo-afm.html) — 라벨 분리로 AFM-II 배열 실측.
- [E4 · O₂ 분자](ex-04-o2-molecule.html) — `tot_magnetization`으로 삼중항 구속.
