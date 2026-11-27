---
note: "31-10-01"
subject: Chemistry
order: 8
date: 2026-11-26
title: "러더퍼드 산란: 건포도 푸딩 모형의 예측과 핵 모형의 관측"
tags: [Chemistry, Physics, Python, Atomic Structure, Simulation]
description: "같은 알파 입자 빔 4,000개를 건포도 푸딩 원자와 핵 원자에 쏘아 비교한다. 푸딩 모형은 최대 3.87°만 휘고 90°를 넘는 입자가 없지만, 핵 모형에서는 20개(이론값 22.5개)가 뒤로 튕기고 분포가 1/sin⁴(θ/2)을 따른다."
---

NOTE 31-10-01 · 러더퍼드 산란: 건포도 푸딩 모형의 예측과 핵 모형의 관측
{: .amm-id}

## 1. 일반 사항

### A. 목적

1. 이 노트는 같은 알파 입자 빔을 두 원자 모형에 쏘아, 각 모형이 예측하는 산란각 분포를 비교한다.
2. 핵 모형의 수치 결과를 러더퍼드 공식과 맞춰 본다.

$$\frac{dN}{d\Omega} \propto \frac{1}{\sin^4(\theta/2)}$$

3. 건포도 푸딩 모형으로는 큰 각도 산란이 왜 나올 수 없는지 수치와 근사식으로 확인한다.

### B. 적용 범위

1. 고정된 점전하(핵 모형) 또는 고정된 균일 대전 구(건포도 푸딩 모형)와 알파 입자 하나 사이의 쿨롱 반발만 다룬다.
2. 2차원 평면 안의 궤적을 계산하고, 입사 위치는 원판 위에 고르게 놓아 3차원 빔의 통계를 흉내 낸다(3.B).
3. 핵의 되튐, 전자의 가림, 금박 안의 다중 산란은 다루지 않는다(4.C).

### C. 결과 요약

1. 핵 모형: 4,000개 중 20개가 90°를 넘게 휜다. 이론값은 22.5개다.
2. 핵 모형의 수치 산란각은 해석해와 최대 1.22° 차이 안에서 일치한다.
3. 건포도 푸딩 모형: 가장 크게 휜 입자도 3.87°이고, 90°를 넘는 입자는 0개다.

## 2. 준비 정보

### A. 필요한 개념

1. 쿨롱 힘, 충돌 매개변수(impact parameter) $$b$$, 입체각 $$d\Omega = 2\pi\sin\theta\,d\theta$$를 알아야 한다.
2. 균일하게 대전된 구 안에서는 전기장이 중심으로부터의 거리에 비례한다는 사실을 쓴다.

### C. 사용 프로그램

| 항목 | 용도 |
|---|---|
| Python, numpy ≥ 1.26, matplotlib ≥ 3.8 | 원본 시뮬레이션과 웹용 데이터 추출 |
| ffmpeg (PATH에 필요) | 원본 스크립트로 영상 파일을 만들 때만 필요 |
| 브라우저 JavaScript | 이 페이지의 애니메이션. 추출한 데이터로 궤적을 다시 적분해 SVG로 그린다 |

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
원본 스크립트는 그림 글꼴로 `cmr10`을 지정한다. 이 글꼴이 없는 환경에서는 matplotlib이 글꼴 경고를 내지만 계산 결과에는 영향이 없다.
</div>

### D. 관련 파일

| 파일 | 내용 |
|---|---|
| [`rutherford_paper.py`]({{ '/files/blog/rutherford-scattering-nuclear-vs-plum-pudding/rutherford_paper.py' | relative_url }}) | 원본 시뮬레이션. 실제 비율 장면, 건포도 푸딩 예측, 핵 모형을 차례로 그리고 본문의 검증 수치를 출력한다. |
| [`export_web_data.py`]({{ '/files/blog/rutherford-scattering-nuclear-vs-plum-pudding/export_web_data.py' | relative_url }}) | 위 스크립트의 같은 난수 시드와 매개변수로 웹 애니메이션용 데이터를 만든다. |
| [`rutherford.json`]({{ '/files/blog/rutherford-scattering-nuclear-vs-plum-pudding/data/rutherford.json' | relative_url }}) | 입사 위치, 발사 시각, 최종 산란각 등 애니메이션 데이터(약 230 KB). |

## 3. 절차

### A. 실제 비율 확인

<figure>
<div class="cv-player" data-cv="rutherford" data-src="{{ '/files/blog/rutherford-scattering-nuclear-vs-plum-pudding/data/rutherford.json' | relative_url }}" aria-label="Animation: zoom out from a gold nucleus to the atom and the detector screen at real proportions, then alpha particles fired at a plum pudding atom and at a nuclear atom, with the angular distribution of detected particles"></div>
<noscript><p>이 애니메이션은 JavaScript가 필요합니다. 원본은 2.D 의 스크립트로 만들 수 있습니다.</p></noscript>
<figcaption>위: 시뮬레이션 패널, 아래: 같은 순간의 분석 그래프. 처음 장면(a) real proportions만 실제 비율이고, 그 뒤 두 장면은 핵 근처를 크게 확대한 모식도라 비율이 실제와 다르다. 재생 막대로 원하는 장면을 고를 수 있다.</figcaption>
</figure>

1. 금 원자핵의 지름을 약 $$10^{-14}$$ m, 원자의 지름을 약 $$10^{-10}$$ m로 둔다. 원자는 핵보다 약 만 배 넓다.
2. 감지판까지의 거리를 수 cm로 둔다. 핵 지름의 약 $$10^{12}$$배다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
첫 장면의 감지판 거리 2 cm는 "수 cm" 규모를 나타내는 어림값이다. Geiger와 Marsden의 1913년 논문 원문으로 확인한 값이 아니다.
</div>

3. 이 비율로는 핵도 궤적도 한 화면에 그릴 수 없음을 확인한다. 이후 장면은 핵 근처를 확대한 모식도로 그린다.

### B. 빔 준비

1. 알파 입자 4,000개를 $$x = -7$$에서 $$+x$$ 방향, 같은 속력으로 출발시킨다.
2. 충돌 매개변수 $$b$$를 반지름 $$R = 2.0$$인 원판 위에 고르게 분포시킨다. 원판 위에서 고르면 $$b$$의 분포는 $$2\pi b\,db$$에 비례한다.

$$b = R\sqrt{u}, \qquad u \sim \mathrm{Uniform}(0, 1)$$

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
궤적은 평면에서 계산하지만 실제 빔은 단면이 원인 3차원 빔이다. 원판 위에 고르게 놓아야 입체각당 검출 수가 $$1/\sin^4(\theta/2)$$을 따른다. $$b$$를 한 직선 위에서만 고르게 놓으면 각도당 검출 수 $$dN/d\theta$$가 $$1/\sin^2(\theta/2)$$ 꼴이 되어 다른 분포가 나온다.
</div>

### C. 핵 모형

1. 핵을 원점에 고정된 점전하로 둔다. 알파 입자의 가속도를 다음처럼 쓴다.

$$\ddot{\mathbf r} = k\,\frac{\mathbf r}{r^3}, \qquad k = d\,v_0^2,\quad d = 0.15$$

2. 속도 베를레(velocity Verlet)로 시간 간격 0.005, 전체 시간 24까지 적분한다.
3. 쿨롱 산란의 해석해로 충돌 매개변수와 산란각을 잇는다.

$$b = d\cot\frac{\theta}{2}$$

4. 90°를 넘는 조건을 구한다. $$\theta > 90^\circ$$이면 $$\cot(\theta/2) < 1$$, 곧 $$b < d$$다.
5. 그 확률은 원판 넓이의 비다.

$$P(\theta > 90^\circ) = \left(\frac{d}{R}\right)^2 = \left(\frac{0.15}{2.0}\right)^2 = 0.005625$$

6. 기댓값을 구한다. $$4000 \times 0.005625 = 22.5$$개다.
7. 입체각당 분포를 유도한다. 빔 단위 넓이당 입자 수가 $$N/(\pi R^2)$$이므로 다음과 같다.

$$\frac{dN}{d\Omega} = \frac{N}{\pi R^2}\,\frac{b}{\sin\theta}\left\lvert\frac{db}{d\theta}\right\rvert = \frac{N}{\pi R^2}\,\frac{(d/2)^2}{\sin^4(\theta/2)}$$

### D. 건포도 푸딩 모형

1. 같은 양전하를 반지름 3.5인 구에 고르게 퍼뜨린다. 구 밖에서는 점전하와 같은 힘을, 구 안에서는 거리에 비례하는 힘을 쓴다.

$$\ddot{\mathbf r} = \begin{cases} k\,\mathbf r / r^3, & r \ge a \\ k\,\mathbf r / a^3, & r < a \end{cases} \qquad a = 3.5$$

2. 같은 4,000개 입사 위치로 같은 적분을 한다.
3. 작은 각도 근사(충격량 근사)로 편향각을 구한다. 직선 경로를 따라 받은 가로 방향 충격량으로 계산한다.

$$\theta \approx \frac{2d}{b}\left[1 - \left(1 - \frac{b^2}{a^2}\right)^{3/2}\right] \quad (b < a,\ \text{라디안})$$

4. 전하가 원자 전체에 퍼져 있으면 어느 경로에서도 힘이 작아, 큰 각도로 꺾일 수 없음을 확인한다.

## 4. 시험 및 검사

### A. 핵 모형

1. 수치 산란각과 3.C.3 의 해석해를 비교한다. 최대 차이는 1.22°다.
2. 90°를 넘은 입자 수를 센다. 20개이고, 기댓값 22.5개와 통계 오차 범위에서 맞는다.
3. 입체각당 분포를 3.C.7 의 곡선과 비교한다. 아래 그래프의 원이 점선을 따라간다.
4. 가장 작은 각도 구간(10~20°)은 이론보다 약 9 % 적게 세어진다. 유한한 거리($$x = -7$$)에서 출발시킨 영향으로 보이며, 출발 거리를 늘리면 줄어든다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
4.A.4 의 원인은 원본 작업 기록의 추정이다. 출발 거리를 늘려 다시 계산해 보는 것으로 확인할 수 있다.
</div>

### B. 건포도 푸딩 모형

1. 가장 크게 휜 입자의 각도를 확인한다. 3.87°다.
2. 90°를 넘은 입자를 센다. 0개다.
3. 수치 결과와 3.D.3 의 근사식을 비교한다. 최대 차이는 0.07°다.
4. 판정: 건포도 푸딩 모형은 큰 각도 산란을 설명하지 못한다.

### C. 실제와 다른 점

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
산란 장면은 핵 근처를 크게 확대한 모식도다. 감지판 거리, 푸딩 모형의 원자 크기, 빔의 폭 모두 실제 비율이 아니다. 그래서 뒤로 튕기는 비율(4,000개 중 20개)도 실제 실험보다 훨씬 높다.
</div>

1. 감지판의 점은 궤적이 원과 만나는 지점이 아니라 최종 진행 방향에 찍는다. 먼 곳의 형광판에서는 닿는 위치가 곧 산란각이기 때문이다.
2. 정면의 회색 띠(direct beam)는 거의 휘지 않고 지나가는 대다수 입자의 자리다. 이 입자들은 시뮬레이션하지 않았다.
3. 핵의 되튐, 전자의 가림 효과, 금박 안의 다중 산란은 넣지 않았다.
4. 실제 장치는 원자를 둘러싼 고정 원형 판이 아니라, 황화아연(ZnS) 형광판을 붙인 현미경을 금박 둘레로 돌려 가며 섬광을 세는 방식이었다. 그림의 원형 판은 교과서식 단순화다.

## 5. 종료

### A. 결과 정리

1. 같은 빔을 쏘았을 때 건포도 푸딩 모형은 최대 3.87°의 작은 편향만 만든다.
2. 핵 모형은 4,000개 중 20개를 90° 너머로 돌려보내고, 분포가 $$1/\sin^4(\theta/2)$$을 따른다.
3. 큰 각도 산란은 양전하가 아주 작은 영역에 모여 있어야만 가능하다.

<script defer src="{{ '/assets/js/chemviz.js' | relative_url }}"></script>
