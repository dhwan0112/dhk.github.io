---
title: "11. 전하밀도와 퍼텐셜"
---

# 11. 전하밀도와 퍼텐셜

## 목차
{:.toc-title}

1. TOC
{:toc}

`pp.x`는 SCF가 만들어 둔 밀도·퍼텐셜을 실공간 격자로 추출해 시각화 가능한
파일로 바꿉니다. 입력은 두 네임리스트입니다 — 무엇을 뽑을가(`&INPUTPP`)와
어떤 형식으로 쓸가(`&PLOT`).

## 입력 골격

```fortran
&INPUTPP
  prefix   = 'si'
  outdir   = './tmp/'
  filplot  = 'si.rho.dat'
  plot_num = 0              ! 0 = 원자가 전하밀도
/
&PLOT
  nfile         = 1
  filepp(1)     = 'si.rho.dat'
  weight(1)     = 1.0
  iflag         = 3         ! 3 = 3D
  output_format = 6         ! 6 = Gaussian cube
  fileout       = 'si.rho.cube'
/
```

`iflag`: 0 = 1D 선 / 1 = 구면평균 / 2 = 2D 단면 / 3 = 3D.
`output_format`: 0 = gnuplot / 5 = XSF(XCrySDen) / 6 = Gaussian cube 등.

## 자주 쓰는 plot_num

| 값 | 내용 | 용도 |
|---|---|---|
| 0 | 원자가 전하밀도 | 결합 성격 관찰 |
| 1 | 총 퍼텐셜 (V_bare + V_H + V_xc) | |
| 2 | 국소 이온 퍼텐셜 | |
| 5 | STM 이미지 | 표면 |
| 6 | 스핀 밀도 ρ↑ − ρ↓ | **자성 분포 시각화** |
| 8 | ELF (전자 국소화 함수) | 결합·고립전자쌍 |
| 11 | bare + Hartree 퍼텐셜 | **슬랩 일함수 계산** |

나머지 값과 PAW 전전자(all-electron) 전하밀도 옵션은 버전에 따라 다르므로
반드시 설치 버전의 `Doc/INPUT_PP.txt`를 확인하세요.

## 일함수 계산의 뼈대

슬랩에서 `plot_num=11`로 퍼텐셜을 뽑고, `average.x`(또는 직접 파싱)로 표면에
평행한 평면 평균을 낸 뒤:

$$\Phi = V_{\mathrm{vacuum}} - E_F$$

진공 준위는 평면평균 퍼텐셜이 진공 한가운데서 평탄해지는 값입니다.
쌍극자 보정과 함께 쓰는 전체 절차는 [15장](15-surfaces.html)과
[예제 E13](ex-13-slab-md.html)에 있습니다.

## Bader 전하 — QE 내장이 아닙니다

Bader 전하 분석은 `pp.x`로 전하밀도를 cube로 뽑은 뒤 Henkelman 그룹의
[`bader` 코드](https://theory.cm.utexas.edu/henkelman/code/bader/)에 넘기는
방식입니다. **PAW를 쓴다면 전전자 전하밀도를 써야 정확하며**, 해당
`plot_num` 값은 설치 버전의 `Doc/INPUT_PP.txt`에서 확인하세요. 원자가
밀도만으로 Bader를 돌리면 코어 전하가 빠져 결과가 왜곡됩니다.

## 시각화 도구

- **VESTA** — 구조 + cube 등가면. 가장 무난한 출발점.
- **XCrySDen** — QE와 궁합이 좋은 고전 도구 (XSF 형식).
- **Python (ASE / pymatgen)** — 후처리를 직접 파싱하는 습관을 들이면 이후
  자동화가 훨씬 쉬워집니다. 본 가이드의 그림도 전부 Python으로 그렸습니다.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    스핀 계에서 <code>plot_num=6</code>(스핀 밀도)을 뽑았는데 0에 가깝게 나오는
    경우 — <code>spin_component</code> 설정과, 애초에 SCF가 자성 해로 수렴했는지
    (<code>total/absolute magnetization</code>)부터 확인하세요. 또, cube 파일은
    금방 수백 MB가 되므로 <code>nx,ny,nz</code>로 격자를 조절하고 저장소를
    관리하세요.
  </p>
</div>

## 관련 예제

- [E13 · 슬랩과 AIMD](ex-13-slab-md.html) — `plot_num=11`로 일함수 실측.
- [E9 · bcc Fe](ex-09-fe-bcc.html) — 스핀 분해 DOS와 함께 보면 좋은 계.
