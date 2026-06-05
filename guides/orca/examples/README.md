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
