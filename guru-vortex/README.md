Guru Vortex Model — Verification Scripts
Singh 2026e: Guru Vortex Model — Pion Cloud, Standing Wave Boundaries, and the Cosmic-Nuclear Connection
Paper: [Zenodo DOI pending]
Prior work: Singh 2026d · Singh 2026b
Author: Mandeep Singh · ORCID: 0009-0003-7176-2395
Date: 30 March 2026
What is the Guru Vortex Model?
The model treats the proton interior as three counter-rotating gluon field layers (like Jupiter's atmospheric bands), with quarks as stable Lagrange points at the shear boundaries. Named after Bṛhaspati (बृहस्पति, Jupiter) — known as Guru (गुरु, "teacher") in Indian tradition.
Key Results
Check
Before (2026d)
After (2026e)
Match
Neutron ⟨r²⟩ sign
Wrong sign
−0.117 fm²
0.5%
Proton charge radius
7.5% off
0.839 fm
0.2%
μ_p/μ_n ratio
No formula
−1.456
0.3%
Cosmic-Nuclear Connection: The vortex rotation profile ω ∝ 1/r^(1-p), where p = e^(-3/4) is the same exponent that gives H₀ = 72.94 km/s/Mpc at cosmic scale.
Scripts
pion_cloud_geometry.py
Two-sphere model: inner proton (0.84 fm) + outer pion cloud (~1.12 fm).
One parameter set (P=0.25, r_π=1.0 fm) fixes neutron sign AND proton radius.
python pion_cloud_geometry.py
guru_vortex_magnetic_moment.py
Counter-rotating vortex model for magnetic moment ratio.
Includes: discrete model, continuous check, cosmic connection, spin derivation.
python guru_vortex_magnetic_moment.py
Requirements
Python 3.6+
NumPy
pip install numpy
Honest Caveats
Pion cloud (Level B): Standard nuclear physics parameters, not tuned. Robust.
μ ratio discrete (Level B→C): 0.3% match with sharp boundaries. Continuous model gives 34% off — result is model-dependent.
Absolute μ values (Level C): ~25% off measured values. Ratio cancels mass factor.
ω ∝ 1/r^(1-p) (Level C): Pattern observed, mechanism not derived.
Citation
M. Singh, "Guru Vortex Model: Pion Cloud, Standing Wave Boundaries, 
and the Cosmic-Nuclear Connection," Zenodo (2026e).
File Structure
speed-gap-framework/
├── damru-verification/              ← Singh 2026d
│   ├── charge_density_check.py
│   ├── pressure_check.py
│   ├── cornell_potential.py
│   └── README.md
│
├── guru-vortex/                     ← Singh 2026e (this folder)
│   ├── pion_cloud_geometry.py
│   ├── guru_vortex_magnetic_moment.py
│   └── README.md
