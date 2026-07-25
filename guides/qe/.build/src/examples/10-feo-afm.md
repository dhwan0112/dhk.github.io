---
title: "E10. FeO AFM (GGA 실패)"
---

# E10. FeO AFM (GGA 실패)

## 목적

반강자성 산화물의 관문 예제입니다. 암염구조 FeO의 AFM-II 배열(교대하는
(111) 스핀 면)을 **같은 원소를 다른 라벨로 분리**해 만들고, GGA(PBE)가 이
계를 **금속으로 잘못 예측**하는 것을 직접 확인합니다. 실험은 갭 ~2.4 eV의
절연체입니다. 이 실패를 눈으로 보는 것이 [E11(DFT+U)](ex-11-feo-hubbard.html)로
넘어가는 동기입니다.

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `ntyp=3` (Fe1/Fe2/O) | **같은 UPF를 두 라벨로 등록** — AFM 배열의 핵심 |
| `starting_magnetization` ±0.6 | Fe1 ↑, Fe2 ↓ 초기화 |
| `ibrav=0` + 능면체 자기셀 | 2 Fe + 2 O, 부피 = 0.5 a³ |
| `mixing_beta=0.2` + `local-TF` | 예민한 자성 산화물의 mixing 처방 |

## 입력 파일

[feo.scf.in 내려받기](files/E10-feo-afm/feo.scf.in)

```fortran
&CONTROL
  calculation = 'scf'
  prefix      = 'FeO'
  outdir      = './tmp/'
  pseudo_dir  = './pseudo/'
  verbosity   = 'high'
  tprnfor     = .true.
  tstress     = .true.
/
&SYSTEM
  ibrav       = 0
  celldm(1)   = 8.18            ! bohr (= 4.33 Å, 큐빅 격자상수)
  nat         = 4
  ntyp        = 3
  ecutwfc     = 70
  ecutrho     = 700
  occupations = 'smearing'
  smearing    = 'mv'
  degauss     = 0.01
  nspin       = 2
  starting_magnetization(1) =  0.6    ! Fe1  ↑
  starting_magnetization(2) = -0.6    ! Fe2  ↓
  starting_magnetization(3) =  0.0    ! O
/
&ELECTRONS
  conv_thr    = 1.0d-8
  mixing_beta = 0.2
  mixing_mode = 'local-TF'
  electron_maxstep = 300
/

ATOMIC_SPECIES
  Fe1  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
  Fe2  55.845  Fe.pbe-spn-kjpaw_psl.1.0.0.UPF   ! 같은 파일, 다른 라벨
  O    15.999  O.pbe-n-kjpaw_psl.1.0.0.UPF

CELL_PARAMETERS (alat)
  0.5  0.5  1.0
  0.5  1.0  0.5
  1.0  0.5  0.5

ATOMIC_POSITIONS (crystal)
  Fe1  0.00  0.00  0.00
  Fe2  0.50  0.50  0.50
  O    0.25  0.25  0.25
  O    0.75  0.75  0.75

K_POINTS (automatic)
  6 6 6  0 0 0
```

라벨 분리 없이는 QE가 두 Fe를 대칭 등가로 보고 AFM 배열을 만들 수
없습니다. 이 라벨 분리는 [DFT+U(E11)](ex-11-feo-hubbard.html)와
[hp.x(E12)](ex-12-feo-hp.html)에서도 그대로 필요합니다.

## 실행

```bash
mpirun -np 8 pw.x -nk 4 -in feo.scf.in > feo.scf.out
```

## 출력에서 확인할 것 — 실측 (이 예제의 진짜 목적)

| 항목 | 실측값 (QE 7.5, PAW) | 해석 |
|---|---|---|
| 총에너지 | −741.81592118 Ry (28회 수렴) | |
| total magnetization | **0.00 μB** | AFM 성립 |
| absolute magnetization | **7.17 μB** | total≈0 + absolute 큼 = AFM의 표지 |
| Fe 국소 모멘트 | +3.31 / −3.31 μB | (111) 면 교대 배열 확인 |
| O 모멘트 | 0.00 | |
| **`the Fermi energy is 14.2231 ev`** | **출력됨 = 금속** | **GGA의 실패.** 실험은 절연체(~2.4 eV) |

<figure>
  <img src="assets/images/qe-e10-e11-feo-dos.png"
       alt="FeO spin-resolved DOS: GGA metallic vs GGA+U gap" />
  <figcaption>
    FeO 스핀 분해 DOS 실측 (QE 7.5, nscf 8×8×8). 왼쪽(이 예제, GGA):
    Fermi 준위에 Fe-3d 상태가 걸려 DOS(E_F)≈3.7 — 금속입니다. 오른쪽은
    <a href="ex-11-feo-hubbard.html">E11</a>에서 U를 켠 결과로, Hubbard
    분리가 일어나되 좁은 t2g 띠가 남는 함정까지 그대로 보입니다.
  </figcaption>
</figure>

AFM 배열은 완벽히 성립했는데도(모멘트 ±3.31 μB) 전자구조는
금속입니다. GGA의 자기상호작용 오차가 국소화된 Fe-3d 전자를 비물리적으로
퍼뜨린 결과이며, U 보정이 필요한 이유입니다 ([13장](13-dft-plus-u.html)).

## 직접 써보기

1. PDOS([E7](ex-07-si-dos.html) 절차)를 뽑아 Fermi 준위에 걸린 상태가
   Fe-3d임을 확인하세요.
2. 강자성 배열(둘 다 +0.6)로 계산해 AFM과 에너지를 비교하세요. 어느 쪽이
   바닥상태인가요?
3. 셀 벡터가 정말 2 formula unit인지 부피로 검산하세요 (행렬식 = 0.5 a³).
4. `starting_magnetization`을 모두 0으로 두면 어떤 해로 수렴하나요?

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>ntyp=2</code>(Fe/O)로 두고 <code>starting_magnetization</code>만
    ±로 주는 것 — 같은 타입의 원자는 같은 초기 자화를 받으므로 AFM이
    만들어지지 않습니다. 그리고 AFM인데 total magnetization이 0이 아니라면
    라벨 분리 실패나 대칭 강제를 의심하세요
    (<a href="ref-errors.html">R3</a> 5절).
  </p>
</div>

## 관련 챕터

[12 스핀 편극과 자성](12-magnetism.html) ·
[13 DFT+U와 HUBBARD 카드](13-dft-plus-u.html) ·
[07 SCF 수렴 제어](07-scf-control.html)
