"""Recompute z-profiles for the 4 combos straight from the production dumps.
Outputs per combo: mass density (g/cm3) per species on 0.25 A bins, molecule-COM
number density per species, and first-layer / bulk benzene mole fractions."""
import numpy as np, pandas as pd, io, sys, json

SPECIES = {
  "OPLS":  {"benzene": {1,2}, "ethanol": set(range(3,12)), "copper": {12}},
  "TraPPE":{"benzene": {1},   "ethanol": {2,3,4,5},        "copper": {6}},
}
MASS = {
  "OPLS":  {1:12.011,2:1.008,3:12.011,4:12.011,5:15.999,6:1.008,7:1.008,8:1.008,9:1.008,10:1.008,11:1.008,12:63.546},
  "TraPPE":{1:13.019,2:15.035,3:14.027,4:15.999,5:1.008,6:63.546},
}
NA = 6.02214076e23
DZ = 0.25

def read_data_mol(path):
    """id -> mol-id from a LAMMPS data file (atom_style full)."""
    lines = open(path).read().splitlines()
    i = next(k for k,l in enumerate(lines) if l.startswith("Atoms"))
    mol = {}
    for l in lines[i+1:]:
        p = l.split()
        if not p: 
            if mol: break
            continue
        if not p[0].isdigit(): break
        mol[int(p[0])] = int(p[1])
    return mol

def frames(path):
    txt = open(path).read()
    blocks = txt.split("ITEM: TIMESTEP")[1:]
    for b in blocks:
        lines = b.split("\n")          # lines[0] = "", lines[1] = timestep value
        nat = int(lines[3]); xlo,xhi = map(float, lines[5].split())
        ylo,yhi = map(float, lines[6].split()); zlo, zhi = map(float, lines[7].split())
        arr = np.loadtxt(io.StringIO("\n".join(lines[9:9+nat])))
        yield arr, (xhi-xlo)*(yhi-ylo), zlo, zhi

def run(combo, ff, datafile):
    mol = read_data_mol(datafile)
    edges = None; nfr = 0
    mass_hist = {s: 0 for s in SPECIES[ff]}; com_hist = {s: 0 for s in ("benzene","ethanol")}
    cu_top = []; liq_top = []
    for arr, area, zlo, zhi in frames(f"{combo}/04_production.lammpstrj"):
        if edges is None:
            edges = np.arange(zlo, zhi + DZ, DZ); centres = 0.5*(edges[:-1]+edges[1:])
        ids = arr[:,0].astype(int); typ = arr[:,1].astype(int); z = arr[:,4]
        m = np.array([MASS[ff][t] for t in typ])
        for s, ts in SPECIES[ff].items():
            sel = np.isin(typ, list(ts))
            h,_ = np.histogram(z[sel], bins=edges, weights=m[sel]); mass_hist[s] = mass_hist[s] + h
        cu = np.isin(typ, list(SPECIES[ff]["copper"]))
        cu_top.append(z[cu].max()); liq_top.append(z[~cu].max())
        # molecule COM (organic only)
        molid = np.array([mol[i] for i in ids])
        for s in ("benzene","ethanol"):
            sel = np.isin(typ, list(SPECIES[ff][s]))
            df = pd.DataFrame({"mol": molid[sel], "mz": m[sel]*z[sel], "m": m[sel]})
            g = df.groupby("mol").sum(); zc = (g.mz/g.m).values
            h,_ = np.histogram(zc, bins=edges); com_hist[s] = com_hist[s] + h
        nfr += 1
    vol_cm3 = area*DZ*1e-24
    out = pd.DataFrame(index=pd.Index(centres, name="z"))
    for s in mass_hist: out[f"rho_{s}"] = mass_hist[s]/(nfr*vol_cm3*NA)       # g/cm3
    for s in com_hist:  out[f"n_{s}"]   = com_hist[s]/(nfr*area*DZ)            # molecules/A^3
    zcu = float(np.mean(cu_top)); ztop = float(np.mean(liq_top))
    # first layer: COM within 5 A of Cu top; bulk: middle third of the liquid film
    first = (out.index > zcu) & (out.index <= zcu+5.0)
    bulk  = (out.index > zcu+10.0) & (out.index < ztop-8.0)
    nb1, ne1 = out.n_benzene[first].sum(), out.n_ethanol[first].sum()
    nbb, neb = out.n_benzene[bulk].mean(), out.n_ethanol[bulk].mean()
    stats = dict(combo=combo, frames=nfr, cu_top=round(zcu,2), liquid_top=round(ztop,2),
                 x_bz_first=round(nb1/(nb1+ne1),3), x_bz_bulk=round(nbb/(nbb+neb),3),
                 n_first_bz=round(nb1*area,1), n_first_et=round(ne1*area,1),
                 rho_bulk_total=round(float((out.rho_benzene+out.rho_ethanol)[bulk].mean()),3),
                 rho_bulk_bz=round(float(out.rho_benzene[bulk].mean()),3), rho_bulk_et=round(float(out.rho_ethanol[bulk].mean()),3))
    out.to_csv(f"{combo}/zprofile_recomputed.csv", float_format="%.6f")
    return stats

if __name__ == "__main__":
    res = []
    for combo, ff, dfile in [("OPLS-AA_PPPM","OPLS","OPLS-AA_MSM/opls.data"),("OPLS-AA_MSM","OPLS","OPLS-AA_MSM/opls.data"),
                             ("TraPPE-UA_PPPM","TraPPE","TraPPE-UA_MSM/trappe.data"),("TraPPE-UA_MSM","TraPPE","TraPPE-UA_MSM/trappe.data")]:
        s = run(combo, ff, dfile); print(json.dumps(s)); res.append(s)
    json.dump(res, open("stats.json","w"), indent=1)
