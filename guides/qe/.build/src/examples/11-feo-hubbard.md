---
title: "E11. FeO DFT+U"
---

# E11. FeO DFT+U

## 목적

[E10](ex-10-feo-afm.html)의 입력 맨 끝에 **`HUBBARD` 카드 세 줄**을 추가해
DFT+U를 켭니다. U가 Fe-3d 매니폴드를 어떻게 갈라놓는지 실측으로 확인하고 —
그리고 이 계의 유명한 함정, **"U를 켰는데도 금속으로 수렴하는" 문제**를
실제로 겪고 진단합니다. 이 함정을 아는 것이 문헌의 FeO+U 결과를 읽는
눈을 만듭니다.

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `HUBBARD (ortho-atomic)` | v7.1+ 신문법, 투영자 지정 ([13장](13-dft-plus-u.html)) |
| `U Fe1-3d 4.6` | 라벨·매니폴드별 U (eV) |
| `starting_ns_eigenvalue` | d 궤도 점유를 특정 극소값으로 유도 (아래 함정 절) |

## 입력 파일

[feo_u.scf.in 내려받기](files/E11-feo-hubbard/feo_u.scf.in) ·
[scan_U.sh](files/E11-feo-hubbard/scan_U.sh)

입력은 E10과 동일하고, 맨 끝에 다음이 추가됩니다.

```fortran
HUBBARD (ortho-atomic)
U Fe1-3d 4.6
U Fe2-3d 4.6
```

U = 4.6 eV는 FeO 문헌에서 자주 쓰이는 관례값입니다. 자기 계에 맞는 U를
직접 계산하는 방법이 [E12](ex-12-feo-hp.html)입니다.

## 실행

```bash
mpirun -np 8 pw.x -nk 4 -in feo_u.scf.in > feo_u.scf.out
```

## 출력에서 확인할 것 — 실측

| 항목 | GGA (E10) | GGA+U (이 예제) |
|---|---|---|
| 총에너지 | −741.81592 Ry | −741.52737 Ry (**직접 비교 금지** — 범함수가 다름) |
| total / absolute magnetization | 0.00 / 7.17 μB | −0.00 / **7.50 μB** |
| Fe 국소 모멘트 | ±3.31 μB | **±3.46 μB** (U가 d 국소화를 강화) |
| 전자구조 | 금속 | **여전히 (반)금속 — 아래 함정 절** |

<figure>
  <img src="assets/images/qe-e10-e11-feo-dos.png"
       alt="FeO spin-resolved DOS: GGA vs GGA+U" />
  <figcaption>
    FeO 스핀 분해 DOS 실측 (QE 7.5). U를 켜자(오른쪽) 점유/비점유 d
    매니폴드가 크게 갈라지며 위아래로 Hubbard 갭이 열립니다. 그러나 이상적
    큐빅 셀에서는 <strong>소수 스핀 t2g에서 유래한 좁은 띠가 Fermi 준위에
    걸린 채</strong> 남습니다 — U만으로 절연체가 되지 않는 함정의 실측입니다.
  </figcaption>
</figure>

## 함정 — U를 켰는데도 금속인 이유 (실측 포함)

DOS를 보면 U는 분명히 일을 했습니다(모멘트 증가, Hubbard 분리). 문제는
Fe²⁺의 소수 스핀 전자 1개가 들어갈 **t2g 궤도 3개가 이상적 큐빅 셀에서
축퇴**라는 점입니다. 전자가 특정 궤도 하나를 고르지 못하고 셋에 걸쳐
비편재화된 좁은 금속 띠를 만듭니다. QE 7.1부터 초기 d 점유를
유사퍼텐셜에서 읽게 되면서 버전에 따라 서로 다른 금속 해로 수렴할 수
있는데, **어느 쪽도 올바른 절연체 바닥상태가 아닙니다**
([13장](13-dft-plus-u.html)의 메일링 리스트 사례).

원고의 처방은 `starting_ns_eigenvalue`로 점유를 유도하는 것입니다.

```fortran
&SYSTEM
  ...
  starting_ns_eigenvalue(5,2,1) = 1.d0   ! Fe1 소수 스핀 최고 고유값 점유
  starting_ns_eigenvalue(5,1,2) = 1.d0   ! Fe2 (반대 스핀 채널)
/
```

실측 결과를 그대로 보고합니다 —

1. 위의 시드로 다시 돌리자 SCF는 **동일한 금속 해로 복귀**했습니다
   (에너지 4×10⁻⁷ Ry 이내 일치).
2. 소수 스핀 점유행렬을 [1,0,0,0,0]으로 **완전 지정**하고 `mixing_beta`를
   0.1로, `degauss`를 0.005로 낮춘 두 번째 시도는 98회 반복까지 10⁻⁴ Ry
   수준에서 진동하며 수렴하지 못했습니다.

즉 이 기하(이상적 rocksalt)와 이 설정에서는 금속 유역이 매우 깊습니다.
실제 FeO는 Néel 온도 아래에서 **[111] 방향 능면체 왜곡**이 일어나며, 이
왜곡이 t2g 축퇴를 깨서 궤도 질서와 절연성이 함께 자리 잡습니다. 완전한
절연체 해를 얻으려면 (1) 왜곡된 실험 구조 사용, (2) 다양한
`starting_ns_eigenvalue` 조합 탐색, (3) QE 7.5의 **궤도 분해 DFT+U**
(t2g/eg에 서로 다른 U — 바로 이런 계를 위해 도입)를 조합해야 합니다.
"계산이 수렴했다 ≠ 물리적으로 맞다"의 살아 있는 사례입니다.

## 직접 써보기

1. [scan_U.sh](files/E11-feo-hubbard/scan_U.sh)로 U = 0, 2, 4, 6, 8 eV를
   스캔하며 Fe 모멘트와 DOS의 Hubbard 분리가 어떻게 변하는지 표로 만드세요.
2. 투영자를 `atomic` ↔ `ortho-atomic`으로 바꿔 같은 U에서 결과가 얼마나
   달라지는지 보세요 — "U 값은 투영자와 세트"라는 것을 체감하게 됩니다.
3. `CELL_PARAMETERS`에 [111] 방향 ~3% 능면체 왜곡을 넣고
   `starting_ns_eigenvalue` 시드와 함께 재계산해 보세요. 갭이 열리나요?
4. `J0 Fe1-3d 0.8`을 추가해 DFT+U+J0를 시도해 보세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    "U를 켰고 SCF가 수렴했으니 절연체가 됐겠지"라고 속단하는 것.
    반드시 <code>the Fermi energy is</code>가 사라지고
    <code>highest occupied, lowest unoccupied level</code>이 나타났는지,
    출력의 <code>Tr[ns(na)]</code>·ns 고유값 블록(verbosity='high')에서
    점유 패턴이 물리적인지 확인하세요. 그리고 GGA와 GGA+U의 총에너지는
    서로 다른 범함수의 값이므로 직접 비교하면 안 됩니다.
  </p>
</div>

## 관련 챕터

[13 DFT+U와 HUBBARD 카드](13-dft-plus-u.html) ·
[14 hp.x 로 U 계산하기](14-hubbard-hp.html) ·
[12 스핀 편극과 자성](12-magnetism.html)
