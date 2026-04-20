"""
w13_potential.py — Singh 2026u, Chapter 1
V = μ²(W⁻¹/³ − 1): derived potential from CM metric
Weak-field limit, uranium example, comparison with Coulomb.

Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
"""

import numpy as np

# ═══ CONSTANTS (CODATA 2018) ═══
m_e_eV = 511099.0     # eV (electron rest energy)
alpha = 1/137.035999206

print("=" * 65)
print("  Singh 2026u Ch 1 — CM Potential V = μ²(W⁻¹/³ − 1)")
print("=" * 65)

def W_func(beta2):
    """CM compression function."""
    return (1 - beta2) / (1 + 2*beta2)

def V_frac(beta2):
    """Fractional binding = W⁻¹/³ − 1."""
    W = W_func(beta2)
    return W**(-1/3) - 1

def E_coulomb(Z, n=1):
    """Coulomb/Bohr binding energy (eV)."""
    beta2 = (Z * alpha / n)**2
    return 0.5 * m_e_eV * beta2

def E_cm(Z, n=1):
    """CM W⁻¹/³ binding energy (eV)."""
    beta2 = (Z * alpha / n)**2
    return 0.5 * m_e_eV * V_frac(beta2)

def E_dirac(Z, n=1):
    """Dirac exact 1s₁/₂ binding energy (eV)."""
    gamma = np.sqrt(1 - (Z*alpha)**2)
    return m_e_eV * (1 - gamma)

# ═══ TABLE 1.1: V_frac at representative β² values ═══
print(f"\n  ─── Table 1.1: V_frac = W⁻¹/³ − 1 at representative β² ───\n")
print(f"  {'β²':<10} {'W':<10} {'W⁻¹/³':<10} {'V_frac':<10} {'Regime'}")
print(f"  {'─'*60}")

test_values = [
    (0.0000, "Free particle"),
    (0.0001, "Hydrogen (Z=1)"),
    (0.01,   "Neon-like (Z≈14)"),
    (0.10,   "Krypton-like (Z≈43)"),
    (0.25,   "Lead-like (Z≈69)"),
    (0.45,   "Uranium (Z=92)"),
    (0.75,   "Confinement wall (OE=3/4)"),
]

for b2, regime in test_values:
    if b2 == 0:
        print(f"  {b2:<10.4f} {'1.000':<10} {'1.000':<10} {'0.000':<10} {regime}")
    else:
        W = W_func(b2)
        Wm13 = W**(-1/3)
        Vf = Wm13 - 1
        print(f"  {b2:<10.4f} {W:<10.4f} {Wm13:<10.4f} {Vf:<10.4f} {regime}")

# ═══ WEAK-FIELD LIMIT ═══
print(f"\n  ─── Weak-field check: V_frac → β² as β² → 0 ───\n")
for b2 in [1e-6, 1e-4, 1e-3, 1e-2]:
    Vf = V_frac(b2)
    ratio = Vf / b2
    print(f"  β² = {b2:.0e}:  V_frac = {Vf:.6e},  V_frac/β² = {ratio:.6f}  (→ 1.000)")

# ═══ URANIUM EXAMPLE ═══
print(f"\n  ─── Uranium (Z = 92) side-by-side ───\n")
Z = 92
b2 = (Z * alpha)**2
W = W_func(b2)
Vf = V_frac(b2)

Ec = E_coulomb(Z)
Ecm = E_cm(Z)
Ed = E_dirac(Z)
Em = 131810.0  # NIST measured

print(f"  β² = (92 × α)² = {b2:.4f}")
print(f"  W  = (1−β²)/(1+2β²) = {W:.4f}")
print(f"  V_frac = W⁻¹/³ − 1 = {Vf:.4f}")
print(f"")
print(f"  Coulomb: E = ½ m_e c² × β²     = {Ec:.0f} eV   error: {(Ec/Em-1)*100:+.2f}%")
print(f"  CM:      E = ½ m_e c² × V_frac = {Ecm:.0f} eV   error: {(Ecm/Em-1)*100:+.2f}%")
print(f"  Dirac:   E = m_e c²(1−γ)       = {Ed:.0f} eV   error: {(Ed/Em-1)*100:+.2f}%")
print(f"  Measured:                         {Em:.0f} eV")
print(f"")
print(f"  Improvement: Coulomb → CM = {abs(Ec/Em-1)/abs(Ecm/Em-1):.0f}× better")

# ═══ SUMMARY ═══
print(f"\n{'=' * 65}")
print(f"  SUMMARY")
print(f"{'=' * 65}")
print(f"""
  V = μ²(W⁻¹/³ − 1)  — derived from CM metric, NOT imposed
  
  Weak field:  V_frac → β² (= Coulomb)
  Strong field: V_frac >> β² (automatic corrections)
  
  Uranium: Coulomb 12.6% off → CM 0.6% off = 20× improvement
  Same 4 lines of math. No new equation needed.
""")
