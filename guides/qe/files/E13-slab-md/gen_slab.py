"""Generate a FeO(100) slab and write it as a QE input.
Never write slab coordinates by hand; always use a generator."""
from ase.build import bulk, surface
from ase.io import write
from ase.constraints import FixAtoms

# rocksalt FeO with the cubic lattice constant a = 4.33 A
feo = bulk("FeO", "rocksalt", a=4.33)

# cut a (100) surface: 4 layers, 8 A of vacuum added on each side
# (16 A total once the cell is closed), then center the slab in the cell
slab = surface(feo, (1, 0, 0), layers=4, vacuum=8.0)
slab.center(axis=2)

# pin the bottom half of the layers at bulk positions; ASE constraints are
# translated into QE if_pos flags (0 0 0 on the fixed atoms)
zs = sorted(set(round(z, 3) for z in slab.positions[:, 2]))
fixed_z = set(zs[: len(zs) // 2])
slab.set_constraint(FixAtoms(
    indices=[i for i, a in enumerate(slab) if round(a.position[2], 3) in fixed_z]))

write(
    "feo100.scf.in", slab, format="espresso-in",
    pseudopotentials={"Fe": "Fe.pbe-spn-kjpaw_psl.1.0.0.UPF",
                      "O":  "O.pbe-n-kjpaw_psl.1.0.0.UPF"},
    kpts=(6, 6, 1),          # one k-point along the vacuum direction
    input_data={
        # tefield/dipfield are &CONTROL variables (&SYSTEM placement raises
        # read_namelists); they switch on the sawtooth dipole correction
        "control": {"calculation": "relax", "prefix": "feo100",
                    "outdir": "./tmp/", "pseudo_dir": "./pseudo/",
                    "tprnfor": True, "forc_conv_thr": 1.0e-4,
                    "tefield": True, "dipfield": True},
        # nonmagnetic demo: a 1x1 (100) cell cannot hold the AFM-II order.
        # real magnetic-surface work needs a larger cell plus starting_magnetization.
        # edir=3: correction along z; emaxpos=0.90 puts the sawtooth peak in
        # the middle of the vacuum; eamp=0 means correction only, no field
        "system": {"ecutwfc": 70, "ecutrho": 700,
                   "occupations": "smearing", "smearing": "mv", "degauss": 0.01,
                   "edir": 3, "emaxpos": 0.90, "eopreg": 0.05, "eamp": 0.0},
        # slabs with vacuum are inhomogeneous: gentle mixing + local-TF,
        # and more than the default 100 iterations for the first SCF
        "electrons": {"conv_thr": 1.0e-8, "mixing_beta": 0.2,
                      "mixing_mode": "local-TF", "electron_maxstep": 200},
        "ions": {"ion_dynamics": "bfgs"},
    },
)
print("wrote feo100.scf.in; open it and read CELL_PARAMETERS/ATOMIC_POSITIONS yourself")
