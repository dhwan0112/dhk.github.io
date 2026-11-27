---
note: "31-20-01"
subject: Chemistry
order: 9
date: 2026-11-26
title: "충돌만으로 맥스웰-볼츠만 분포가 만들어지는 과정"
tags: [Chemistry, Physics, Python, Kinetic Theory, Molecular Dynamics]
description: "모든 입자가 같은 속력에서 출발한 2차원 기체 196개가 충돌만으로 맥스웰-볼츠만 분포에 도달한다. 평형 평균 속력 1.180은 2차원 이론값 1.177과 맞고, 한 순간의 분포가 이론에서 벗어나는 정도는 입자 수의 제곱근에 반비례해 줄어든다."
---

NOTE 31-20-01 · 충돌만으로 맥스웰-볼츠만 분포가 만들어지는 과정
{: .amm-id}

## 1. 일반 사항

### A. 목적

1. 이 노트는 모든 입자가 같은 속력에서 출발해도, 충돌만으로 속력 분포가 맥스웰-볼츠만 분포가 됨을 분자동역학으로 보인다.
2. 2차원 맥스웰-볼츠만 분포와 평균 속력을 유도하고 시뮬레이션과 비교한다.

$$P(v) = \frac{mv}{k_\mathrm{B}T}\exp\!\left(-\frac{mv^2}{2k_\mathrm{B}T}\right), \qquad \langle v\rangle = \sqrt{\frac{\pi k_\mathrm{B}T}{2m}}$$

3. 한 순간의 분포가 이론에서 벗어나는 정도가 입자 수에 따라 어떻게 줄어드는지 확인한다.

### B. 적용 범위

1. 반발력만 있는 2차원 입자계(WCA 퍼텐셜)에 적용한다.
2. 단위는 환산 단위다. 길이 $$\sigma$$, 에너지 $$\varepsilon$$, 질량 $$m$$을 1로 두고 $$k_\mathrm{B} = 1$$로 쓴다.
3. 3차원 교과서 식과의 차이는 3.C 에서 다룬다.

### C. 결과 요약

1. 196개 입자가 같은 속력에서 출발해 충돌로 분포를 넓히고, 맥스웰-볼츠만 분포에 도달한다.
2. 평형 평균 속력은 1.180이고, 2차원 이론값 $$\sqrt{\pi k_\mathrm{B}T/2m} = 1.177$$과 맞는다.
3. 한 순간의 분포와 이론의 rms 편차는 입자 수가 네 배가 될 때마다 절반이 된다($$1/\sqrt N$$).

## 2. 준비 정보

### A. 필요한 개념

1. 등분배 정리: 2차원에서 입자 하나의 평균 운동 에너지는 $$k_\mathrm{B}T$$다(자유도 2개 × $$k_\mathrm{B}T/2$$).
2. 가우스 적분 $$\int_0^\infty v^2 e^{-av^2}\,dv = \dfrac{\sqrt\pi}{4a^{3/2}}$$을 쓴다.

### C. 사용 프로그램

| 항목 | 용도 |
|---|---|
| Python, numpy ≥ 1.26, matplotlib ≥ 3.8 | 원본 시뮬레이션과 웹용 데이터 추출 |
| ffmpeg (PATH에 필요) | 원본 스크립트로 영상 파일을 만들 때만 필요 |
| 브라우저 JavaScript | 이 페이지의 애니메이션. 저장된 위치와 속력으로 SVG를 그리고 분포를 계산한다 |

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
원본 스크립트는 그림 글꼴로 `cmr10`을 지정한다. 이 글꼴이 없는 환경에서는 matplotlib이 글꼴 경고를 내지만 계산 결과에는 영향이 없다.
</div>

### D. 관련 파일

| 파일 | 내용 |
|---|---|
| [`maxwell_boltzmann.py`]({{ '/files/blog/maxwell-boltzmann-distribution-from-collisions/maxwell_boltzmann.py' | relative_url }}) | 196개 입자의 분포 형성과 가열. 평균 속력과 에너지 보존을 출력한다. |
| [`mb_convergence.py`]({{ '/files/blog/maxwell-boltzmann-distribution-from-collisions/mb_convergence.py' | relative_url }}) | 입자 수 25, 100, 400, 1600의 수렴 비교. 같은 폴더의 `maxwell_boltzmann.py`를 import한다. |
| [`export_web_data.py`]({{ '/files/blog/maxwell-boltzmann-distribution-from-collisions/export_web_data.py' | relative_url }}) | 위 두 스크립트의 같은 시드와 매개변수로 웹 애니메이션용 데이터를 만든다. |
| [`maxwell_boltzmann.json`]({{ '/files/blog/maxwell-boltzmann-distribution-from-collisions/data/maxwell_boltzmann.json' | relative_url }}), [`mb_convergence.json`]({{ '/files/blog/maxwell-boltzmann-distribution-from-collisions/data/mb_convergence.json' | relative_url }}) | 프레임별 위치와 속력(16비트 정수로 저장, 약 0.4 MB와 0.9 MB). |

## 3. 절차

### A. 모형 설정

1. 입자 사이 퍼텐셜로 WCA 퍼텐셜(레너드-존스에서 반발 부분만 남긴 것)을 쓴다.

$$U(r) = \begin{cases} 4\varepsilon\left[\left(\dfrac{\sigma}{r}\right)^{12} - \left(\dfrac{\sigma}{r}\right)^{6}\right] + \varepsilon, & r < 2^{1/6}\sigma \\ 0, & r \ge 2^{1/6}\sigma \end{cases}$$

2. 입자 196개를 14 × 14 격자에 놓는다. 밀도는 $$\rho\sigma^2 = 0.50$$, 상자 한 변은 $$\sqrt{196/0.5} = 19.8\,\sigma$$다. 경계는 주기 경계다.
3. 모든 입자에 같은 속력 $$\sqrt2$$를 주고 방향만 무작위로 정한다. 전체 운동량은 0으로 맞춘다. 이때 $$k_\mathrm{B}T = \tfrac12 v^2 = 1.00$$이다.
4. 속도 베를레로 시간 간격 0.004씩 적분하고, 10단계마다 한 프레임을 저장한다.
5. 150프레임 뒤 모든 속도에 $$\sqrt2$$를 곱해 운동 에너지를 두 배로 만들고 90프레임을 더 진행한다.

<figure>
<div class="cv-player" data-cv="maxwell-boltzmann" data-src="{{ '/files/blog/maxwell-boltzmann-distribution-from-collisions/data/maxwell_boltzmann.json' | relative_url }}" aria-label="Animation: 196 discs in a periodic box shaded by speed, all starting at the same speed; the speed histogram spreads into the two-dimensional Maxwell-Boltzmann curve and shifts right after the gas is heated"></div>
<noscript><p>이 애니메이션은 JavaScript가 필요합니다. 원본은 2.D 의 스크립트로 만들 수 있습니다.</p></noscript>
<figcaption>위: 주기 상자 안의 입자. 빠른 입자일수록 글자색에 가깝게 칠했다(밝은 테마에서는 어둡게, 어두운 테마에서는 밝게). 아래: 속력 분포(실선, 최근 8프레임 평균)와 그 순간 온도의 2차원 맥스웰-볼츠만 곡선(점선). 처음에는 한 속력에 몰려 있던 분포가 충돌로 넓어지고, 가열 뒤에는 오른쪽으로 옮겨 간다.</figcaption>
</figure>

### B. 2차원 분포 유도

1. 속도 성분 하나의 분포를 볼츠만 인자로 쓴다. 두 성분은 서로 독립이다.

$$f(v_x, v_y) = \frac{m}{2\pi k_\mathrm{B}T}\exp\!\left(-\frac{m(v_x^2 + v_y^2)}{2k_\mathrm{B}T}\right)$$

2. 속력 $$v$$와 $$v + dv$$ 사이의 영역은 속도 평면의 고리이고, 넓이는 $$2\pi v\,dv$$다.
3. 고리의 넓이를 곱해 속력 분포를 얻는다.

$$P(v)\,dv = f\cdot 2\pi v\,dv = \frac{mv}{k_\mathrm{B}T}\exp\!\left(-\frac{mv^2}{2k_\mathrm{B}T}\right)dv$$

4. 규격화를 확인한다. $$u = mv^2/2k_\mathrm{B}T$$로 치환하면 $$\int_0^\infty e^{-u}\,du = 1$$이다.
5. 평균 속력을 구한다. $$a = m/2k_\mathrm{B}T$$로 두고 2.A.2 의 적분을 쓴다.

$$\langle v\rangle = \frac{m}{k_\mathrm{B}T}\int_0^\infty v^2 e^{-av^2}\,dv = \frac{m}{k_\mathrm{B}T}\cdot\frac{\sqrt\pi}{4}\left(\frac{2k_\mathrm{B}T}{m}\right)^{3/2} = \sqrt{\frac{\pi k_\mathrm{B}T}{2m}}$$

### C. 3차원 식과의 차이

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
3차원에서는 속력 $$v$$인 속도들이 넓이 $$4\pi v^2$$인 구면 위에 있으므로 분포에 $$v^2$$이 곱해진다. 2차원에서는 둘레 $$2\pi v$$인 원 위에 있으므로 $$v$$가 곱해진다. 그래서 이 노트의 곡선은 교과서의 3차원 곡선보다 0 근처에서 더 가파르게 올라가고, 평균 속력도 $$\sqrt{8k_\mathrm{B}T/\pi m}$$이 아니라 $$\sqrt{\pi k_\mathrm{B}T/2m}$$이다.
</div>

### D. 입자 수에 따른 수렴

1. 입자 수를 25, 100, 400, 1600으로 바꿔 같은 밀도에서 따로 계산한다. 초기 속도는 $$k_\mathrm{B}T = 1$$의 가우스 분포에서 뽑는다.
2. 400단계 평형화한 뒤 55프레임을 기록한다.
3. 각 프레임 하나의 속력 히스토그램과 이론 곡선의 rms 편차를 $$v < 4$$ 구간에서 구하고, 프레임에 걸쳐 평균한다.

<figure>
<div class="cv-player" data-cv="mb-convergence" data-src="{{ '/files/blog/maxwell-boltzmann-distribution-from-collisions/data/mb_convergence.json' | relative_url }}" aria-label="Animation: the same gas with 25, 100, 400 and 1600 particles; the single-snapshot speed histogram fluctuates less around the Maxwell-Boltzmann curve as the particle count grows"></div>
<noscript><p>이 애니메이션은 JavaScript가 필요합니다. 원본은 2.D 의 스크립트로 만들 수 있습니다.</p></noscript>
<figcaption>입자 수 25 → 100 → 400 → 1600. 아래 그래프의 실선은 평균하지 않은 한 순간의 분포다. 입자가 많을수록 점선 곡선 주위의 흔들림이 작아진다.</figcaption>
</figure>

## 4. 시험 및 검사

### A. 평형 분포

1. 가열 전 평형 구간(75~150프레임)의 평균 속력을 구한다. 1.180이다.
2. 같은 구간의 온도 $$k_\mathrm{B}T = 0.88$$을 3.B.5 에 넣는다. $$\sqrt{\pi \times 0.882/2} = 1.177$$이다.
3. 판정: 차이 0.003으로 일치한다.

### B. 에너지 보존

1. 가열 전후 각 구간에서 전체 에너지(운동 + 퍼텐셜)의 변동 폭을 평균값으로 나눈다.
2. 두 구간 모두 0.04 % 미만이다.

### C. 온도가 내려가는 이유

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
초기 온도 1.00이 평형에서 0.88로 내려가는 것은 오류가 아니다. 격자에서 출발한 입자들이 서로 부딪치면서 운동 에너지 일부가 퍼텐셜 에너지로 옮겨 간다. 전체 에너지는 4.B 처럼 보존된다.
</div>

### D. 입자 수 수렴

| 입자 수 $$N$$ | $$k_\mathrm{B}T$$ | rms 편차 | rms 편차 × $$\sqrt N$$ |
|---|---|---|---|
| 25 | 1.01 | 0.257 | 1.29 |
| 100 | 0.93 | 0.118 | 1.18 |
| 400 | 0.87 | 0.058 | 1.17 |
| 1600 | 0.87 | 0.030 | 1.21 |

1. 입자 수가 네 배가 될 때마다 rms 편차가 대략 절반이 됨을 확인한다.
2. rms 편차 × $$\sqrt N$$이 1.2 근처로 거의 일정하다. 편차는 $$1/\sqrt N$$에 비례한다.

## 5. 종료

### A. 결과 정리

1. 같은 속력에서 출발한 기체도 충돌만으로 맥스웰-볼츠만 분포에 도달한다.
2. 2차원 분포는 $$P(v) \propto v\,e^{-mv^2/2k_\mathrm{B}T}$$이고, 평균 속력 $$\sqrt{\pi k_\mathrm{B}T/2m}$$이 시뮬레이션과 맞는다.
3. 한 순간의 분포가 이론에서 벗어나는 정도는 $$1/\sqrt N$$로 줄어든다. 거시적인 기체에서는 분포가 사실상 곡선 그대로다.

<script defer src="{{ '/assets/js/chemviz.js' | relative_url }}"></script>
