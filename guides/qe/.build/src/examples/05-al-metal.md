---
title: "E5. fcc Al 금속"
---

# E5. fcc Al 금속

## 목적

첫 **금속** 계산입니다. `occupations='smearing'`이 왜 필요한지, 페르미
준위가 어디에 찍히는지, 그리고 smearing 종류와 `degauss`가 에너지에 어떤
흔적을 남기는지 실측으로 확인합니다.

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `occupations='smearing'` | 금속의 부분 점유 |
| `smearing='mv'` | Marzari-Vanderbilt (cold) — 금속 권장 |
| `degauss` | smearing 폭 (Ry) |
| `nbnd=8` | 기본값보다 넉넉한 밴드 수 |

## 입력 파일

[al.scf.in 내려받기](files/E05-al-metal/al.scf.in)

```fortran
&CONTROL
  calculation = 'scf'
  prefix      = 'al'
  outdir      = './tmp/'
  pseudo_dir  = './pseudo/'
  verbosity   = 'high'
/
&SYSTEM
  ibrav       = 2
  celldm(1)   = 7.65        ! bohr (= 4.05 Å)
  nat         = 1
  ntyp        = 1
  ecutwfc     = 40
  ecutrho     = 320
  occupations = 'smearing'
  smearing    = 'mv'        ! Marzari-Vanderbilt (cold) — 금속에 권장
  degauss     = 0.02        ! Ry
  nbnd        = 8           ! 기본값보다 넉넉하게
/
&ELECTRONS
  conv_thr    = 1.0d-8
  mixing_beta = 0.7
/

ATOMIC_SPECIES
  Al  26.9815  Al.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (alat)
  Al  0.00  0.00  0.00

K_POINTS (automatic)
  12 12 12  0 0 0
```

## 실행

```bash
mpirun -np 6 pw.x -nk 6 -in al.scf.in > al.scf.out
```

## 출력에서 확인할 것 — 실측

| 항목 | 실측값 (QE 7.5, PAW) |
|---|---|
| 총에너지 | −39.50323368 Ry |
| **페르미 준위** | `the Fermi energy is 7.7450 ev` — 금속의 표지 |
| `smearing contrib. (-TS)` | smearing이 남긴 오염의 크기 |

절연체([E1](ex-01-si-scf.html))에서는 `highest occupied level`이 나오던
자리에, 금속에서는 `the Fermi energy is`가 나옵니다. **이 줄이 곧 "이 계는
금속으로 수렴했다"는 진단**입니다 — [E10](ex-10-feo-afm.html)에서 이 진단을
다시 만나게 됩니다.

## smearing 종류별 degauss 스캔 — 실측

같은 계에서 smearing 종류(gaussian/mv/fd) × degauss(0.005~0.05 Ry)를
스캔했습니다.

<figure>
  <img src="assets/images/qe-e05-smearing.png"
       alt="Al total energy vs degauss for three smearing types" />
  <figcaption>
    fcc Al 실측 (QE 7.5, 12×12×12 k). cold smearing(mv)은 0.01→0.05 Ry에서
    에너지가 0.3 mRy만 움직여 사실상 평탄한 반면, gaussian은 3 mRy,
    Fermi-Dirac은 22 mRy나 흘러갑니다. "mv는 외삽이 필요 없다"는 말의
    실측 근거입니다.
  </figcaption>
</figure>

한 가지 실전 사고도 있었습니다 — `mv`에 `degauss=0.005`를 주자 12³ 격자로는
적분 전하가 3.003으로 어긋나며 **`charge is wrong`으로 정지**했습니다.
smearing 폭을 줄이면 그만큼 조밀한 k-격자가 필요합니다. degauss와 k-격자는
**함께 수렴**시키는 짝입니다 ([06장](06-occupations.html)).

## 직접 써보기

1. k-격자를 8³ → 16³으로 바꿔가며 degauss별 에너지 요동을 관찰하세요.
   degauss가 작을수록 k 요구가 커지는 것을 확인할 수 있습니다.
2. `nbnd`를 지우면 QE가 몇 개를 잡는지 출력에서 확인하세요.
3. `occupations='fixed'`로 바꾸면 어떤 에러가 나는지 직접 겪어 보세요
   ([R3](ref-errors.html)에 있는 바로 그 메시지입니다).

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    degauss를 크게 두고 "수렴 잘 된다"며 만족하는 것.
    <code>smearing contrib. (-TS)</code>가 크면 결과가 σ→0 극한에서 멀리
    있다는 뜻입니다. 목표 물성이 degauss에 둔감한지 항상 확인하세요.
    자성 금속에서는 과한 degauss가 자기모멘트를 지웁니다
    (<a href="ex-09-fe-bcc.html">E9</a>).
  </p>
</div>

## 관련 챕터

[06 점유수와 smearing](06-occupations.html) ·
[05 컷오프와 k-점 수렴](05-convergence.html)
