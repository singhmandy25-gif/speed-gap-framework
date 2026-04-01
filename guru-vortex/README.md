Guru Vortex Model — Verification Scripts (V2: 1 April 2026)
Singh 2026e V2: Guru Vortex Model — Pion Cloud, Standing Wave Boundaries, and the Cosmic-Nuclear Connection
Paper: DOI: 10.5281/zenodo.19332481
Prior: Singh 2026d · Singh 2026b
Author: Mandeep Singh · ORCID: 0009-0003-7176-2395
EPJC: Under Review (EPJC-26-03-414)
Key Results (V2 — 1 April 2026)
Check
Result
Match
Neutron ⟨r²⟩ sign
−0.117 fm²
0.5% (zero free params!)
Proton charge radius
0.839 fm
0.2% (zero free params!)
μ_p/μ_n ratio
−1.456
0.3% (C+E=1 derived)
H₀ (cosmic scale)
72.94 km/s/Mpc
0.09σ (same p!)
V2 New Discoveries (1 April 2026)
1. P = 1/4 is NOT a free parameter
P = 1 − f_horizon = 1 − 3/4 = 1/4. The volume outside the confinement horizon = leakable fraction = pion fluctuation probability. Both neutron and proton fixes now have zero free parameters.
2. WHY (1−p) sets nuclear rotation — C + E = 1
Virial theorem: Compression + Expansion = 1. Cosmic E = p = 0.4724 (expansion → H₀). Nuclear C = (1−p) = 0.5276 (compression → rotation). Proton = compressed matter; rotation is how compression manifests dynamically. ω ∝ 1/r^(1−p) is a consequence, not a coincidence.
3. Discrete model = correct physics
Standing wave nodes = mathematical zeros = zero width. All continuous profiles (Gaussian, Lorentzian, exponential, density-pit) give μ ratio ~−2.0 (34–38% off). Only exact point nodes give −1.456. The discrete model is not an approximation — it is the correct physics of wave nodes.
4. Absolute μ path found
Guru ratio (−1.456) + measured sum (μ_p + μ_n = 0.8798) → μ_p = 2.809 (0.6%), μ_n = −1.929 (0.9%). Currently circular; sum derivable from published pion cloud + relativistic corrections.
Scripts
pion_cloud_geometry.py
Two-sphere model with P = 1 − f_horizon = 1/4 (derived, not fitted).
Zero free parameters for neutron sign fix AND proton radius fix.
python pion_cloud_geometry.py
guru_vortex_magnetic_moment.py
Counter-rotating vortex model with C+E=1 derivation.
Includes: discrete vs continuous proof, absolute μ path, cosmic connection.
python guru_vortex_magnetic_moment.py
Requirements
pip install numpy
Open Questions Status
#
Question
Status
1
Why (1−p) = rotation?
✅ Solved — C+E=1 (Virial)
2
Discrete vs continuous?
✅ Solved — nodes = zero width
3
Absolute μ values?
🔄 Path found — ratio + sum → <1%
4
Quark masses?
❓ Open — direction right, magnitude off
5
P = 0.25 from geometry?
✅ Solved — 1 − f_horizon = 1/4
File Structure
speed-gap-framework/
├── damru-verification/              ← Singh 2026d
│   ├── charge_density_check.py
│   ├── pressure_check.py
│   ├── cornell_potential.py
│   └── README.md
│
├── guru-vortex/                     ← Singh 2026e V2 (this folder)
│   ├── pion_cloud_geometry.py
│   ├── guru_vortex_magnetic_moment.py
│   └── README.md
Citation
M. Singh, "Guru Vortex Model: Pion Cloud, Standing Wave Boundaries, 
and the Cosmic-Nuclear Connection," V2, Zenodo (2026e).
DOI: 10.5281/zenodo.19332481
