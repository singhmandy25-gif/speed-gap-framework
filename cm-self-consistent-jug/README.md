Self-Consistent Quantization, 3D Kepler Law, and Standing-Wave Quark Positions
Paper 2026s | Mandeep Singh | 16 April 2026
DOI: 10.5281/zenodo.19598344
Summary
Within the CM framework (OE + W = 1), the Klein-Gordon wave equation is solved in two complementary settings. Part I (Exterior): KG coupled to the CM Euler-Lagrange field equation — the wave modifies the medium, the medium reshapes the wave. Self-consistency converges at all 7 coupling strengths (α_g = 0.1–0.9), with back-reaction shifting binding energies by 7–20%. Proper volume (W⁻¹/³) produces 2.2–2.8× more equal shells than coordinate volume — a 3D analog of Kepler's second law. Part II (Interior): KG inside a finite sphere with hard wall at OE = 3/4 (proton = confined "jug"). Standing-wave nodes at f = 1/3 (0.2%) and f = 2/3 (0.4%) match Damru quark positions, beating JLAB (3.9%) and Cornell (4.3%). The u-quark position (f = 2/3) was not found by any previous method. Zero free parameters.
Five Key Results
#
Result
Section
Status
1
Coupled KG+EL converges — 50 iterations, 7 α_g values, <0.001%
Ch. 3
DEMONSTRATED
2
Back-reaction significant — +7% (α_g=0.3) to +20% (α_g=0.5)
Ch. 3
DEMONSTRATED
3
3D Kepler law — proper volume wins 7/7, avg 2.6× better
Ch. 5
DEMONSTRATED
4
Jug node at f = 1/3 (d quark, 0.2%) and f = 2/3 (u quark, 0.4%)
Ch. 7
DEMONSTRATED
5
1/D = 1/3 cone geometry connects exterior + interior to D = 3
Ch. 8
CONSISTENT
Paper Structure
Chapter 1: Introduction — From Metric to Wave Equation
Chapter 2: The Coupled System — KG + Euler-Lagrange Equations
Chapter 3: Self-Consistency — Convergence Results
Chapter 4: Probability Averages — The Kepler Analogy
Chapter 5: The 3D Kepler Law — Proper Volume Test
Chapter 6: Interior vs Exterior — Two Sides of One Wall
Chapter 7: The Jug Test — Standing Waves in a Confined Sphere
Chapter 8: From Cones to Quarks — Dimension Counting
Chapter 9: Complete Verification Table (8 tables, 20 results)
Chapter 10: Honest Limits and Future Directions
Chapter 11: Conclusion
Files
File
Description
cm_coupled_full_study.py
Coupled KG+EL self-consistency iteration, 7 α_g values, 24 bound states, 3D Kepler law test (Part I)
cm_rotating_kg.py
KG eigenvalues l=0,1,2 at 7 couplings, wavefunction peaks, ⟨OE⟩ averages, rotation splitting
cm_kg_complete.py
Complete eigenvalue scan + real rotation term Ω²r²⟨sin²θ⟩ in KG equation
cm_jug.py
The jug test — KG inside confined sphere, standing-wave nodes at f = 1/3, 1/2, 2/3 (Part II)
README.md
This file
Master Scorecard (Table 9.8)
#
Result
Evidence
Status
Part I: Exterior KG



1
Coupled KG+EL converges
50 iterations, 7 α_g values
DEMONSTRATED
2
Back-reaction significant
+7% to +20%
DEMONSTRATED
3
24 bound states found
7 α_g × 2–4 states
COMPUTED
4
Proper volume always best
7/7, avg 2.6×
DEMONSTRATED
5
Exterior peak at f_prob ≈ 1/3
7/7 couplings, 0.6–4.9%
DEMONSTRATED
6
4π+2π=6π decomposition
Algebraic identity
DERIVED
7
⟨OE⟩ ≈ 1/4 at α_g=0.3
2.8% from 1/4
PATTERN
8
⟨OE⟩ ≈ 1/2 at α_g=0.7
6.7% from 1/2
PATTERN
Part II: Interior Jug



9
Jug node at f = 1/3 (d quark)
0.2% deviation, l=1 n=5
DEMONSTRATED
10
Jug node at f = 2/3 (u quark)
0.4% deviation, l=3 n=5
DEMONSTRATED
11
Jug node at f = 1/2 (neck)
2.6% deviation, l=2 n=3
DEMONSTRATED
12
Robust across 4 W(r) models
All give nodes near 1/3, 2/3
DEMONSTRATED
Dimension Counting



13
Quark charges from D=3
1/3, 2/3 = 1/D, 2/D
CONSISTENT
14
3 generations from D=3
D intervals of 1/(D+1)
CONSISTENT
15
20/20 hadron charges
All baryons + mesons
EXACT
Open



16
Selection rule (l, n)
Why l=1 n=5 and l=3 n=5?
OPEN
17
Interior W(r) not derived
Model assumed, not from field eq.
OPEN
18
Quark masses
Positions found, masses not
OPEN
19
Interior field equation
2/r² singularity
OPEN
20
Spin (Dirac equation)
Not attempted
OPEN
Total: 12 demonstrated + 4 patterns + 5 open
How to Run
Bash
Jug Test Results (Table 9.7)
Position
Target f_vol
Best node
State (l, n)
Deviation
Previous best
d quark
1/3 = 0.3333
0.3339
l=1, n=5
0.2%
Burkert JLAB 3.9%
neck
1/2 = 0.5000
0.4869
l=2, n=3
2.6%
Burkert JLAB 3.9%
u quark
2/3 = 0.6667
0.6638
l=3, n=5
0.4%
Not found before
Citation
Code
Links
Companion papers: 2026r — KG in CM metric | 2026d — Damru Geometry | 2026m — CM Wave Equation
Predecessor: 2026p — OE as Time, Frequency Rule | 2026q — Geometric Quantization
CM Metric: 2026j | Field Equation: 2026k
Full framework: Speed Gap Framework on GitHub
ORCID: 0009-0003-7176-2395
