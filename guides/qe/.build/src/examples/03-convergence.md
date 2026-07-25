---
title: "E3. 수렴 테스트 자동화"
---

# E3. 수렴 테스트 자동화

## 목적

**여기가 QE 실력의 분기점입니다.** ecutwfc, k-점, 그리고 힘의 수렴 테스트를
셸 스크립트로 자동화하는 표준 절차를 익힙니다. 판정 기준을 meV/atom과
meV/Å로 환산하는 감각까지가 이 예제의 목표입니다. 배경은
[05장](05-convergence.html).

## 새로 나오는 것

| 항목 | 역할 |
|---|---|
| `sed`로 입력 파생 | 하나의 기준 입력에서 스캔 입력들을 생성 |
| `grep '^!'` | 수렴된 총에너지만 추출 |
| meV/atom 환산 | ΔE × 13605.7 / nat |

## 입력 파일

기준 입력은 [E1](ex-01-si-scf.html)과 동일합니다
([si.scf.in](files/E03-convergence/si.scf.in)).

[conv_ecut.sh](files/E03-convergence/conv_ecut.sh) ·
[conv_kpts.sh](files/E03-convergence/conv_kpts.sh) ·
[conv_force.sh](files/E03-convergence/conv_force.sh)

```bash
#!/bin/bash
# conv_ecut.sh — ecutwfc 수렴. ecutrho 는 8배로 함께 올린다 (PAW/US 기준).
NAT=2
printf "# ecutwfc(Ry)  E_total(Ry)   dE_vs_last(meV/atom)\n" > conv_ecut.dat
LAST=""
for E in 20 25 30 35 40 45 50 60 70 80; do
  sed -e "s/ecutwfc *=.*/ecutwfc      = $E/" \
      -e "s/ecutrho *=.*/ecutrho      = $((E*8))/" si.scf.in > tmp_e$E.in
  pw.x -in tmp_e$E.in > tmp_e$E.out
  EN=$(grep '^!' tmp_e$E.out | tail -1 | awk '{print $5}')
  echo "$E  $EN" >> conv_ecut.dat
  LAST=$EN
done
awk -v nat=$NAT -v ref="$LAST" '!/^#/{printf "%6s  %16s  %10.3f\n",$1,$2,($2-ref)*13605.7/nat}' conv_ecut.dat
```

k-점 스캔(`conv_kpts.sh`)은 `K_POINTS` 줄을, 힘 스캔(`conv_force.sh`)은
대칭을 깬 구조(Si를 0.25 → 0.26으로 변위)의 첫 원자 힘을 같은 방식으로
추출합니다.

## 실행

```bash
bash conv_ecut.sh
bash conv_kpts.sh  > conv_kpts.dat
bash conv_force.sh > conv_force.dat
```

## 출력·그림 — 실측

<figure>
  <img src="assets/images/qe-e03-convergence.png"
       alt="Si convergence: dE vs ecutwfc, dE vs k-grid, force vs ecutwfc" />
  <figcaption>
    실리콘 수렴 실측 (QE 7.5, PAW, ecutrho = 8×ecutwfc 동시 스캔).
    왼쪽: 컷오프 — 변분 원리 덕분에 위에서 아래로 단조 수렴합니다.
    가운데: k-격자 — 단조가 아니어도 정상입니다. 오른쪽: 변위 구조의 힘 —
    이 계에서는 40 Ry면 힘도 0.03 meV/Å 수준으로 수렴합니다.
  </figcaption>
</figure>

숫자로 보는 판정 (기준: 최밀 스캔 값):

| ecutwfc | ΔE (meV/atom) | | k-격자 | ΔE (meV/atom) |
|---|---|---|---|---|
| 20 | 13.72 | | 2³ | 1279 |
| 25 | 5.03 | | 4³ | 94.2 |
| 30 | 1.76 | | 6³ | 12.0 |
| **40** | **0.91** | | **8³** | **1.95** |
| 50 | 0.27 | | 10³ | 0.36 |
| 60 | 0.14 | | 12³ | 0.073 |

- 총에너지 1 meV/atom 기준이면 **ecutwfc 40 Ry, k 10×10×10** 부근이
  합격선입니다. E1의 30 Ry / 8³은 학습용 잠정값이었던 셈입니다.
- 힘(변위 구조의 Fx ≈ 0.0288 Ry/bohr = 0.741 eV/Å)은 30 → 40 Ry에서
  0.5 meV/Å 변하고 이후 0.03 meV/Å 이내로 안정됩니다. ML 퍼텐셜 학습
  데이터라면 이 힘 기준(~1 meV/Å)으로 판정하세요.

## 직접 써보기

1. `ecutrho`를 `ecutwfc`의 4배로 고정한 채 같은 테스트를 반복하고, PAW에서
   무슨 일이 생기는지 관찰하세요 ([04장](04-pseudopotentials.html)의 함정).
2. 에너지가 수렴한 컷오프와 힘이 수렴한 컷오프를 비교하세요. 어느 쪽이 더
   높은가요?
3. 스캔 결과를 그림으로 그리는 파이썬 스크립트를 직접 써 보세요 (본
   가이드의 그림 스크립트는 저장소 `.build/plot_qe.py`에 있습니다).

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    힘을 추출할 때 <code>grep 'atom    1 ... force' | tail -1</code>처럼
    <strong>마지막 매치</strong>를 집으면 총힘이 아니라 출력 뒤쪽의 기여 분해
    블록(SCF correction, ~10⁻⁶)을 잡습니다. 총힘은 <code>Forces acting on
    atoms</code> 직후의 <strong>첫 매치</strong>입니다. 실제로 이 예제를
    처음 실측할 때 이 함정에 걸렸고, 위 스크립트는 수정된 판입니다.
  </p>
</div>

## 관련 챕터

[05 컷오프와 k-점 수렴](05-convergence.html) ·
[04 유사퍼텐셜](04-pseudopotentials.html)
