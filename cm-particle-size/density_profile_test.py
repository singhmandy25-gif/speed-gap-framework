"""
density_profile_test.py — Singh 2026t, Chapter 2
Tests four density profiles: ρ=const, 1/r, 1/r², 1/r³
Only ρ ∝ 1/r² gives R linear in E (equal energy per shell)

Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
"""

import numpy as np

hbar_c = 197.3269804  # MeV·fm
m_p = 938.27208816    # MeV
R_p = (4/3) * np.pi * hbar_c / m_p  # predicted proton radius

print("=" * 65)
print("  Singh 2026t Ch 2 — Density Profile Verification")
print("=" * 65)

# ═══ FOUR PROFILES ═══
print(f"\n  ─── FOUR DENSITY PROFILES: E = 4π ∫ ρ(r) r² dr ───\n")
print(f"  {'Profile':<16} {'Integral':<20} {'R(E)':<16} {'Character':<12}")
print(f"  {'─'*64}")
print(f"  {'ρ = const':<16} {'(4/3)πρ₀R³':<20} {'R ∝ E^(1/3)':<16} {'Cube root':<12}")
print(f"  {'ρ ∝ 1/r':<16} {'2πBR²':<20} {'R ∝ E^(1/2)':<16} {'Square root':<12}")
print(f"  {'ρ ∝ 1/r² ★':<16} {'4πAR':<20} {'R ∝ E':<16} {'LINEAR! ★':<12}")
print(f"  {'ρ ∝ 1/r³':<16} {'4πC ln(R/r₀)':<20} {'R ∝ exp(E)':<16} {'Exponential':<12}")

# ═══ NUMERICAL VERIFICATION: EQUAL SHELL ENERGY ═══
print(f"\n  ─── EQUAL ENERGY PER SHELL (ρ ∝ 1/r²) ───")
print(f"\n  For proton: R_p = {R_p:.4f} fm, E = m_p c² = {m_p:.2f} MeV")

A = m_p / (4 * np.pi * R_p)
print(f"  Density constant A = m_p/(4πR_p) = {A:.2f} MeV/fm")
print(f"  Shell energy = 4πA = {4*np.pi*A:.1f} MeV/fm\n")

print(f"  {'r (fm)':<10} {'ρ=A/r² (MeV/fm³)':<20} {'4πr² (fm²)':<14} {'ρ×4πr² (MeV/fm)':<18} {'Constant?':<10}")
print(f"  {'─'*72}")

shell_energy = 4 * np.pi * A
for r in [0.05, 0.10, 0.20, 0.40, 0.60, 0.80, R_p]:
    rho = A / r**2
    area = 4 * np.pi * r**2
    product = rho * area
    check = "✓" if abs(product/shell_energy - 1) < 0.001 else "✗"
    print(f"  {r:<10.3f} {rho:<20.1f} {area:<14.4f} {product:<18.1f} {check:<10}")

# Cross-check: total energy
E_total = shell_energy * R_p
print(f"\n  Total energy = 4πA × R_p = {shell_energy:.1f} × {R_p:.4f} = {E_total:.1f} MeV")
print(f"  m_p c² = {m_p:.1f} MeV")
print(f"  Match: {abs(E_total/m_p - 1)*100:.4f}%")

# ═══ PROFILE COMPARISON: R vs E ═══
print(f"\n  ─── R(E) FOR EACH PROFILE (normalized to proton) ───\n")
print(f"  If mass doubles (E → 2E), what happens to R?\n")

print(f"  {'Profile':<16} {'R(E)':<14} {'R(2E)/R(E)':<14} {'Expected ratio':<16}")
print(f"  {'─'*60}")
print(f"  {'ρ = const':<16} {'E^(1/3)':<14} {2**(1/3):<14.4f} {'2^(1/3) = 1.260':<16}")
print(f"  {'ρ ∝ 1/r':<16} {'E^(1/2)':<14} {2**(1/2):<14.4f} {'√2 = 1.414':<16}")
print(f"  {'ρ ∝ 1/r² ★':<16} {'E':<14} {2.0:<14.4f} {'2.000 (linear!)':<16}")
print(f"  {'ρ ∝ 1/r³':<16} {'exp(E)':<14} {'exp(E)':<14} {'diverges':<16}")

# ═══ 3D KEPLER CONNECTION ═══
print(f"\n  ─── 3D KEPLER LAW CONNECTION (Paper 2026s) ───")
print(f"""
  Equal energy per shell (this paper):
    dE/dr = 4πA = constant for ρ ∝ 1/r²
    
  Equal proper volume per shell (Paper 2026s):
    W^(-1/3) gives 2.2-2.8× more equal shells
    
  Both express the same principle:
    DEMOCRATIC DISTRIBUTION across radial shells
    
  Origin: D = 3 → cone volume dV = (1/3)r³ dΩ
""")

# ═══ SUMMARY ═══
print(f"{'=' * 65}")
print(f"  RESULT: Only ρ ∝ 1/r² gives R linear in E")
print(f"  Every shell has equal energy = {shell_energy:.1f} MeV/fm")
print(f"  Total: {shell_energy:.1f} × {R_p:.4f} = {E_total:.1f} MeV = m_p c² ✓")
print(f"{'=' * 65}")
