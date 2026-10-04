---
layout: default
title: "1. 시스템 개요"
nav_order: 2
parent: 가이드
has_children: false
---

# 1. 시스템 개요와 화학적 배경
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<p class="amm-id">NOTE 32-01-00 · 시스템 개요와 화학적 배경</p>

## 1. 일반 사항

### A. 목적

1. 이 노트는 Cu 표면 위 벤젠-에탄올 경쟁 흡착 시스템의 화학적 배경과 시뮬레이션 셀 기하를 다룬다.
2. 이 노트는 흡착을 이루는 세 가지 기여, 다섯 단계 프로토콜, 분석 대상 물리량을 정한다.

### B. 적용 범위

1. 박스 30 × 30 × 41.895 Å³, `boundary p p f` 의 슬랩 시스템에 적용한다.
2. UROPS run 의 [`opls.data`](../../files/blog/pppm-vs-msm/opls.data) 에 든 Cu 슬랩과 Cu-유기 LJ 계수를 기준으로 한다.

### C. 결과 요약

1. `opls.data` 의 Cu 슬랩은 fcc(100) 이 아니라 bcc 쌓임이다. 주기 경계를 사이에 두고 원자가 1.08 Å 까지 붙어 있다.
2. Heinz et al. (2008) 의 12-6 Cu 파라미터는 ε = 4.72 kcal/mol, σ = 2.330 Å 이다.
3. UROPS run 의 Cu-유기 ε 는 Heinz 값을 기하 평균한 값보다 약 30배 약하다.

## 2. 준비 정보

### A. 필요한 개념

1. LAMMPS 기초(NOTE 31-01-00 ~ 31-08-00).
2. 면심입방(fcc) 결정 구조와 밀러 지수.
3. 물리 흡착과 화학 흡착의 구분.

### B. 참조 자료

| 참조 | 제목 |
|------|------|
| Heinz 외 (2008) | H. Heinz, R. A. Vaia, B. L. Farmer, R. R. Naik, "Accurate Simulation of Surfaces and Interfaces of Face-Centered Cubic Metals Using 12-6 and 9-6 Lennard-Jones Potentials", *J. Phys. Chem. C* **112**, 17281-17290 (2008). DOI: [10.1021/jp801931d](https://doi.org/10.1021/jp801931d) |
| Vitos 외 (1998) | L. Vitos, A. V. Ruban, H. L. Skriver, J. Kollár, "The surface energy of metals", *Surf. Sci.* **411**, 186-202 (1998). DOI: [10.1016/S0039-6028(98)00363-X](https://doi.org/10.1016/S0039-6028(98)00363-X) |
| Irving, Kirkwood (1950) | J. H. Irving, J. G. Kirkwood, "The Statistical Mechanical Theory of Transport Processes. IV. The Equations of Hydrodynamics", *J. Chem. Phys.* **18**, 817-829 (1950). DOI: [10.1063/1.1747782](https://doi.org/10.1063/1.1747782) |
| Tyson, Miller (1977) | W. R. Tyson, W. A. Miller, "Surface free energies of solid metals: Estimation from liquid surface tension measurements", *Surf. Sci.* **62**, 267-276 (1977). DOI: [10.1016/0039-6028(77)90442-3](https://doi.org/10.1016/0039-6028(77)90442-3) |
| Mishin 외 (2001) | Y. Mishin, M. J. Mehl, D. A. Papaconstantopoulos, A. F. Voter, J. D. Kress, "Structural stability and lattice defects in copper: Ab initio, tight-binding, and embedded-atom calculations", *Phys. Rev. B* **63**, 224106 (2001). DOI: [10.1103/PhysRevB.63.224106](https://doi.org/10.1103/PhysRevB.63.224106) |
| NOTE 32-03-00 | [힘장 비교](03-force-fields) |
| NOTE 32-05-00 | [5단계 프로토콜](05-protocol) |
| NOTE 32-07-00 | [분석 방법](07-analysis) |
| 예제 E3 | [Cu(100) 슬랩](ex-03-cu-slab.html) |

### D. 관련 파일

| 항목 | 용도 |
|------|------|
| [`opls.data`](../../files/blog/pppm-vs-msm/opls.data) | UROPS run 의 데이터 파일 (Cu 371원자 포함) |

## 3. 절차

### A. 화학적 배경 확인

1. 벤젠과 에탄올은 서로 다른 결합 양상을 갖는 대표적인 유기 분자이다.
    1. 벤젠은 비편극성(nonpolar) π-전자 시스템을 가진다.
    2. 에탄올은 극성(polar) 수산기(-OH)를 통해 수소 결합 네트워크를 형성한다.
2. 두 분자가 섞인 액체가 전이금속 표면에 닿을 때 어느 쪽이 먼저 흡착하는지는 분리 공정과 촉매 설계에서 중요한 문제다.
3. 구리(Cu)는 채워진 3d 궤도를 가지는 대표적인 fcc 금속이다. 가스상 벤젠 분자의 π-궤도와 도너-억셉터 상호작용을 형성할 수 있다(Cu의 [Ar]3d¹⁰4s¹ 전자 배치를 참고).
4. 에탄올은 표면 위에서 수산기를 통한 수소 결합과 메틸기를 통한 약한 분산력으로 흡착한다.
5. 두 분자가 동시에 존재하면 표면 점유 경쟁이 발생한다.

### B. 시뮬레이션 셀 기하 설정

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
UROPS run 의 [`opls.data`](../../files/blog/pppm-vs-msm/opls.data) 에 든 Cu 슬랩은 fcc(100) 이 아니다.

- Cu 371원자는 z = 0, 1.81, 3.62, 5.42, 7.23 Å 의 다섯 층에 81, 64, 81, 64, 81개씩 있다.
- 한 층은 간격 3.615 Å 의 정사각 격자이다. 다음 층은 a/2 높이에서 (a/2, a/2) 만큼 밀려 있다. 이것은 bcc 쌓임이다.
- 최근접 거리가 3.13 Å 로 fcc Cu 의 2.56 Å 보다 길다.
- 81원자 층은 한 줄에 9개라 9 × 3.615 = 32.5 Å 인데 박스는 30 Å 이다. 그래서 x(또는 y) = 0 과 28.92 Å 의 원자가 주기 경계를 사이에 두고 1.08 Å 까지 붙어 있다.

fcc(100) 슬랩은 `lattice fcc 3.615` 와 `create_atoms` 로 만드는 편이 안전하다([예제 E3](ex-03-cu-slab.html)). 그때는 박스 가로를 격자 상수의 정수배(예: 8 × 3.615 = 28.92 Å)로 맞춘다.
</div>

1. 슬랩 기하(slab geometry)를 다음과 같이 구성한다.
    1. 박스 크기를 30 × 30 × 41.895 Å³ 로 둔다.
    2. 경계 조건을 x, y 방향 주기적, z 방향 비주기로 둔다(`boundary p p f`).
    3. z 축 하단에 fcc Cu 슬랩을 배치한다(격자 상수 a = 3.615 Å).
    4. Cu 슬랩 위 진공-액체 영역에 벤젠과 에탄올을 무작위로 배치한다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
표면 흡착 시뮬레이션에서는 보통 z 축을 비주기로 둔다. 슬랩 위에 진공 영역을 두어, 두 분자가 표면으로 들어오고 떨어져 나가는 과정을 자연스럽게 보기 위해서다.
</div>

<figure>
  <img src="assets/images/cu-cell.svg" alt="Cu 표면 흡착 시뮬레이션 셀의 슬랩 기하 모식도" style="width:100%;max-width:860px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    그림 1. 시뮬레이션 셀의 단면(x–z) 모식도. z 하단에 Cu 슬랩(고정),
    그 위 진공-액체 영역에 벤젠(π)·에탄올(−OH)이 배치되고, z 상단에는
    분자 이탈을 막는 <code>wall/lj93</code> 벽이 있다. x·y는 주기 경계(p),
    z는 비주기 경계(f)다. 그림은 시스템 구성 모식도이며, 실제 Cu(100) 슬랩의
    원자 배열은 아래 그림 2에서 확인할 수 있다.
  </figcaption>
</figure>

### C. Cu 슬랩의 결정학적 면 확인

1. 노출면이 (100) 인지 (111) 인지는 슬랩을 자르는 결정 방향으로 정해진다.
2. 두 결정면의 성질을 비교한다.

| 결정면 | 표면 원자 밀도 (atoms/Å²) | 표면 에너지, 계산 (J/m²) | 특징 |
|--------|---------------------------|---------------------|------|
| Cu(100) | 0.153 | 2.17 | 정사각형 배열, hollow site |
| Cu(111) | 0.177 | 1.95 | 육각형 배열, 가장 안정 |

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
표면 원자 밀도는 $2/a^2$와 $4/(\sqrt{3}a^2)$로 계산했다. 표면 에너지는 Vitos 외 (1998), *Surf. Sci.* 411, 186 의 DFT 값이다. 면 평균 실험값은 약 1.79 J/m² (Tyson & Miller 1977) 로, 계산값보다 낮다.
</div>

<figure>
  <img src="assets/images/cu-slab.png" alt="실제로 실행한 Cu(100) 슬랩의 측면도와 z 방향 원자 밀도 프로파일" style="width:100%;max-width:880px;height:auto;border:1px solid var(--border-color);border-radius:6px;" />
  <figcaption style="font-size:0.85rem;color:var(--text-muted);text-align:center;margin-top:0.5rem;">
    그림 2. 위 슬랩 기하를 실제로 구성해 돌린 결과(LAMMPS 22 Jul 2025, EAM Mishin 2001,
    fcc <em>a</em> = 3.615 Å, 1664 원자, NVT 열욕 300 K, 하단 두 면 고정). 왼쪽은 측면도(x–z 투영)로
    하단의 이산적인 Cu 원자층과 그 위의 진공 영역이 그대로 보인다.
    오른쪽 z-밀도 프로파일에서 각 봉우리는 (100) 원자 한 층(층 간격 ≈ 1.81 Å)에 해당하며,
    진공 영역에서는 밀도가 0으로 떨어진다. <code>boundary p p f</code>의 슬랩+진공 구조가
    수치로 드러난다. 이 그림은 금속 슬랩만 따로 돌린 것이고, 본문의 production 단계에서는
    이 슬랩 위에 유기 분자를 올리고 Cu를 고정한다.
  </figcaption>
</figure>

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
위 슬랩 기하를 데이터 파일 없이 EAM만으로 만들어 실행하는 예제는 <a href="ex-03-cu-slab.html">예제 E3 — Cu(100) 슬랩</a> 이다. 전체 입력과 z 밀도 프로파일 출력을 한자리에서 확인할 수 있다.
</div>

### D. 흡착 기여 분해

1. 이 시스템의 흡착을 세 가지 기여로 나눈다.
2. 분산 인력(London dispersion)을 Cu 원자와 유기 분자 사이의 비결합 12-6 Lennard-Jones 항으로 모형화한다.
    1. Heinz et al. (2008) 의 12-6 Cu 파라미터는 ε = 4.72 kcal/mol, σ = 2.330 Å 이다.
    2. 2.616 Å 은 σ 가 아니라 퍼텐셜 최소 위치 $r_0 = 2^{1/6}\sigma$ 이다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
UROPS run 은 Heinz 값을 쓰지 않았다. Cu-Cu 는 EAM (Mishin 2001) 이고, Cu-유기 쌍은 ε = 0.012–0.029 kcal/mol 을 직접 넣었다. Heinz 값을 기하 평균으로 섞으면 벤젠 C-Cu 가 0.575 kcal/mol 인데, 실제 입력은 0.0187 kcal/mol 로 약 30배 약하다([3장](03-force-fields)).
</div>

3. 정전기 상호작용(Coulomb)을 장거리 방법으로 처리한다. PPPM 또는 MSM을 쓴다.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
에탄올의 -O-H 결합은 큰 부분 전하 (q_O ≈ -0.7, q_H ≈ +0.435) 를 가지므로 장거리 정전기 처리가 꼭 필요하다.
</div>

4. π-d 궤도 상호작용은 LJ 파라미터에 녹여 간접적으로 표현한다. 고전 힘장은 이 효과를 명시적으로 다루지 않는다.

<div class="amm-warning" markdown="1">
<span class="amm-label">경고</span>
양자역학적 효과를 제대로 잡으려면 DFT 나 ReaxFF가 필요하다. 여기서는 INTERFACE-FF의 LJ 파라미터가 금속의 표면 에너지에 fit되어 있어 계면 거동을 어느 정도 재현한다고 기대할 수 있다. 그러나 위처럼 Cu-유기 ε 를 따로 줄였다면 그 근거는 사라진다.
</div>

### E. 다섯 단계 프로토콜 구성

1. 시뮬레이션을 다음 다섯 단계로 진행한다.

| 단계 | 명칭 | 목적 | 이유 |
|------|------|------|-------------|
| 1 | 소프트 완화 (Soft potential relaxation) | 원자 중첩 해소 | 초기 무작위 배치에서 발생하는 비물리적 큰 힘 제거 |
| 2 | 에너지 최소화 (Minimization) | 국소 최소점 도달 | 0 K 정적 평형 구조 (potential energy surface의 minimum) |
| 3 | 단계적 가열 (Staged heating) | 0.1 K → 300 K 점진 가열 | 운동 에너지를 천천히 주입하여 구조 붕괴 방지 |
| 4 | 평형화 (Equilibration) | 300 K NVT 평형 | 열역학적 평형 분포 확보, 자기 상관 시간 이상 |
| 5 | Production | 통계 수집 | 평형 앙상블 평균 계산 |

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
단계별로 왜 필요한지는 [5단계 프로토콜](05-protocol)에서 자세히 다룬다.
</div>

## 4. 시험 및 검사

### A. 분석 대상 물리량

1. 이 시뮬레이션에서 다음 물리량을 계산한다.
    1. 동경 분포 함수(Radial Distribution Function, g(r)): 분자 간 구조 상관.
    2. 밀도 프로파일(z 방향): 계면에서의 분자별 분포.
    3. 분리 효율 지수(Separation Efficiency Index, SEI): 0 (완전 혼합) ~ 1 (완전 분리).
    4. 흡착 에너지: 표면 결합 강도의 정량 지표.
    5. 계면 장력(Irving-Kirkwood 방법): 계면의 열역학적 안정성.

<div class="amm-note" markdown="1">
<span class="amm-label">참고</span>
분석 방법은 [분석 방법](07-analysis)에서 자세히 다룬다.
</div>
