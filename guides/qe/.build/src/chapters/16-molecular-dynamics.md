---
title: "16. 분자동역학"
---

# 16. 분자동역학

## 목차
{:.toc-title}

1. TOC
{:toc}

`pw.x`의 `calculation='md'`는 매 스텝 SCF를 수렴시키고 그 힘으로 원자를
움직이는 **Born-Oppenheimer MD(BOMD)**입니다. (Car-Parrinello MD는 별도
실행 파일 `cp.x`가 담당합니다.) 유한온도 샘플링, 그리고 특히 **ML 퍼텐셜
학습 데이터 생성의 출발점**입니다.

## 입력 골격

```fortran
&CONTROL
  calculation  = 'md'
  nstep        = 2000
  dt           = 20.0        ! Rydberg 원자단위 ≈ 0.968 fs
  tprnfor      = .true.
  tstress      = .true.
  disk_io      = 'none'      ! MD는 I/O가 병목
/
&SYSTEM
  ...
  nosym        = .true.      ! MD 필수 (아래 흔한 실수)
/
&IONS
  ion_dynamics    = 'verlet'
  ion_temperature = 'svr'    ! stochastic velocity rescaling
  tempw           = 300.0    ! K
  nraise          = 100
/
```

- `dt`는 **Rydberg 원자단위**입니다 (20.0 a.u. ≈ 0.968 fs). fs가 아닙니다.
- 온도조절기는 `'svr'`(stochastic velocity rescaling, Bussi-Donadio-Parrinello)
  가 정준 앙상블을 올바르게 샘플링하면서 안정적이라 기본 선택으로 좋습니다.
  `nraise`는 제어 주기입니다.
- `disk_io='none'`으로 파동함수 저장을 끄지 않으면 MD는 I/O에 잠깁니다.
- 매 스텝이 SCF이므로 `&ELECTRONS` 설정(수렴 임계값, mixing)이 그대로
  속도를 지배합니다. 이전 스텝에서 파동함수·퍼텐셜을 외삽하는
  `pot_extrapolation`/`wfc_extrapolation`이 MD 속도에 큰 영향을 줍니다.

## 실측 — FeO+U 셀의 300 K BOMD

<figure>
  <img src="assets/images/qe-e13-md.png"
       alt="FeO BOMD: temperature and conserved energy vs time" />
  <figcaption>
    FeO(+U) 4원자 셀의 BOMD 실측 (QE 7.5, SVR 300 K, 0.19 ps). 초반에
    이온들이 이상적 격자점을 벗어나며 위치에너지를 크게 방출하는 과도
    구간이 보이고, 작은 셀 특유의 큰 온도 요동(~1/√N) 속에서 SVR가
    평형화를 진행합니다. 학습 데이터는 평형화된 뒤부터 추출합니다.
    설정과 수치는 <a href="ex-13-slab-md.html">예제 E13</a>.
  </figcaption>
</figure>

## ML 퍼텐셜 학습 데이터를 만들 때의 원칙

- 모든 프레임에서 `ecutwfc`·`ecutrho`·k-그리드·smearing·U를 **완전히
  동일하게 고정**하세요. 설정이 섞인 데이터셋은 학습 단계에서 복구가
  불가능합니다.
- 수렴 기준은 에너지가 아니라 **힘**으로 잡습니다
  ([05장](05-convergence.html)의 힘 기준 수렴).
- 연속된 MD 프레임은 강하게 상관되어 있으므로 **간격을 두고 추출**하세요
  (예: 50 스텝마다).
- 응력까지 학습시키려면 `tstress=.true.`가 필요하지만, **nosym+U(ortho-atomic)
  조합에서는 Hubbard 응력이 `stres_hub` 에러로 죽는 제약**이 있습니다
  (QE 7.5 실측). 이 경우 추출한 프레임에 대해 별도 scf로 응력을 계산하세요.
- 출력에서 각 스텝의 `Ekin + Etot (const)` 항이 보존되는지, 온도(`temperature`)
  가 목표 주위에서 요동하는지 확인하세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <strong><code>nosym = .true.</code> 없이 MD를 돌리는 것.</strong> 대칭은
    초기 구조에서 잡히는데 열운동이 첫 스텝부터 그 대칭을 깨므로, QE가
    <code>checkallsym: some of the original symmetry operations not
    satisfied</code>로 멈춥니다 — 본 가이드 실측에서 실제로 겪은 에러입니다.
    또 DFT+U 계의 MD라면 <code>mixing_fixed_ns</code>도 함께 쓰세요 —
    nosym 상태에서는 축퇴 궤도 사이의 회전 때문에 SCF가 정체하는데, 초기
    반복 동안 점유행렬을 동결하면 풀립니다
    (<a href="ex-13-slab-md.html">E13</a> 실측).
    또, <code>dt</code>를 fs로 착각해 20 fs 스텝으로 돌리면 궤적이 즉시
    발산합니다. 마지막으로, MD 도중 SCF가 가끔 수렴 실패해도 QE는 이전
    밀도로 계속 진행할 수 있는데 그 프레임의 힘은 오염되어 있습니다 — 학습
    데이터로 쓸 궤적이라면 로그에서 <code>convergence NOT achieved</code>를
    검색해 해당 프레임을 걸러내세요.
  </p>
</div>

## 관련 예제

- [E13 · 슬랩과 AIMD](ex-13-slab-md.html) — FeO 셀 300 K BOMD 실측과
  프레임 추출 요령.
