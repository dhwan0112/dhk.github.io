# ORCA 가이드 — 예제와 템플릿 (worked examples & templates)

여기 있는 모든 `.out`은 **ORCA 6.1.1로 실제 실행한 결과**입니다 (illustrative 아님).
실행:  `orca water.inp > water.out`

## 예제 — 입력 + 실제 출력

| 폴더 | 계산 | 실제 결과 |
|------|------|-----------|
| `01-single-point/` | water, B3LYP/def2-SVP | FINAL SPE −76.321274 Eh |
| `02-opt-freq/` | water, 최적화+진동수+열화학 | Gibbs −76.422869 Eh, 허수진동수 0 |
| `03-dlpno-ccsdt/` | water, DLPNO-CCSD(T)/cc-pVTZ | −76.331959 Eh |
| `04-solvation-smd/` | water, SMD(water) 단일점 | −76.332972 Eh |
| `05-casscf-h2/` | H₂ CASSCF(2,2), 늘어난 결합 (다중참조) | E(CAS) −1.056125 Eh, N(occ) 1.81/0.19 |
| `06-fragment-merge/` | [Mn(H₂O)]²⁺ 금속·리간드 조각 병합 → CASSCF(5,5) | 병합이 Mn 3d⁵를 활성공간에 배치(N(occ) 1.00×5); 수렴 에너지 −1225.0207 Eh는 기본 guess 기준 |

`05-casscf-h2/`의 `dissociation_{rhf,cas}.dat`은 H–H 거리 0.4–3.0 Å를 RHF·CASSCF로 훑은 실제 곡선 데이터다(`assets/img/h2-dissociation.png`의 출처). RHF는 해리에서 −0.826 Eh로 발산, CASSCF는 −1.0 Eh로 정상 — 단일참조가 깨지는 고전적 사례.

`06-fragment-merge/`는 금속과 리간드를 따로 풀어 `orca_mergefrag`로 궤도를 합치는 절차를 실제로 돌린 것이다. `fragMn.inp`(Mn²⁺ 고스핀)·`fragH2O.inp`(물)를 각각 계산해 `.gbw`를 얻고, `mergefrag.log`처럼 병합한 뒤(`Dimension` 31+24=55, `NEl` 23+10=33으로 맞아떨어진다) `super-cas-merged.inp`가 그 병합 guess를 읽는다. 병합은 다섯 Mn 3d를 활성 공간에 그대로 넣어 준다(UHF ⟨S²⟩=8.751, CASSCF N(occ)=1.0×5). 다만 raw 병합 궤도는 정렬이 안 돼 회전이 흔들릴 수 있어, 이 단순한 계에서는 기본 guess가 곧장 수렴한다(`cas-default.{inp,out}`, E=−1225.0207). **조각 병합은 기본 guess가 엉뚱한 d-점유로 빠지는 어려운 착물에서 진가를 내며, 항상 N(occ)·에너지를 기본 guess와 비교해 도움이 되는지 확인한다.** 자세한 설명은 가이드 13장 CASSCF의 "조각 병합" 절에 있다.

## 템플릿 — 바로 고쳐 쓰는 스켈레톤 (전부 ORCA 6.1.1에서 실행 검증)

| 파일 | 용도 |
|------|------|
| `templates/single-point.inp` | 단일점 에너지 |
| `templates/opt-freq.inp` | 최적화 + 진동수 + 열화학 |
| `templates/solvation-smd.inp` | SMD 용매 단일점 |
| `templates/dlpno-composite-step1.inp` | DFT 최적화+진동수(D4) → `step1.xyz` 생성 |
| `templates/dlpno-composite-step2.inp` | DLPNO-CCSD(T)/CBS 정밀 단일점 (`AutoAux`, step1.xyz 읽기) |

`mol.xyz`를 자기 분자 좌표 파일로 바꿔 쓰면 됩니다.

**검증 중 발견한 함정 두 가지** (템플릿에 반영됨):
- `DLPNO-CCSD(T) Extrapolate(...)`는 **`AutoAux`가 없으면** "보조 기저집합 필요" 오류로 죽는다.
- DFT 최적화(D4)와 CCSD(T)를 한 입력의 `$new_job`으로 묶으면 **D4가 CC 단계로 넘어가** "분산 + CC 동시 금지" 오류가 난다 → 단계를 **별도 파일로 분리**한다.
