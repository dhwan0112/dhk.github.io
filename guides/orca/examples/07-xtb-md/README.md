# 07-xtb-md — GFN2-xTB와 r2SCAN-3c로 본 알라닌 다이펩타이드 (xTB opt/freq, MD)

가이드 16장(GFN-xTB)과 17장(분자동역학)의 예제. 모든 `.out`은 NUS HPC Vanda 클러스터에서
**ORCA 6.1.0**(`module load ORCA/6.1.0-gompi-2023b-avx2`, 8코어)으로 실제 실행한 결과다.
xTB 계산은 모듈의 `bin/`에 들어 있는 `otool_xtb`(xtb 6.7.1)를 ORCA가 `-P 8`로 호출했다.

| 파일 | 계산 | 실제 결과 |
|------|------|-----------|
| `ala.xyz` | 출발 구조 (Ace-Ala-NMe, 원자 22개) | — |
| `o01-xtb-opt-freq.{inp,out,xyz}` | `XTB2 Opt Freq ALPB(water)` | E −32.991364 Eh, G −32.848402 Eh, φ/ψ −82.6/72.8 (C7eq), 허수 진동수 0, 9.9 s |
| `o02-r2scan-opt-freq.{inp,out,xyz}` | `r2SCAN-3c Opt Freq CPCM(water)`, o01 구조에서 출발 | E −495.775841 Eh, G −495.628066 Eh, φ/ψ −85.9/73.9 (C7eq), 허수 진동수 0, 14 min 27 s |
| `o03-xtb-md.{inp,out,md.log}` | `XTB2 MD ALPB(water)`, NHC 300 K, 0.5 fs × 20000 = 10 ps | 57 min 48 s (0.173 s/step), 1 ps 이후 T = 301.6 ± 63.7 K |
| `o04-r2scan-md.{inp,out,md.log}` | 같은 MD를 r2SCAN-3c/CPCM으로 200스텝(100 fs) | 1 h 1 min 51 s (18.6 s/step, xTB의 약 107배). 100 fs로는 평형 전이라 비용 비교용 |

실행 순서는 o01 → o02 → o03 → o04이고, 입력은 각자 같은 이름의 하위 디렉터리에서 돈다고 가정한다
(`../ala.xyz`, `../o01-xtb-opt-freq/o01-xtb-opt-freq.xyz`처럼 상대 경로로 앞 단계 구조를 읽는다).

```bash
for name in o01-xtb-opt-freq o02-r2scan-opt-freq o03-xtb-md o04-r2scan-md; do
    mkdir -p $name && cp $name.inp $name/ && (cd $name && orca $name.inp > $name.out)
done
```

`o03-xtb-md.md.log`에는 스텝마다 온도, 운동·퍼텐셜 에너지, 보존량이 들어 있다. 좌표 궤적
`o03-xtb-md.traj.xyz`(1001프레임, 1.4 MB)는 용량 때문에 넣지 않았다. 가이드의 그림
`assets/img/orca-xtb-md.gif`, `assets/img/orca-xtb-md-dihedrals.png`가 이 궤적에서 나왔다.
