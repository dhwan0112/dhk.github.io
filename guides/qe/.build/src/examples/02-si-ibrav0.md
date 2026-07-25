---
title: "E2. ibrav=0 다시 쓰기"
---

# E2. ibrav=0 다시 쓰기

## 목적

[E1](ex-01-si-scf.html)과 **물리적으로 동일한 계**를 `ibrav=0` +
`CELL_PARAMETERS`로 다시 정의합니다. 두 표현의 등가성을 총에너지로
확인하고, 좌표 단위 옵션(`alat`/`crystal`/`angstrom`)을 몸에 익힙니다.
자동 생성기(ASE 등)가 뱉는 입력이 전부 이 형식이므로, 읽을 줄 알아야
합니다.

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `ibrav = 0` | 셀을 직접 지정하겠다는 선언 |
| `CELL_PARAMETERS (angstrom)` | 셀 벡터 3개를 행으로 |
| `ATOMIC_POSITIONS (crystal)` | 분수 좌표 — 셀과 구조의 분리 |

## 입력 파일

[si_ibrav0.scf.in 내려받기](files/E02-si-ibrav0/si_ibrav0.scf.in)

```fortran
&CONTROL
  calculation = 'scf'
  prefix      = 'si_ibrav0'
  outdir      = './tmp/'
  pseudo_dir  = './pseudo/'
  verbosity   = 'high'
/
&SYSTEM
  ibrav       = 0           ! 셀을 직접 지정하겠다는 선언
  nat         = 2
  ntyp        = 1
  ecutwfc     = 30
  ecutrho     = 240
  occupations = 'fixed'
/
&ELECTRONS
  conv_thr    = 1.0d-8
/

ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-kjpaw_psl.1.0.0.UPF

CELL_PARAMETERS (angstrom)
  -2.715   0.000   2.715
   0.000   2.715   2.715
  -2.715   2.715   0.000

ATOMIC_POSITIONS (crystal)
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25

K_POINTS (automatic)
  8 8 8  0 0 0
```

## 실행

```bash
mpirun -np 6 pw.x -nk 6 -in si_ibrav0.scf.in > si_ibrav0.scf.out
```

## 출력에서 확인할 것 — 실측 비교

| 항목 | E1 (`ibrav=2`) | E2 (`ibrav=0`) |
|---|---|---|
| 총에너지 | −93.45273690 Ry | −93.45274992 Ry |
| `Sym. Ops.` | 48 (반전 포함) | 48 (반전 포함) |

- 대칭은 두 경우 모두 48개가 온전히 잡혔습니다. 잘 정렬된
  `CELL_PARAMETERS`라면 `ibrav=0`이라도 대칭 탐지가 실패하지 않습니다
  (일반적으로는 실패할 수 있으니 항상 확인하세요).
- 에너지 차이는 1.3×10⁻⁵ Ry(원자당 0.09 meV)로, 완전한 일치가 아닙니다.
  원인은 문법이 아니라 **격자상수의 반올림**입니다: E1의
  `celldm(1)=10.26 bohr`는 5.4293 Å이고, E2의 셀(2.715 Å 반격자)은
  정확히 5.4300 Å입니다. "같은 구조"를 두 번 쓸 때 단위 변환의 자릿수까지
  맞춰야 소수점 끝까지 일치합니다 — 그 자체로 좋은 교훈입니다.

## 직접 써보기

1. `CELL_PARAMETERS`의 단위를 `angstrom` → `alat`로 바꾸고 `celldm(1)`을
   도입해 같은 구조를 표현하세요. `celldm(1)=10.2614` (= 5.4300 Å)로 두면
   E2와 소수점까지 일치하는지 확인하세요.
2. `ATOMIC_POSITIONS (crystal)`을 `(angstrom)`으로 변환해 쓰세요. 두 결과의
   총에너지가 같은지 확인하세요.
3. 셀 벡터의 성분 하나를 일부러 0.001 Å 틀어 보세요. `Sym. Ops.` 수가
   몇 개로 떨어지고 기약 k-점이 몇 개로 늘어나는지 관찰하세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <code>ibrav=0</code>인데 <code>celldm(1)</code>도 함께 준 경우,
    <code>CELL_PARAMETERS</code>의 단위 옵션이 없으면 <code>alat</code>(=
    <code>celldm(1)</code>) 단위로 해석됩니다. 단위 옵션을 <strong>항상
    명시</strong>하는 습관이 사고를 막습니다. 좌표 규약 전체는
    <a href="03-units-coordinates.html">03장</a>.
  </p>
</div>

## 관련 챕터

[03 단위계와 좌표계](03-units-coordinates.html) ·
[02 입력 파일 구조](02-input-structure.html)
