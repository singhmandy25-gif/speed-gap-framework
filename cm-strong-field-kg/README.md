CM Strong-Field Klein-Gordon Equation
Paper: Singh 2026r — "Strong-Field Klein-Gordon Equation in the CM Metric: Spatial Flatness, Effective Mass, and Eigenvalue Predictions"
DOI: 10.5281/zenodo.19564200
Date: 14 April 2026
Author: Mandeep Singh (ORCID: 0009-0003-7176-2395)
Summary
The Klein-Gordon equation for a massive scalar field in the CM metric:
ds² = W^(1/3) c²dt² − W^(−1/3)(dr² + r²dΩ²)
W = (1−β²)/(1+2β²),  β² = 2GM/(rc²)
produces a radial equation with three unique properties:
Spatial Laplacian is flat — √(−g)×g^rr = −r²sinθ (W cancels exactly)
Effective mass increases — μ_eff = μ W^(−1/6) > μ near source (opposite to GR)
Weaker binding than GR — fewer bound states, ground state shift up to +18.5%
Key Results
α_g
n
ω_CM
ω_GR
Shift
CM levels
GR levels
0.1
1
0.099527
0.099363
+0.17%
2
2
0.3
1
0.290355
0.276221
+5.12%
2
3
0.5
1
0.466887
0.393937
+18.52%
3
4
Files
File
Description
verify_2026r.py
Master verification: all eigenvalue checks (11 tests)
eigenvalue_compare.py
CM vs GR eigenvalue computation (shooting method)
kg_derivation_sympy.py
SymPy verification of the CM KG equation derivation
Running
pip install numpy scipy sympy
python verify_2026r.py        # Runs all 11 checks
python eigenvalue_compare.py  # Full CM vs GR comparison
python kg_derivation_sympy.py # Symbolic equation verification
Related Papers
Paper
DOI
Topic
2026j
10.5281/zenodo.19435054
CM Metric
2026k
10.5281/zenodo.19448621
CM Field Equation
2026n
10.5281/zenodo.19498973
Surface Redshift
2026i
10.5281/zenodo.19414588
Dynamical Lagrangian
2026q
10.5281/zenodo.19554475
Geometric Quantization
2026p
10.5281/zenodo.19553969
OE as Time
Citation
@article{Singh2026r,
  author  = {Singh, Mandeep},
  title   = {Strong-Field Klein-Gordon Equation in the CM Metric: Spatial Flatness, Effective Mass, and Eigenvalue Predictions},
  year    = {2026},
  doi     = {10.5281/zenodo.19564200},
  url     = {https://doi.org/10.5281/zenodo.19564200}
}
