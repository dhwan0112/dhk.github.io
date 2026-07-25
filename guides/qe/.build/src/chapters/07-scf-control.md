---
title: "07. SCF 수렴 제어"
---

# 07. SCF 수렴 제어

## 목차
{:.toc-title}

1. TOC
{:toc}

SCF(자기일관장) 루프는 "전하밀도 추측 → Kohn-Sham 방정식 풀기 → 새 밀도 →
섞기(mixing) → 반복"의 순환입니다. `&ELECTRONS` 네임리스트가 이 순환을
제어합니다.

## 핵심 변수

| 변수 | 기본값 | 역할 |
|---|---|---|
| `conv_thr` | 1.0d-6 | 수렴 임계값 (Ry). 힘·응력이 필요하면 1.0d-8, `hp.x` 선행 계산은 1.0d-12 권장 |
| `mixing_beta` | 0.7 | 새 밀도를 얼마나 섞을가. **자성·금속은 0.1~0.3** |
| `mixing_mode` | `'plain'` | `'plain'`(Broyden) / `'TF'` / `'local-TF'`. **금속·슬랩·자성계는 `'local-TF'`** |
| `mixing_ndim` | 8 | 혼합에 쓰는 이전 반복 수. 늘리면 메모리 증가 |
| `electron_maxstep` | 100 | 최대 반복 횟수 |
| `diagonalization` | `'david'` | `'david'` / `'cg'` / `'ppcg'` / `'paro'` / `'rmm-davidson'` |
| `startingwfc` / `startingpot` | `'atomic+random'` / `'atomic'` | `'file'`이면 이전 계산에서 이어받기 |

출력에서는 매 반복의 `estimated scf accuracy`가 `conv_thr` 아래로 내려가는
과정을 지켜봅니다. 수렴하면 `convergence has been achieved in N iterations`가
찍힙니다.

## mixing_beta의 직관

밀도를 크게 섞으면(`0.7`) 수렴이 빠르지만, 금속·자성계처럼 응답이 예민한
계에서는 밀도가 진동하며 발산합니다. 이런 계는 조금씩(`0.2~0.3`) 섞어야
합니다. `mixing_mode='local-TF'`는 공간적으로 불균일한 계(슬랩, 진공 포함,
자성 산화물)에서 특히 효과적입니다.

실측 예로, 본 가이드의 [FeO AFM 계산(E10)](ex-10-feo-afm.html)은
`mixing_beta = 0.2` + `local-TF`로 설정했습니다. GGA FeO는 (틀린) 금속 상태로
수렴하는 예민한 계라 기본값 0.7로는 진동합니다.

## 수렴 실패 시 진단 순서

`convergence NOT achieved after N iterations`가 나오면 **순서대로**
시도하세요.

1. `mixing_beta` 0.7 → 0.3 → 0.1
2. `mixing_mode = 'local-TF'` (금속, 슬랩, 자성계에 효과적)
3. `electron_maxstep` 증가 (200~500)
4. `mixing_ndim` 증가 (8 → 12~16, 메모리 여유가 있을 때)
5. `degauss`를 일시적으로 키워 수렴시킨 뒤, `startingpot='file'`로 재시작하며
   줄이기
6. `diagonalization = 'cg'` 또는 `'ppcg'` (느리지만 안정)
7. 초기 구조가 비물리적이지 않은지 확인 (원자 간 거리가 너무 가깝지 않은가)

대각화 단계의 문제(`c_bands: N eigenvalues not converged`,
`cdiaghg: problems computing cholesky`)와 그 밖의 오류 대처는
[R3 · 오류 사전](ref-errors.html)에 증상별로 정리했습니다.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    수렴이 안 된다고 <code>conv_thr</code>를 느슨하게 풀어버리는 것.
    임계값을 1.0d-4로 풀면 "수렴 달성" 메시지는 나오지만 힘과 응력은 쓰레기가
    됩니다. 문제의 원인은 거의 항상 mixing(위 1~4번)이지 임계값이 아닙니다.
    반대로, 구조 최적화·MD·hp.x처럼 힘이나 선형 응답을 쓰는 계산은
    <code>conv_thr</code>를 <strong>더 엄격하게</strong>(1.0d-8 ~ 1.0d-12)
    잡아야 합니다.
  </p>
</div>

## 관련 예제

- [E9 · bcc Fe 강자성](ex-09-fe-bcc.html) — 자성 금속의 mixing 설정 실전.
- [E10 · FeO AFM](ex-10-feo-afm.html) — local-TF + 낮은 beta가 필요한 예민한 계.
