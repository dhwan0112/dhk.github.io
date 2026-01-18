---
title: "LAMMPS 시뮬레이션 시작하기"
date: 2025-01-18
category: Computation
tags: [LAMMPS, MD, Tutorial]
---

LAMMPS를 처음 시작하는 분들을 위한 간단한 가이드입니다.

## 설치

Ubuntu에서 LAMMPS를 설치하는 방법:

```bash
sudo apt-get update
sudo apt-get install lammps
```

## 기본 입력 파일 구조

LAMMPS 입력 파일은 다음과 같은 구조를 가집니다:

```
# Initialization
units metal
atom_style atomic

# System definition
lattice fcc 3.615
region box block 0 10 0 10 0 10
create_box 1 box
create_atoms 1 box

# Force field
pair_style eam
pair_coeff * * Cu_u3.eam

# Settings
velocity all create 300 12345

# Run
run 10000
```

## 에너지 계산

시스템의 총 에너지는 다음과 같이 계산됩니다:

$$E_{total} = E_{kinetic} + E_{potential}$$

여기서 운동 에너지는:

$$E_{kinetic} = \frac{1}{2}\sum_i m_i v_i^2$$

## 다음 단계

다음 포스트에서는 구리 표면 시뮬레이션을 다룰 예정입니다.
