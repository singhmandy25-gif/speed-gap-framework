cm-alpha-s-derivation
Verification code for: Singh 2026v — "The Strong Coupling Constant from Clausius-Mossotti Geometry: Two Derivations, Zero Parameters"
DOI: 10.5281/zenodo.19740577
What this paper derives
The strong coupling constant α_s from the CM framework (OE + W = 1) with zero fitted parameters.
Method
α_s (CM)
α_s (QCD)
Match
Interior field eq (quarks, 1 GeV)
0.496
0.47 ± 0.04
5.4%
Transmission formula (1 GeV)
0.462
0.47 ± 0.04
1.6%
OE profile (7-scale average)
—
—
8.1%
Barycenter mirror (1.78 GeV)
0.316
0.330
4.2%
Λ_QCD = m_p/(D+1)
234.6 MeV
200–340 MeV
Inside range
Files
Script
What it verifies
verify_alpha_s.py
Both running formulas (D1 + D2) at 7 QCD energies
verify_barycenter.py
Mirror symmetry, β²=1/10, OE=1/4, α_s=1/√10
verify_lambda_qcd.py
Λ_QCD = m_p/4, OE×W parabola, quark landscape
interior_field_eq.py
Self-coupled ODE, wall→centre profile, α_s at quarks
complete_verification.py
Runs ALL tests, prints pass/fail summary
Usage
Bash
All scripts print results to stdout. No external data files needed.
Inputs (zero fitted parameters)
Constant
Value
Source
m_p
938.272 MeV
PDG 2024
m_e
0.511 MeV
PDG 2024
R_p
0.881 fm
CODATA 2018
α
1/137.036
CODATA 2018
ℏc
197.327 MeV·fm
CODATA 2018
D
3
spatial dimensions
Framework
Part of the Speed Gap Framework.
Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
