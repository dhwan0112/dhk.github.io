---
title: "LAMMPS 덤프에서 z-밀도 프로파일 뽑기 — ASE + pandas 40줄, 그리고 fix ave/chunk와 맞춰 보기"
date: 2026-08-22
category: Computation
tags: [LAMMPS, Python, ASE, Analysis]
description: "슬랩 시뮬레이션 후처리의 출발점인 z-방향 수밀도 프로파일을 ASE와 pandas로 직접 계산하는 짧은 스크립트. 같은 Cu(100) 슬랩에 대해 LAMMPS fix ave/chunk 결과와 빈 단위로 대조해서 어디가 같고 어디가 다른지 확인하고, 그 위에 얹을 표면 과잉량 함수까지 정리했다."
---

슬랩 시뮬레이션에서 제일 먼저 보는 양은 표면 수직 방향(z)의 밀도 프로파일이다. LAMMPS 안에서 `fix ave/chunk`로 바로 뽑을 수 있지만, 나는 결국 파이썬 쪽으로 옮겼다. 이유는 세 가지다.

1. 돌리고 난 뒤에 빈 폭을 바꾸거나 종(type)별로 쪼개고 싶을 때 시뮬레이션을 다시 돌리고 싶지 않다.
2. 벤젠/에탄올처럼 분자 단위로 봐야 하는 계는 원자가 아니라 분자 질량중심 기준이 필요한데, 이건 후처리가 편하다.
3. 밀도 프로파일은 끝이 아니라 시작이다. 표면 과잉량, 층별 조성 같은 다음 계산이 전부 이 배열을 입력으로 받는다.

대신 직접 짠 코드는 한 번은 LAMMPS 내부 결과와 맞춰 봐야 한다. 아래는 그 스크립트와 대조 결과다.

## 스크립트

```python
"""z-number-density profile per atom type from a LAMMPS dump (ASE + pandas).

usage: python zprofile.py dump.lammpstrj [dz]  ->  zprofile.csv
"""
import sys
import numpy as np
import pandas as pd
from ase.io import iread


def z_profile(dumpfile, dz=0.25):
    """Return a DataFrame: index = bin centre z (Å), one column per LAMMPS type,
    values = number density (atoms/Å^3) averaged over all frames in the dump."""
    counts, nframes, edges, area = {}, 0, None, None
    for atoms in iread(dumpfile, format="lammps-dump-text", index=":"):
        lx, ly, lz = atoms.cell.lengths()
        if edges is None:                       # bins fixed by the first frame
            edges = np.arange(0.0, lz + dz, dz)
            area = lx * ly
        z = atoms.positions[:, 2]
        types = atoms.arrays["type"]            # ASE keeps the LAMMPS type here
        for t in np.unique(types):
            h, _ = np.histogram(z[types == t], bins=edges)
            counts[t] = counts.get(t, 0) + h
        nframes += 1
    centres = 0.5 * (edges[:-1] + edges[1:])
    df = pd.DataFrame({f"type{t}": c / (nframes * area * dz) for t, c in counts.items()},
                      index=pd.Index(centres, name="z"))
    df.attrs["nframes"] = nframes
    return df


if __name__ == "__main__":
    dump = sys.argv[1]
    dz = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
    prof = z_profile(dump, dz)
    prof.to_csv("zprofile.csv", float_format="%.6f")
    print(f"{prof.attrs['nframes']} frame(s), {len(prof)} bins of {dz} Å")
    print(prof[prof.sum(axis=1) > 0].head(8))
```

`iread`는 프레임을 하나씩 넘겨주므로 수 GB짜리 궤적도 메모리에 다 올리지 않는다. 결과는 행이 z, 열이 type인 DataFrame 하나라서 그 다음 계산은 전부 열 연산으로 끝난다.

처음 짤 때 걸렸던 부분 두 가지:

- **ASE는 type을 원소로 읽지 않는다.** `specorder`를 안 주면 모든 원자가 `H`로 들어온다. 원소 기호가 필요하면 `iread(..., specorder=["Cu"])`처럼 type 순서대로 넘겨야 하고, 그냥 type 번호만 쓸 거면 위처럼 `atoms.arrays["type"]`을 읽는 게 가장 덜 헷갈린다.
- **빈의 원점을 LAMMPS와 맞춰야 비교가 된다.** `compute chunk/atom bin/1d z lower 0.25 units box`는 박스 하단(`zlo`)에서 시작하는 0.25 Å 빈이다. 위 코드의 `np.arange(0.0, lz + dz, dz)`는 좌표가 `zlo = 0`인 경우에만 같은 빈이 된다. `zlo`가 0이 아니면 `atoms.cell`이 아니라 덤프의 `BOX BOUNDS`를 직접 읽어서 원점을 맞춰야 한다. NPT처럼 박스가 변하는 궤적이면 "첫 프레임 빈 고정"도 다시 생각해야 한다.

## fix ave/chunk와 대조

대조에 쓴 계는 LAMMPS 가이드 [cu-01]({{ '/guides/lammps/cu-01-system.html' | relative_url }})에 나오는 Cu(100) 슬랩이다. 8×8 단위격자 면적에 (100)면 13장, 1664원자, 맨 아래 한 층은 `setforce 0`으로 고정, 나머지는 300 K NVT. 10000스텝 평형 후 5000스텝 동안 `fix ave/chunk 100 50 5000`으로 시간 평균 프로파일(`zdens.dat`)을 뽑고, 마지막 프레임을 `write_dump`로 저장했다. 위 스크립트는 그 마지막 프레임 하나를 읽는다. 입력 파일과 두 출력 파일은 글 끝에 있다.

<figure>
<img src="{{ '/images/blog/zprofile-cu100.png' | relative_url }}" alt="Cu(100) slab z number-density profile: Python single frame vs LAMMPS time average">
<figcaption>왼쪽: 전체 프로파일. 실선이 파이썬(마지막 프레임 1장), 점선이 LAMMPS <code>fix ave/chunk</code>(5000스텝 평균). 오른쪽: 3–5번째 원자면 확대, 점은 빈 중심.</figcaption>
</figure>

정리하면:

| 구간 | 파이썬 (프레임 1장) | LAMMPS (시간 평균) | 비고 |
|---|---|---|---|
| 고정층 z = 0.125, 1.875 Å | 0.6122 | 0.6122 | 소수점 4자리까지 동일 |
| 가동층, 면 하나당 원자 수 | 128.0 | 128.0 | 13개 면 전부, 면 주위 ±0.9 Å 빈 합 |
| 가동층, 빈 하나의 값 | 1–2개 빈에 몰림 | 3–4개 빈으로 퍼짐 | 열진동 때문 |

고정층이 소수점 넷째 자리까지 같은 건 당연하지만, 빈 원점과 면적·부피 정규화가 LAMMPS와 똑같이 잡혔다는 증거라서 제일 먼저 봐야 하는 숫자다. 가동층은 빈 하나씩 보면 다르다. 스냅샷 한 장은 원자가 있는 빈에 카운트가 몰리고, 5000스텝 평균은 원자가 열진동으로 오간 범위만큼 퍼진다. 하지만 면 하나를 통째로 적분하면 둘 다 정확히 128이다. 즉 정규화는 맞고, 차이는 순전히 "한 장이냐 평균이냐"다.

실제 분석에서는 당연히 production 구간 전체를 `iread`로 돌려 평균한다. 여기서 한 장만 쓴 건 두 방법의 차이가 어디서 오는지 눈에 보이게 하려는 것이다.

## 그 다음: 표면 과잉량

벤젠/에탄올 같은 2성분 액체가 Cu 위에 있으면, 프로파일에서 바로 알고 싶은 건 "표면이 벌크보다 벤젠을 얼마나 더 끌어안고 있나"다. Gibbs의 상대 표면 과잉량으로 쓰면

$$
\Gamma_{2}^{(1)} = \int_{z_\text{wall}}^{z_\text{bulk}} \left[ \rho_2(z) - \rho_2^{\,b}\,\frac{\rho_1(z)}{\rho_1^{\,b}} \right] dz
$$

여기서 1은 용매(에탄올), 2는 용질(벤젠), 위첨자 b는 벌크 값이다. 용매의 과잉량이 0이 되도록 분할면을 잡는 정의라서, 분할면을 어디에 둘지 고민할 필요가 없다. 위 DataFrame이 있으면 이 정도로 끝난다.

```python
def surface_excess(prof, solute, solvent, z_wall, z_bulk_from, z_bulk_to):
    """Gibbs relative surface excess Γ_solute^(solvent) in molecules/Å^2."""
    bulk = prof.loc[z_bulk_from:z_bulk_to].mean()
    sel = prof.loc[z_wall:z_bulk_to]
    dz = np.diff(sel.index.values).mean()
    integrand = sel[solute] - bulk[solute] * sel[solvent] / bulk[solvent]
    return float(integrand.sum() * dz)
```

`prof`의 열이 원자 type이 아니라 분자 종이어야 하므로, 실제로는 `z_profile` 안에서 z 대신 분자 질량중심을 히스토그램에 넣는 버전을 쓴다. 분자 id는 덤프에서 못 가져온다 — 덤프에 `mol` 열을 넣어도 ASE의 dump 리더는 그 열을 버린다(확인해 봤다). 대신 데이터 파일을 `read("system.data", format="lammps-data", atom_style="full")`로 읽으면 `atoms.arrays["mol-id"]`에 들어오고, 원자 순서는 id로 정렬된 덤프와 같으므로 그걸 프레임마다 재사용하면 된다. 함수 자체는 합성 프로파일로 확인했다. 두 성분이 벽 너머에서 균일하면 정확히 0이 나오고, 벤젠에 가우시안 흡착 봉우리를 얹으면 그 봉우리 면적이 그대로 돌아온다.

벤젠/에탄올–Cu 계의 실제 값은 PPPM과 MSM 비교 글에서 다룬다. 힘장·정전기 처리별로 이 숫자가 어떻게 달라지는지가 그 글의 본론이다.

## 파일

- [`zprofile.py`]({{ '/files/blog/zprofile/zprofile.py' | relative_url }}) — 위 스크립트
- [`excess.py`]({{ '/files/blog/zprofile/excess.py' | relative_url }}) — 표면 과잉량 함수
- [`in.cu_slab`]({{ '/files/blog/zprofile/in.cu_slab' | relative_url }}) — LAMMPS 입력 (EAM, Mishin 2001 `Cu_mishin1.eam.alloy` 필요)
- [`slab_final.dump`]({{ '/files/blog/zprofile/slab_final.dump' | relative_url }}), [`zdens.dat`]({{ '/files/blog/zprofile/zdens.dat' | relative_url }}) — 대조에 쓴 출력

```bash
python zprofile.py slab_final.dump 0.25    # -> zprofile.csv
```
