Damru Geometry — Verification Scripts
Paper: Singh (2026d) "Damru Geometry: From Sphere Fractions to Quark Charges, Confinement, and Binding Margins"
Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
Related: Singh 2026b (Zenodo) | Singh 2026c (Zenodo)
What is this?
The Damru Geometry predicts specific radial positions inside the proton from pure sphere algebra:
Position
f = ξ³
r (fm)
Method
Down quark
1/3
0.582
f = ξ³, R = 0.84 fm
Neck (equal split)
1/2
0.667
f = ξ³
Up quark
2/3
0.734
f = ξ³
These scripts verify these predictions against published experimental data and QCD calculations.
Scripts
1. charge_density_check.py
What: Fourier-transforms proton electromagnetic form factor → charge density ρ(r)
Data: Kelly (2004) and Arrington (2004) parametrizations
Result: Charge density is smooth — no structure at predicted positions
Status: Scope boundary (geometry describes forces, not charge cloud)
2. pressure_check.py
What: Computes pressure distribution from Burkert et al. (Nature 557, 396, 2018) D-term
Data: Tripole D-term parametrization (d₁ = −1.47, M²_D = 1.39 GeV²)
Result: Maximum confining pressure at r = 0.641 fm vs Neck = 0.667 fm → 3.9% match
Status: Strong positive — independent verification
3. cornell_potential.py
What: Solves radial Schrödinger equation with Cornell potential V(r) = −4αs/(3r) + σr
Parameters: αs = 0.39, σ = 0.18 GeV², m_q = 0.336 GeV (standard QCD values)
Result: Ground state peak at r = 0.696 fm vs Neck = 0.667 fm → 4.3% match
Status: Supportive — quantum mechanics agrees with geometry
Requirements
python >= 3.8
numpy
scipy
matplotlib
Run
python charge_density_check.py    # → saves charge_density.png
python pressure_check.py          # → saves pressure_distribution.png
python cornell_potential.py       # → saves cornell_wavefunction.png
Summary of Results
Check
Prediction
Data
Match
Status
Pressure: max confinement
Neck = 0.667 fm
0.641 fm (Burkert 2018)
3.9%
Strong positive
Cornell: wavefunction peak
Neck = 0.667 fm
0.696 fm (QCD standard)
4.3%
Supportive
Cornell: excited node
d-quark = 0.582 fm
0.618 fm
6.2%
Supportive
Charge density
Structure at 0.582, 0.734 fm
Smooth (Kelly 2004)
None
Scope boundary
Proton charge radius
0.778 fm
0.841 fm (measured)
7.5%
Partial
Three independent methods (geometry, experiment, QCD) converge on the same radial region: 0.64–0.70 fm.
References
Burkert, V.D., Elouadrhiri, L., Girod, F.X. (2018). Nature 557, 396–399.
Kelly, J.J. (2004). Phys. Rev. C 70, 068202.
Arrington, J. (2004). Phys. Rev. C 69, 022201.
Djukanovic, D. et al. (2024). Phys. Rev. Lett. 132, 211901.
