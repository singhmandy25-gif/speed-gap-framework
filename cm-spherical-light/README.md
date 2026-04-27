cm-spherical-light
Reproducibility folder for Singh 2026w: "Spherical Light: Wavelength as Sphere Size, Redshift as Dilution, and the Universal Rule m × R = n × ħc"
Paper
DOI: (to be assigned upon Zenodo upload)
Date: 27 April 2026
Author: Mandeep Singh (ORCID: 0009-0003-7176-2395)
What This Folder Contains
File
Purpose
verify_all.py
Single script verifying all 51 numerical claims in the paper
requirements.txt
Python dependencies (NumPy only)
expected_output.txt
Full expected output for comparison
README.md
This file
How to Run
Bash
Expected: 51/51 checks pass with ✅ PASS.
What Is Verified (7 categories, 51 checks)
1. Proton Internal Structure (Ch 1, 2B, 6A)
Proton mode count: m_p × R_p / ħc = (4/3)π (0.007% match)
Area × ρ = 1065 MeV/fm at 5 radii (exact)
Mean/local density ratio = D = 3 at 4 radii (exact)
Wall OE = D/(D+1) = 3/4 (exact)
Transmission p = e^(-3/4) = 0.4724 (exact)
Born rule: P ∝ ρ ∝ 1/r² (follows from above)
2. Proton OE Profile + Barycenter (Ch 7A)
d quark position: r/R_p = (1/3)^(1/3) = 0.693
u quark position: r/R_p = (2/3)^(1/3) = 0.874
Barycenter: r = 28.8 fm (0.015% match)
3. Wave = Sphere Relations (Ch 1, 2A, 3, 5B)
R = ħc/E for 4 energies (exact)
Fusion energy: 2p + 2n → He-4 = 28.3 MeV (0.09% match)
4. Electron Modes + Z Scaling (Ch 6A)
Electron mode count: m_e × a₀ / ħc = 1/α (exact)
H shell levels: n²/α modes for n = 1–4 (exact)
Mode count at shell 1 for 7 atoms: H to U (< 0.05% all)
Mode matching: Z = 3/(4πα) = 32.7 (0.05% match)
5. Electron Shell Budget (Ch 6B)
Cap × OE = 6(Zα)² for Fe, 4 shells (exact)
Full shell absorbs 3/4 (exact)
Budget 6(Zα)² for 6 atoms: H to U (< 0.2% all)
Noble gas: 2 full shells → remaining = 1/16 (exact)
6. Iron Stability Formulas (Ch 7B)
A(Fe) = (m_p/m_e) × (4/3)π × α = 56.13 (0.2% match to 56)
ΔA + 6(Zα)² = 1.004 at Fe (0.4% from unity)
Flux per nucleon for 6 nuclei: H to Fe
Relativistic OE = 1 at Z = 79.1 (0.02% match)
Wall-level OE = 3/4 at Z = 68.5 (0.03% match)
7. Cosmology (Ch 5A)
p = e^(-3/4) = 0.4724 (exact)
Ω_m = (1−p)² = 0.2784 (0.001% match)
T at recombination: 3000.8 K (0.001% match)
H₀ = 70.05 km/s/Mpc (from Singh 2026b, see cm-hubble-constant-derivation/)
Dependencies
Python 3.x
math module (standard library only — no external packages required)
Framework
Part of the Speed Gap / Clausius-Mossotti Framework. See also:
cm-hubble-constant-derivation/ — H₀ and Ω_m derivation (2026b)
cm-particle-size/ — Proton radius and quark masses (2026s)
cm-w13-corrections/ — Relativistic corrections (2026u)
cm-alpha-s-derivation/ — Strong coupling constant (2026v)
