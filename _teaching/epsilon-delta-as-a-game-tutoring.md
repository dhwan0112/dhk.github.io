---
subject: Math
order: 4
date: 2026-10-02
title: "ε-δ 정의를 과외에서 설명하는 방법: 상대가 ε을 내면 나는 δ로 답한다"
tags: [Math, Calculus, Limit]
description: "과외에서 ε-δ 정의를 설명할 때 쓰는 순서를 정리했다. 정의를 두 사람의 게임으로 읽고, 일차함수·이차함수·유리함수에서 δ를 찾는 절차를 따라가며 δ = min(1, ε/7) 같은 선택이 왜 필요한지 반례로 확인한다. 극한이 존재하지 않음을 보이는 부정 명제와 자주 보는 실수도 함께 적었다."
---

ε-δ 정의에서 막히는 지점은 거의 항상 같다. 기호 자체보다 "누가 먼저 무엇을 고르는가"가 머리에 들어오지 않는다. 그래서 과외에서 나는 정의를 문장으로 외우게 하기 전에 게임으로 먼저 읽힌다. 상대가 허용 오차 ε을 내밀면, 나는 그 ε을 보고 δ를 내놓는다. 어떤 ε이 와도 이길 수 있는 δ 공식을 가지고 있으면 극한이 증명된 것이다. 이 틀을 잡아 두면 이차함수에서 쓰는 δ = min(1, ε/7) 같은 선택도, 극한이 존재하지 않는다는 증명도 같은 게임의 연장으로 설명된다.

## 정의를 게임으로 읽기

정의는 이렇다.

$$
\lim_{x \to a} f(x) = L
\iff
\forall \varepsilon > 0,\ \exists \delta > 0 :\ 0 < \lvert x - a \rvert < \delta \implies \lvert f(x) - L \rvert < \varepsilon
$$

양화사 순서대로 읽으면 게임 규칙이 된다. 상대(의심하는 쪽)가 먼저 양수 $$\varepsilon$$을 고른다. "$$f(x)$$를 $$L$$에서 이만큼 안쪽으로 붙들어 둘 수 있나?"라는 도전이다. 그다음 내가 양수 $$\delta$$를 고른다. $$a$$에서 $$\delta$$ 이내(단 $$a$$ 자체는 빼고)의 모든 $$x$$에 대해 $$\lvert f(x) - L \rvert < \varepsilon$$이면 내가 이긴다. 극한이 $$L$$이라는 말은 상대가 어떤 $$\varepsilon$$을 골라도 내가 이기는 전략이 있다는 뜻이다.

$$\lim_{x \to 3}(2x+1) = 7$$로 몇 판 해 본다. 상대가 $$\varepsilon = 0.1$$을 내면, $$\lvert (2x+1) - 7 \rvert = 2\lvert x - 3 \rvert$$이므로 $$\lvert x - 3 \rvert < 0.05$$면 된다. $$\delta = 0.05$$로 답한다. $$\varepsilon = 0.001$$이 오면 $$\delta = 0.0005$$. 몇 판 하다 보면 매번 계산할 필요가 없다는 게 보인다. $$\delta = \varepsilon/2$$라는 공식 하나로 모든 판을 이긴다. 증명이란 이 공식을 제시하고 그것이 항상 이긴다는 걸 보이는 것이다.

게임으로 읽으면 두 가지가 자연스럽게 따라온다. $$\delta$$는 $$\varepsilon$$을 본 뒤에 고르니 $$\varepsilon$$에 의존해도 되지만, $$x$$는 $$\delta$$를 정한 뒤 상대가 구간 안에서 아무거나 찍는 것이라 $$\delta$$가 $$x$$에 의존하면 안 된다. 그리고 이기는 $$\delta$$보다 작은 $$\delta$$도 역시 이긴다. 구간을 좁히면 상대가 찍을 수 있는 $$x$$가 줄어들 뿐이기 때문이다. 뒤에 나오는 min 트릭이 전부 이 성질 위에 서 있다.

## δ를 찾는 절차

증명은 두 단계로 나눠서 쓰게 한다. 먼저 연습장에서 $$\lvert f(x) - L \rvert$$를 $$\lvert x - a \rvert$$에 대한 식으로 바꾸고, 이게 $$\varepsilon$$보다 작아지려면 $$\lvert x - a \rvert$$가 얼마나 작아야 하는지 거꾸로 푼다. 여기서 $$\delta$$가 나온다. 그다음 답안에는 순서를 뒤집어서 "임의의 $$\varepsilon > 0$$이 주어졌다, $$\delta = \cdots$$로 두자, $$0 < \lvert x - a \rvert < \delta$$라 하면 ... $$< \varepsilon$$"으로 앞에서부터 쓴다. 연습장 작업은 증명이 아니다. 답안에 연습장 순서를 그대로 옮기면 결론에서 출발해 가정을 끌어내는 글이 된다.

### 일차함수

$$\lim_{x \to 2}(3x + 1) = 7$$.

$$
\lvert (3x+1) - 7 \rvert = \lvert 3x - 6 \rvert = 3\lvert x - 2 \rvert
$$

이 값이 $$\varepsilon$$보다 작으려면 $$\lvert x - 2 \rvert < \varepsilon/3$$이면 된다. $$\delta = \varepsilon/3$$로 두면 $$0 < \lvert x - 2 \rvert < \delta$$일 때 $$3\lvert x - 2 \rvert < 3 \cdot \varepsilon/3 = \varepsilon$$이다. 일반적으로 $$mx + b$$ ($$m \neq 0$$)이면 $$\delta = \varepsilon/\lvert m \rvert$$. 기울기가 가파를수록 $$x$$를 더 좁게 묶어야 한다는 그림과 맞는다.

### 이차함수와 min(1, ε/7)

$$\lim_{x \to 3} x^2 = 9$$부터 진짜 문제가 생긴다.

$$
\lvert x^2 - 9 \rvert = \lvert x - 3 \rvert \cdot \lvert x + 3 \rvert
$$

$$\lvert x - 3 \rvert$$는 $$\delta$$로 조절하지만 $$\lvert x + 3 \rvert$$는 $$x$$에 따라 변한다. 여기서 흔히 나오는 답이 $$\delta = \varepsilon/\lvert x + 3 \rvert$$인데, 앞에서 말한 대로 $$\delta$$에 $$x$$가 들어가면 반칙이다. 필요한 건 $$\lvert x + 3 \rvert$$를 $$x$$와 무관한 상수로 위에서 누르는 것이다.

그래서 먼저 $$x$$를 3 근처로 묶어 둔다. $$\lvert x - 3 \rvert < 1$$이면 $$2 < x < 4$$이고 $$5 < x + 3 < 7$$이라 $$\lvert x + 3 \rvert < 7$$이다. 그 안에서는

$$
\lvert x^2 - 9 \rvert < 7\lvert x - 3 \rvert
$$

이므로 $$\lvert x - 3 \rvert < \varepsilon/7$$이면 충분하다. 두 조건($$\lvert x - 3 \rvert < 1$$과 $$\lvert x - 3 \rvert < \varepsilon/7$$)을 동시에 만족시키려면 작은 쪽을 고른다.

$$
\delta = \min\left(1, \frac{\varepsilon}{7}\right)
$$

$$0 < \lvert x - 3 \rvert < \delta$$이면 $$\delta \le 1$$에서 $$\lvert x + 3 \rvert < 7$$, $$\delta \le \varepsilon/7$$에서 $$\lvert x - 3 \rvert < \varepsilon/7$$이 나오고, 둘을 곱하면 $$\lvert x^2 - 9 \rvert < \varepsilon$$이다.

min이 왜 필요한지는 반례 하나로 보여 준다. $$\delta = \varepsilon/7$$만 쓰고 상대가 $$\varepsilon = 10$$을 냈다고 하자. $$\delta = 10/7 \approx 1.43$$이고, $$x = 4.4$$는 $$\lvert x - 3 \rvert = 1.4 < \delta$$라 구간 안에 있다. 그런데 $$4.4^2 - 9 = 10.36 > 10$$. 진다. $$\varepsilon$$이 크면 $$\varepsilon/7$$이 1을 넘어서 "$$\lvert x + 3 \rvert < 7$$"이라는 전제가 깨지기 때문이다. min의 1이 그 전제를 지켜 준다.

1이라는 숫자에 특별한 의미는 없다. $$\lvert x - 3 \rvert < 1/2$$로 묶으면 $$x + 3 < 6.5$$이고 $$\delta = \min(1/2,\ 2\varepsilon/13)$$이 된다. 이것도 맞는 답이다. 과외에서는 이 점을 일부러 짚는다. 1은 계산이 편해서 고르는 것이지 정답이 하나로 정해져 있는 게 아니고, 바로 다음 예제처럼 1을 고르면 안 되는 경우도 있다.

### 유리함수: 분모를 아래에서 누르기

$$\lim_{x \to 2} \frac{x+1}{x-1} = 3$$.

$$
\left\lvert \frac{x+1}{x-1} - 3 \right\rvert = \left\lvert \frac{x + 1 - 3x + 3}{x-1} \right\rvert = \frac{2\lvert x - 2 \rvert}{\lvert x - 1 \rvert}
$$

이번엔 분모 $$\lvert x - 1 \rvert$$를 아래에서 눌러야 한다(분모가 작아지면 전체가 커지니까). 습관대로 $$\lvert x - 2 \rvert < 1$$로 묶으면 $$1 < x < 3$$인데, 이 구간은 $$x = 1$$에 한없이 가까운 점을 포함해서 $$\lvert x - 1 \rvert$$가 0에 얼마든지 가까워진다. 아래 경계가 안 생긴다. 함수의 특이점 $$x = 1$$까지의 거리가 1이니 그보다 좁게 묶어야 한다.

$$\lvert x - 2 \rvert < 1/2$$로 묶으면 $$3/2 < x < 5/2$$, $$\lvert x - 1 \rvert > 1/2$$이므로

$$
\frac{2\lvert x - 2 \rvert}{\lvert x - 1 \rvert} < 4\lvert x - 2 \rvert
$$

따라서 $$\delta = \min(1/2,\ \varepsilon/4)$$. 숫자로 확인하면 $$\varepsilon = 0.1$$일 때 $$\delta = 0.025$$이고, 구간 양 끝 $$x = 2.025$$와 $$x = 1.975$$에서 오차는 각각 0.0488과 0.0513으로 0.1 안에 있다.

묶는 반지름을 고르는 기준을 말로 하면 "그 안에 함수가 망가지는 점이 들어오지 않을 만큼"이다. 다항식은 망가지는 점이 없어서 아무 반지름이나 되고, 유리함수는 분모의 영점까지 거리보다 작아야 한다.

## 극한이 존재하지 않음: 게임을 반대편에서

극한이 $$L$$이 아니라는 명제는 정의를 부정해서 얻는다. $$\forall$$와 $$\exists$$가 서로 바뀌고, "이면"은 "이면서"가 된다.

$$
\lim_{x \to a} f(x) \neq L
\iff
\exists \varepsilon > 0,\ \forall \delta > 0,\ \exists x :\ 0 < \lvert x - a \rvert < \delta \ \text{and}\ \lvert f(x) - L \rvert \ge \varepsilon
$$

게임으로 읽으면 이번엔 내가 의심하는 쪽이다. 내가 $$\varepsilon$$ 하나를 골라 두면, 상대가 어떤 $$\delta$$를 내놓든 그 구간 안에서 $$\varepsilon$$ 밖으로 튀는 $$x$$를 하나 찾아낼 수 있다. 극한이 아예 존재하지 않는다는 건 모든 실수 $$L$$에 대해 이게 된다는 뜻이다.

$$f(x) = \lvert x \rvert / x$$, $$a = 0$$으로 해 본다. $$x > 0$$이면 1, $$x < 0$$이면 $$-1$$이다. 임의의 $$L$$에 대해 $$\varepsilon = 1$$을 고른다. 상대가 어떤 $$\delta$$를 내도 $$x = \delta/2$$와 $$x = -\delta/2$$는 둘 다 $$0 < \lvert x \rvert < \delta$$를 만족하고, 함숫값은 1과 $$-1$$이다. 그런데

$$
\lvert 1 - L \rvert + \lvert -1 - L \rvert \ge \lvert (1 - L) - (-1 - L) \rvert = 2
$$

이므로 둘 중 적어도 하나는 $$L$$에서 1 이상 떨어져 있다. 그 점이 내가 찾는 $$x$$다. 이 논증은 $$L$$이 뭐든 통하니 극한은 존재하지 않는다.

$$\sin(1/x)$$도 같은 모양이다. $$x_n = 1/(2\pi n + \pi/2)$$에서 값이 1, $$y_n = 1/(2\pi n + 3\pi/2)$$에서 $$-1$$이고, $$n$$을 키우면 두 점 모두 상대의 $$\delta$$ 안으로 들어온다. 나머지는 위와 똑같이 $$\varepsilon = 1$$로 끝난다.

## 자주 보는 실수

과외하면서 반복해서 보는 실수를 모아 둔다.

- $$\delta$$에 $$x$$를 넣는다. $$\delta = \varepsilon/\lvert x + 3 \rvert$$ 같은 답. 게임 순서상 $$\delta$$를 낼 때는 아직 $$x$$가 정해지지 않았다.
- min을 빼먹는다. 작은 $$\varepsilon$$만 떠올리면 $$\varepsilon/7$$이면 충분해 보이지만, 위의 $$\varepsilon = 10$$, $$x = 4.4$$처럼 큰 $$\varepsilon$$에서 깨진다. "$$\varepsilon$$이 크면 어떻게 되나"를 한 번 물어보는 게 가장 빠른 점검이다.
- 연습장 순서로 답안을 쓴다. $$\lvert f(x) - L \rvert < \varepsilon$$에서 출발해 $$\lvert x - a \rvert < \delta$$를 끌어내면 방향이 반대다. 각 단계가 거꾸로도 성립하는지 확인하지 않으면 증명이 안 된다.
- 부정에서 "이면"을 그대로 둔다. "$$0 < \lvert x - a \rvert < \delta$$이면 $$\lvert f(x) - L \rvert \ge \varepsilon$$"은 구간 안의 모든 $$x$$가 튄다는 훨씬 강한 주장이다. 필요한 건 튀는 $$x$$가 하나 있다는 것이다.
- $$x = a$$에서의 값을 극한에 섞는다. 정의의 $$0 < \lvert x - a \rvert$$는 $$f(a)$$를 보지 않겠다는 뜻이다. 예를 들어 "$$\lim fg = 0$$이면 $$\lim f = 0$$ 또는 $$\lim g = 0$$"의 반례로 $$g(0) = 1$$, $$x \neq 0$$에서 $$g(x) = 0$$인 함수를 드는 경우가 있는데, 이 $$g$$는 $$x \to 0$$에서 극한이 0이라 반례가 되지 못한다. 제대로 된 반례는 $$x > 0$$에서 1이고 나머지에서 0인 $$f$$와 $$x < 0$$에서 1이고 나머지에서 0인 $$g$$다. 곱은 어디서나 0인데 $$f$$와 $$g$$ 모두 0에서 극한이 존재하지 않는다.

마지막 실수는 내 연습문제 해답에도 들어 있었다. 정의의 $$0 < \lvert x - a \rvert$$ 부분은 설명할 때도 가볍게 넘어가기 쉽다.
