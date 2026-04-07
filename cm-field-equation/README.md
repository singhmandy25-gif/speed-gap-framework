CM Field Equation — Verification Code
Paper: "The CM Field Equation: From Clausius-Mossotti Medium to Scalar-Tensor Gravity"
Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
Date: 7 April 2026
Overview
The CM field equation OE' = −OE²/3 is derived from first principles (Clausius–Mossotti medium response, sphere geometry, complementarity OE+W=1) — independent of Newton and Einstein. This folder contains the verification code.
Key Equation
OE' = −OE²/3        (how emptiness spreads)
W'  = (1−W)²/3      (how compression spreads)
Φ   = (1/6) ln W    (scalar field = gravitational potential)
g_tt = W^(1/3)       (time dilation)
g_rr = W^(-1/3)      (space stretch)
g_tt × g_rr = 1      (exact — absent in GR!)
Files
File
Description
cm_field_equation_verify.py
Complete verification: 88 tests (16 test groups)
README.md
This file
Running
pip install numpy sympy
python cm_field_equation_verify.py
Expected output: 88/88 tests passed ✅
What is verified (16 test groups)
#
Test
Method
1
OE' = −OE²/3
Sympy algebraic + 8 numerical points
2
W' = (1−W)²/3
Sympy algebraic + 5 numerical points
3
ΔOE + ΔW = 0
Sympy algebraic + 3 numerical points
4
Φ ≈ −ε (weak field)
6 points, 96–99.99% match
5
g_tt × g_rr = 1
7 points, exact
6
∇²Φ three forms identical
Sympy + 8 numerical points
7
Taylor: 8ε⁴ − 96ε⁵ + 480ε⁶
Sympy series coefficients
8
Special points (r=4, r=2, horizon)
Exact values
9
Φ' = (1−W)²/(18W)
Sympy + 5 numerical points
10
□Φ = −W^(1/3) × ∇²Φ
5 numerical points
11
V'(Φ) round-trip → ∇²Φ
6 numerical points
12
GPS: Einstein = CM = +38.56 μs/day
Full calculation
13
Proton confinement: c_inside < v_escape
Exact values
14
OE + W = 1 (everywhere)
7 numerical points
15
∇²OE + ∇²W = 0
Sympy algebraic
16
General D: OE' = −OE²/D
Sympy algebraic
Requirements
Python 3.8+
NumPy
SymPy (optional — numerical tests run without it)
Related Papers
Paper 2026j: CM Metric
Paper 2026i: Dynamical Lagrangian
Full framework: speed-gap-framework
