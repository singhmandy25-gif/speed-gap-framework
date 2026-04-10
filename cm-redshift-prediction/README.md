CM Redshift Prediction — Verification Scripts
Paper: Singh 2026n — "Gravitational Surface Redshift from the CM Metric: An EOS-Independent Test, Coordinate Corrections, and Interior Field Equation"
Zenodo DOI: (to be added after upload)
What This Paper Does
The CM metric predicts a different surface gravitational redshift than GR for the same neutron star (same M, same R):
GR:  z = (1 − 2GM/Rc²)^(−1/2) − 1
CM:  z = W^(−1/6) − 1,   W = (1−2ε)/(1+4ε),   ε = GM/Rc²
The difference is 28–37% for NICER-observed pulsars — EOS-independent, zero free parameters.
For PSR J0740+6620: Iron Kα line at 5.10 keV (CM) vs 4.57 keV (GR) — 540 eV gap.
Files
File
Description
Checks
verify_2026n.py
Complete verification suite (§2–§8)
61/61 pass
coordinate_correction.py
§2: R_circ = r × W^(−1/6) conversion
12 checks
redshift_prediction.py
§3–4: z_CM vs z_GR for NICER pulsars
20 checks
Quick Start
python3 verify_2026n.py
Expected output: FINAL SCORE: 61/61 PASS, 0/61 FAIL
Key Results
Quantity
GR
CM
Difference
Test
Photon sphere (circ.)
1.500 r_s
2.010 r_s
+34%
—
Shadow size
2.598 r_s
2.857 r_s
+10.0%
EHT
ISCO (circ.)
3.000 r_s
3.308 r_s
+10.3%
—
ISCO frequency
f_GR
0.828 f_GR
−17.2%
LIGO
Surface redshift (J0740)
0.401
0.254
−36.6%
X-ray lines
Iron Kα (J0740)
4.57 keV
5.10 keV
+540 eV
XRISM (108σ)
Dependencies
Python 3.6+
NumPy
Author
Mandeep Singh
Independent Researcher, Haryana, India
ORCID: 0009-0003-7176-2395
Email: singhmandy25@gmail.com
