---
layout: page
title: Research
permalink: /research/
---

<div class="prose-page">

<p>Two UROPS projects and a final-year project, all in the <a href="https://ungur-group.github.io/website/" rel="noopener">Ungur group</a>. Newest first.</p>

<article class="project" id="fe-oxidation">
    <p class="project-when">Final-year project, CM4288. AY2025/26 Semester 2 to present.</p>
    <h2>A reactive machine-learning potential for iron oxidation</h2>
    <p>The aim is to simulate the oxidation of iron with near-DFT accuracy on time and length scales that DFT itself cannot reach. I generate reference data with periodic DFT in Quantum ESPRESSO and use it to train a machine-learning interatomic potential. The potential has to handle bond breaking and the growth of the oxide layer.</p>
    <p class="project-tools">Quantum ESPRESSO, machine-learning interatomic potentials, reactive MD.</p>
</article>

<article class="project" id="cu-benzene-ethanol">
    <p class="project-when">UROPS, CM3288 and CM3289. AY2024/25 Semester 2 to AY2025/26 Semester 1.</p>
    <h2>Benzene and ethanol on Cu(100) and Cu(111)</h2>
    <p>I simulated a benzene/ethanol mixture in contact with copper surfaces using classical MD in LAMMPS. To separate the effect of the force field from the effect of the long-range electrostatics, I ran four combinations (OPLS-AA or TraPPE-UA, each with PPPM or MSM) through the same five-stage protocol: soft-potential relaxation, energy minimisation, staged heating, equilibration and production.</p>
    <p>I wrote the Python tooling for setting up and analysing the runs (ASE, NumPy, SciPy, pandas, matplotlib): radial distribution functions, density profiles, surface excess and interfacial tension, averaged over replicate simulations. I presented intermediate results as a poster at the NUS Science Summer Institute 2025 symposium. The <a href="{{ '/guides/lammps/' | relative_url }}">Korean LAMMPS guide</a> grew out of this project.</p>
    <p>A later check found that the copper slab in the PPPM/MSM comparison run was not a correct fcc(100) surface, so absolute first-layer values from that run should not be read as Cu(100) values. The comparison between the two methods still holds because both used the same slab. Details are in the <a href="{{ '/blog/2026/08/22/pppm-vs-msm-cu-benzene-ethanol/' | relative_url }}">PPPM and MSM note</a>.</p>
    <p class="project-tools">LAMMPS, OPLS-AA, TraPPE-UA, PPPM, MSM, Python.</p>
</article>

<article class="project" id="dy3">
    <p class="project-when">UROPS, CM2288. AY2023/24 Semester 2.</p>
    <h2>Exchange and anisotropy in a Dy<sub>3</sub> triangle</h2>
    <p>The molecule is a triangular Dy<sub>3</sub> cluster with <em>C</em><sub>3</sub> symmetry, a candidate for a toroidal arrangement of magnetic moments. I calculated its low-lying energy spectrum, the exchange between the Dy ions, and its magnetic response.</p>
    <p>A full-cluster multireference calculation was too expensive, so I used two shortcuts. The first replaces two of the three Dy(III) ions with closed-shell Lu(III) and uses the <em>C</em><sub>3</sub> symmetry for the other two sites. The second computes the metal centre and the ligand shell separately and merges their molecular orbitals.</p>
    <p>For the Dy site I ran CASSCF(9,7) over the 4<em>f</em> shell (21 spin–orbit configurations) with the scalar-relativistic DKH Hamiltonian and the def2-SVP basis, added NEVPT2 dynamic correlation and second-order spin–orbit coupling via QDPT in ORCA, and extracted single-ion anisotropy tensors with SINGLE_ANISO.</p>
    <p>I then modelled the cluster in POLY_ANISO with a Heisenberg exchange Hamiltonian on pseudospins <em>S</em>* = 1/2 per site, scanning the isotropic exchange <em>J</em> from −0.35 to −0.75 cm<sup>−1</sup>. The best fit is <em>J</em> ≈ −0.50 to −0.55 cm<sup>−1</sup> (antiferromagnetic), with Ising-limit single-ion anisotropy (<em>g<sub>x</sub></em>, <em>g<sub>y</sub></em> ≈ 0). With these parameters the calculated χ<em>T</em>(<em>T</em>) from 0 to 300 K and <em>M</em>(<em>H</em>) at 1.9 K match unpublished experimental data, which supports a non-collinear, toroidal arrangement of the local moments in the Dy<sub>3</sub> plane.</p>
    <p class="project-tools">ORCA (CASSCF, NEVPT2, QDPT), SINGLE_ANISO, POLY_ANISO.</p>
</article>

</div>
