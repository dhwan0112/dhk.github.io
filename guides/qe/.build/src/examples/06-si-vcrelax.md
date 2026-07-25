---
title: "E6. Si vc-relax"
---

# E6. Si vc-relax

## 목적

**일부러 틀린 격자상수(10.00 bohr)에서 출발**해, 셀까지 함께 푸는
`vc-relax`로 실리콘의 PBE 평형 격자상수를 찾습니다. BFGS 궤적을 읽는 법과
Pulay stress 재계산 원칙까지 확인합니다.

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `calculation='vc-relax'` | 원자 + 셀 최적화 |
| `&IONS` / `&CELL` | BFGS 설정, `press_conv_thr` |
| `cell_dofree='ibrav'` | 큐빅 대칭을 유지한 채 셀 크기만 |
| `etot_conv_thr` / `forc_conv_thr` | 이온 스텝 수렴 기준 |

## 입력 파일

[si.vcrelax.in 내려받기](files/E06-si-vcrelax/si.vcrelax.in)

```fortran
&CONTROL
  calculation   = 'vc-relax'
  prefix        = 'si_vc'
  outdir        = './tmp/'
  pseudo_dir    = './pseudo/'
  etot_conv_thr = 1.0d-5      ! Ry
  forc_conv_thr = 1.0d-4      ! Ry/bohr
  nstep         = 100
  tprnfor       = .true.
  tstress       = .true.
/
&SYSTEM
  ibrav       = 2
  celldm(1)   = 10.00         ! 일부러 틀린 값에서 출발
  nat         = 2
  ntyp        = 1
  ecutwfc     = 40
  ecutrho     = 320
  occupations = 'fixed'
/
&ELECTRONS
  conv_thr    = 1.0d-10       ! vc-relax는 더 엄격하게
/
&IONS
  ion_dynamics   = 'bfgs'
/
&CELL
  cell_dynamics  = 'bfgs'
  press_conv_thr = 0.1        ! kbar
  cell_dofree    = 'ibrav'    ! 큐빅 대칭 유지
/

ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (alat)
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25

K_POINTS (automatic)
  8 8 8  0 0 0
```

## 실행

```bash
mpirun -np 6 pw.x -nk 6 -in si.vcrelax.in > si.vcrelax.out
```

## 출력·그림 — 실측

<figure>
  <img src="assets/images/qe-e06-vcrelax.png"
       alt="Si vc-relax: energy and pressure vs BFGS step" />
  <figcaption>
    BFGS 스텝별 에너지·압력 실측 (QE 7.5, PBE). 압축 상태(+109 kbar)에서
    출발해 6 스텝 만에 압력이 0.1 kbar 아래로 떨어지며 수렴합니다.
  </figcaption>
</figure>

| 항목 | 실측값 |
|---|---|
| BFGS 수렴 | 6 SCF 사이클 |
| 최종 부피 | 275.989 bohr³ = 40.897 Å³ (원시셀, V = a³/4) |
| **평형 격자상수** | **a = 5.469 Å** |
| 실험값 | 5.431 Å → **PBE가 +0.70% 과대평가** |

출력 끝의 `Begin final coordinates` 블록에 최종 셀
(`CELL_PARAMETERS (alat= 10.0)`의 스케일 0.5168)이 정리됩니다. GGA(PBE)가
격자상수를 ~1% 부풀리는 것은 잘 알려진 체계적 경향이며, 그대로
실측됐습니다.

**마무리 원칙** — 최종 구조로 `scf`를 새로 한 번 더 돌리세요. 셀이 변하면
평면파 기저가 변하므로(Pulay stress) 마지막 스텝의 에너지는 옛 기저의
값입니다 ([09장](09-relaxation.html)).

## 직접 써보기

1. `cell_dofree='ibrav'` 대신 `'all'`로 바꿔 보세요. 최종 셀이 큐빅을
   유지하나요?
2. 원자 하나를 (0.25, 0.25, 0.25) → (0.26, 0.26, 0.26)으로 옮기고
   `relax`(셀 고정)로 되돌아오는지 확인하세요.
3. 위 2번 구조에서 두 원자 모두에 `if_pos 0 0 0`을 걸면 어떻게 되나요?
4. 최적화된 구조로 `scf`를 재실행해 마지막 스텝 에너지와 비교해 보세요 —
   차이가 Pulay 오염의 크기입니다.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>vc-relax</code>에 느슨한 <code>conv_thr</code>(1.0d-6)를 쓰는 것 —
    힘·응력에 잡음이 실려 BFGS가 진동합니다. 응력은 컷오프에도 민감하므로,
    응력 기준 수렴(<a href="05-convergence.html">05장</a>)을 먼저 통과한
    컷오프를 쓰세요.
  </p>
</div>

## 관련 챕터

[09 구조 최적화](09-relaxation.html) ·
[05 컷오프와 k-점 수렴](05-convergence.html)
