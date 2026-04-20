"""
w13_vs_coulomb_vs_dirac.py — Singh 2026u, Chapter 3
Full test: 23 hydrogen-like ions, Z = 1 to 92.
Coulomb vs CM W⁻¹/³ vs Dirac, compared with NIST measured values.

Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
"""

import numpy as np

m_e = 511099.0  # eV
alpha = 1/137.035999206

def E_coulomb(Z): return 0.5 * m_e * (Z*alpha)**2
def E_cm(Z):
    b2 = (Z*alpha)**2
    W = (1 - b2)/(1 + 2*b2)
    return 0.5 * m_e * (W**(-1/3) - 1)
def E_dirac(Z):
    g = np.sqrt(1 - (Z*alpha)**2)
    return m_e * (1 - g)

# ═══ DATA: 23 hydrogen-like ions ═══
# (element, Z, E_measured in eV) — NIST Atomic Spectra Database
ions = [
    ("H",     1,    13.6),
    ("He+",   2,    54.4),
    ("Li2+",  3,    122.5),
    ("Be3+",  4,    217.7),
    ("B4+",   5,    340.2),
    ("C5+",   6,    490.0),
    ("N6+",   7,    667.0),
    ("O7+",   8,    871.4),
    ("F8+",   9,    1103.1),
    ("Ne9+",  10,   1362.2),
    ("Si13+", 14,   2673.2),
    ("Ar17+", 18,   4426.2),
    ("Ti21+", 22,   6625.8),
    ("Fe25+", 26,   9277.7),
    ("Zn29+", 30,   12389.0),
    ("Kr35+", 36,   17936.0),
    ("Mo41+", 42,   24466.0),
    ("Ag46+", 47,   30313.0),
    ("Xe53+", 54,   40271.0),
    ("W73+",  74,   79296.0),
    ("Au78+", 79,   93460.0),
    ("Pb81+", 82,   101137.0),
    ("U91+",  92,   131810.0),
]

print("=" * 80)
print("  Singh 2026u Ch 3 — Full Test: Z = 1 to 92")
print("=" * 80)

# ═══ MAIN TABLE ═══
print(f"\n  {'Ion':<8} {'Z':<4} {'E_Coul':<10} {'E_CM':<10} {'E_Dirac':<10} {'E_meas':<10} {'Coul%':<8} {'CM%':<8} {'Dir%':<8} {'Best'}")
print(f"  {'─'*86}")

cm_wins = 0
cm_beats_both = 0
coul_errs = []
cm_errs = []
dirac_errs = []

for name, Z, Em in ions:
    Ec = E_coulomb(Z)
    Ecm = E_cm(Z)
    Ed = E_dirac(Z)
    
    ec_err = (Ec/Em - 1)*100
    ecm_err = (Ecm/Em - 1)*100
    ed_err = (Ed/Em - 1)*100
    
    coul_errs.append(abs(ec_err))
    cm_errs.append(abs(ecm_err))
    dirac_errs.append(abs(ed_err))
    
    # Determine best
    if abs(ecm_err) < abs(ec_err) and abs(ecm_err) < abs(ed_err):
        best = "CM ★"
        cm_wins += 1
        cm_beats_both += 1
    elif abs(ecm_err) < abs(ec_err):
        best = "CM"
        cm_wins += 1
    elif abs(ed_err) < abs(ec_err):
        best = "Dirac"
    else:
        best = "—"
    
    print(f"  {name:<8} {Z:<4} {Ec:<10.0f} {Ecm:<10.0f} {Ed:<10.0f} {Em:<10.0f} {ec_err:>+7.2f} {ecm_err:>+7.2f} {ed_err:>+7.2f}  {best}")

# ═══ SCORECARD ═══
print(f"\n{'=' * 80}")
print(f"  SCORECARD")
print(f"{'=' * 80}")

avg_coul = np.mean(coul_errs)
avg_cm = np.mean(cm_errs)
avg_dirac = np.mean(dirac_errs)

# Heavy atoms only (Z > 26)
heavy = [(c, m, d) for (_, Z, _), c, m, d in zip(ions, coul_errs, cm_errs, dirac_errs) if Z > 26]
avg_coul_heavy = np.mean([h[0] for h in heavy])
avg_cm_heavy = np.mean([h[1] for h in heavy])
avg_dirac_heavy = np.mean([h[2] for h in heavy])

print(f"""
  CM closer to measured than Coulomb:  {cm_wins}/23
  CM closer than BOTH Coul and Dirac:  {cm_beats_both}/23

  Average |error| (all Z):
    Coulomb:  {avg_coul:.2f}%
    CM:       {avg_cm:.2f}%
    Dirac:    {avg_dirac:.2f}%

  Average |error| (Z > 26, heavy atoms):
    Coulomb:  {avg_coul_heavy:.2f}%
    CM:       {avg_cm_heavy:.2f}%
    Dirac:    {avg_dirac_heavy:.2f}%

  Uranium (Z=92):
    Coulomb: {coul_errs[-1]:.2f}%  →  CM: {cm_errs[-1]:.2f}%
    Improvement: {coul_errs[-1]/cm_errs[-1]:.0f}× better

  Gap closed (Coulomb → Dirac):
    Total gap: {avg_coul:.2f} − {avg_dirac:.2f} = {avg_coul - avg_dirac:.2f}%
    CM closes: {avg_coul:.2f} − {avg_cm:.2f} = {avg_coul - avg_cm:.2f}%
    Fraction:  {(avg_coul - avg_cm)/(avg_coul - avg_dirac)*100:.1f}%

  Free parameters: ZERO
""")
