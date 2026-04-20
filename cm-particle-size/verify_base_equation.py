"""
verify_base_equation.py — Singh 2026t, Chapters 1–3
Base equation E = mc² = hf = (4/3)hc/(2R)
Proton radius R_p = (4/3)π × ℏ/(m_p c) = 0.881 fm
Neutron radius R_n = (4/3)π × ℏ/(m_n c) = 0.880 fm

Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
No adjustable parameters. Inputs: ℏc, m_p, m_n from CODATA 2018.
"""

import numpy as np

# ═══ CONSTANTS (CODATA 2018) ═══
hbar_c = 197.3269804  # MeV·fm (ℏc)
m_p = 938.27208816    # MeV (proton mass)
m_n = 939.56542052    # MeV (neutron mass)
D = 3                 # spatial dimensions

# ═══ BASE EQUATION ═══
# E = mc² = hf = (4/3) × hc/(2R)
# R = (4/3)π × ℏ/(mc) = (4/3)π × λ_C

factor_baryon = (4/3) * np.pi  # = (D+1)/D × π = 4.18879...

print("=" * 65)
print("  Singh 2026t — Base Equation & Proton Radius Verification")
print("=" * 65)

print(f"\n  Base equation: E = mc² = hf = (4/3) × hc/(2R)")
print(f"  Factor: (4/3)π = (D+1)/D × π = {factor_baryon:.5f}")
print(f"  D = {D} (spatial dimensions)")

# ═══ PROTON ═══
lambda_C_p = hbar_c / m_p  # reduced Compton wavelength
R_p_pred = factor_baryon * lambda_C_p

# Measurements
R_p_escatter = 0.877   # fm, electron scattering (Mainz 2010)
R_p_muonic = 0.84184   # fm, muonic hydrogen (Pohl 2010)
R_p_nist = 0.8433      # fm, NIST H spectroscopy (Bullis 2026)

print(f"\n  ─── PROTON ───")
print(f"  λ_C(p) = ℏc / m_p c² = {hbar_c} / {m_p} = {lambda_C_p:.5f} fm")
print(f"  R_p = (4/3)π × λ_C = {factor_baryon:.5f} × {lambda_C_p:.5f} = {R_p_pred:.4f} fm")
print(f"\n  Comparison with measurements:")
print(f"    vs e-p scattering (0.877 fm):  {(R_p_pred/R_p_escatter - 1)*100:+.2f}%")
print(f"    vs muonic H (0.842 fm):        {(R_p_pred/R_p_muonic - 1)*100:+.2f}%")
print(f"    vs NIST 2026 (0.843 fm):       {(R_p_pred/R_p_nist - 1)*100:+.2f}%")

# ═══ NEUTRON ═══
lambda_C_n = hbar_c / m_n
R_n_pred = factor_baryon * lambda_C_n
R_n_meas = 0.862  # fm, magnetic radius

print(f"\n  ─── NEUTRON ───")
print(f"  λ_C(n) = {lambda_C_n:.5f} fm")
print(f"  R_n = (4/3)π × λ_C = {R_n_pred:.4f} fm")
print(f"  Measured (magnetic): {R_n_meas} fm")
print(f"  Error: {(R_n_pred/R_n_meas - 1)*100:+.2f}%")

# ═══ SELF-CONSISTENCY CHECK ═══
# From R, recover mass: m = (4/3)π × ℏc / (R × c²)
m_from_R = factor_baryon * hbar_c / R_p_pred
print(f"\n  ─── SELF-CONSISTENCY ───")
print(f"  m from R_p: (4/3)π × ℏc / R_p = {m_from_R:.3f} MeV")
print(f"  m_p actual: {m_p:.3f} MeV")
print(f"  Match: {abs(m_from_R/m_p - 1)*100:.6f}% (algebraic identity)")

# ═══ FREQUENCY ═══
h_eV = 4.135667696e-15  # eV·s (Planck constant)
f_p = m_p * 1e6 / (h_eV * 1e6)  # Hz: mc²/h, convert MeV to eV
f_p_clean = m_p * 1e6 * 1.602176634e-19 / 6.62607015e-34
print(f"\n  ─── FREQUENCY ───")
print(f"  f_p = m_p c² / h = {f_p_clean:.3e} Hz")
print(f"  = {f_p_clean/1e23:.2f} × 10²³ Hz (Compton frequency)")

# ═══ R × m PRODUCT ═══
print(f"\n  ─── R × m PRODUCT (should be constant = (4/3)π × ℏc) ───")
expected = factor_baryon * hbar_c
print(f"  Expected: (4/3)π × ℏc = {expected:.2f} MeV·fm")
print(f"  Proton:   R_p × m_p = {R_p_pred * m_p:.2f} MeV·fm ✓")
print(f"  Neutron:  R_n × m_n = {R_n_pred * m_n:.2f} MeV·fm ✓")

# ═══ SUMMARY ═══
print(f"\n{'=' * 65}")
print(f"  SUMMARY")
print(f"{'=' * 65}")
print(f"""
  Base equation: E = mc² = hf = (4/3) × hc/(2R)
  
  Proton:  R_p = {R_p_pred:.4f} fm  vs {R_p_escatter} fm → {(R_p_pred/R_p_escatter-1)*100:+.2f}% (e-scatter)
  Neutron: R_n = {R_n_pred:.4f} fm  vs {R_n_meas} fm → {(R_n_pred/R_n_meas-1)*100:+.2f}% (magnetic)
  
  Free parameters: ZERO
  Inputs: ℏc (CODATA), m_p (CODATA), (4/3)π (D=3 geometry)
""")
