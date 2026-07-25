---
title: "E7. Si DOS·PDOS"
---

# E7. Si DOS·PDOS

## 목적

상태밀도 파이프라인 — scf → nscf → `dos.x` → `projwfc.x` — 를 처음부터
끝까지 실행합니다. **순서와 `prefix`/`outdir` 일치가 전부**라는 것을 몸으로
익히고, Löwdin 전하까지 읽습니다.

```
scf (8³ k) ─→ nscf (16³ k, tetrahedra) ─┬─→ dos.x       (총 DOS)
                                         └─→ projwfc.x   (PDOS + Löwdin)
```

## 새로 나오는 카드·변수

| 항목 | 역할 |
|---|---|
| `calculation='nscf'` + `occupations='tetrahedra'` | 고정 밀도 위 조밀 k 고유값 ([08장](08-scf-nscf.html)) |
| `nbnd=12` | 전도대까지 넉넉히 |
| `&DOS` (dos.x) | Emin/Emax/DeltaE |
| `&PROJWFC` (projwfc.x) | PDOS 분해, Löwdin |

## 입력 파일

[si.scf.in](files/E07-si-dos/si.scf.in) ·
[si.nscf.in](files/E07-si-dos/si.nscf.in) ·
[si.dos.in](files/E07-si-dos/si.dos.in) ·
[si.projwfc.in](files/E07-si-dos/si.projwfc.in) ·
[run.sh](files/E07-si-dos/run.sh)

nscf 입력의 핵심 부분:

```fortran
&SYSTEM
  ...
  nbnd = 12                   ! 전도대까지 넉넉히
  occupations = 'tetrahedra'  ! 사면체법 (아래 실측 노트 참고)
/
K_POINTS (automatic)
  16 16 16  0 0 0             ! 사면체법은 반드시 Γ 중심 (shift 0 0 0)
```

<div class="warning">
  <div class="note-title">실측 노트 — tetrahedra_opt와 projwfc.x</div>
  <p>
    처음에는 최적화 사면체법 <code>occupations='tetrahedra_opt'</code>로
    돌렸는데, <strong>QE 7.5에서 dos.x(총 DOS)와 Löwdin 전하는 정상인데
    projwfc.x의 PDOS 파일이 전부 0으로 나오는 문제</strong>를 확인했습니다
    (직렬/병렬, lsym 유무 무관). 고전 사면체법 <code>'tetrahedra'</code>로
    nscf를 다시 돌리면 PDOS가 정상적으로 나옵니다. 이 예제의 입력 파일은
    그래서 <code>'tetrahedra'</code>로 배포합니다.
  </p>
</div>

`dos.x` 입력:

```fortran
&DOS
  prefix = 'si'
  outdir = './tmp/'
  fildos = 'si.dos'
  Emin   = -10.0
  Emax   =  20.0
  DeltaE =  0.05
/
```

## 실행

```bash
pw.x       -in si.scf.in     > si.scf.out
pw.x       -in si.nscf.in    > si.nscf.out
dos.x      -in si.dos.in     > si.dos.out
projwfc.x  -in si.projwfc.in > si.projwfc.out
grep -A20 'Lowdin Charges' si.projwfc.out
```

## 출력·그림 — 실측

<figure>
  <img src="assets/images/qe-e07-dos-pdos.png"
       alt="Si total DOS with s/p projected DOS" />
  <figcaption>
    실리콘 총 DOS와 s/p 분해 PDOS 실측 (QE 7.5, nscf 16×16×16, tetrahedra).
    가전자대 하단(-12~-8 eV)은 s, 상단은 p가 지배하고, 갭이 열려 있습니다.
  </figcaption>
</figure>

출력 파일 해독:

- `si.dos` — 1열 E(eV), 2열 DOS, 3열 적분 DOS. 적분 DOS는 가전자대 꼭대기에서
  정확히 8(원자가 전자 수)이어야 합니다 — 검산 포인트.
- `si.pdos.pdos_atm#1(Si)_wfc#2(p)` — 원자 1의 p 궤도 분해 DOS.
- **Löwdin 전하 실측**: 원자당 총 3.9637 e (s 1.1617 + p 2.8020),
  spilling parameter 0.0091. 원자가 전자 4개와의 차이(스필링)는 원자 궤도
  기저가 평면파 상태를 완전히 담지 못하는 몫입니다 — Fe의 d 점유·모멘트를
  읽을 때도 같은 한계를 염두에 두세요.

## 직접 써보기

1. nscf의 k-격자를 8³ → 24³으로 바꿔가며 DOS가 얼마나 매끄러워지는지
   관찰하세요.
2. `occupations='tetrahedra'` 대신 `'smearing'`으로 하면 DOS가 어떻게
   뭉개지나요? `'tetrahedra_opt'`로 바꾸면 PDOS에 무슨 일이 생기나요?
3. `si.dos`의 3열(적분 DOS)이 가전자대 꼭대기에서 8과 일치하는지 확인하세요.
4. Löwdin 전하의 총합과 원자가 전자수의 차이(스필링)의 의미를 생각해 보세요.

<div class="warning">
  <div class="note-title">흔한 실수</div>
  <p>
    nscf의 <code>K_POINTS</code>에 시프트(<code>1 1 1</code>)를 남겨 두는 것 —
    사면체법은 Γ 중심 그리드를 요구하므로 에러가 나거나 조용히 다른 결과가
    나옵니다. 그리고 <code>prefix</code>/<code>outdir</code>이 한 글자라도
    다르면 <code>cannot open file ... .save</code>로 파이프라인이 끊깁니다
    (<a href="ref-errors.html">R3</a>).
  </p>
</div>

## 관련 챕터

[10 상태밀도와 밴드](10-dos-bands.html) ·
[08 SCF와 NSCF](08-scf-nscf.html)
