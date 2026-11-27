---
layout: page
title: Research
permalink: /research/
---

<div class="prose-page">

<p>Two UROPS projects and a final-year project, all in the <a href="https://ungur-group.github.io/website/" rel="noopener">Ungur group</a>. Newest first.</p>

{% assign p = site.data.research | where: "id", "fe-oxidation" | first %}
<article class="project" id="{{ p.id }}">
    <p class="project-when">{{ p.period }}</p>
    <h2>{{ p.title }}</h2>
    <p>The aim is to simulate how an iron surface oxidises with near-DFT accuracy, on time and length scales that DFT itself cannot reach. I am building a fourth-generation magnetic high-dimensional neural network potential (4G-mHDNNP) for iron and its oxides. Atomic charges come from charge equilibration, and atomic magnetic moments enter through sACSF*, a spin-dependent atom-centred symmetry function that takes the moment as a continuous value.</p>
    <p>I implemented sACSF* in RuNNer 2.0 and in the LAMMPS ML-RUNNER interface. It agrees with an independent Python reference in all 36 tested combinations (deviation at most 10<sup>−10</sup>) and passes a finite-difference force check (relative error 8.7 × 10<sup>−8</sup>).</p>
    <p>The training data are spin-polarised PBE and PBE+U ab initio MD runs in Quantum ESPRESSO covering Fe metal, the Fe(110) surface with adsorbed O<sub>2</sub>, FeO, Fe<sub>3</sub>O<sub>4</sub> and α-Fe<sub>2</sub>O<sub>3</sub>: 28 trajectories, 5,201 frames and 214,354 atomic environments. On 1,408 test structures held out by trajectory, the short-range fit reaches a mean absolute error of 7.58 meV/atom in energy and 98.85 meV/Å in force.</p>
    <p>The continuous descriptor has not yet shown an improvement over discrete spin labels, and the model gets the energy difference between Fe<sub>3</sub>O<sub>4</sub> magnetic states wrong (DFT +284 meV/Fe, model −138 meV/Fe). MD of the Fe(110)+O surface is still exploratory, and its physical validity has not been established. The next steps are paired magnetic-state data, gas-phase O<sub>2</sub> and reactive-surface data, and a validated way to supply the moments.</p>
    <p class="project-tools">{{ p.tools }}</p>
    {% include research-links.html project=p thumbnail=true %}
</article>

{% assign p = site.data.research | where: "id", "cu-benzene-ethanol" | first %}
<article class="project" id="{{ p.id }}">
    <p class="project-when">{{ p.period }}</p>
    <h2>{{ p.title }}</h2>
    <p>I simulated a benzene/ethanol mixture in contact with copper surfaces using classical MD in LAMMPS. To separate the effect of the force field from the effect of the long-range electrostatics, I ran four combinations (OPLS-AA or TraPPE-UA, each with PPPM or MSM) through the same five-stage protocol: soft-potential relaxation, energy minimisation, staged heating, equilibration and production.</p>
    <p>I wrote the Python tooling for setting up and analysing the runs (ASE, NumPy, SciPy, pandas, matplotlib): radial distribution functions, density profiles, surface excess and interfacial tension, averaged over replicate simulations. I presented intermediate results as a poster at the NUS Science Summer Institute 2025 symposium. The <a href="{{ '/guides/lammps/' | relative_url }}">Korean LAMMPS guide</a> grew out of this project.</p>
    <p>A later check found that the copper slab in the PPPM/MSM comparison run was not a correct fcc(100) surface, so absolute first-layer values from that run should not be read as Cu(100) values. The comparison between the two methods still holds because both used the same slab. Details are in the <a href="{{ '/blog/2026/08/22/pppm-vs-msm-cu-benzene-ethanol/' | relative_url }}">PPPM and MSM note</a>.</p>
    <p>A Cu(111) comparison is planned.</p>
    <p class="project-tools">{{ p.tools }}</p>
</article>

{% assign p = site.data.research | where: "id", "dy3" | first %}
<article class="project" id="{{ p.id }}">
    <p class="project-when">{{ p.period }}</p>
    <h2>{{ p.title }}</h2>
    <p>The molecule is a triangular Dy<sub>3</sub> cluster with <em>C</em><sub>3</sub> symmetry, a candidate for a toroidal arrangement of magnetic moments. I calculated its low-lying energy spectrum, the exchange between the Dy ions, and its magnetic response.</p>
    <p>A full-cluster multireference calculation was too expensive, so I used two shortcuts. The first replaces two of the three Dy(III) ions with closed-shell Lu(III) and uses the <em>C</em><sub>3</sub> symmetry for the other two sites. The second computes the metal centre and the ligand shell separately and merges their molecular orbitals.</p>
    <p>For the Dy site I ran CASSCF(9,7) over the 4<em>f</em> shell (21 spin–orbit configurations) with the scalar-relativistic DKH Hamiltonian and the def2-SVP basis, added NEVPT2 dynamic correlation and second-order spin–orbit coupling via QDPT in ORCA, and extracted single-ion anisotropy tensors with SINGLE_ANISO.</p>
    <p>I then modelled the cluster in POLY_ANISO with a Heisenberg exchange Hamiltonian on pseudospins <em>S</em>* = 1/2 per site, scanning the isotropic exchange <em>J</em> from −0.35 to −0.75 cm<sup>−1</sup>. The best fit is <em>J</em> ≈ −0.50 to −0.55 cm<sup>−1</sup> (antiferromagnetic), with Ising-limit single-ion anisotropy (<em>g<sub>x</sub></em>, <em>g<sub>y</sub></em> ≈ 0). With these parameters the calculated χ<em>T</em>(<em>T</em>) from 0 to 300 K and <em>M</em>(<em>H</em>) at 1.9 K match unpublished experimental data, which supports a non-collinear, toroidal arrangement of the local moments in the Dy<sub>3</sub> plane.</p>
    <p class="project-tools">{{ p.tools }}</p>
</article>

<section class="project" id="presentations">
    <h2>Presentations</h2>
    <ul class="presentations">
        {% for talk in site.data.presentations %}
        <li>{{ talk.title }}, {{ talk.venue }}, {{ talk.year }}.{% if talk.path %} {% include file-link.html path=talk.path label="PDF" %}{% endif %}</li>
        {% endfor %}
    </ul>
</section>

</div>
