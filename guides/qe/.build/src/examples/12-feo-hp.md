---
title: "E12. hp.x 로 U 계산"
---

# E12. hp.x 로 U 계산

## 목적

[E11](ex-11-feo-hubbard.html)에서는 U = 4.6 eV를 "주어진 값"으로
썼습니다. 이번에는 그 U를 **선형 응답(DFPT)으로 직접 계산**합니다.
경험 파라미터 없이, 이 계·이 유사퍼텐셜·이 투영자에 맞는 U가 나옵니다.
배경은 [14장](14-hubbard-hp.html).

```
pw.x (U ≈ 0 을 넣은 scf, conv_thr 1e-12) → hp.x → FeO.Hubbard_parameters.dat
```

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `HUBBARD` 카드에 U = 1.0d-8 | hp.x가 섭동할 원자·매니폴드 인식용 (사실상 0) |
| `conv_thr = 1.0d-12` | 선형 응답은 바닥상태 품질에 민감 |
| `&INPUTHP` | hp.x 입력 — `nq1/nq2/nq3`, `conv_thr_chi` |

## 입력 파일

[feo_hp_scf.in](files/E12-feo-hp/feo_hp_scf.in) ·
[feo.hp.in](files/E12-feo-hp/feo.hp.in) ·
[run.sh](files/E12-feo-hp/run.sh)

SCF 입력은 [E10](ex-10-feo-afm.html)과 동일한 셀에 다음이 더해집니다.

```fortran
&ELECTRONS
  conv_thr         = 1.0d-12     ! hp.x 선행 계산은 매우 엄격하게
  ...
/
...
HUBBARD (ortho-atomic)
U Fe1-3d 1.0d-8
U Fe2-3d 1.0d-8
```

hp.x 입력:

```fortran
&INPUTHP
  prefix       = 'FeO'
  outdir       = './tmp/'
  nq1 = 2, nq2 = 2, nq3 = 2
  conv_thr_chi = 1.0d-6      ! 금속성(GGA) 바닥상태에선 1.0d-8 이 잔차 노이즈에 걸린다 (실측)
  iverbosity   = 2
/
```

`conv_thr_chi`에 관한 실측 노트 — 처음에는 1.0d-8로 돌렸는데, χ 값 자체는
일곱 자리까지 안정된 뒤에도 잔차가 10⁻⁷ 부근의 노이즈 플로어에서 진동하며
임계값을 넘지 못했습니다(46회 반복까지 확인). GGA FeO처럼 바닥상태가
금속성인 계에서는 응답 함수의 수치 노이즈가 그 수준이라, 1.0d-6으로
완화했습니다. χ의 상대 변동은 0.1% 미만이므로 U에 미치는 영향은
0.01 eV 이하입니다.

## 실행

```bash
pw.x -in feo_hp_scf.in > feo_hp_scf.out
hp.x -in feo.hp.in     > feo.hp.out
cat FeO.Hubbard_parameters.dat
```

hp.x는 비등가 Hubbard 원자마다 섭동 계산을 돌리므로 시간이 걸립니다
(`-nk` 풀 병렬 적용 가능, q-점은 `start_q`/`last_q`로 분할 가능).

## 출력에서 확인할 것 — 실측

| 항목 | 실측값 (QE 7.5, PAW, ortho-atomic) |
|---|---|
| 선행 SCF | −741.81592119 Ry (conv_thr 1e-12, 3분 15초) |
| 섭동 원자 | 1개 — Fe2는 hp.x가 대칭 등가로 인식해 건너뜀 |
| **계산된 U (Fe-3d)** | **5.2235 eV** (Fe1·Fe2 동일) |
| 소요 시간 | 1시간 57분 (8랭크, 2×2×2 q → 기약 q점 4개) |

`FeO.Hubbard_parameters.dat`에 원자별 U와 χ₀·χ 행렬 전체가 정리됩니다.
계산된 U = 5.22 eV는 [E11](ex-11-feo-hubbard.html)에서 쓴 문헌 관례값
4.6 eV보다 0.6 eV쯤 큽니다 — 어느 쪽이 "맞다"기보다, U는
투영자·유사퍼텐셜·자기 배열과 세트로만 의미가 있다는 것을 보여 주는
쌍입니다. 자기 계에는 자기 계에서 계산한 U를 쓰는 것이 원칙입니다.

## 직접 써보기

1. `nq`를 1×1×1 → 2×2×2로 바꿔 U가 얼마나 변하는지 확인하세요. q 수렴
   없이 얻은 U는 신뢰할 수 없습니다.
2. 계산된 U를 [E11](ex-11-feo-hubbard.html)의 HUBBARD 카드에 넣어 갭과
   모멘트가 어떻게 변하는지 확인하세요.
3. 얻은 U로 scf → hp.x를 한 번 더 돌려(self-consistent U) 값이 안정되는지
   보세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    선행 scf의 <code>conv_thr</code>를 평소처럼 1.0d-8로 두는 것 — 응답
    행렬에 잡음이 들어가 U가 흔들립니다. 그리고 <code>HUBBARD</code> 카드
    없이 hp.x를 돌리면 "어떤 원자를 섭동할지" 알 수 없어 실패합니다.
    U를 아주 작은 값(1.0d-8)으로라도 반드시 지정하세요.
  </p>
</div>

## 관련 챕터

[14 hp.x 로 U 계산하기](14-hubbard-hp.html) ·
[13 DFT+U와 HUBBARD 카드](13-dft-plus-u.html)
