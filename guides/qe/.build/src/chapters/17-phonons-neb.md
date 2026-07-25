---
title: "17. 포논과 반응 경로"
---

# 17. 포논과 반응 경로

## 목차
{:.toc-title}

1. TOC
{:toc}

이 장은 상세 가이드가 아니라 **지도**입니다. `ph.x`와 `neb.x`는 각각 책
한 권 분량의 주제이므로, 언제 필요해지고 어디서 시작하면 되는지만
정리합니다.

## ph.x — 포논 (DFPT)

밀도범함수 섭동이론(DFPT)으로 동역학 행렬을 계산합니다. 필요해지는 순간:

- **구조 안정성 검증** — 최적화된 구조가 진짜 극소인지(허수 진동수가 없는지)
- 진동 스펙트럼, 열역학량(자유에너지, 엔트로피), 열팽창(`thermo_pw`와 조합)
- 전자-포논 결합

워크플로의 뼈대:

```
pw.x (scf, 매우 엄격한 conv_thr) → ph.x (&INPUTPH, ldisp=.true., nq 격자)
  → q2r.x (실공간 힘상수) → matdyn.x (임의 q 분산·DOS)
```

`&INPUTPH`의 핵심: `tr2_ph`(응답 수렴, 보통 1.0d-14), `ldisp`와
`nq1/nq2/nq3`(q-격자), `epsil`(유전 텐서, 극성 절연체의 LO-TO 분리에 필요),
`fildyn`. 계산량이 크므로 `-ni`(이미지 병렬)와 `start_q`/`last_q` 분할이
실전 필수입니다.

시작점: `PHonon/examples/`, 그리고 [예제 E6](ex-06-si-vcrelax.html)처럼
잘 수렴된 구조. **최적화가 덜 된 구조의 포논은 허수 모드 투성이가 되며,
그것은 물리가 아니라 미수렴의 신호**일 수 있습니다.

## neb.x — 반응 경로와 활성화 장벽

Nudged Elastic Band로 초기·최종 상태 사이의 최소 에너지 경로(MEP)와 전이
상태를 찾습니다. 산화 메커니즘, 확산 장벽, 표면 반응 연구의 핵심 도구입니다.

입력 구조가 `pw.x`와 다릅니다 — `BEGIN`/`END` 블록 안에 경로 설정(`&PATH`)과
엔진 입력(pw.x 입력과 동일)이 함께 들어갑니다.

```
BEGIN
BEGIN_PATH_INPUT
&PATH
  string_method = 'neb'
  num_of_images = 7
  nstep_path    = 100
  opt_scheme    = 'broyden'
  CI_scheme     = 'auto'      ! climbing image — 장벽 정점을 정확히
  path_thr      = 0.05        ! eV/Å
/
END_PATH_INPUT
BEGIN_ENGINE_INPUT
&CONTROL
 ...                          ! pw.x 입력과 동일
/
BEGIN_POSITIONS
FIRST_IMAGE
ATOMIC_POSITIONS (crystal)
 ...
LAST_IMAGE
ATOMIC_POSITIONS (crystal)
 ...
END_POSITIONS
END_ENGINE_INPUT
END
```

실전 요령:

- 초기·최종 상태를 **각각 먼저 완전히 최적화**한 뒤 NEB에 넣습니다.
- 이미지 수는 홀수로 시작(5~9), `-ni`로 이미지 병렬.
- `CI_scheme='auto'`(climbing image)를 켜야 장벽 꼭대기가 정확해집니다.

## 그 밖의 확장 지도

| 목표 | 도구 | 비고 |
|---|---|---|
| 국소화 궤도 / d-band 해석 | `pw2wannier90.x` + Wannier90 | 밴드 내삽에도 사용 |
| 워크플로 자동화 | AiiDA + aiida-quantumespresso, ASE, pymatgen | **대량 데이터 생성 시 사실상 필수** |
| 유한온도 열역학 | `thermo_pw` | ph.x 기반 |
| Car-Parrinello MD | `cp.x` | BOMD([16장](16-molecular-dynamics.html))와 별개 코드 |

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    포논·NEB를 <strong>수렴 테스트가 끝나지 않은 설정</strong> 위에 쌓는 것.
    두 방법 모두 미세한 힘·에너지 차이를 다루므로, 바탕 SCF의 품질
    (<code>conv_thr</code>, 컷오프, k-점)이 조금만 느슨해도 허수 모드나
    들쭉날쭉한 경로로 돌아옵니다. 항상 <a href="05-convergence.html">05장</a>
    체계를 먼저 통과시키세요.
  </p>
</div>
