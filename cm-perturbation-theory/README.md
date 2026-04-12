CM Perturbation Theory — Test Suite & Verification
Paper: "Cosmological Perturbation Theory from the Clausius–Mossotti Framework: Growth Equation, Observational Tests, and a Falsifiable Prediction"
Author: Mandeep Singh
Date: 12 April 2026
Zenodo: 10.5281/zenodo.19530368
ORCID: 0009-0003-7176-2395
CM Growth Equation
δ̈ + 2H · W^(1/6) · δ̇ = 4πGρ̄δ · W^(1/3)

W = Ω_m(z),  H₀ = 70.05 km/s/Mpc,  Ω_m = 0.2784
All derived from p = e^(-3/4), zero fitted cosmological parameters.
Key Predictions
Quantity
CM
GR/ΛCDM
γ (growth index)
0.607 ± 0.010
0.549
H₀ (km/s/Mpc)
70.05
67.4
Ω_m
0.2784
0.315
S₈
0.785
0.832
σ₈(z=0)
0.815
0.811
Falsifiable prediction: γ = 0.607, testable by Euclid (2.9σ separation) and DESI within 2–3 years.
Test Results (VPS Verified)
#
Test
Result
χ²/N or σ
Status
1
Matter era CM=GR
exact at z>10
—
✅ PASS
2
S₈ vs lensing
DES match
0.52σ
✅ PASS
3
fσ₈(z) vs RSD
8 points
1.14
✅ PASS
4
H(z) chronometers
30 points
0.45
✅ PASS
5
BAO vs DESI DR1
12 points, CM > ΛCDM
1.51
✅ PASS
6
Age of universe
13.74 Gyr
0.48σ
✅ PASS
Files
File
Description
cm_complete_tests.py
Full 9-test suite (growth eq, H(z), BAO, fσ₈, S₈, age, γ)
cm_fix_sne_peaks.py
SNe Ia + CLASS peak comparison fix
cm_fix_units_refit.py
CLASS unit diagnosis + A_s refit attempt
cm_predictions.py
Complete prediction tables at all redshifts
README.md
This file
How to Run
# Requirements: Python 3.10+, scipy, numpy
# Optional: CLASS v3.3.4 (for CMB tests)

pip install numpy scipy

# Run all tests:
python cm_complete_tests.py

# Generate prediction tables:
python cm_predictions.py
CLASS Configuration (if using CMB tests)
omega_b    = 0.02237   (BBN)
omega_cdm  = 0.11424   (CM derived)
h          = 0.7005    (CM derived)
A_s        = 2.1e-9    (adopted from Planck)
n_s        = 0.9649    (adopted from Planck)
tau_reio   = 0.054     (adopted from Planck)
CLASS v3.3.4, unmodified. MD5(source/background.c) = 5156074d51a98395741ac3cf6ff48175
Tension Resolution
All three cosmological tensions share one root cause: ΛCDM's Ω_m = 0.315 is too high.
Tension
ΛCDM
CM
Improvement
H₀ (vs DESI)
4.75σ
0.02σ
eliminated
S₈ (vs DES)
3.29σ
0.52σ
eliminated
Ω_m (vs DESI+DES)
3.50σ
0.16σ
eliminated
Total σ²
77.8
8.6
89% reduced
Citation
@article{Singh2026o,
  author  = {Singh, Mandeep},
  title   = {Cosmological Perturbation Theory from the {Clausius--Mossotti} Framework: Growth Equation, Observational Tests, and a Falsifiable Prediction},
  year    = {2026},
  note    = {Zenodo, 10.5281/zenodo.19530368},
  url     = {https://github.com/singhmandy25-gif/speed-gap-framework/tree/main/cm-perturbation-theory}
}
Related Papers
2026b (H₀ derivation): Zenodo 19159035
2026d (Damru Geometry): Zenodo 19313279
2026j (CM Metric): Zenodo 19435054
2026k (CM Field Equation): Zenodo 19448621
2026n (Gravitational Redshift): Zenodo 19498973
"One equation, six tests, one prediction. The universe will decide."
