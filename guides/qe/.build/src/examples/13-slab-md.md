---
title: "E13. 슬랩과 AIMD"
---

# E13. 슬랩과 AIMD

## 목적

응용 3종 세트를 한 번에 다룹니다 — (1) ASE로 FeO(100) 슬랩을 **생성**하고
(손으로 쓰지 않습니다), (2) 쌍극자 보정을 켠 채 relax한 뒤 `pp.x`로
**일함수**를 구하고, (3) FeO 벌크 셀로 **Born-Oppenheimer MD**를 돌려
ML 퍼텐셜 학습 데이터 샘플링의 출발점을 만듭니다. 배경은
[15장](15-surfaces.html)·[16장](16-molecular-dynamics.html).

## 새로 나오는 것

| 항목 | 역할 |
|---|---|
| `ase.build.surface` | 슬랩 생성기 — 좌표 수작업 금지 |
| `tefield`/`dipfield`/`edir`/`emaxpos` | 쌍극자 보정 |
| `FixAtoms` → `if_pos 0 0 0` | 하단 층 고정 |
| `calculation='md'` + SVR | BOMD와 온도조절 |
| `pp.x plot_num=11` | 일함수용 정전 퍼텐셜 |

## 입력 파일

[gen_slab.py](files/E13-slab-md/gen_slab.py) ·
[feo_md.in](files/E13-slab-md/feo_md.in) ·
[pp_workfunction.in](files/E13-slab-md/pp_workfunction.in)

슬랩 생성기의 핵심부:

```python
from ase.build import bulk, surface
from ase.constraints import FixAtoms

feo = bulk("FeO", "rocksalt", a=4.33)
slab = surface(feo, (1, 0, 0), layers=4, vacuum=8.0)   # 진공 8 Å (양쪽 합 16 Å)
slab.center(axis=2)
# 하단 절반 층 고정 -> QE의 if_pos 플래그로 변환된다
```

생성된 `feo100.scf.in`을 **직접 열어 읽어보세요** — `CELL_PARAMETERS`와
`ATOMIC_POSITIONS (angstrom)`, `if_pos` 플래그가 어떻게 쓰였는지 읽을 수
있는 것이 [E2](ex-02-si-ibrav0.html)를 한 이유입니다. 슬랩 입력에는
쌍극자 보정(`tefield`/`dipfield`는 `&CONTROL`, `edir=3`·`emaxpos=0.90`은
`&SYSTEM`)과 6×6×1 k-격자(진공 방향 1)가 들어 있습니다. 슬랩 SCF는
비자성으로 단순화했습니다 — 1×1 (100) 셀은 FeO의 AFM-II 배열을 기하적으로
담을 수 없기 때문입니다 ([15장](15-surfaces.html)).

## 실행

```bash
python gen_slab.py                                     # feo100.scf.in 생성
mpirun -np 8 pw.x -nk 4 -in feo100.scf.in > feo100.relax.out
mpirun -np 8 pp.x -in pp_workfunction.in  > pp_workfunction.out
mpirun -np 8 pw.x -nk 4 -in feo_md.in     > feo_md.out
```

실측에서는 지면 사정상 relax를 최대 25 BFGS 스텝, MD를 `nstep=200`
(약 0.2 ps)으로 줄인 사본으로 돌렸습니다. 게재된 입력 파일은
`nstep=2000` 원본 그대로입니다 (단, 실측 중 두 가지 결함을 발견해
고쳤습니다 — `tefield`/`dipfield`의 네임리스트 소속과 MD의
`nosym=.true.`; 아래 흔한 실수 참조).

## 출력·그림 — 실측 (1) 슬랩과 일함수

| 항목 | 실측값 (QE 7.5) |
|---|---|
| 슬랩 | FeO(100) 4층, 8원자(1×1), 진공 16 Å, 비자성 시연 |
| relax | 25 BFGS 스텝 사본 (마지막 총힘 0.005 Ry/au — 시연용 부분 최적화) |
| 진공 준위 / Fermi 준위 | 7.35 eV / 2.40 eV (진공 평탄도 std 0.05 eV) |
| **일함수 Φ = V_vac − E_F** | **4.95 eV** |

<figure>
  <img src="assets/images/qe-e13-workfunction.png"
       alt="Planar-averaged electrostatic potential of the FeO(100) slab" />
  <figcaption>
    FeO(100) 슬랩의 평면평균 정전 퍼텐셜(pp.x plot_num=11) 실측. 진공
    구간에서 퍼텐셜이 평탄해진 것을 확인한 뒤 진공 준위와 Fermi 준위의
    차이로 일함수를 읽습니다.
  </figcaption>
</figure>

## 출력·그림 — 실측 (2) BOMD

<figure>
  <img src="assets/images/qe-e13-md.png"
       alt="FeO BOMD: temperature and conserved energy trace" />
  <figcaption>
    FeO(+U) 벌크 셀의 BOMD 실측 (SVR 300 K, dt = 20 a.u. ≈ 0.968 fs,
    200 스텝 ≈ 0.19 ps). 첫 몇 스텝에서 이온들이 이상적 격자점을 벗어나며
    위치에너지가 약 2.5 eV 방출됩니다(파란 선) — 열운동이 t2g 축퇴를 풀며
    낮은 전자 상태가 열리는, E11에서 본 물리의 연장입니다. 온도(주황)의
    ±100 K대 요동은 오류가 아니라 4원자 셀의 정상 통계입니다(상대 요동
    ~1/√N). nraise=100(≈0.1 ps) 결합의 SVR가 서서히 평형화를 진행합니다.
  </figcaption>
</figure>

이 과도 구간이 곧 실무 교훈입니다 — **학습 데이터 프레임은 평형화가 끝난
구간에서만 추출**해야 합니다. 초기 궤적을 섞으면 인위적 고에너지 구조가
데이터셋을 오염시킵니다.

ML 학습 데이터로 쓸 때의 원칙([16장](16-molecular-dynamics.html)):
모든 프레임에서 컷오프·k·smearing·U 동일, 힘 기준 수렴, 상관을 피해
간격을 두고(예: 50 스텝) 프레임 추출. 응력이 필요하면 추출 프레임에 대해
별도 scf로 계산합니다(흔한 실수 참조).

## 직접 써보기

1. `layers=4 → 6`으로 두꺼운 슬랩을 만들어 일함수가 얼마나 변하는지
   확인하세요 (층 수도 수렴 파라미터입니다).
2. `dipfield`를 끄고 같은 계산을 반복해 평면평균 퍼텐셜의 진공 구간이
   어떻게 기울어지는지 관찰하세요.
3. MD 로그에서 50 스텝 간격으로 에너지·힘 프레임을 추출하는 파서를
   작성하세요.
4. 같은 프레임에 대해 컷오프를 60 → 90 Ry로 바꿔 힘이 얼마나 변하는지
   측정하고, ML 목표 정확도(~50 meV/Å)와 비교하세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    <strong><code>tefield</code>/<code>dipfield</code>는 <code>&amp;CONTROL</code>
    소속입니다.</strong> <code>&amp;SYSTEM</code>에 넣으면
    <code>read_namelists ... bad line</code>으로 즉시 멈춥니다 — 실측 중
    실제로 겪고 생성기를 고쳤습니다(위치 파라미터 <code>edir</code> 등만
    <code>&amp;SYSTEM</code>). <strong>MD에는 <code>nosym=.true.</code>가
    필수입니다</strong> — 없으면 첫 스텝의 열운동이 초기 대칭을 깨는 순간
    <code>checkallsym</code> 에러로 멈춥니다(역시 실측으로 확인).
    그리고 <strong>nosym 상태의 DFT+U는 SCF가 정체하기 쉽습니다</strong> —
    대칭이 풀리면 축퇴 t2g 사이의 궤도 회전이 자유로워져 밀도가 계속
    출렁이기 때문입니다. 실측에서 기본 설정으로는 100회 반복에도
    7×10⁻⁵ Ry에서 멈췄고, <code>mixing_fixed_ns=30</code>(초기 반복 동안
    점유행렬 ns 동결)을 넣어야 풀렸습니다. 그래도 10⁻⁸ Ry까지는 내려가기
    어려워, 게재 입력의 <code>conv_thr</code>는 BOMD 관례 수준인
    10⁻⁶으로 잡았습니다. 응력도 함정입니다 — nosym+U(ortho-atomic)에서
    <code>tstress=.true.</code>는 <code>stres_hub: non-symmetric stress
    contribution</code> 에러로 죽습니다(QE 7.5 실측). NVT 샘플링에는 응력이
    필요 없으므로 껐고, 응력이 필요하면 추출 프레임에 대해 별도 scf로
    계산하면 됩니다.
    또, <code>emaxpos</code>(톱니 꼭짓점)는 반드시 진공 한가운데 두어야
    하고, <code>dt</code>는 Rydberg 원자단위입니다(20 a.u. ≈ 0.968 fs) —
    fs로 착각하면 궤적이 즉시 발산합니다.
  </p>
</div>

## 관련 챕터

[15 표면·슬랩과 일함수](15-surfaces.html) ·
[16 분자동역학](16-molecular-dynamics.html) ·
[11 전하밀도와 퍼텐셜](11-postprocessing.html)
