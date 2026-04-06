CM Metric — From Clausius–Mossotti to Schwarzschild
Paper: Singh 2026j (V2: 6 April 2026)
Author: Mandeep Singh
ORCID: 0009-0003-7176-2395
Zenodo DOI: 10.5281/zenodo.19425285
The Formula
ds² = W^(1/3) c²dt² − W^(−1/3)(dr² + r²dΩ²)

W = (1 − β²)/(1 + 2β²)      β² = 2GM/(rc²)
OE = 1 − W = 3β²/(1 + 2β²)  OE + W = 1 (always)
Three steps. Zero parameters.
Clausius–Mossotti (1879) → Schwarzschild (1916).
Results Summary
Weak Field: 6/6 Classical Tests PASS (CM = GR)
#
Test
CM
GR
Observed
Type
1
Mercury precession
42.99"/cen
42.98"/cen
42.98 ± 0.04
Direct
2
Light bending
1.7517"
1.7517"
1.75 ± 0.06"
Direct
3
Gravitational redshift
2.46×10⁻¹⁵
2.46×10⁻¹⁵
2.57 ± 0.26×10⁻¹⁵
Direct
4
Shapiro delay
247.3 μs
247.3 μs
250 ± 5 μs
Direct
5
Binary pulsar decay
−2.404×10⁻¹²
−2.404×10⁻¹²
−2.421×10⁻¹²
Direct
6
GW speed
c
c
|v−c|/c < 5×10⁻¹⁶
Direct
Strong Field: 5 Testable Predictions (CM ≠ GR)
Quantity
GR
CM
Deviation
Test by
Photon sphere
1.500 r_s
1.414 r_s (= √2)
−5.7%
EHT
BH shadow
2.598 r_s
2.857 r_s
+10.0%
EHT
ISCO radius
3.000 r_s
2.811 r_s
−6.3%
LIGO
ISCO binding energy
5.72%
5.45%
−4.7%
LIGO
ISCO frequency
f_GR
0.828 f_GR
−17.2%
LIGO
Rotation (V2 — Section 4.5)
Result
CM
GR
Status
Frame dragging (slow)
ω = 2GJ/(c²r³)
ω = 2GJ/(c²r³)
✅ Identical
Hidden symmetry: ν'+λ'
= 0 (exact)
≠ 0 (generally)
CM special!
g_tt × g_rr
= 1 (exact)
≠ 1 (generally)
CM special!
Gravity Probe B
37 mas/yr
37 mas/yr
✅ CM = GR
Event horizon (spinning)
ABSENT (Δ>0)
Present (Kerr)
🔮 Prediction!
GW echoes
Predicted
Not expected
🔮 LIGO O5 test
Files in This Folder
File
Description
Singh_2026j_COMPLETE.html
Full paper (8 chapters + §4.5 rotation)
cm_verify_all.py
Master verification: 36 tests (V2)
cm_kerr_analysis.py
Rotation analysis: slow + full, no-horizon prediction
cm_metric_12tests.py
All 12 static tests
cm_photon_shadow_isco.py
Photon sphere + shadow + ISCO
cm_mercury_binet.py
Mercury precession (12 systems)
README.md
This file
How to Verify
# Run master verification (36 tests):
python3 cm_verify_all.py

# Run rotation analysis:
python3 cm_kerr_analysis.py
Citation
@article{Singh2026j,
  author  = {Singh, Mandeep},
  title   = {The CM Metric: From Clausius--Mossotti to Schwarzschild},
  year    = {2026},
  journal = {Zenodo},
  doi     = {10.5281/zenodo.19425285},
  note    = {Speed Gap Framework, Paper 2026j V2}
}
Related Papers
2026a — Speed Gap Framework: DOI: 10.5281/zenodo.19142702
2026b v3 — Cosmic OE: DOI: 10.5281/zenodo.19244123
2026d — Damru Geometry: DOI: 10.5281/zenodo.19313279
2026e — Guru Vortex: DOI: 10.5281/zenodo.19332481
2026h — Unified Lagrangian: DOI: 10.5281/zenodo.19400730
2026i — Dynamical Lagrangian: DOI: 10.5281/zenodo.19414588
Mandeep Singh | Haryana, India | April 2026
"145 years. Zero parameters. Atom to black hole. No horizon."
