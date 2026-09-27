import numpy as np, pandas as pd, json
from profiles import frames, read_data_mol, SPECIES, MASS, FIRST_LAYER
NBLOCKS = 10
mol = read_data_mol("OPLS-AA_MSM/opls.data")
out = {}
for combo in ["OPLS-AA_PPPM", "OPLS-AA_MSM"]:
    xs, nb_list, ne_list, cu_tops = [], [], [], []
    for arr, area, zlo, zhi in frames(f"{combo}/04_production.lammpstrj"):
        ids = arr[:,0].astype(int); typ = arr[:,1].astype(int); z = arr[:,4]
        m = np.array([MASS["OPLS"][t] for t in typ]); molid = np.array([mol[i] for i in ids])
        zcu = z[typ==12].max(); cu_tops.append(zcu)
        res = {}
        for s in ("benzene","ethanol"):
            sel = np.isin(typ, list(SPECIES["OPLS"][s]))
            df = pd.DataFrame({"mol": molid[sel], "mz": m[sel]*z[sel], "m": m[sel]}); g = df.groupby("mol").sum()
            zc = (g.mz/g.m).values; res[s] = int(((zc > zcu) & (zc <= zcu+FIRST_LAYER)).sum())
        ntot = res["benzene"] + res["ethanol"]
        nb_list.append(res["benzene"]); ne_list.append(res["ethanol"]); xs.append(res["benzene"]/ntot if ntot else np.nan)
    xs = np.array(xs); nb = np.array(nb_list); ne = np.array(ne_list)
    nuse = len(xs) // NBLOCKS * NBLOCKS          # 2000 frames -> 10 blocks x 200 frames (400 ps each)
    blocks = np.nanmean(xs[:nuse].reshape(NBLOCKS, -1), axis=1)
    half = len(xs) // 2
    out[combo] = dict(x_mean=float(np.nanmean(xs)), x_block_se=float(blocks.std(ddof=1)/np.sqrt(len(blocks))),
                      nb_mean=float(nb.mean()), ne_mean=float(ne.mean()),
                      x_first_half=float(np.nanmean(xs[:half])), x_second_half=float(np.nanmean(xs[half:])),
                      blocks=[round(float(b),3) for b in blocks])
    pd.DataFrame({"frame": np.arange(len(xs)), "x_bz_first": xs, "n_bz": nb, "n_et": ne}).to_csv(f"{combo}/first_layer_timeseries.csv", index=False)
    print(combo, json.dumps(out[combo]))
with open("blocks.json", "w") as f:
    json.dump(out, f, indent=1)
