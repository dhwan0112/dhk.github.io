---
layout: default
title: "2. 입력 파일 구조"
---

# 2. 입력 파일 구조
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

`pw.x` 입력은 **네임리스트(namelist)**와 **카드(card)** 두 부분으로 이루어집니다.
네임리스트는 Fortran 스타일의 `&이름 ... /` 블록으로 계산 설정을 담고, 카드는
원자 종류·좌표·k점 같은 구조 정보를 담습니다.

## 2.1 네임리스트

| 네임리스트 | 필수 | 역할 |
|------------|------|------|
| `&control`   | ✔ | 계산 종류, 입출력 경로, 수렴 임계 |
| `&system`    | ✔ | 격자·원자 수·컷오프·점유(occupation) |
| `&electrons` | ✔ | SCF 순환 제어(mixing, conv_thr) |
| `&ions`      | relax류일 때 | 이온 이동 방식(BFGS 등) |
| `&cell`      | vc-relax류일 때 | 셀 이동 방식·압력 |

`&ions`, `&cell` 은 구조 최적화([06장](06-relax.html))에서만 씁니다.

### &control

```fortran
&control
  calculation = 'scf'      ! scf | nscf | bands | relax | vc-relax | md ...
  prefix      = 'si'       ! 출력 파일 접두어
  outdir      = './out'    ! 임시/결과 저장 디렉토리
  pseudo_dir  = './pseudo' ! 유사퍼텐셜 UPF 디렉토리
  verbosity   = 'high'     ! 'high' 면 밴드 등 더 자세히 출력
/
```

`calculation` 이 계산의 성격을 결정합니다. `prefix` 와 `outdir` 는 이후
후처리(`bands.x`, `dos.x`)가 같은 값을 참조해야 하므로 스텝 간에 일치시켜야
합니다.

### &system

구조와 기저를 정의하는, 가장 변수가 많은 블록입니다.

```fortran
&system
  ibrav     = 2          ! 브라베 격자 번호 (0이면 CELL_PARAMETERS 직접 지정)
  celldm(1) = 10.26      ! 격자 상수 a (bohr).  ibrav에 따라 celldm(2..6)도 사용
  nat       = 2          ! 셀 내 원자 수
  ntyp      = 1          ! 원자 종류 수
  ecutwfc   = 40.0       ! 파동함수 평면파 컷오프 (Ry)
  ecutrho   = 320.0      ! 전하밀도 컷오프 (Ry). 생략하면 4*ecutwfc
/
```

- `ibrav` 는 결정 격자를 번호로 지정합니다(2 = FCC, 3 = BCC, 4 = 육방, 1 = 단순
  입방 …). `ibrav = 0` 이면 `CELL_PARAMETERS` 카드로 격자 벡터를 직접 씁니다.
- `ecutwfc` / `ecutrho` 는 유사퍼텐셜에 맞춰 정해야 합니다([03장](03-pseudopotentials.html)).
- 금속이면 여기에 `occupations`, `smearing`, `degauss` 가 추가됩니다([05장](05-scf-convergence.html)).

### &electrons

```fortran
&electrons
  conv_thr    = 1.0d-8   ! SCF 수렴 임계 (Ry). 전체 에너지 변화가 이보다 작으면 종료
  mixing_beta = 0.7      ! 전하밀도 mixing 비율 (수렴이 흔들리면 0.2~0.3으로 낮춤)
/
```

## 2.2 카드

카드는 대문자 키워드 뒤에 데이터가 오는 블록입니다.

### ATOMIC_SPECIES

```fortran
ATOMIC_SPECIES
  Si  28.0855  Si.pbe-n-rrkjus_psl.1.0.0.UPF
```

원소 라벨, 원자 질량(amu), 유사퍼텐셜 파일 이름을 종류마다 한 줄씩 씁니다.
파일은 `pseudo_dir` 안에 있어야 합니다.

### ATOMIC_POSITIONS

```fortran
ATOMIC_POSITIONS (alat)
  Si  0.00 0.00 0.00
  Si  0.25 0.25 0.25
```

괄호 안 단위가 중요합니다. `alat`(격자 상수 단위), `crystal`(격자 벡터의 분율
좌표), `angstrom`, `bohr` 를 쓸 수 있습니다. 분자·비대칭 구조에는 `crystal` 이나
`angstrom` 이 편합니다.

### K_POINTS

```fortran
K_POINTS (automatic)
  8 8 8  0 0 0        ! Monkhorst-Pack 8x8x8, 오프셋 0 0 0
```

SCF에는 보통 `automatic`(Monkhorst-Pack 격자)을 씁니다. 밴드구조처럼 경로를
따라갈 때는 `crystal_b` / `tpiba_b` 로 고대칭점을 나열합니다([07장](07-bands-dos.html)).
자세한 선택은 [04장](04-kpoints.html)에서 다룹니다.

### CELL_PARAMETERS

`ibrav = 0` 일 때만 씁니다. 격자 벡터 세 줄을 직접 지정합니다.

```fortran
CELL_PARAMETERS (angstrom)
  5.43 0.00 0.00
  0.00 5.43 0.00
  0.00 0.00 5.43
```

## 2.3 자주 하는 실수

- 네임리스트 끝의 `/` 를 빠뜨리면 파싱이 멈춥니다.
- `nat`, `ntyp` 가 실제 카드의 원자 수·종류 수와 다르면 오류가 납니다.
- `ATOMIC_POSITIONS` 의 단위 괄호를 빠뜨리면 기본값(`alat`)으로 해석돼
  구조가 엉뚱해질 수 있습니다.
- `pseudo_dir` 경로가 틀리면 `error ... reading pseudopotential` 가 납니다
  ([08장](08-troubleshooting.html)).

각 변수의 전체 목록과 기본값은 공식 입력 설명서
[INPUT_PW](https://www.quantum-espresso.org/Doc/INPUT_PW.html)에 정리돼 있습니다.
