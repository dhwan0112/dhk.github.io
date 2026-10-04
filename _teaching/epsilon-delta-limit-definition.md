---
note: "11-10-01"
subject: Math
order: 4
date: 2026-09-30
title: "극한의 ε-δ 정의"
tags: [Math, Calculus, Limit]
description: "극한의 ε-δ 정의를 전칭 기호(∀)와 존재 기호(∃)가 번갈아 나오는 논리 구조로 해설한다. 일차·이차·유리함수에서 δ를 구성하는 절차를 다루고, δ = min(1, ε/7)처럼 구간을 먼저 제한해야 하는 이유를 반례로 보인다. 극한의 부정 명제로 극한이 존재하지 않음을 증명하는 방법과 자주 발생하는 논리적 오류도 짚는다."
---

NOTE 11-10-01 · 극한의 ε-δ 정의
{: .amm-id}

## 1. 일반 사항

### A. 목적

1. 이 노트는 극한의 ε-δ 정의를 양화사 $$\forall$$, $$\exists$$ 가 교대하는 논리 구조로 해설한다.
2. 이 노트는 일차·이차·유리함수에서 $$\delta$$ 를 구성하는 절차를 제시한다.
3. 이 노트는 정의의 부정 명제로 극한이 존재하지 않음을 증명하는 절차를 제시한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
ε-δ 정의의 핵심 난점은 기호가 아니라 "어느 쪽이 먼저 무엇을 고르는가"라는 양화사 순서다. 이 노트는 정의를 두 참가자의 게임으로 해석한다. 상대가 허용 오차 $$\varepsilon$$ 을 제시하면, 증명하는 쪽은 그 $$\varepsilon$$ 을 보고 $$\delta$$ 를 제시한다. 어떤 $$\varepsilon$$ 에도 성립하는 $$\delta$$ 공식이 있으면 극한이 증명된다. 이 틀에서 $$\delta = \min(1, \varepsilon/7)$$ 같은 선택과 극한의 비존재 증명이 같은 구조의 연장으로 설명된다.
</div>

### B. 적용 범위

1. 실변수 함수의 한 점 $$x \to a$$ 에서의 유한 극한 $$L$$ 에 적용한다.
2. 일차함수, 이차함수, 유리함수의 $$\delta$$ 구성을 다룬다.
3. 극한의 비존재 증명은 $$\lvert x \rvert / x$$ 와 $$\sin(1/x)$$ 의 $$x \to 0$$ 를 다룬다.

### C. 결과 요약

1. 일차함수 $$mx + b$$ ($$m \neq 0$$) 에서는 $$\delta = \varepsilon/\lvert m \rvert$$ 이다.
2. $$\lim_{x \to 3} x^2 = 9$$ 에서는 $$\delta = \min(1, \varepsilon/7)$$ 이다. min 이 없으면 $$\varepsilon = 10$$ 에서 반례가 생긴다.
3. $$\lim_{x \to 2} (x+1)/(x-1) = 3$$ 에서는 $$\delta = \min(1/2, \varepsilon/4)$$ 이다. 제한 반지름은 분모의 영점까지 거리보다 작아야 한다.
4. 극한의 부정은 $$\exists \varepsilon,\ \forall \delta,\ \exists x$$ 꼴이며, "이면"이 "이면서"로 바뀐다.

## 2. 준비 정보

### A. 필요한 개념

1. 절댓값 부등식과 삼각부등식을 다룰 수 있어야 한다.
2. 전칭 기호($$\forall$$)와 존재 기호($$\exists$$)의 의미를 알아야 한다.

### C. 사용 프로그램

| 항목 | 용도 |
|---|---|
| Python, matplotlib, Pillow | 그림 GIF 두 개 생성(`make_gifs.py`) |

### D. 관련 파일

- [`make_gifs.py`]({{ '/files/blog/epsilon-delta-limit-definition/make_gifs.py' | relative_url }}) — 위 GIF 두 개를 만드는 스크립트 (matplotlib, Pillow)

```bash
python make_gifs.py    # -> images/blog/epsilon-delta-limit-definition/*.gif
```

## 3. 절차

### A. 정의의 양화사 구조

1. 극한의 정의를 다음과 같이 쓴다.

$$
\lim_{x \to a} f(x) = L
\iff
\forall \varepsilon > 0,\ \exists \delta > 0 :\ 0 < \lvert x - a \rvert < \delta \implies \lvert f(x) - L \rvert < \varepsilon
$$

2. 양화사 순서대로 게임 규칙으로 해석한다.
   1. 상대(의심하는 쪽)가 먼저 양수 $$\varepsilon$$ 을 고른다. "$$f(x)$$ 를 $$L$$ 에서 이만큼 안쪽으로 붙들어 둘 수 있는가"라는 도전이다.
   2. 증명하는 쪽이 양수 $$\delta$$ 를 고른다.
   3. $$a$$ 에서 $$\delta$$ 이내($$a$$ 자체는 제외)의 모든 $$x$$ 에 대해 $$\lvert f(x) - L \rvert < \varepsilon$$ 이면 증명하는 쪽이 이긴다.
   4. 극한이 $$L$$ 이라는 명제는 상대가 어떤 $$\varepsilon$$ 을 골라도 이기는 전략이 존재한다는 뜻이다.
3. $$\lim_{x \to 3}(2x+1) = 7$$ 에 적용한다.
   1. $$\lvert (2x+1) - 7 \rvert = 2\lvert x - 3 \rvert$$ 이다.
   2. $$\varepsilon = 0.1$$ 이면 $$\lvert x - 3 \rvert < 0.05$$ 이면 되므로 $$\delta = 0.05$$ 로 답한다.
   3. $$\varepsilon = 0.001$$ 이면 $$\delta = 0.0005$$ 로 답한다.
4. 개별 계산 대신 공식 $$\delta = \varepsilon/2$$ 를 제시한다. 이 공식 하나로 모든 $$\varepsilon$$ 에 대해 이긴다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
증명은 $$\delta$$ 공식을 제시하고, 그 공식이 항상 이긴다는 것을 보이는 일이다.
</div>

5. 게임 구조에서 두 성질을 확인한다.
   1. $$\delta$$ 는 $$\varepsilon$$ 을 본 뒤에 고르므로 $$\varepsilon$$ 에 의존해도 된다.
   2. $$x$$ 는 $$\delta$$ 를 정한 뒤 상대가 구간 안에서 임의로 고른다. 따라서 $$\delta$$ 는 $$x$$ 에 의존하면 안 된다.
   3. 이기는 $$\delta$$ 보다 작은 $$\delta$$ 도 역시 이긴다. 구간을 좁히면 상대가 고를 수 있는 $$x$$ 가 줄어들 뿐이다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
3.D 와 3.E 의 min 구성은 모두 마지막 성질, 즉 더 작은 $$\delta$$ 도 이긴다는 성질에 근거한다.
</div>

### B. δ 구성의 두 단계

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
예비 계산 순서를 그대로 답안에 옮기면 결론에서 출발해 가정을 끌어내는 글이 된다. 이 글은 증명이 아니다.
</div>

1. 예비 계산에서 $$\lvert f(x) - L \rvert$$ 를 $$\lvert x - a \rvert$$ 에 대한 식으로 바꾼다.
2. 이 식이 $$\varepsilon$$ 보다 작아지려면 $$\lvert x - a \rvert$$ 가 얼마나 작아야 하는지 거꾸로 푼다. 여기서 $$\delta$$ 가 나온다.
3. 답안은 순서를 뒤집어 앞에서부터 쓴다. "임의의 $$\varepsilon > 0$$ 이 주어졌다. $$\delta = \cdots$$ 로 둔다. $$0 < \lvert x - a \rvert < \delta$$ 라 하면 ... $$< \varepsilon$$."

### C. 일차함수

1. 대상 극한을 정한다. $$\lim_{x \to 2}(3x + 1) = 7$$ 이다.
2. 오차를 $$\lvert x - 2 \rvert$$ 로 나타낸다.

$$
\lvert (3x+1) - 7 \rvert = \lvert 3x - 6 \rvert = 3\lvert x - 2 \rvert
$$

3. 이 값이 $$\varepsilon$$ 보다 작으려면 $$\lvert x - 2 \rvert < \varepsilon/3$$ 이면 된다.
4. $$\delta = \varepsilon/3$$ 로 둔다. $$0 < \lvert x - 2 \rvert < \delta$$ 이면 $$3\lvert x - 2 \rvert < 3 \cdot \varepsilon/3 = \varepsilon$$ 이다.
5. 일반화한다. $$mx + b$$ ($$m \neq 0$$) 이면 $$\delta = \varepsilon/\lvert m \rvert$$ 이다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
기울기가 가파를수록 $$x$$ 를 더 좁게 묶어야 한다는 기하적 해석과 일치한다.
</div>

### D. 이차함수와 min(1, ε/7)

1. 대상 극한을 정한다. $$\lim_{x \to 3} x^2 = 9$$ 이다.
2. 오차를 인수분해한다.

$$
\lvert x^2 - 9 \rvert = \lvert x - 3 \rvert \cdot \lvert x + 3 \rvert
$$

3. 두 인수의 성격을 구분한다. $$\lvert x - 3 \rvert$$ 는 $$\delta$$ 로 조절되지만 $$\lvert x + 3 \rvert$$ 는 $$x$$ 에 따라 변한다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
$$\delta = \varepsilon/\lvert x + 3 \rvert$$ 는 답이 아니다. $$\delta$$ 에 $$x$$ 가 들어가면 3.A 의 양화사 순서를 위반한다. $$\lvert x + 3 \rvert$$ 를 $$x$$ 와 무관한 상수로 위에서 눌러야 한다.
</div>

4. $$x$$ 를 3 근처로 먼저 제한한다. $$\lvert x - 3 \rvert < 1$$ 이면 $$2 < x < 4$$ 이다.
5. 이 범위에서 $$5 < x + 3 < 7$$ 이므로 $$\lvert x + 3 \rvert < 7$$ 이다.
6. 제한된 범위에서 다음 부등식을 얻는다.

$$
\lvert x^2 - 9 \rvert < 7\lvert x - 3 \rvert
$$

7. $$\lvert x - 3 \rvert < \varepsilon/7$$ 이면 충분함을 확인한다.
8. 두 조건 $$\lvert x - 3 \rvert < 1$$ 과 $$\lvert x - 3 \rvert < \varepsilon/7$$ 을 동시에 만족하도록 작은 쪽을 고른다.

$$
\delta = \min\left(1, \frac{\varepsilon}{7}\right)
$$

9. 증명을 완성한다.
   1. $$0 < \lvert x - 3 \rvert < \delta$$ 라 한다.
   2. $$\delta \le 1$$ 에서 $$\lvert x + 3 \rvert < 7$$ 이다.
   3. $$\delta \le \varepsilon/7$$ 에서 $$\lvert x - 3 \rvert < \varepsilon/7$$ 이다.
   4. 둘을 곱하면 $$\lvert x^2 - 9 \rvert < \varepsilon$$ 이다.

<figure>
<img src="{{ '/images/blog/epsilon-delta-limit-definition/epsilon-delta-game.gif' | relative_url }}" alt="epsilon-delta game for x^2 at 3: epsilon shrinks from 6 to 0.6 and delta = min(1, epsilon/7) keeps the graph inside the band">
<figcaption>lim x→3 x² = 9 에서 ε 을 6, 3, 1.5, 0.6 으로 줄일 때마다 δ = min(1, ε/7) 로 답한다. δ 구간(세로 띠) 안의 그래프가 ε 띠(가로 띠) 안에 머문다.</figcaption>
</figure>

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
min 이 필요한 이유는 4.A 의 반례로 확인한다. 제한 반지름 1에는 특별한 의미가 없다. $$\lvert x - 3 \rvert < 1/2$$ 로 묶으면 $$x + 3 < 6.5$$ 이고 $$\delta = \min(1/2,\ 2\varepsilon/13)$$ 이 된다. 이것도 맞는 답이다. 1은 계산이 편해서 고르는 값이며 정답이 하나로 정해져 있지 않다. 3.E 처럼 1을 고르면 안 되는 경우도 있다.
</div>

### E. 유리함수: 분모를 아래에서 제한

1. 대상 극한을 정한다. $$\lim_{x \to 2} \frac{x+1}{x-1} = 3$$ 이다.
2. 오차를 정리한다.

$$
\left\lvert \frac{x+1}{x-1} - 3 \right\rvert = \left\lvert \frac{x + 1 - 3x + 3}{x-1} \right\rvert = \frac{2\lvert x - 2 \rvert}{\lvert x - 1 \rvert}
$$

3. 분모 $$\lvert x - 1 \rvert$$ 를 아래에서 누른다. 분모가 작아지면 전체가 커지기 때문이다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
관성적으로 $$\lvert x - 2 \rvert < 1$$ 로 묶으면 $$1 < x < 3$$ 이다. 이 구간은 $$x = 1$$ 에 한없이 가까운 점을 포함하므로 $$\lvert x - 1 \rvert$$ 의 아래 경계가 생기지 않는다. 특이점 $$x = 1$$ 까지의 거리가 1이므로 그보다 좁게 묶어야 한다.
</div>

4. $$\lvert x - 2 \rvert < 1/2$$ 로 제한한다. 이때 $$3/2 < x < 5/2$$ 이고 $$\lvert x - 1 \rvert > 1/2$$ 이다.
5. 제한된 범위에서 다음 부등식을 얻는다.

$$
\frac{2\lvert x - 2 \rvert}{\lvert x - 1 \rvert} < 4\lvert x - 2 \rvert
$$

6. $$\delta = \min(1/2,\ \varepsilon/4)$$ 로 둔다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
제한 반지름의 기준은 "그 안에 함수가 정의되지 않는 점이 들어오지 않을 만큼"이다. 다항식은 그런 점이 없으므로 임의의 반지름을 쓸 수 있다. 유리함수는 분모의 영점까지 거리보다 작아야 한다.
</div>

### F. 극한이 존재하지 않음의 증명

1. 정의를 부정한다. $$\forall$$ 와 $$\exists$$ 가 서로 바뀌고, "이면"은 "이면서"가 된다.

$$
\lim_{x \to a} f(x) \neq L
\iff
\exists \varepsilon > 0,\ \forall \delta > 0,\ \exists x :\ 0 < \lvert x - a \rvert < \delta \ \text{and}\ \lvert f(x) - L \rvert \ge \varepsilon
$$

2. 게임의 역할을 바꾸어 해석한다.
   1. 이번에는 증명하는 쪽이 의심하는 쪽이다. 먼저 $$\varepsilon$$ 하나를 고른다.
   2. 상대가 어떤 $$\delta$$ 를 내놓든, 그 구간 안에서 $$\varepsilon$$ 밖으로 벗어나는 $$x$$ 를 하나 찾는다.
   3. 극한이 존재하지 않는다는 명제는 모든 실수 $$L$$ 에 대해 이것이 가능하다는 뜻이다.
3. $$f(x) = \lvert x \rvert / x$$, $$a = 0$$ 에 적용한다. $$x > 0$$ 이면 1, $$x < 0$$ 이면 $$-1$$ 이다.
   1. 임의의 $$L$$ 에 대해 $$\varepsilon = 1$$ 을 고른다.
   2. 임의의 $$\delta$$ 에 대해 $$x = \delta/2$$ 와 $$x = -\delta/2$$ 는 둘 다 $$0 < \lvert x \rvert < \delta$$ 를 만족한다.
   3. 두 점의 함숫값은 1과 $$-1$$ 이다.
4. 삼각부등식을 적용한다.

$$
\lvert 1 - L \rvert + \lvert -1 - L \rvert \ge \lvert (1 - L) - (-1 - L) \rvert = 2
$$

5. 두 점 중 적어도 하나는 $$L$$ 에서 1 이상 떨어져 있다. 그 점을 $$x$$ 로 고른다.
6. 이 논증은 $$L$$ 에 무관하게 성립하므로 극한은 존재하지 않는다.
7. $$\sin(1/x)$$, $$a = 0$$ 에 같은 절차를 적용한다.
   1. $$x_n = 1/(2\pi n + \pi/2)$$ 에서 값은 1이다.
   2. $$y_n = 1/(2\pi n + 3\pi/2)$$ 에서 값은 $$-1$$ 이다.
   3. $$n$$ 을 키우면 두 점 모두 상대의 $$\delta$$ 안으로 들어온다.
   4. 나머지는 3단계에서 6단계까지와 같이 $$\varepsilon = 1$$ 로 끝난다.

## 4. 시험 및 검사

### A. min 생략 시 반례

1. $$\delta = \varepsilon/7$$ 만 쓰고 상대가 $$\varepsilon = 10$$ 을 낸다고 가정한다.
2. $$\delta = 10/7 \approx 1.43$$ 이다.
3. $$x = 4.4$$ 는 $$\lvert x - 3 \rvert = 1.4 < \delta$$ 이므로 구간 안에 있다.
4. $$4.4^2 - 9 = 10.36 > 10$$ 이므로 조건이 깨진다.
5. 판정: $$\varepsilon$$ 이 크면 $$\varepsilon/7$$ 이 1을 넘어 "$$\lvert x + 3 \rvert < 7$$" 전제가 깨진다. min 의 1이 이 전제를 유지한다.

<figure>
<img src="{{ '/images/blog/epsilon-delta-limit-definition/min-counterexample.gif' | relative_url }}" alt="Counterexample with epsilon = 10: delta = epsilon/7 admits x = 4.4 where x^2 leaves the band; delta = min(1, epsilon/7) does not">
<figcaption>ε = 10 에서 δ = ε/7 만 쓰면 x = 4.4 가 구간에 들어와 x² = 19.36 이 ε 띠 위로 벗어난다. δ = min(1, ε/7) = 1 이면 그래프가 띠 안에 남는다.</figcaption>
</figure>

### B. 유리함수 δ 수치 확인

1. $$\varepsilon = 0.1$$ 이면 $$\delta = \min(1/2,\ 0.1/4) = 0.025$$ 이다.
2. 구간 양 끝 $$x = 2.025$$ 와 $$x = 1.975$$ 에서 오차를 계산한다. 각각 0.0488 과 0.0513 이다.
3. 판정: 두 값 모두 0.1 안에 있으므로 합격이다.

### C. 자주 발생하는 논리적 오류

1. $$\delta$$ 에 $$x$$ 를 넣는 오류를 점검한다.
   1. 예: $$\delta = \varepsilon/\lvert x + 3 \rvert$$.
   2. 양화사 순서상 $$\delta$$ 를 정할 때는 아직 $$x$$ 가 정해지지 않았다.
2. min 을 생략하는 오류를 점검한다.
   1. 작은 $$\varepsilon$$ 만 고려하면 $$\varepsilon/7$$ 로 충분해 보인다.
   2. 4.A 의 $$\varepsilon = 10$$, $$x = 4.4$$ 처럼 큰 $$\varepsilon$$ 에서 깨진다.
   3. "$$\varepsilon$$ 이 크면 어떻게 되는가"를 확인하는 것이 가장 빠른 점검이다.
3. 예비 계산 순서로 답안을 쓰는 오류를 점검한다.
   1. $$\lvert f(x) - L \rvert < \varepsilon$$ 에서 출발해 $$\lvert x - a \rvert < \delta$$ 를 끌어내면 방향이 반대다.
   2. 각 단계가 역방향으로도 성립하는지 확인하지 않으면 증명이 되지 않는다.
4. 부정 명제에서 "이면"을 그대로 두는 오류를 점검한다.
   1. "$$0 < \lvert x - a \rvert < \delta$$ 이면 $$\lvert f(x) - L \rvert \ge \varepsilon$$" 은 구간 안의 모든 $$x$$ 가 벗어난다는 훨씬 강한 주장이다.
   2. 필요한 것은 벗어나는 $$x$$ 가 하나 존재한다는 것이다.
5. $$x = a$$ 에서의 값을 극한에 섞는 오류를 점검한다.
   1. 정의의 $$0 < \lvert x - a \rvert$$ 는 $$f(a)$$ 를 고려하지 않는다는 뜻이다.
   2. 명제 "$$\lim fg = 0$$ 이면 $$\lim f = 0$$ 또는 $$\lim g = 0$$" 의 반례로 $$g(0) = 1$$, $$x \neq 0$$ 에서 $$g(x) = 0$$ 인 함수를 드는 경우가 있다.
   3. 이 $$g$$ 는 $$x \to 0$$ 에서 극한이 0이므로 반례가 되지 못한다.
   4. 올바른 반례는 $$x > 0$$ 에서 1이고 나머지에서 0인 $$f$$ 와, $$x < 0$$ 에서 1이고 나머지에서 0인 $$g$$ 다.
   5. 곱은 어디서나 0이지만 $$f$$ 와 $$g$$ 모두 0에서 극한이 존재하지 않는다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
정의의 $$0 < \lvert x - a \rvert$$ 조건은 연습문제 해답에서도 간과되기 쉽다.
</div>

## 5. 종료

### A. 결과 정리

1. 극한의 정의는 $$\forall \varepsilon,\ \exists \delta$$ 의 양화사 순서로 해석한다. $$\delta$$ 는 $$\varepsilon$$ 에 의존하고 $$x$$ 에 의존하지 않는다(3.A).
2. $$\delta$$ 는 예비 계산으로 찾고, 답안은 역순으로 쓴다(3.B).
3. 오차 식에 $$x$$ 에 따라 변하는 인수가 있으면 구간을 먼저 제한하고 min 으로 결합한다(3.D, 3.E).
4. 제한 반지름은 함수가 정의되지 않는 점까지의 거리보다 작아야 한다(3.E).
5. 극한의 비존재는 부정 명제 $$\exists \varepsilon,\ \forall \delta,\ \exists x$$ 로 증명한다(3.F).
