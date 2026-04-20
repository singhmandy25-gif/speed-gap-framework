"""
alpha_formula_verify.py — Singh 2026t, Chapter 5
α = (π²/OE + D/(4π)) × m_e/m_p = 1/137.045 (0.006%)
α-free Bohr: E = (m_e³c²/2m_p²) × G² × Z²/n²

Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
"""

import numpy as np

# ═══ CONSTANTS ═══
hbar_c = 197.3269804   # MeV·fm
m_e = 0.51099895000    # MeV (electron mass)
m_p = 938.27208816     # MeV (proton mass)
alpha_meas = 1/137.035999206  # CODATA 2018
D = 3                  # spatial dimensions
OE = 3/4               # confinement wall = D/(D+1)

print("=" * 65)
print("  Singh 2026t Ch 5 — Fine Structure Constant Verification")
print("=" * 65)

# ═══ α FORMULA ═══
print(f"\n  ─── α FORMULA ───")
print(f"  α = (π²/OE + D/(4π)) × m_e/m_p")
print(f"\n  Inputs:")
print(f"    π² = {np.pi**2:.6f}")
print(f"    OE = D/(D+1) = {D}/{D+1} = {OE:.4f}")
print(f"    D = {D}")
print(f"    4π = {4*np.pi:.6f}")
print(f"    m_e/m_p = {m_e/m_p:.6e}")

# Step 1: Geometric factor G
term1 = np.pi**2 / OE          # = (4/3)π²
term2 = D / (4 * np.pi)        # = 3/(4π)
G = term1 + term2

print(f"\n  Step 1: Geometric factor G")
print(f"    π²/OE = (4/3)π² = {term1:.4f}")
print(f"    D/(4π) = 3/(4π) = {term2:.4f}")
print(f"    G = {term1:.4f} + {term2:.4f} = {G:.4f}")

# Step 2: α
alpha_CM = G * m_e / m_p
alpha_inv_CM = 1 / alpha_CM

print(f"\n  Step 2: α = G × m_e/m_p")
print(f"    α = {G:.4f} × {m_e/m_p:.6e}")
print(f"    α = {alpha_CM:.8e}")
print(f"    α⁻¹ = {alpha_inv_CM:.3f}")

# Compare
print(f"\n  Step 3: Compare")
print(f"    α⁻¹(CM)      = {alpha_inv_CM:.6f}")
print(f"    α⁻¹(measured) = {1/alpha_meas:.6f}")
print(f"    Error = {(alpha_CM/alpha_meas - 1)*100:+.4f}% = {abs(alpha_CM/alpha_meas - 1)*1e6:.0f} ppm")

# ═══ α-FREE BOHR FORMULA ═══
print(f"\n  ─── α-FREE BOHR FORMULA ───")
print(f"  Standard:  E = ½ m_e c² × α² × Z²/n²  (α = input)")
print(f"  CM:        E = (m_e³c²/2m_p²) × G² × Z²/n²  (NO α!)")
print(f"\n  G² = {G**2:.4f}")
print(f"  m_e³c²/(2m_p²) = {m_e**3 / (2*m_p**2):.6e} MeV")

prefactor = (m_e**3) / (2 * m_p**2) * G**2  # in MeV
prefactor_eV = prefactor * 1e6  # convert to eV

print(f"  Prefactor = {prefactor_eV:.3f} eV")

# ═══ VERIFICATION: H-LIKE IONS ═══
print(f"\n  ─── VERIFICATION: HYDROGEN-LIKE IONS (n=1) ───\n")
print(f"  {'Ion':<10} {'Z':<4} {'E_CM (eV)':<12} {'E_meas (eV)':<13} {'Error':<8}")
print(f"  {'─'*48}")

ions = [
    ("H",       1,  13.598),
    ("He⁺",     2,  54.418),
    ("Li²⁺",    3,  122.454),
    ("Be³⁺",    4,  217.719),
    ("C⁵⁺",     6,  489.993),
    ("Ne⁹⁺",   10,  1362.199),
]

for name, Z, E_meas in ions:
    E_CM = prefactor_eV * Z**2
    err = (E_CM / E_meas - 1) * 100
    print(f"  {name:<10} {Z:<4} {E_CM:<12.3f} {E_meas:<13.3f} {err:>+6.3f}%")

# ═══ BOHR RADIUS ═══
print(f"\n  ─── BOHR RADIUS ───")
# a₀ = ℏ/(α m_e c) = ℏc/(α m_e c²)
# CM: a₀ = m_p/(G × m_e) × λ_C(e)
a0_standard = hbar_c / (alpha_meas * m_e)  # fm
a0_CM = hbar_c * m_p / (G * m_e**2)        # fm
a0_meas = 52917.7211  # fm (CODATA)

print(f"  a₀(standard) = ℏc/(α m_e c²) = {a0_standard:.1f} fm")
print(f"  a₀(CM)       = ℏc m_p/(G m_e²) = {a0_CM:.1f} fm")
print(f"  a₀(CODATA)   = {a0_meas:.1f} fm")
print(f"  CM error: {(a0_CM/a0_meas - 1)*100:+.4f}%")

# ═══ WHAT REMAINS INPUT ═══
print(f"\n  ─── WHAT REMAINS INPUT ───")
print(f"  m_e/m_p = {m_e/m_p:.6e} ← measured, NOT derived")
print(f"  Partial: m_u/m_e = (4/3)π = {(4/3)*np.pi:.3f} (derived, 0.9%)")
print(f"  Open:    m_p/m_u = {m_p/2.16:.0f} (confinement energy, NOT derived)")

# ═══ SUMMARY ═══
print(f"\n{'=' * 65}")
print(f"  SUMMARY")
print(f"{'=' * 65}")
print(f"""
  α = (π²/OE + D/(4π)) × m_e/m_p
    = {G:.4f} × {m_e/m_p:.6e}
    = 1/{alpha_inv_CM:.3f}  (measured: 1/137.036)
    Error: {abs(alpha_CM/alpha_meas - 1)*100:.4f}% = {abs(alpha_CM/alpha_meas - 1)*1e6:.0f} ppm
  
  α-free Bohr: E = (m_e³c²/2m_p²) × G² × Z²/n²
    H:    {prefactor_eV*1:.3f} eV  (measured: 13.598)  → 0.04%
    He⁺:  {prefactor_eV*4:.3f} eV  (measured: 54.418)  → 0.004%
    C⁵⁺:  {prefactor_eV*36:.3f} eV (measured: 489.993) → 0.05%
  
  Bohr radius: {a0_CM:.1f} fm (CODATA: {a0_meas:.1f} fm) → {(a0_CM/a0_meas - 1)*100:+.4f}%
  
  Status: OBSERVED (pattern match, not derivation)
  Input:  m_e/m_p (not derived from framework)
""")
