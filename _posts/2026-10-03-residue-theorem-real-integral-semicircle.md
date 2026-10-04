---
title: "유수 정리를 이용한 실적분 계산"
date: 2026-10-03
category: Study
tags: [Math, Complex Analysis, Residue Theorem]
description: "유수 정리로 ∫dx/(x²+1) = π 를 처음부터 끝까지 계산하는 절차. 증명의 대부분은 큰 반원 호 적분이 0으로 가는 단계이며, 이 호 적분은 정확히 2arctan(1/R) 이라 ML 상한과 수치로 비교한다. 아래 반평면 경로로 교차 검증하고, e^{ix} 가 붙을 때 이 검증이 깨지는 조건(Jordan 보조정리)을 정리한다."
---

NOTE 11-30-01 · 유수 정리를 이용한 실적분 계산
{: .amm-id}

## 1. 일반 사항

### A. 목적

1. 이 노트는 유수 정리(residue theorem)로 다음 실적분을 계산한다.

$$
\int_{-\infty}^{\infty} \frac{dx}{x^2+1} = 2\pi i \cdot \frac{1}{2i} = \pi
$$

2. 이 노트는 증명의 각 단계 중 어느 단계가 실제로 성립 여부를 결정하는지 확인한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
답은 $$\arctan x$$ 로 바로 확인된다. 이 노트의 목적은 답이 아니라 절차의 검증이다. 유수 계산은 한 줄이고, 성립 여부를 결정하는 단계는 큰 반원 호 위의 적분이 0으로 가는 단계다.
</div>

### B. 적용 범위

1. 피적분함수가 유리함수 $$P/Q$$ 이고 $$\deg Q \ge \deg P + 2$$ 인 경우에 적용한다.
2. 실수축 위에 특이점이 없는 경우에 적용한다.
3. $$e^{iax}$$ 인자가 붙는 경우는 4.C 와 4.D 에서 다룬다.

### C. 결과 요약

1. $$\int_{-\infty}^{\infty} dx/(x^2+1) = \pi$$ 이다.
2. 위 반평면 경로와 아래 반평면 경로가 같은 값을 준다.
3. 호 적분의 참값은 $$2\arctan(1/R)$$ 이고, ML 상한 $$\pi R/(R^2-1)$$ 은 큰 $$R$$ 에서 참값의 약 $$\pi/2$$ 배다.
4. $$e^{ix}$$ 가 붙으면 아래 반평면 경로는 오답 $$\pi e$$ 를 준다.

## 2. 준비 정보

### A. 필요한 개념

1. 복소수의 극형식 $$z = Re^{i\theta}$$ 를 다룰 수 있어야 한다.
2. 단순극(simple pole)의 정의를 알아야 한다.

### B. 참조 자료

| 참조 | 제목 |
|---|---|
| 유수 정리 | 닫힌 경로 적분 = $$2\pi i \times$$ (경로 안쪽 유수의 합) |
| ML 부등식 | $$\lvert \int_\gamma f\,dz \rvert \le M L$$, $$M = \max_\gamma \lvert f \rvert$$, $$L$$ = 경로 길이 |
| Jordan 보조정리 | $$\int_0^{\pi} e^{-aR\sin\theta}\,R\,d\theta < \pi/a$$ ($$a > 0$$) |

### C. 사용 프로그램

| 항목 | 용도 |
|---|---|
| Python, mpmath | 경로 적분 수치 확인, 진동 적분(`quadosc`) |
| Python, matplotlib, Pillow | 그림 GIF 두 개 생성(`make_gifs.py`) |

### D. 관련 파일

- [`make_gifs.py`]({{ '/files/blog/residue-theorem-real-integral-semicircle/make_gifs.py' | relative_url }}) — 위 GIF 두 개를 만드는 스크립트 (matplotlib, Pillow)

```bash
python make_gifs.py    # -> images/blog/residue-theorem-real-integral-semicircle/*.gif
```

## 3. 절차

### A. 복소화 및 특이점 확인

1. 실변수 $$x$$ 를 복소변수 $$z$$ 로 바꾼다.

$$
f(z) = \frac{1}{z^2+1} = \frac{1}{(z-i)(z+i)}
$$

2. 분모가 0이 되는 점을 찾는다. $$z = i$$, $$z = -i$$ 두 점이다.
3. $$z = i$$ 근처에서 $$f$$ 를 다음과 같이 나눈다.

$$
f(z) = \frac{1}{z-i} \cdot \frac{1}{z+i}
$$

4. 극의 차수를 판정한다.
   1. 뒤 인수 $$1/(z+i)$$ 는 $$z = i$$ 에서 해석적이고 값은 $$1/(2i) \neq 0$$ 이다.
   2. 앞 인수에 $$(z-i)$$ 가 1제곱으로만 있으므로 $$z = i$$ 는 단순극이다.
   3. 같은 이유로 $$z = -i$$ 도 단순극이다.
5. 실수축 위에 특이점이 없음을 확인한다.

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
실수축 위에 극이 있으면 경로가 극을 지나가므로 이 절차를 쓸 수 없다. 이 경우 주치(principal value) 적분 절차로 바꾼다.
</div>

### B. 경로 설계

1. 닫힌 경로 $$C$$ 를 두 부분으로 구성한다.
   1. 실수축 위의 선분 $$[-R, R]$$.
   2. 위 반평면의 반원 호 $$\Gamma_R$$: $$z = Re^{i\theta}$$, $$0 \le \theta \le \pi$$.
2. 진행 방향을 반시계 방향으로 정한다. $$-R$$ 에서 $$R$$ 까지 실수축을 따라간 뒤 호를 따라 돌아온다.
3. $$R > 1$$ 로 잡는다. 이때 $$z = i$$ 만 경로 안에 있고 $$z = -i$$ 는 바깥에 있다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
선분 위에서 $$z = x$$, $$dz = dx$$ 이므로 선분 적분이 곧 구하려는 적분의 유한 구간 버전이다. 호는 경로를 닫는 보조 부품이며, $$R \to \infty$$ 에서 사라져야 한다. 유수 정리는 경로 안쪽 극만 센다.
</div>

### C. 유수 계산

1. 단순극 $$z = a$$ 의 유수 공식을 적용한다.

$$
\operatorname*{Res}_{z=a} f(z) = \lim_{z \to a} (z-a) f(z)
$$

2. $$a = i$$ 를 대입한다.

$$
\operatorname*{Res}_{z=i} \frac{1}{z^2+1} = \lim_{z \to i} \frac{1}{z+i} = \frac{1}{2i} = -\frac{i}{2}
$$

3. 결과를 $$P(a)/Q'(a)$$ 공식으로 확인한다. $$Q'(z) = 2z$$ 이므로 $$1/(2i)$$ 로 같다.
4. 유수 정리를 적용한다.

$$
\oint_C \frac{dz}{z^2+1} = 2\pi i \cdot \frac{1}{2i} = \pi
$$

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
$$1/(2i) = -i/2$$ 는 분자와 분모에 $$-i$$ 를 곱해 얻는다($$2i \cdot (-i) = 2$$). 경로 적분 값 $$\pi$$ 는 $$R > 1$$ 이면 $$R$$ 과 무관하다. 경로 안에 들어오는 극이 바뀌지 않기 때문이다.
</div>

### D. 경로 분해

1. 닫힌 경로 적분을 선분 적분과 호 적분으로 나눈다.

$$
\pi = \int_{-R}^{R} \frac{dx}{x^2+1} + \int_{\Gamma_R} \frac{dz}{z^2+1}
$$

2. 첫 항이 $$R \to \infty$$ 에서 구하려는 적분이 됨을 확인한다.
3. 남은 작업을 정한다. 호 적분이 0으로 감을 보이면 절차가 끝난다.

### E. 호 적분 소멸 증명

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
이 단계를 생략하면 유수 계산이 맞아도 결과가 틀릴 수 있다. 증명이 틀리는 경우는 대부분 이 단계에서 틀린다. 4.C 의 아래 반평면 경로가 그 예다.
</div>

1. 호 위에서 $$\lvert z \rvert = R$$ 임을 이용해 역삼각부등식을 적용한다.

$$
\lvert z^2 + 1 \rvert \ge \lvert z \rvert^2 - 1 = R^2 - 1 \qquad (R > 1)
$$

2. 호 위의 최댓값을 정한다. $$\lvert f(z) \rvert \le M = 1/(R^2-1)$$ 이다.
3. 호의 길이를 정한다. $$L = \pi R$$ 이다.
4. ML 부등식을 적용한다.

$$
\left\lvert \int_{\Gamma_R} \frac{dz}{z^2+1} \right\rvert \le \frac{\pi R}{R^2-1} \xrightarrow{R \to \infty} 0
$$

5. $$R \to \infty$$ 로 보내 결과를 얻는다.

$$
\int_{-\infty}^{\infty} \frac{dx}{x^2+1} = \pi
$$

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
분모는 $$R^2$$ 으로, 호 길이는 $$R$$ 로 자라므로 상한은 $$1/R$$ 로 줄어든다. 일반 유리함수 $$P/Q$$ 에서 $$\deg Q \ge \deg P + 2$$ 를 요구하는 이유가 이 계산이다. 차수 차이가 1이면 $$M \sim 1/R$$ 과 $$L \sim R$$ 이 상쇄되어 상한이 상수로 남는다.
</div>

## 4. 시험 및 검사

### A. 호 적분 참값과 ML 상한 비교

1. 선분 적분 $$2\arctan R$$ 로부터 호 적분의 참값을 구한다.

$$
\int_{\Gamma_R} \frac{dz}{z^2+1} = \pi - 2\arctan R = 2\arctan\frac{1}{R}
$$

2. $$z = Re^{i\theta}$$ 로 매개화하여 $$\theta$$ 에 대해 mpmath 로 수치 적분한다. 위 식과 20자리까지 일치한다.
3. 참값과 ML 상한을 비교한다.

| $$R$$ | 선분 적분 $$2\arctan R$$ | 호 적분 (참값) $$2\arctan(1/R)$$ | ML 상한 $$\pi R/(R^2-1)$$ |
|---|---|---|---|
| 2 | 2.2143 | 0.9273 | 2.0944 |
| 10 | 2.9423 | 0.1993 | 0.3173 |
| 100 | 3.1216 | 0.0200 | 0.0314 |

4. 판정: 큰 $$R$$ 에서 참값은 $$2/R$$, 상한은 $$\pi/R$$ 로 간다. 상한은 참값의 약 $$\pi/2$$ 배이고 감소 속도는 같다. 증명에는 0으로 간다는 사실만 필요하므로 합격이다.

<figure>
<img src="{{ '/images/blog/residue-theorem-real-integral-semicircle/contour-growing.gif' | relative_url }}" alt="Semicircular contour growing with R: segment integral 2 arctan R approaches pi, arc integral 2 arctan(1/R) decays below the ML bound">
<figcaption>R 을 키워도 경로 적분은 π 로 일정하다. 선분 적분 2arctan R 은 π 로, 호 적분 2arctan(1/R) 은 ML 상한 πR/(R²−1) 아래에서 0 으로 간다.</figcaption>
</figure>

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
$$R = 100$$ 에서도 선분 적분은 $$\pi$$ 보다 0.02 작다. 꼬리가 $$1/x^2$$ 로만 줄어들어 수렴이 느리다.
</div>

### B. 최종값 확인

1. $$\arctan x$$ 의 극한값으로 확인한다. $$-\infty$$ 에서 $$-\pi/2$$, $$+\infty$$ 에서 $$\pi/2$$ 이므로 차이는 $$\pi$$ 다.
2. mpmath 수치 적분으로 확인한다. 결과는 $$3.14159265358979\ldots$$ 로 일치한다.

### C. 아래 반평면 경로로 교차 검증

1. 아래 반평면에 반원을 그려 경로를 닫는다. 이 경로 안에는 $$z = -i$$ 만 있다.
2. 진행 방향이 시계 방향임을 확인한다. $$-R$$ 에서 $$R$$ 로 간 뒤 아래쪽 호로 돌아온다.
3. $$z = -i$$ 의 유수를 계산한다.

$$
\operatorname*{Res}_{z=-i} \frac{1}{z^2+1} = \lim_{z \to -i} \frac{1}{z-i} = \frac{1}{-2i}
$$

4. 시계 방향이므로 유수 정리에 음의 부호를 붙인다.

$$
\oint_{C'} \frac{dz}{z^2+1} = -2\pi i \cdot \frac{1}{-2i} = \pi
$$

5. 아래쪽 호에서도 $$\lvert z^2+1 \rvert \ge R^2 - 1$$ 이 성립함을 확인한다. 호 적분은 0으로 가고 결과는 $$\pi$$ 로 같다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
두 경로가 일치하는 것은 우연이 아니다. 큰 원 전체로 감싸면 원 적분은 두 유수의 합 $$1/(2i) + 1/(-2i) = 0$$ 에 $$2\pi i$$ 를 곱한 값이다. 이는 $$\lvert f \rvert \sim 1/R^2$$ 인 함수의 큰 원 적분이 0으로 간다는 사실과 맞는다. 위쪽 경로 값과 아래쪽 경로 값의 차이가 이 원 적분이므로 둘은 같다.
</div>

### D. 교차 검증이 깨지는 조건: $$e^{ix}$$ 인자

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
$$e^{iaz}$$ ($$a > 0$$) 가 붙으면 반드시 위 반평면으로 닫는다. $$e^{-iaz}$$ 가 붙으면 아래로 닫는다. 반대쪽으로 닫으면 계산은 오류 없이 끝나지만 값이 틀린다. 닫는 방향을 자유롭게 고를 수 있는 것은 $$1/(z^2+1)$$ 처럼 양쪽에서 모두 작아지는 함수뿐이다.
</div>

1. $$\cos x/(x^2+1)$$ 을 구하기 위해 $$e^{iz}/(z^2+1)$$ 을 적분하고 실수부를 취한다.
2. 위 반평면에서 $$z = x + iy$$ 이면 $$\lvert e^{iz} \rvert = e^{-y} \le 1$$ 임을 확인한다. 3.E 의 ML 추정이 그대로 성립한다.
3. 위 반평면 경로로 계산한다. 결과는 수치 적분 값과 일치한다.

$$
\int_{-\infty}^{\infty} \frac{e^{ix}}{x^2+1}\,dx = 2\pi i \cdot \frac{e^{i \cdot i}}{2i} = \frac{\pi}{e} \approx 1.1557
$$

4. 비교를 위해 아래 반평면 경로로 계산한다.
   1. $$y < 0$$ 에서 $$\lvert e^{iz} \rvert = e^{\lvert y \rvert}$$ 는 $$e^R$$ 까지 커진다.
   2. 이 경로의 값은 $$-2\pi i \cdot e/(-2i) = \pi e \approx 8.540$$ 으로 오답이다.
   3. 아래쪽 호 적분은 0이 아니라 $$\pi e - \pi/e = 2\pi\sinh 1 \approx 7.384$$ 로 간다.
   4. $$R = 20$$ 에서 호 적분을 직접 수치 적분하면 7.3797 로, 위 값에 근접한다.

<figure>
<img src="{{ '/images/blog/residue-theorem-real-integral-semicircle/jordan-upper-vs-lower.gif' | relative_url }}" alt="Size of e^(iz) on the upper and lower arcs, and the arc integrals versus R: upper goes to 0, lower to 2 pi sinh 1">
<figcaption>e^(iz) 의 크기는 위쪽 호에서 e^(−R sin θ) 로 줄고 아래쪽 호에서 e^(R sin θ) 로 커진다. 위쪽 호 적분은 0 으로, 아래쪽 호 적분은 2π sinh 1 ≈ 7.384 로 간다.</figcaption>
</figure>

### E. ML 상한이 부족한 경우: Jordan 보조정리

1. 차수 차이가 1인 $$x e^{ix}/(x^2+1)$$ 에 ML 부등식을 적용한다.
   1. 호 위에서 $$\lvert f \rvert \le R/(R^2-1)$$, 호 길이는 $$\pi R$$ 이다.
   2. 상한은 $$\pi R^2/(R^2-1) \to \pi$$ 로 0이 되지 않는다. ML 부등식으로는 증명할 수 없다.
2. Jordan 보조정리(Jordan's lemma)를 적용한다. 위 반원 위에서 다음이 성립한다.

$$
\int_0^{\pi} e^{-aR\sin\theta}\,R\,d\theta < \frac{\pi}{a}
$$

3. 호 길이 $$\pi R$$ 대신 $$\pi/a$$ 를 곱한다. 상한은 $$\pi R/(R^2-1) \to 0$$ 이다.
4. 수치로 확인한다. $$R = 10, 50, 200$$ 에서 실제 호 적분의 크기는 0.173, 0.038, 0.0048 이고, 상한(0.317, 0.063, 0.016) 아래에 있다.
5. $$z = i$$ 의 유수를 계산한다. $$i e^{-1}/(2i) = 1/(2e)$$ 이다.
6. 유수 정리를 적용하고 허수부를 취한다.

$$
\int_{-\infty}^{\infty} \frac{x e^{ix}}{x^2+1}\,dx = 2\pi i \cdot \frac{1}{2e} = \frac{i\pi}{e}
\quad\Longrightarrow\quad
\int_{-\infty}^{\infty} \frac{x\sin x}{x^2+1}\,dx = \frac{\pi}{e}
$$

7. mpmath 진동 적분(`quadosc`)으로 확인한다. 결과는 $$\pi/e$$ 로 일치한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
지수 인자 $$e^{-aR\sin\theta}$$ 는 호의 대부분에서 작고, 실수축 근처의 짧은 구간에서만 1에 가깝다. 그래서 유효 길이가 상수 $$\pi/a$$ 로 줄어든다. 이 적분은 절대수렴하지 않고 조건수렴한다.
</div>

## 5. 종료

### A. 결과 정리

1. 유수 정리로 실적분을 계산하는 절차는 네 단계다.
   1. 특이점을 찾는다(3.A).
   2. 구하려는 실적분이 한 조각이 되도록 닫힌 경로를 고른다(3.B).
   3. 안쪽 극의 유수를 더해 $$2\pi i$$ 를 곱한다(3.C).
   4. 보조 경로가 사라짐을 보인다(3.E).
2. 앞의 세 단계는 기계적이다. 네 번째 단계에서 닫는 방향과, ML 부등식으로 충분한지 Jordan 보조정리가 필요한지를 정한다.

### B. 후속 작업

1. 실수축 위에 극이 있는 경우: 주치 적분과 작은 반원 우회 경로를 다룬다.
