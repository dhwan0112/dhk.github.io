import numpy as np
import pandas as pd


def surface_excess(prof, solute, solvent, z_wall, z_bulk_from, z_bulk_to):
    """Gibbs relative surface excess Γ_solute^(solvent) in molecules/Å^2.

    prof: DataFrame from z_profile(); index = z, columns = species densities.
    z_wall: z of the topmost Cu plane; densities below it are ignored.
    [z_bulk_from, z_bulk_to]: window used to define bulk densities.
    The solvent's own excess is zero by construction (Gibbs convention),
    so the result does not depend on where exactly the dividing surface is."""
    bulk = prof.loc[z_bulk_from:z_bulk_to].mean()
    sel = prof.loc[z_wall:z_bulk_to]
    dz = np.diff(sel.index.values).mean()
    integrand = sel[solute] - bulk[solute] * sel[solvent] / bulk[solvent]
    return float(integrand.sum() * dz)
