---
title: "E4. O₂ 분자 (삼중항)"
---

# E4. O₂ 분자 (삼중항)

## 목적

주기 코드로 **고립 분자**를 다루는 법을 배웁니다 — 진공 상자, Γ점 계산,
주기 이미지 보정, 그리고 스핀 상태 고정. O₂의 바닥상태는 삼중항(S=1)이며,
Fe–O 계를 다룬다면 O₂는 반드시 한 번 거쳐야 하는 기준계입니다. GGA가 O₂
결합에너지를 크게 과대평가하는 유명한 사례를 직접 확인합니다.

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `K_POINTS gamma` | Γ 한 점 — 분자는 분산이 없고, 실수 파동함수 최적화 사용 |
| `assume_isolated='mt'` | Martyna-Tuckerman 주기 이미지 보정 |
| `nspin=2` + `tot_magnetization` | 스핀 편극 + 총 자화 **구속** (삼중항 강제) |
| `ibrav=1` + 큰 `celldm(1)` | 진공 상자 (20 bohr) |

## 입력 파일

[o2.scf.in](files/E04-o2-molecule/o2.scf.in) ·
[o_atom.scf.in](files/E04-o2-molecule/o_atom.scf.in)

```fortran
&CONTROL
  calculation       = 'scf'
  prefix            = 'o2'
  outdir            = './tmp/'
  pseudo_dir        = './pseudo/'
  verbosity         = 'high'
  tprnfor           = .true.
/
&SYSTEM
  ibrav             = 1
  celldm(1)         = 20.0        ! bohr — 진공 상자
  nat               = 2
  ntyp              = 1
  ecutwfc           = 60
  ecutrho           = 480
  assume_isolated   = 'mt'        ! Martyna-Tuckerman 주기 이미지 보정
  nspin             = 2
  tot_magnetization = 2.0         ! 삼중항 강제 (2개의 Fermi 준위 사용)
  occupations       = 'smearing'
  smearing          = 'gaussian'
  degauss           = 0.001
/
&ELECTRONS
  conv_thr          = 1.0d-8
  mixing_beta       = 0.3
/

ATOMIC_SPECIES
  O  15.9994  O.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS (angstrom)
  O  0.000  0.000  0.000
  O  0.000  0.000  1.210

K_POINTS gamma
```

원자 O 입력(`o_atom.scf.in`)은 `nat=1`, 같은 상자·컷오프에
`tot_magnetization=2.0`(원자 O의 바닥상태 ³P)입니다.

## 실행

```bash
mpirun -np 6 pw.x -in o2.scf.in     > o2.scf.out
mpirun -np 6 pw.x -in o_atom.scf.in > o_atom.scf.out
```

Γ점 하나뿐이므로 `-nk` 풀 병렬은 의미가 없고 G-벡터 분산만 씁니다.

## 출력에서 확인할 것 — 실측

| 항목 | 실측값 (QE 7.5, PAW) |
|---|---|
| E(O₂) | −83.03824491 Ry |
| E(O 원자) | −41.26799048 Ry |
| total magnetization | 2.00 μB (구속값 그대로) |
| absolute magnetization | 2.05 μB (스핀 밀도가 공간 분포하므로 2보다 약간 큼 — 정상) |
| **결합 에너지 D = 2E(O) − E(O₂)** | **0.50226 Ry = 6.83 eV** |

실험 결합에너지는 5.12 eV(D₀)입니다. **PBE가 1.7 eV나 과대평가**하는 것이
그대로 실측됩니다 — O₂를 기준으로 산화물 형성에너지를 계산할 때 보정이
필요한 이유이며, 문헌에서 "O₂ 보정"이 등장하는 배경입니다.

`tot_magnetization` vs `starting_magnetization`:

| 변수 | 의미 | 언제 쓰나 |
|---|---|---|
| `starting_magnetization(i)` | **초기 추측**. SCF가 자유롭게 바꿈 | 대부분의 경우 |
| `tot_magnetization` | 셀 전체 자화를 **구속**. up/down 별도 Fermi 준위 | 특정 스핀 상태를 강제할 때 |

## 직접 써보기

1. `tot_magnetization = 0.0`(단일항)으로 바꿔 에너지를 비교하세요. 삼중항이
   얼마나 더 안정한가요?
2. 상자를 20 → 25 bohr로 키우면 에너지가 얼마나 변하나요 (진공 수렴)?
3. `assume_isolated`를 빼면 에너지가 얼마나 달라지나요? 주기 이미지
   상호작용의 크기를 직접 재 보세요.
4. 결합 길이를 1.16 → 1.26 Å로 스캔해 평형 길이를 구하고 실험값 1.21 Å과
   비교하세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    분자를 <code>occupations='fixed'</code>로 돌리는 것 — O₂처럼 부분 점유
    (축퇴된 π* 궤도)가 본질인 계는 스핀 상태를 고정해도 미세한 smearing이
    있어야 수렴이 안정합니다(여기서는 degauss 0.001 Ry). 또, 진공 상자가
    작으면 <code>assume_isolated</code>로도 다 못 걷어내는 이미지 상호작용이
    남습니다 — 상자 크기도 수렴 파라미터입니다.
  </p>
</div>

## 관련 챕터

[06 점유수와 smearing](06-occupations.html) ·
[12 스핀 편극과 자성](12-magnetism.html)
