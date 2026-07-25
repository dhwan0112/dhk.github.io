"""FeO(100) 슬랩 생성 후 QE 입력으로 저장.
슬랩 좌표를 손으로 쓰는 것은 오류의 온상이므로 반드시 생성기를 쓴다."""
from ase.build import bulk, surface
from ase.io import write
from ase.constraints import FixAtoms

feo = bulk("FeO", "rocksalt", a=4.33)
slab = surface(feo, (1, 0, 0), layers=4, vacuum=8.0)
slab.center(axis=2)

# 하단 2개 층 고정 -> QE 의 if_pos 플래그로 변환된다
zs = sorted(set(round(z, 3) for z in slab.positions[:, 2]))
fixed_z = set(zs[: len(zs) // 2])
slab.set_constraint(FixAtoms(
    indices=[i for i, a in enumerate(slab) if round(a.position[2], 3) in fixed_z]))

write(
    "feo100.scf.in", slab, format="espresso-in",
    pseudopotentials={"Fe": "Fe.pbe-spn-kjpaw_psl.1.0.0.UPF",
                      "O":  "O.pbe-n-kjpaw_psl.1.0.0.UPF"},
    kpts=(6, 6, 1),
    input_data={
        # tefield/dipfield 는 &CONTROL 변수다 (&SYSTEM 에 넣으면 read_namelists 에러)
        "control": {"calculation": "relax", "prefix": "feo100",
                    "outdir": "./tmp/", "pseudo_dir": "./pseudo/",
                    "tprnfor": True, "forc_conv_thr": 1.0e-4,
                    "tefield": True, "dipfield": True},
        # 비자성 시연: 1x1 (100) 셀은 AFM-II 배열을 담을 수 없다.
        # 실제 연구라면 자기 배열을 담는 더 큰 셀 + starting_magnetization 필요.
        "system": {"ecutwfc": 70, "ecutrho": 700,
                   "occupations": "smearing", "smearing": "mv", "degauss": 0.01,
                   "edir": 3, "emaxpos": 0.90, "eopreg": 0.05, "eamp": 0.0},
        "electrons": {"conv_thr": 1.0e-8, "mixing_beta": 0.2,
                      "mixing_mode": "local-TF", "electron_maxstep": 200},
        "ions": {"ion_dynamics": "bfgs"},
    },
)
print("feo100.scf.in 생성 완료 — 생성된 CELL_PARAMETERS/ATOMIC_POSITIONS 를 직접 읽어볼 것")
