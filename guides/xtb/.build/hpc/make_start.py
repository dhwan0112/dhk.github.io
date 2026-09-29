"""Build the alanine dipeptide (Ace-Ala-NMe) starting geometry.

Writes ala.xyz and backbone.json (0-based atom indices for phi/psi).
Heavy-atom indices follow the SMILES order; AddHs appends hydrogens after them,
so the indices stay valid for every xtb/ORCA trajectory started from ala.xyz.
"""
import json

from rdkit import Chem
from rdkit.Chem import AllChem

SMILES = "CC(=O)N[C@@H](C)C(=O)NC"
# CH3-C(=O)-N-CA(CB)-C(=O)-N-CH3
#  0   1  2  3  4  5  6  7  8  9
PATTERN = Chem.MolFromSmarts("[CH3]C(=O)N[CH1]([CH3])C(=O)N[CH3]")

mol = Chem.MolFromSmiles(SMILES)
match = mol.GetSubstructMatch(PATTERN)
assert len(match) == 10, match
c_ace, n1, ca, c2, n2 = match[1], match[3], match[4], match[6], match[8]

molh = Chem.AddHs(mol)
params = AllChem.ETKDGv3()
params.randomSeed = 20260928
cids = AllChem.EmbedMultipleConfs(molh, numConfs=20, params=params)
res = AllChem.MMFFOptimizeMoleculeConfs(molh, maxIters=2000)
best = min(cids, key=lambda c: res[c][1])
conf = molh.GetConformer(best)

with open("ala.xyz", "w") as f:
    f.write(f"{molh.GetNumAtoms()}\nalanine dipeptide, RDKit ETKDG+MMFF seed 20260928\n")
    for a in molh.GetAtoms():
        p = conf.GetAtomPosition(a.GetIdx())
        f.write(f"{a.GetSymbol():2s} {p.x:12.6f} {p.y:12.6f} {p.z:12.6f}\n")

with open("backbone.json", "w") as f:
    json.dump({"phi": [c_ace, n1, ca, c2], "psi": [n1, ca, c2, n2],
               "natoms": molh.GetNumAtoms()}, f, indent=1)

print("wrote ala.xyz", molh.GetNumAtoms(), "atoms; phi", [c_ace, n1, ca, c2],
      "psi", [n1, ca, c2, n2])
