The Speed Gap: A Scaling Framework from Atomic Constants to the Hubble Constant
Paper: Singh 2026b V4
Zenodo DOI: 10.5281/zenodo.19604521
Date: 16 April 2026
Version: V4 (supersedes V1–V3)
Summary
A self-contained derivation of the Hubble constant H₀ = 70.05 km s⁻¹ Mpc⁻¹ from five fundamental constants (α, G, ℏ, c, mₑ) and one model-independent CMB observation (θ* = 0.5965°), with no freely adjustable cosmological parameters.
The derivation uses:
D = 3 sphere geometry → gives p = e^(-3/4) = 0.4724 (geometric decay parameter)
Virial complementarity → gives Ω_m = (1-p)² = 0.2784 and Ω_DE = p(2-p) = 0.7216
Differential complementarity ΔA+ΔB=0 → requires standard Friedmann H(z)
θ CMB constraint* → fixes H₀ = 70.05
Key Results
1. H₀ Matches Late-Universe Measurements
Measurement
H₀
Distance from 70.05
DESI + DES PEDE (2024)
70.06 ± 1.07
0.01σ ★
TRGB (Freedman 2024)
69.96 ± 1.53
0.1σ
CCHP
69.85 ± 1.75
0.1σ
DESI BAO alone
70.3 ± 1.3
0.2σ
TDCOSMO (lensing)
71.6 ± 1.5
1.0σ
SH0ES (Cepheids)
73.04 ± 1.04
2.9σ
Planck + ΛCDM
67.36 ± 0.54
5.0σ
2. CMB Angular Scale θ* (CLASS Unmodified)
Model
Fitted params
100×θ_s
Error vs Planck
Speed Gap V4
0
1.042082
0.094%
ΛCDM best-fit
6
1.0405
0.37%
Speed Gap is 3.9× better than ΛCDM with six fewer fitted parameters.
3. S_8 Tension Resolved
Model
S_8
Distance from DES Y3 (0.776 ± 0.017)
Speed Gap V4
0.7748
0.07σ
Planck + ΛCDM
0.832
3.3σ
Speed Gap matches DES Y3 47× better than ΛCDM.
4. DESI DR1 BAO
Model
χ²/N (12 points)
Speed Gap V4
1.51
ΛCDM best-fit
1.79
Δχ² = 3.35 in favour of Speed Gap.
The Derivation Chain
Code
Zero fitted cosmological parameters at any step.
What Changed from V3
The V3 (27 March 2026) introduced a modified Friedmann equation with factors (SG/SG₀)^p and (SG₀/SG)^k modulating matter and dark energy sectors. That formulation violated the framework's own A+B=1 principle at z > 0.
V4 corrects this:
H(z) = standard Friedmann (ΔA+ΔB=0 is rigorous consequence of A+B=1)
D = 11 dimensional mapping removed (was artifact of modified Friedmann)
k_cons = 8.477 and k_phys = 1.256 not needed
Framework now uses D = 3 only across all scales (atomic + cosmic)
H₀ corrected: 72.94 → 70.05 (matches DESI+DES PEDE to 0.01σ)
Ω_m corrected: 0.315 (Planck input) → 0.2784 (geometrically derived)
Full derivation of the correction: Singh 2026g (authoritative reference).
Files in This Folder
File
Description
verify_h0_70.05.py
Clean standalone Python solver. Derives Ω_m, Ω_DE from p = e^(-3/4), applies standard Friedmann, verifies H₀ = 70.05 is self-consistent with Planck θ*. Run this first — requires only numpy + scipy.
cm_complete_tests.py
Full verification suite (9 tests + BAO + SNe). Tests growth equation, dark energy equation of state, S_8 derivation, cosmic chronometers, DESI BAO, Pantheon+ SNe. Requires scipy.
class_verification_v4.py
CLASS v3.3.4 unmodified verification. Uses V4 parameters to compute full C_ℓ spectrum, σ_8, θ*, r_s. Compares with ΛCDM best-fit. Requires classy (see install notes).
Quick Start
Minimum — derive H₀ from scratch (no CLASS needed)
Bash
Expected output:
Code
Full verification — 9 tests + BAO + SNe
Bash
CLASS verification (requires classy)
Bash
Reproducibility
All scripts verified on:
Ubuntu 24.04 LTS
Python 3.12
numpy 2.1, scipy 1.14
classy (CLASS v3.3.4, unmodified)
CLASS source code integrity — MD5 checksum of background.c:
Code
(matches official CLASS distribution — confirming no source modifications).
CLASS inputs used:
Code
Speed Gap predictions emerge purely from changed input parameters, not from modified physics. This is required by ΔA+ΔB=0.
Companion Papers (Speed Gap Framework)
Singh 2026a — Original Speed Gap concept. DOI: 10.5281/zenodo.19142702
Singh 2026c — Deep scaling connections (3/4 from three routes). DOI: 10.5281/zenodo.19227973
Singh 2026f — Ω_m = (1-p)² derivation + CMB self-consistency. DOI: 10.5281/zenodo.19372437
Singh 2026g ⭐ — ΔA+ΔB=0 and dark energy as orbital emptiness (V4 correction source). DOI: 10.5281/zenodo.19383758
Singh 2026h — Unified Lagrangian L = OE − W. DOI: 10.5281/zenodo.19400730
Singh 2026o — Cosmological perturbation theory from CM. DOI: 10.5281/zenodo.19530368
Singh 2026s — Self-consistent quantisation + quark positions. DOI: 10.5281/zenodo.19598344
All papers together: Zenodo community
Citation
If you use these scripts or results, please cite:
Code
BibTeX:
Bibtex
License
MIT License — see LICENSE at the repository root.
Contact
Mandeep Singh
Independent Researcher, Haryana, India
ORCID: 0009-0003-7176-2395
Email: singhmandy25@gmail.com
GitHub: @singhmandy25-gif
"From the density pit of a single proton to the expansion of the observable universe — 41 orders of magnitude, one principle: Speed Gap = 0 at equilibrium."
