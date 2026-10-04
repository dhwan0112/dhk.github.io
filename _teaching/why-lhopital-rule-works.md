---
subject: Math
order: 5
date: 2026-09-30
title: "로피탈 정리의 증명과 반례"
tags: [Math, Calculus, Limit]
description: "로피탈 정리의 증명은 분자와 분모에 같은 점 c를 쓰는 코시 평균값 정리 한 줄이다. 평균값 정리를 두 번 쓰면 안 되는 이유와, 그 한 줄을 곡선의 할선과 접선으로 기하학적으로 해석하는 법을 다룬다. f'/g'의 극한이 없거나 g'이 0이 되는 반례를 통해 로피탈 정리가 적용되지 않는 조건도 짚는다."
---

NOTE 11-10-02 · 로피탈 정리의 증명과 반례
{: .amm-id}

## 1. 일반 사항

### A. 목적

1. 이 노트는 로피탈 정리(L'Hôpital's rule)의 증명을 제시한다. 정리의 주장은 "분자와 분모를 따로 미분해도 극한이 같다"이다.
2. 증명의 핵심은 다음 한 줄이다. $$f(a) = g(a) = 0$$ 이면 $$a$$ 와 $$x$$ 사이의 어떤 점 $$c$$ 에서 다음이 성립한다.

$$
\frac{f(x)}{g(x)} = \frac{f'(c)}{g'(c)}
$$

3. $$x \to a$$ 이면 $$c$$ 도 $$a$$ 로 끌려간다. 이 등식을 주는 정리가 코시 평균값 정리다.
4. 이 노트는 각 조건이 증명의 어느 단계에서 쓰이는지 확인하고, 조건을 빼면 무엇이 깨지는지 반례로 확인한다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
주요 오개념은 $$f'/g'$$ 의 극한이 없을 때 "원래 극한도 없다"고 결론짓는 것이다. 정리의 방향을 반대로 적용한 오류다. 4.C 에서 반례를 제시한다.
</div>

### B. 적용 범위

1. $$x \to a$$ 의 0/0 꼴에 적용한다(3.D).
2. $$x \to \infty$$ 와 ∞/∞ 꼴에 적용한다(3.F).
3. $$0\cdot\infty$$, $$\infty - \infty$$, $$1^\infty$$, $$0^0$$, $$\infty^0$$ 꼴은 위 두 꼴로 바꾸어 적용한다(3.G).

### C. 결과 요약

1. 로피탈 정리는 "도함수의 비가 수렴하면 원래 비도 같은 값으로 수렴한다"는 한 방향의 주장이다.
2. 근거는 원래 비가 어떤 점에서의 도함수 비와 정확히 같다는 코시 평균값 정리다.
3. 평균값 정리를 분자와 분모에 따로 쓰면 서로 다른 두 점이 생겨 증명이 막힌다.
4. 조건마다 증명에서 맡은 역할이 있고, 그 조건을 빼면 반례가 생긴다.

## 2. 준비 정보

### A. 필요한 개념

1. 극한의 ε-δ 정의를 알아야 한다(NOTE 11-10-01).
2. 매개변수 곡선의 기울기 $$dy/dx$$ 를 계산할 수 있어야 한다.

### B. 참조 자료

| 참조 | 제목 |
|---|---|
| 롤의 정리(Rolle's theorem) | $$h(a) = h(b)$$ 이면 $$h'(c) = 0$$ 인 $$c \in (a, b)$$ 가 있다 |
| 평균값 정리(mean value theorem) | $$f(b) - f(a) = f'(c)(b - a)$$ 인 $$c \in (a, b)$$ 가 있다 |
| 코시 평균값 정리(Cauchy's mean value theorem) | 3.C 참조 |

### C. 사용 프로그램

| 항목 | 용도 |
|---|---|
| Python, matplotlib, Pillow | 그림 GIF 두 개 생성(`make_gifs.py`) |

### D. 관련 파일

- [`make_gifs.py`]({{ '/files/blog/why-lhopital-rule-works/make_gifs.py' | relative_url }}) — 위 GIF 두 개를 만드는 스크립트 (matplotlib, Pillow)

```bash
python make_gifs.py    # -> images/blog/why-lhopital-rule-works/*.gif
```

## 3. 절차

### A. 단순한 경우와 그 한계

1. 교과서의 일반적인 설명을 확인한다. $$f(a) = g(a) = 0$$ 이고 $$f', g'$$ 이 $$a$$ 에서 연속이며 $$g'(a) \neq 0$$ 이면 다음이 성립한다.

$$
\frac{f(x)}{g(x)} = \frac{\dfrac{f(x) - f(a)}{x - a}}{\dfrac{g(x) - g(a)}{x - a}} \;\longrightarrow\; \frac{f'(a)}{g'(a)}
$$

2. 이 설명의 한계를 확인한다.
   1. $$\lim_{x\to 0} (1 - \cos x)/x^2$$ 에 한 번 적용하면 $$\sin x/(2x)$$ 가 된다.
   2. 분모의 도함수 $$2x$$ 는 $$x = 0$$ 에서 0이다.
   3. 로피탈 정리를 두 번 이상 쓰는 모든 문제가 이 경우에 해당한다.
3. 필요한 정리의 형태를 정한다. $$f'(a)$$, $$g'(a)$$ 의 값이 아니라 $$f'/g'$$ 의 극한만 가정하는 정리가 필요하다.

### B. 평균값 정리를 두 번 쓰면 안 되는 이유

1. 평균값 정리를 분자와 분모에 따로 적용한다. $$f(x) = f'(c_1)(x - a)$$, $$g(x) = g'(c_2)(x - a)$$ 이다.

$$
\frac{f(x)}{g(x)} = \frac{f'(c_1)}{g'(c_2)}
$$

2. 이 단계에서 증명이 막힘을 확인한다.
   1. $$c_1$$ 과 $$c_2$$ 는 일반적으로 다른 점이다.
   2. 가정은 같은 점에서의 비 $$f'(t)/g'(t)$$ 에 대한 것이다.
   3. 서로 다른 점에서 잰 분자와 분모의 비는 가정과 연결되지 않는다.
3. 두 함수에 같은 $$c$$ 를 쓰는 평균값 정리가 필요하다.

### C. 코시 평균값 정리 증명

1. 정리를 진술한다. $$f, g$$ 가 $$[a, b]$$ 에서 연속, $$(a, b)$$ 에서 미분가능하고 $$(a, b)$$ 에서 $$g' \neq 0$$ 이면 다음을 만족하는 $$c \in (a, b)$$ 가 있다.

$$
\frac{f(b) - f(a)}{g(b) - g(a)} = \frac{f'(c)}{g'(c)}
$$

2. 분모가 없는 보조함수를 정의한다.

$$
h(t) = \big[f(t) - f(a)\big]\big[g(b) - g(a)\big] - \big[g(t) - g(a)\big]\big[f(b) - f(a)\big]
$$

3. $$h(a) = 0$$ 임을 확인한다.
4. $$h(b)$$ 도 두 항이 같아 0임을 확인한다.
5. 롤의 정리로 $$h'(c) = 0$$ 인 $$c$$ 를 얻는다.
6. $$h'(c) = 0$$ 을 풀어 쓴다. $$f'(c)\,[g(b) - g(a)] = g'(c)\,[f(b) - f(a)]$$ 이다.
7. 양변을 나눌 수 있는지 확인한다.
   1. $$g'(c) \neq 0$$ 은 가정이다.
   2. $$g(b) = g(a)$$ 라면 롤의 정리로 $$g'$$ 이 $$(a, b)$$ 어딘가에서 0이 되어 가정에 어긋난다. 따라서 $$g(b) \neq g(a)$$ 이다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
$$g' \neq 0$$ 조건은 이 단계에서 처음 쓰인다.
</div>

### D. 0/0 꼴 증명

1. 가정을 정한다.
   1. $$a$$ 를 뺀 근방에서 $$f, g$$ 가 미분가능하고 $$g' \neq 0$$ 이다.
   2. $$\lim_{x\to a} f = \lim_{x\to a} g = 0$$ 이다.
   3. $$\lim_{x\to a} f'(x)/g'(x) = L$$ 이다.
2. $$f(a) = g(a) = 0$$ 으로 정의한다. 두 함수가 $$a$$ 에서 연속이 된다.
3. $$x > a$$ 라 한다. $$x < a$$ 도 같은 방법으로 처리한다.
4. $$[a, x]$$ 에서 평균값 정리를 쓴다. $$g(x) = g'(\xi)(x - a) \neq 0$$ 이므로 $$f/g$$ 가 정의된다.
5. 코시 평균값 정리를 적용한다.

$$
\frac{f(x)}{g(x)} = \frac{f(x) - f(a)}{g(x) - g(a)} = \frac{f'(c_x)}{g'(c_x)}, \qquad a < c_x < x
$$

6. $$\varepsilon > 0$$ 을 잡는다. $$0 < \lvert t - a\rvert < \delta$$ 일 때 $$\lvert f'(t)/g'(t) - L\rvert < \varepsilon$$ 인 $$\delta$$ 가 있다.
7. $$0 < \lvert x - a\rvert < \delta$$ 이면 $$0 < \lvert c_x - a\rvert < \lvert x - a\rvert < \delta$$ 이다.
8. 결론을 얻는다.

$$
\left\lvert \frac{f(x)}{g(x)} - L \right\rvert = \left\lvert \frac{f'(c_x)}{g'(c_x)} - L \right\rvert < \varepsilon
$$

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
$$c_x$$ 가 $$a$$ 와 $$x$$ 사이에 엄격하게 있다는 점이 중요하다. $$c_x = a$$ 일 수 있다면 $$a$$ 에서의 $$f'/g'$$ 값이 필요하지만, 그 값은 가정에 없다. $$L = \pm\infty$$ 여도 부등식만 바꾸면 같은 증명이 성립한다.
</div>

9. 조건이 쓰인 위치를 대조한다.

| 조건 | 증명에서 쓰인 곳 |
|---|---|
| $$f, g \to 0$$ | $$a$$에서 0으로 정의해 연속으로 만든다 |
| $$a$$ 근방 미분가능 | $$[a, x]$$에서 코시 평균값 정리 |
| $$g' \neq 0$$ | $$g(x) \neq 0$$, 그리고 $$g'(c_x)$$로 나누기 |
| $$\lim f'/g'$$ 존재 | $$c_x$$에서의 값을 $$L$$ 근처로 묶기 |

### E. 매개변수 곡선의 할선과 접선으로 해석

1. $$x$$ 를 매개변수로 보고 평면 위의 점 $$(g(x), f(x))$$ 로 곡선을 만든다.
2. $$x \to a$$ 이면 이 점은 원점으로 간다.
3. 각 비의 기하적 의미를 정한다.
   1. $$f(x)/g(x)$$ 는 원점과 곡선 위의 점을 잇는 할선의 기울기다.
   2. $$f'(x)/g'(x)$$ 는 그 점에서 곡선의 접선 기울기다. 매개변수 곡선의 기울기가 $$dy/dx = f'/g'$$ 이기 때문이다.
4. 코시 평균값 정리를 매개변수 곡선의 평균값 정리로 해석한다. 원점에서 어떤 점까지 그은 할선과 평행한 접선이 그 사이 어딘가에 있다.
5. 원점 근처에서 접선 기울기가 모두 $$L$$ 가까이 모이면, 할선 기울기도 그중 하나이므로 $$L$$ 가까이에 있다.
6. $$g' \neq 0$$ 의 기하적 의미를 정한다.
   1. $$g'$$ 은 곡선의 가로 방향 속도다.
   2. $$g' \neq 0$$ 이면 곡선은 가로 방향으로 되돌아가지 않고 한쪽으로만 움직인다.
   3. $$g'$$ 이 부호를 바꾸면 곡선이 좌우로 오가며 할선과 접선의 관계가 흐트러질 수 있다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
4.D 의 $$g' \neq 0$$ 누락 반례가 정확히 6단계의 마지막 경우에 해당한다. 구체적 예시는 4.A 에서 확인한다.
</div>

### F. x → ∞ 와 ∞/∞ 꼴

1. $$x \to \infty$$ 를 $$t = 1/x$$ 로 치환한다. $$t \to 0^+$$ 가 된다.
2. $$F(t) = f(1/t)$$, $$G(t) = g(1/t)$$ 로 둔다.
3. 연쇄법칙에서 $$-1/t^2$$ 이 분자·분모에 똑같이 붙어 약분된다. 따라서 $$F'(t)/G'(t) = f'(1/t)/g'(1/t)$$ 이다.
4. 3.D 의 증명을 그대로 적용한다.
5. ∞/∞ 꼴의 가정을 정한다. ∞/∞ 꼴은 $$a$$ 에서 0으로 정의하는 방법을 쓸 수 없으므로 증명이 다르다.
   1. $$a$$ 의 오른쪽 근방에서 $$f, g$$ 가 미분가능하고 $$g' \neq 0$$ 이다.
   2. $$x \to a^+$$ 일 때 $$\lvert g\rvert \to \infty$$ 이다.
   3. $$f'/g' \to L$$ (유한) 이다.
6. $$\varepsilon$$ 에 대해 $$a < t < a + \delta$$ 에서 $$\lvert f'(t)/g'(t) - L\rvert < \varepsilon$$ 이 되게 $$\delta$$ 를 잡는다.
7. $$y$$ 를 $$(a, a+\delta)$$ 안에 고정한다.
8. $$a < x < y$$ 에서 $$[x, y]$$ 에 코시 평균값 정리를 쓰고 $$g(x)$$ 로 나누어 정리한다.

$$
\frac{f(x)}{g(x)} = \frac{f(y)}{g(x)} + \frac{f'(c)}{g'(c)}\left(1 - \frac{g(y)}{g(x)}\right), \qquad x < c < y
$$

9. 각 항의 극한을 확인한다.
   1. $$y$$ 는 고정이고 $$\lvert g(x)\rvert \to \infty$$ 이므로 첫 항은 0으로 간다.
   2. 괄호는 1로 간다.
   3. $$f'(c)/g'(c)$$ 는 항상 $$(L - \varepsilon, L + \varepsilon)$$ 안에 있다.
10. $$x$$ 가 $$a$$ 에 충분히 가까우면 $$f(x)/g(x)$$ 는 $$L$$ 에서 $$\varepsilon$$ 의 몇 배 이내에 있다. $$\varepsilon$$ 은 임의로 작게 잡을 수 있다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
이 증명에는 $$f \to \infty$$ 가 한 번도 쓰이지 않는다. 필요한 것은 분모의 발산뿐이다.
</div>

### G. 다른 부정형의 변환

<div class="amm-caution" markdown="1">
<span class="amm-label">주의</span>
$$0\cdot\infty$$ 꼴에서는 어느 쪽을 분모로 내리는지에 따라 계산량이 달라진다. 잘못 고르면 도함수의 비가 원래보다 복잡해진다.
</div>

1. $$0\cdot\infty$$ 는 한쪽을 분모로 내린다.
   1. $$x \ln x = \dfrac{\ln x}{1/x}$$ 로 쓰면 도함수의 비가 $$\dfrac{1/x}{-1/x^2} = -x \to 0$$ 으로 바로 끝난다.
   2. $$\dfrac{x}{1/\ln x}$$ 로 쓰면 도함수의 비가 $$-x(\ln x)^2$$ 이 되어 원래보다 복잡해진다.
2. $$\infty - \infty$$ 는 통분한다. $$\dfrac{1}{\sin x} - \dfrac{1}{x} = \dfrac{x - \sin x}{x \sin x}$$ 에 두 번 적용하면 $$\dfrac{\sin x}{2\cos x - x\sin x} \to 0$$ 이다.
3. $$1^\infty$$, $$0^0$$, $$\infty^0$$ 은 로그를 취해 $$0\cdot\infty$$ 로 만든다.
   1. $$\ln (1+x)^{1/x} = \ln(1+x)/x \to 1$$ 이므로 $$(1+x)^{1/x} \to e$$ 이다.
   2. $$\ln x^x = x\ln x \to 0$$ 이므로 $$x^x \to 1$$ 이다.

## 4. 시험 및 검사

### A. 할선과 접선의 기하적 해석 확인

1. $$g(x) = x^2$$, $$f(x) = x^3$$ 으로 둔다. 곡선은 $$(x^2, x^3)$$ 이다.
2. 할선 기울기는 $$x$$, 접선 기울기는 $$3x/2$$ 이다.
3. $$x = 1$$ 에서 할선 기울기는 1, 접선 기울기는 1.5로 다르다.
4. 할선과 평행한 접선을 찾는다. $$3c/2 = 1$$ 에서 $$c = 2/3$$ 이고, 이 값은 $$(0, 1)$$ 안에 있다.
5. 판정: 두 기울기 모두 $$x \to 0$$ 에서 0으로 간다. 3.E 의 해석과 일치한다.

<figure>
<img src="{{ '/images/blog/why-lhopital-rule-works/secant-tangent.gif' | relative_url }}" alt="Curve (x^2, x^3): the secant from the origin (slope x) and the parallel tangent at c = 2x/3 both flatten as x goes to 0">
<figcaption>곡선 (x², x³) 위의 점이 원점으로 갈 때 할선 기울기 x 와 접선 기울기 3x/2 가 함께 0 으로 간다. 할선과 평행한 접선의 접점은 c = 2x/3 이다.</figcaption>
</figure>

### B. 부정형이 아닌 경우

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
부정형이 아닌 극한에 로피탈 정리를 쓰면 틀린 값이 나온다.
</div>

1. $$\lim_{x\to 0} \dfrac{\cos x}{1 + x}$$ 는 대입하면 1이다.
2. 로피탈 정리를 쓰면 $$\dfrac{-\sin x}{1} \to 0$$ 이 나온다.
3. 판정: 3.D 의 첫 단계 "$$a$$ 에서 0으로 정의해 연속으로 만든다"가 성립하지 않는 경우다.

### C. f'/g' 의 극한이 없는 경우

1. $$f'/g'$$ 의 극한이 없으면 정리는 아무것도 주장하지 않는다. 원래 극한이 없다는 뜻이 아니다. 가장 흔한 오개념이다.
2. ∞/∞ 꼴의 예를 확인한다.

$$
\lim_{x\to\infty} \frac{x + \sin x}{x} = \lim_{x\to\infty}\left(1 + \frac{\sin x}{x}\right) = 1
$$

3. 도함수의 비를 계산한다. $$1 + \cos x$$ 로 0과 2 사이를 오가며 수렴하지 않는다.
4. 나머지 조건을 확인한다. ∞/∞ 꼴이고 $$g' = 1 \neq 0$$ 이므로 다른 조건은 모두 만족한다.
5. 0/0 꼴의 예를 확인한다. $$f(x) = x^2 \sin(1/x)$$, $$g(x) = \sin x$$ 로 둔다.

$$
\frac{f(x)}{g(x)} = x\sin\frac{1}{x}\cdot\frac{x}{\sin x} \;\longrightarrow\; 0
$$

6. 위 극한이 0인 이유를 확인한다. $$\lvert x\sin(1/x)\rvert \le \lvert x\rvert$$ 이다.
7. 도함수의 비를 계산한다. $$f'(x) = 2x\sin(1/x) - \cos(1/x)$$ 이므로 $$f'/g'$$ 은 $$x \to 0$$ 에서 대략 $$-1$$ 과 $$1$$ 사이를 진동한다.
8. 판정: 곡선으로 보면 할선은 수렴하지만 접선이 원점 근처에서 계속 흔들리는 경우다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
코시 평균값 정리가 보장하는 것은 "할선 기울기가 어떤 접선 기울기와 같다"는 사실뿐이다. 따라서 접선들이 흔들려도 할선은 수렴할 수 있다.
</div>

### D. g' ≠ 0 을 빠뜨린 경우

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
$$g' \neq 0$$ 조건을 빠뜨리면 $$f'/g'$$ 이 수렴해도 원래 비가 수렴하지 않을 수 있다. 계산은 오류 없이 끝나지만 결론이 거짓이다.
</div>

1. $$x \to \infty$$ 에서 다음 두 함수를 정의한다.

$$
f(x) = x + \sin x\cos x, \qquad g(x) = e^{\sin x} f(x)
$$

2. 둘 다 무한대로 감을 확인한다. $$f \ge x - \tfrac12$$, $$g \ge e^{-1}(x - \tfrac12)$$ 이다.
3. 미분한다. $$f'(x) = 2\cos^2 x$$, $$g'(x) = e^{\sin x}\cos x\,(x + \sin x\cos x + 2\cos x)$$ 이다.
4. 공통인수 $$\cos x$$ 를 약분한다.

$$
\frac{f'(x)}{g'(x)} = \frac{2\cos x}{e^{\sin x}\,(x + \sin x\cos x + 2\cos x)} \;\longrightarrow\; 0
$$

5. 위 극한이 0인 이유를 확인한다. 분자는 유계이고 분모는 $$e^{-1}(x - \tfrac52)$$ 보다 크다.
6. 원래 비를 계산한다. $$f(x)/g(x) = e^{-\sin x}$$ 는 $$1/e$$ 와 $$e$$ 사이를 오가며 수렴하지 않는다.
7. 판정: $$g'$$ 이 $$x = \pi/2 + k\pi$$ 마다 0이 된다.
   1. 아무리 큰 $$x$$ 이후를 잡아도 $$g' \neq 0$$ 인 구간이 없다. 약분한 $$\cos x$$ 가 바로 그 0이다.
   2. 코시 평균값 정리가 주는 점 $$c$$ 가 $$\cos c = 0$$ 인 점일 수 있다.
   3. 그 점에서는 $$f'(c) = g'(c) = 0$$ 이므로 등식 $$f'(c)[g(b) - g(a)] = g'(c)[f(b) - f(a)]$$ 가 $$0 = 0$$ 이 된다. 할선 기울기에 대해 아무 정보도 주지 않는다.
   4. 곡선 그림으로는 $$g$$ 가 증가와 감소를 반복하며 곡선이 가로로 앞뒤를 오가는 상황이다.

<figure>
<img src="{{ '/images/blog/why-lhopital-rule-works/gprime-zero-counterexample.gif' | relative_url }}" alt="f'/g' tends to 0 while f/g = e^(-sin x) keeps oscillating between 1/e and e; vertical lines mark zeros of g'">
<figcaption>f′/g′ 은 0 으로 수렴하지만 f/g = e^(−sin x) 는 1/e 와 e 사이를 계속 오간다. 세로선은 g′ = 0 인 x = π/2 + kπ 다.</figcaption>
</figure>

### E. 순환논법

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
$$\lim_{x\to 0}\sin x/x = 1$$ 을 로피탈 정리로 증명하면 순환논법이 된다.
</div>

1. 로피탈 정리를 적용하면 $$\cos 0 = 1$$ 을 쓰게 된다.
2. $$\sin$$ 의 도함수가 $$\cos$$ 라는 사실 자체가 이 극한에서 나온다.
3. 판정: 계산 도구로는 쓸 수 있지만 이 극한의 증명이 될 수는 없다.

## 5. 종료

### A. 결과 정리

1. 로피탈 정리는 "도함수의 비가 수렴하면 원래 비도 같은 값으로 수렴한다"는 한 방향의 주장이다.
2. 근거는 원래 비가 어떤 점에서의 도함수 비와 정확히 같다는 코시 평균값 정리다(3.C, 3.D).
3. 조건과 증명 단계의 대응은 3.D 의 표로 확인한다.
4. 각 조건을 빼면 4.B 에서 4.D 까지의 반례가 생긴다.
