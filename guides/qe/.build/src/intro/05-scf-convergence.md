---
layout: default
title: "5. SCF와 수렴"
---

# 5. SCF와 수렴
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

DFT의 전자 문제는 스스로를 참조합니다. 전하밀도가 유효 퍼텐셜을 만들고, 그
퍼텐셜이 다시 파동함수와 전하밀도를 만듭니다. 이 순환을 입력과 출력 전하밀도가
같아질 때까지 반복하는 것이 **자체무결(self-consistent field, SCF)** 계산입니다.

## 5.1 SCF 순환 읽기

`&electrons` 의 두 변수가 순환을 제어합니다.

```fortran
&electrons
  conv_thr    = 1.0d-8   ! 수렴 임계 (Ry)
  mixing_beta = 0.7      ! 새 전하밀도를 섞는 비율
/
```

출력에서 매 반복마다 `estimated scf accuracy` 가 찍히고, 이 값이 `conv_thr`
아래로 내려가면 수렴합니다.

```text
     iteration #  1 ...   estimated scf accuracy <   0.05408644 Ry
     iteration #  3 ...   estimated scf accuracy <   0.00010828 Ry
     iteration #  5 ...   estimated scf accuracy <   0.00000047 Ry
```

- `conv_thr` 은 보통 전체 에너지 계산에 10⁻⁶~10⁻⁸ Ry, 힘·구조 최적화에는
  10⁻⁸~10⁻⁹ Ry 처럼 더 엄격히 잡습니다.
- `mixing_beta` 는 새 전하밀도를 얼마나 공격적으로 반영할지입니다. 기본 0.7이
  잘 수렴하지만, **진동하며 수렴이 안 되면 0.2~0.3으로 낮추는 것**이 첫 대응입니다.

## 5.2 금속의 문제 — 왜 smearing이 필요한가

반도체·절연체는 점유된 밴드와 빈 밴드 사이에 띠간격(gap)이 있어, 각 k점에서 어떤
상태가 채워지는지 뚜렷합니다. 반면 금속은 페르미 준위가 밴드를 가로지르므로,
k점을 옮길 때마다 점유가 0과 1 사이에서 급변합니다. 이 불연속 때문에 유한한
k점으로는 적분이 잘 수렴하지 않고 SCF가 진동합니다.

**Smearing**(번짐)은 페르미 준위 근처의 점유를 매끄러운 함수로 퍼뜨려 이
불연속을 완화합니다.

```fortran
&system
  occupations = 'smearing'
  smearing    = 'mv'      ! Marzari-Vanderbilt(cold). 'gaussian','mp','fd'도 있음
  degauss     = 0.02      ! 번짐 폭 (Ry)
/
```

- `smearing = 'mv'`(cold smearing)나 `'mp'`(Methfessel-Paxton)는 전체 에너지의
  degauss 의존성이 작아 금속에 널리 쓰입니다.
- `degauss` 가 크면 수렴은 쉬워지지만 물리가 뭉개집니다. 보통 0.01~0.02 Ry.
- **degauss를 바꾸면 k점 밀도도 다시 수렴을 확인**해야 합니다. 둘은 함께 움직입니다.

금속을 smearing으로 SCF하면 반도체와 달리 페르미 준위가 출력됩니다.

```text
     the Fermi energy is     7.7439 ev
```

알루미늄을 실제로 smearing SCF해 페르미 준위와 금속성 상태밀도를 확인하는 과정은
[예제 E3](ex-03-metal-smearing.html)에 있습니다.

<div class="tip">
  <div class="note-title">절연체에 smearing을 쓰면?</div>
  <p>
    띠간격이 뚜렷한 절연체에 굳이 smearing을 쓸 필요는 없습니다(기본
    <code>occupations='fixed'</code>). 다만 수렴 안정성 때문에 작은 degauss를
    쓰기도 합니다. 반대로 <b>금속에 fixed를 쓰면</b> 거의 수렴하지 않습니다.
  </p>
</div>

## 5.3 수렴이 안 될 때

1. `mixing_beta` 를 0.2~0.3으로 낮춥니다(가장 흔한 해결).
2. 금속이면 `smearing` 을 켜고 k점을 늘립니다.
3. 초기 구조가 나쁘면(원자가 너무 가깝거나) 먼저 구조를 점검합니다.
4. `mixing_mode = 'local-TF'` 나 더 많은 `electron_maxstep` 을 시도합니다.
5. 자기(magnetic) 계는 초기 자기모멘트(`starting_magnetization`)를 줍니다.

자세한 진단은 [08장](08-troubleshooting.html)에서 다룹니다.

## 5.4 요점

- SCF는 `estimated scf accuracy` 가 `conv_thr` 아래로 내려가면 수렴입니다.
- 수렴이 흔들리면 `mixing_beta` 를 낮추는 것이 첫 대응입니다.
- 금속은 `occupations='smearing'` + 촘촘한 k점이 필수입니다.
- degauss와 k점 밀도는 함께 수렴을 확인해야 합니다.
