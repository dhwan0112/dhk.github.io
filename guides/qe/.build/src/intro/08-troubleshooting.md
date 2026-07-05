---
layout: default
title: "8. 트러블슈팅과 운영"
---

# 8. 트러블슈팅과 운영
{: .no_toc }

## 목차
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 8.1 자주 나는 오류

| 증상 | 흔한 원인과 대응 |
|------|------------------|
| `reading pseudopotential` 오류 | `pseudo_dir` 경로·파일 이름 오타. `ATOMIC_SPECIES` 의 이름과 실제 UPF 파일명 일치 확인. |
| `SCF correction compared to forces is large` | 힘 임계에 비해 SCF가 덜 수렴. `conv_thr` 을 더 작게. |
| `convergence NOT achieved` | `mixing_beta` 를 0.2~0.3으로. 금속이면 smearing + k점 증가. |
| `Not enough space allocated for radial FFT` | US/PAW인데 `ecutrho` 가 작음. 8~12×ecutwfc로. |
| `too many bands are not converged` | `nbnd` 를 늘리거나 `diagonalization='cg'` 시도. |
| `S matrix not positive definite` | 원자가 너무 가까움 — 초기 구조 점검. |
| 에너지가 이상하게 낮음/발산 | LDA·PBE 유사퍼텐셜 혼용, 또는 컷오프가 너무 낮음. |

## 8.2 결과가 의심스러울 때 점검 순서

1. **JOB DONE.** 로 정상 종료했는가? 중간에 멈췄으면 그 앞 오류를 봅니다.
2. **수렴**했는가? `estimated scf accuracy < conv_thr` 확인.
3. **컷오프·k점**이 수렴 범위인가? ([03](03-pseudopotentials.html)·[04](04-kpoints.html)장)
4. **구조**가 의도한 대로인가? 출력 초반의 `site n. ... positions` 로 확인.
5. **유사퍼텐셜**이 같은 범함수·적절한 컷오프인가?
6. 금속인데 smearing을 켰는가? 절연체인데 간격이 맞는가?

## 8.3 병렬 실행 — 무엇을 나누는가

`pw.x` 는 여러 축으로 병렬화합니다. 가장 효과적인 것부터:

```bash
# k점 풀 병렬(-nk): k점을 npool개 그룹으로 나눔. k점 많은 계에 가장 효율적
mpirun -np 16 pw.x -nk 4 -in scf.in > scf.out    # 16 프로세스, 4 풀(풀당 4)
```

- `-nk`(k-point pools): k점을 나눕니다. **k점이 많을수록 효율이 좋아** 대개 첫
  번째로 씁니다.
- 그 밖에 `-nb`(band), `-nt`(FFT task), `-nd`(선형대수) 축이 있으나, 입문
  단계에서는 `-nk` 만으로 충분한 경우가 많습니다.

<div class="tip">
  <div class="note-title">작은 계는 스레드를 끄세요</div>
  <p>
    원자 몇 개짜리 계에 OpenMP 스레드를 16개씩 띄우면 오히려 느려집니다
    (스레드가 서로 기다리며 CPU만 태웁니다). <code>export OMP_NUM_THREADS=1</code>
    로 끄고 MPI로 k점을 병렬화하는 편이 보통 빠릅니다. 본 가이드의 실리콘 SCF는
    이렇게 하면 2분 걸리던 것이 3초로 줄었습니다.
  </p>
</div>

## 8.4 성능 감각

- 출력 끝의 `PWSCF : ... CPU ... WALL` 로 소요 시간을 봅니다. `CPU` 가 `WALL` 의
  수십 배면 스레드 과다입니다(위 팁 참고).
- 계산량은 대략 (평면파 수) × (k점 수) × (밴드 수)에 비례합니다. `ecutwfc`,
  k점, 셀 크기를 키우면 그만큼 무거워집니다.
- `outdir` 에는 파동함수·전하밀도가 쌓이므로, 큰 계는 디스크 여유와
  `wf_collect`/정리 습관이 필요합니다.

## 8.5 좋은 운영 습관

- 새 계는 **작게 시작**합니다. 성긴 k점·낮은 컷오프로 돌려 흐름을 확인한 뒤
  수렴값으로 키웁니다.
- 스텝 간 `prefix`·`outdir` 를 일관되게 유지합니다(후처리가 이를 참조).
- 입력 파일과 유사퍼텐셜 출처를 함께 보관해 재현성을 확보합니다.
- 장시간 계산은 `tmux`/배치 스케줄러로 돌리고, 중간 재시작(`restart_mode`)을
  활용합니다.

## 8.6 더 알아보기

- 각 프로그램 입력 변수: [INPUT_PW](https://www.quantum-espresso.org/Doc/INPUT_PW.html) 등 공식 설명서
- 사용자 포럼과 메일링 리스트: [quantum-espresso.org](https://www.quantum-espresso.org/)
- 예제로 전체 흐름 익히기: [E1](ex-01-si-scf.html)–[E4](ex-04-relax.html)
