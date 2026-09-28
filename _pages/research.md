---
layout: page
title: Research
description: Undergraduate research in computational chemistry, Department of Chemistry, NUS
permalink: /research/
---

<section class="current-research">
    <div class="container">
        <h2 class="section-title">Research Projects</h2>
        <p class="contact-subtitle" style="text-align:center;margin-bottom:2rem;">Two UROPS projects and a final-year project under A/P Liviu Ungur (<a href="https://ungur-group.github.io/website/" target="_blank" rel="noopener">Ungur Group</a>).</p>
        <div class="research-list">

            <div class="research-item">
                <div class="research-number">01</div>
                <div class="research-content">
                    <h3>Anisotropic Magnetism of a Dy(III) Trinuclear Cluster</h3>
                    <p class="research-meta">UROPS CM2288 · AY2023/24 Sem 2 · Grade: B+</p>
                    <p class="research-description">
                        Evaluated the low-lying energy spectrum, magnetic exchange, and anisotropic magnetic response of a Dy<sub>3</sub> triangular cluster (<em>C</em><sub>3</sub> point-group symmetry) — a candidate for toroidal magnetic moment behaviour and single-molecule magnetism. Made the full-cluster <em>ab initio</em> treatment tractable through two cost-reduction strategies: (i) replacing two of the three Dy sites with closed-shell Lu(III) to exploit the <em>C</em><sub>3</sub> symmetry, and (ii) a fragmentation scheme that computes the metal centre and the ligand shell separately and merges their molecular orbitals.
                    </p>
                    <p class="research-description">
                        <strong>Electronic structure (ORCA):</strong> CASSCF(9,7) over the Dy 4<em>f</em> shell (21 spin–orbit configurations), scalar-relativistic DKH Hamiltonian with def2-SVP basis, NEVPT2 dynamic correlation, second-order spin–orbit coupling via QDPT, and single-ion anisotropy tensors extracted with SINGLE_ANISO.
                    </p>
                    <p class="research-description">
                        <strong>Polynuclear response (POLY_ANISO):</strong> Heisenberg-type exchange Hamiltonian on pseudospins <em>S</em>* = 1/2 per Dy site; isotropic exchange parameter <em>J</em> scanned over −0.35 to −0.75 cm<sup>−1</sup> and fitted to experiment. Best fit <em>J</em> ≈ −0.50 to −0.55 cm<sup>−1</sup> (antiferromagnetic) with Ising-limit single-site anisotropy (<em>g<sub>x</sub></em>, <em>g<sub>y</sub></em> ≈ 0); computed χ<em>T</em>(<em>T</em>) (0–300 K) and low-<em>T</em> <em>M</em>(<em>H</em>) at 1.9 K reproduced unpublished experimental data with excellent agreement, supporting a non-colinear (toroidal) arrangement of local moments in the Dy<sub>3</sub> plane.
                    </p>
                    <div class="research-tags">
                        <span class="tag">ORCA</span>
                        <span class="tag">CASSCF / NEVPT2</span>
                        <span class="tag">QDPT-SOC</span>
                        <span class="tag">SINGLE_ANISO</span>
                        <span class="tag">POLY_ANISO</span>
                        <span class="tag">Lanthanide SMM</span>
                    </div>
                </div>
            </div>

            <div class="research-item">
                <div class="research-number">02</div>
                <div class="research-content">
                    <h3>Molecular Dynamics of an Organic Solvent System at a Cu Surface</h3>
                    <p class="research-meta">UROPS CM3288 / CM3289 · AY2024/25 Sem 2 – AY2025/26 Sem 1 · Grade: A / A</p>
                    <p class="research-description">
                        Investigated the behaviour of a benzene/ethanol mixture in contact with Cu(100) and Cu(111) surfaces using classical molecular dynamics in LAMMPS. Compared four framework combinations — OPLS-AA vs TraPPE-UA force fields × PPPM vs MSM electrostatics — under a unified five-stage protocol (soft relaxation → energy minimisation → staged heating → equilibration → production), so that the effect of force-field choice and long-range Coulomb treatment on interfacial adsorption can be analysed independently.
                    </p>
                    <p class="research-description">
                        Developed Python pipelines (ASE, NumPy, SciPy, pandas, matplotlib) for trajectory pre- and post-processing, and for automated analysis of interfacial observables (radial distribution functions, density profiles, surface excess, interfacial tension) across replicate simulations. Intermediate results presented as a poster at the <strong>NUS Science Summer Institute 2025 Symposium</strong>. A self-contained Korean LAMMPS guide derived from this work is published under <a href="{{ '/guides/lammps/' | relative_url }}">/guides/lammps/</a>.
                    </p>
                    <div class="research-tags">
                        <span class="tag">LAMMPS</span>
                        <span class="tag">Cu(100) · Cu(111)</span>
                        <span class="tag">OPLS-AA</span>
                        <span class="tag">TraPPE-UA</span>
                        <span class="tag">PPPM · MSM</span>
                        <span class="tag">Interfacial MD</span>
                    </div>
                </div>
            </div>

            <div class="research-item">
                <div class="research-number">03</div>
                <div class="research-content">
                    <h3>Reactive Machine-Learning Force Field for Iron Oxidation</h3>
                    <p class="research-meta">Final Year Project CM4288 · AY2025/26 Sem 2 – Present</p>
                    <p class="research-description">
                        Developing a reactive machine-learning interatomic potential to describe the oxidation of iron, bridging <em>ab initio</em> accuracy with the time- and length-scales accessible to molecular dynamics. Reference data are generated from periodic DFT in Quantum ESPRESSO and used to train an ML force field capable of capturing bond-breaking and oxide-layer growth — the broader goal is to connect electronic-structure predictions to macroscopic iron-oxidation kinetics.
                    </p>
                    <div class="research-tags">
                        <span class="tag">Quantum ESPRESSO</span>
                        <span class="tag">Machine-Learning Potential</span>
                        <span class="tag">Reactive MD</span>
                        <span class="tag">Fe Oxidation</span>
                    </div>
                </div>
            </div>

        </div>
    </div>
</section>
