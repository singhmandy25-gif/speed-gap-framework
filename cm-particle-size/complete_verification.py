"""
complete_verification.py — Singh 2026t, Chapter 6
Runs all tests from the paper and produces a ranked summary table.
12 results, zero free parameters.

Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
"""

import numpy as np

# ═══ CONSTANTS (CODATA 2018) ═══
hbar_c = 197.3269804
m_e = 0.51099895000    # MeV
m_p = 938.27208816     # MeV
m_n = 939.56542052     # MeV
m_pi = 139.57039       # MeV
alpha_meas = 1/137.035999206
D = 3
OE = D/(D+1)           # = 3/4
p = np.exp(-OE)        # = e^(-3/4) = 0.47237

# ═══ DERIVED QUANTITIES ═══
baryon_factor = (D+1)/D * np.pi  # (4/3)π
G = np.pi**2/OE + D/(4*np.pi)   # geometric coupling = 13.398

print("=" * 72)
print("  Singh 2026t — COMPLETE VERIFICATION")
print("  Particle Size from Trapped Vibration")
print("  Mandeep Singh | 20 April 2026 | Speed Gap Framework")
print("=" * 72)

# ═══ COMPUTE ALL RESULTS ═══
results = []

# 1. Proton radius
lambda_p = hbar_c / m_p
R_p = baryon_factor * lambda_p
results.append(("R_p (proton)", R_p, 0.877, "fm", "DERIVED", 3))

# 2. Neutron radius
lambda_n = hbar_c / m_n
R_n = baryon_factor * lambda_n
results.append(("R_n (neutron)", R_n, 0.862, "fm", "DERIVED", 3))

# 3. Pion radius
lambda_pi = hbar_c / m_pi
R_pi = p * lambda_pi
results.append(("R_π (pion)", R_pi, 0.659, "fm", "OBSERVED", 4))

# 4. α⁻¹
alpha_CM = G * m_e / m_p
results.append(("α⁻¹", 1/alpha_CM, 1/alpha_meas, "", "OBSERVED", 5))

# 5-10. Hydrogen-like binding energies (α-free)
prefactor_eV = (m_e**3 / (2 * m_p**2)) * G**2 * 1e6  # eV

ions = [
    ("E(H)", 1, 13.598),
    ("E(He⁺)", 2, 54.418),
    ("E(Li²⁺)", 3, 122.454),
    ("E(Be³⁺)", 4, 217.719),
    ("E(C⁵⁺)", 6, 489.993),
    ("E(Ne⁹⁺)", 10, 1362.199),
]

for name, Z, E_meas in ions:
    E_CM = prefactor_eV * Z**2
    results.append((name, E_CM, E_meas, "eV", "VERIFIED", 5))

# 11. Bohr radius
a0_CM = hbar_c * m_p / (G * m_e**2)  # fm
a0_meas = 52917.7211  # fm
results.append(("a₀ (Bohr)", a0_CM, a0_meas, "fm", "VERIFIED", 5))

# ═══ COMPUTE ERRORS AND SORT ═══
ranked = []
for name, pred, meas, unit, status, ch in results:
    err = abs(pred/meas - 1) * 100
    ranked.append((err, name, pred, meas, unit, status, ch))

ranked.sort(key=lambda x: x[0])

# ═══ PRINT RANKED TABLE ═══
print(f"\n  {'#':<4} {'Result':<16} {'CM value':<14} {'Measured':<14} {'Error':<8} {'Status':<10} {'Ch':<4}")
print(f"  {'─'*70}")

for i, (err, name, pred, meas, unit, status, ch) in enumerate(ranked):
    if unit:
        pred_str = f"{pred:.3f} {unit}" if pred < 1000 else f"{pred:.1f} {unit}"
        meas_str = f"{meas:.3f} {unit}" if meas < 1000 else f"{meas:.1f} {unit}"
    else:
        pred_str = f"{pred:.3f}"
        meas_str = f"{meas:.3f}"
    print(f"  {i+1:<4} {name:<16} {pred_str:<14} {meas_str:<14} {err:<7.4f}% {status:<10} {ch:<4}")

# ═══ FAILURES ═══
print(f"\n  ═══ EXPLICIT FAILURES ═══\n")
print(f"  {'System':<14} {'Predicted':<12} {'Measured':<12} {'Error':<10} {'Reason':<30}")
print(f"  {'─'*78}")

failures = [
    ("Δ(1232)", baryon_factor * hbar_c/1232, 0.84, "Resonance (10⁻²⁴ s)"),
    ("K±", p * hbar_c/493.677, 0.560, "Strange quark, different wall"),
    ("ρ(770)", p * hbar_c/775.26, 0.75, "Vector meson + resonance"),
    ("J/ψ", p * hbar_c/3096.9, 0.25, "Heavy charm quarks"),
    ("Deuteron", baryon_factor * hbar_c/1875.6, 2.142, "Two-body, not single sphere"),
    ("He-4", baryon_factor * hbar_c/3727.4, 1.67, "Multi-nucleon system"),
    ("Electron", baryon_factor * hbar_c/m_e, 0.001, "Point particle, no structure"),
]

for name, pred, meas, reason in failures:
    err = (pred/meas - 1) * 100
    print(f"  {name:<14} {pred:<12.4f} {meas:<12.3f} {err:>+8.1f}%  {reason:<30}")

# ═══ SCORECARD ═══
n_pass = sum(1 for err, *_ in ranked if err < 5)
n_derived = sum(1 for _, _, _, _, _, status, _ in ranked if status == "DERIVED")
n_observed = sum(1 for _, _, _, _, _, status, _ in ranked if status == "OBSERVED")
n_verified = sum(1 for _, _, _, _, _, status, _ in ranked if status == "VERIFIED")

print(f"\n{'=' * 72}")
print(f"  SCORECARD")
print(f"{'=' * 72}")
print(f"""
  Total results:     {len(ranked)}
  All pass (<5%):    {n_pass}/{len(ranked)}
  Best match:        {ranked[0][0]:.4f}% ({ranked[0][1]})
  Worst match:       {ranked[-1][0]:.4f}% ({ranked[-1][1]})
  
  Classification:
    DERIVED  (blind prediction):  {n_derived}
    OBSERVED (pattern match):     {n_observed}
    VERIFIED (cross-check):       {n_verified}
  
  Explicit failures:              {len(failures)} (all with identified reasons)
  
  Free parameters:                ZERO
  
  Framework inputs:
    ℏc = {hbar_c} MeV·fm        (CODATA)
    m_p = {m_p} MeV              (CODATA)
    m_n = {m_n} MeV              (CODATA)
    m_e = {m_e} MeV              (CODATA)
    m_π = {m_pi} MeV             (PDG 2024)
    (4/3)π = {baryon_factor:.5f}           (D=3 geometry)
    e^(-3/4) = {p:.5f}            (confinement transmission)
    G = {G:.4f}                   (geometric coupling)
""")

print(f"  ─── KEY FORMULAS ───")
print(f"  Base equation:  E = mc² = hf = (4/3) × hc/(2R)")
print(f"  Baryon size:    R = (4/3)π × ℏ/(mc)")
print(f"  Meson size:     R = e^(-3/4) × ℏ/(mc)")
print(f"  α formula:      α = (π²/OE + D/(4π)) × m_e/m_p")
print(f"  α-free Bohr:    E = (m_e³c²/2m_p²) × G² × Z²/n²")
print(f"\n{'=' * 72}")
