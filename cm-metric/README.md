CM Metric — From Clausius–Mossotti to Schwarzschild
Paper: Singh 2026j
Author: Mandeep Singh
ORCID: 0009-0003-7176-2395
Zenodo DOI: 10.5281/zenodo.19425285
The Formula
ds² = W^(1/3) c²dt² − W^(−1/3)(dr² + r²dΩ²)

W = (1 − β²)/(1 + 2β²)      β² = 2GM/(rc²)
OE = 1 − W = 3β²/(1 + 2β²)   OE + W = 1 (always)
Three steps. Zero parameters. Clausius–Mossotti (1879) → Schwarzschild (1916).
W(r) = CM compression function (from 1879 dielectric theory)
W^(1/3) = per-dimension share (D = 3 spatial dimensions)
Assign to time = gravity affects all dimensions equally
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
EHT Shadow Comparison
Black Hole
GR
CM
Observed
Status
M87*
39.7 μas
43.6 μas
42 ± 3 μas
✅ CM within error
SgrA*
50.7 μas
55.7 μas
48.7 ± 7 μas
⚠️ Marginal
Key Physics
Why W^(1/3)?
  W = total 3D compression (Clausius–Mossotti)
  W^(1/3) = share per dimension (depolarisation factor N = 1/D)
  Time gets same share → g_tt = W^(1/3) ≈ 1 − 2GM/(rc²)
  = Schwarzschild at 1PN. Zero parameters.

Why 2/3 became 1?
  L_dyn (paper 2026i): space only → 4π (sphere) → 2/3 × GR
  CM metric (this paper): space + time → 6π (sphere + circle) → 1 × GR
  Missing 1/3 = time dimension = W^(1/3) on g_tt

OE form:
  g_tt = (1 − OE)^(1/3)
  Time dilation = OE/3 = one dimension's share of orbital emptiness
Connection to Framework
Layer
Paper
Formula
Key Result
1. Foundation
2026a
OE + W = 1
Complementarity
2. Cosmology
2026a–b
Ω_DE = OE(β_cosmic)
H₀ = 70.05 km/s/Mpc
3. Nuclear
2026d–e
f = 3/4 (proton horizon)
μ_p/μ_n = −1.456
4. Static
2026h
L = OE − W
Action S = nh
5. Dynamics
2026i
L_dyn = T_OE + V/W
+2/3 × GR, universal
6. Spacetime
2026j
ds² = W^(1/3)c²dt² − ...
Full GR + predictions
Files in This Folder
File
Description
Singh_2026j_COMPLETE.html
Full paper (8 chapters, 23 SVGs, 23 references)
cm_verify_all.py
Master verification: 29 tests, every number checked
cm_metric_12tests.py
All 12 tests in one script
cm_photon_shadow_isco.py
Photon sphere + shadow + ISCO computation
cm_mercury_binet.py
Mercury precession (Binet equation, λ=3)
README.md
This file
How to Verify
import numpy as np

c = 2.998e8; G = 6.674e-11; M_sun = 1.989e30

def W(r, M):
    b2 = 2*G*M/(r*c**2)
    return (1-b2)/(1+2*b2)

# Mercury: g_tt should equal Schwarzschild at 1PN
r_merc = 5.79e10  # meters
M = M_sun
eps = G*M/(r_merc*c**2)

gtt_CM = W(r_merc, M)**(1/3)
gtt_GR = 1 - 2*eps

print(f"g_tt(CM)  = {gtt_CM:.12f}")
print(f"g_tt(GR)  = {gtt_GR:.12f}")
print(f"Match: {abs(gtt_CM-gtt_GR):.2e}")
# Output: Match: ~10⁻¹⁵ (identical at 1PN)

# Photon sphere: 8ε² = 1 → r = √2 r_s
eps_ph = 1/(2*np.sqrt(2))
r_ph = 1/(2*eps_ph)  # in r_s units
print(f"CM photon sphere = {r_ph:.4f} r_s (GR = 1.5000)")
Citation
@article{Singh2026j,
  author  = {Singh, Mandeep},
  title   = {The CM Metric: From Clausius--Mossotti to Schwarzschild},
  year    = {2026},
  journal = {Zenodo},
  doi     = {10.5281/zenodo.19425285},
  note    = {Speed Gap Framework, Paper 2026j}
}
Related Papers
2026a — Speed Gap Framework (foundation): DOI: 10.5281/zenodo.19142702
2026b v3 — Cosmic OE, Ω_m derivation: DOI: 10.5281/zenodo.19244123
2026c — Deep Scaling Connections: DOI: 10.5281/zenodo.19227973
2026d — Damru Geometry (nuclear): DOI: 10.5281/zenodo.19313279
2026e — Guru Vortex (magnetic moments): DOI: 10.5281/zenodo.19332481
2026h — Unified Lagrangian L = OE − W: DOI: 10.5281/zenodo.19400730
2026i — Dynamical OE Lagrangian: DOI: 10.5281/zenodo.19414588
Mandeep Singh | Haryana, India | April 2026
"145 years. Zero parameters. Atom to black hole."
