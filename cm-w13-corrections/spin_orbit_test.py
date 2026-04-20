"""
spin_orbit_test.py — Singh 2026u, Chapter 4
Five spin correction variants tested against hydrogen-like ions.
Result: every correction makes it WORSE. Plain W⁻¹/³ is optimal.

Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
"""

import numpy as np

m_e = 511099.0  # eV
alpha = 1/137.035999206

def W_func(b2): return (1 - b2)/(1 + 2*b2)
def V_frac(b2): return W_func(b2)**(-1/3) - 1

def E_plain_cm(Z):
    """Plain CM: E = ½ m_e c² × (W⁻¹/³ − 1)"""
    b2 = (Z*alpha)**2
    return 0.5 * m_e * V_frac(b2)

def E_cm_minus_R4(Z):
    """CM − R/4: multiply by (1 − β²/4)"""
    b2 = (Z*alpha)**2
    return 0.5 * m_e * V_frac(b2) * (1 - b2/4)

def E_cm_plus_R4(Z):
    """CM + R/4: spin from 2026m (V×W×6/20)"""
    b2 = (Z*alpha)**2
    Vf = V_frac(b2)
    W = W_func(b2)
    return 0.5 * m_e * Vf * (1 + Vf * W * 6/20)

def E_cm_3quarter(Z):
    """CM × 3/4 + ¼β²: D/(D+1) weighting"""
    b2 = (Z*alpha)**2
    return 0.5 * m_e * (0.75 * V_frac(b2) + 0.25 * b2)

def E_w14(Z):
    """W⁻¹/⁴ instead of W⁻¹/³"""
    b2 = (Z*alpha)**2
    W = W_func(b2)
    return 0.5 * m_e * (W**(-1/4) - 1)

def E_dirac(Z):
    g = np.sqrt(1 - (Z*alpha)**2)
    return m_e * (1 - g)

# Test ions
ions = [
    ("H",     1,    13.6),
    ("C5+",   6,    490.0),
    ("Ne9+",  10,   1362.2),
    ("Ar17+", 18,   4426.2),
    ("Fe25+", 26,   9277.7),
    ("Kr35+", 36,   17936.0),
    ("Ag46+", 47,   30313.0),
    ("Xe53+", 54,   40271.0),
    ("W73+",  74,   79296.0),
    ("Au78+", 79,   93460.0),
    ("U91+",  92,   131810.0),
]

methods = [
    ("Plain CM",    E_plain_cm),
    ("CM−R/4",      E_cm_minus_R4),
    ("CM+R/4",      E_cm_plus_R4),
    ("CM×3/4",      E_cm_3quarter),
    ("W⁻¹/⁴",      E_w14),
    ("Dirac",       E_dirac),
]

print("=" * 80)
print("  Singh 2026u Ch 4 — Spin-Orbit Test: 5 Variants")
print("=" * 80)

# ═══ MAIN TABLE ═══
header = f"  {'Ion':<8} {'Z':<4}"
for name, _ in methods:
    header += f" {name:<10}"
print(f"\n{header}")
print(f"  {'─'*76}")

all_errs = {name: [] for name, _ in methods}

for ion_name, Z, Em in ions:
    row = f"  {ion_name:<8} {Z:<4}"
    for mname, mfunc in methods:
        E = mfunc(Z)
        err = abs(E/Em - 1) * 100
        all_errs[mname].append(err)
        row += f" {err:<10.2f}"
    print(row)

# ═══ AVERAGES ═══
print(f"  {'─'*76}")
row = f"  {'Avg |err|':<12}"
for mname, _ in methods:
    avg = np.mean(all_errs[mname])
    row += f" {avg:<10.2f}"
print(row)

# ═══ RANKING ═══
print(f"\n  ─── RANKING (best to worst) ───\n")
avgs = [(np.mean(all_errs[name]), name) for name, _ in methods]
avgs.sort()

for i, (avg, name) in enumerate(avgs):
    marker = "★ BEST" if i == 0 else ""
    ratio = f"{avg/avgs[0][0]:.1f}× worse" if i > 0 else ""
    print(f"  {i+1}. {name:<12} {avg:.2f}%  {ratio}  {marker}")

# ═══ W⁻¹/⁴ FAILURE EXPLANATION ═══
print(f"\n  ─── Why W⁻¹/⁴ fails: weak-field check ───")
b2_small = 0.001
V_13 = W_func(b2_small)**(-1/3) - 1
V_14 = W_func(b2_small)**(-1/4) - 1
print(f"  At β² = {b2_small}:")
print(f"    W⁻¹/³ − 1 = {V_13:.6f}  (ratio to β²: {V_13/b2_small:.4f} → 1.0)")
print(f"    W⁻¹/⁴ − 1 = {V_14:.6f}  (ratio to β²: {V_14/b2_small:.4f} → 0.75)")
print(f"  W⁻¹/⁴ gives only 75% of Coulomb → 25% error from start!")

# ═══ SUMMARY ═══
print(f"\n{'=' * 80}")
print(f"  SUMMARY")
print(f"{'=' * 80}")
print(f"""
  Plain W⁻¹/³ is BEST: {avgs[0][1]} at {avgs[0][0]:.2f}%
  
  Every spin correction makes it WORSE:
    CM−R/4:  {np.mean(all_errs['CM−R/4']):.2f}% ({np.mean(all_errs['CM−R/4'])/avgs[0][0]:.0f}× worse)
    CM+R/4:  {np.mean(all_errs['CM+R/4']):.1f}% ({np.mean(all_errs['CM+R/4'])/avgs[0][0]:.0f}× worse)
    CM×3/4:  {np.mean(all_errs['CM×3/4']):.2f}% ({np.mean(all_errs['CM×3/4'])/avgs[0][0]:.1f}× worse)
    W⁻¹/⁴:  {np.mean(all_errs['W⁻¹/⁴']):.1f}% ({np.mean(all_errs['W⁻¹/⁴'])/avgs[0][0]:.0f}× worse)
  
  Reason: W⁻¹/³ already contains spin-orbit EQUIVALENT
  Adding spin on top = DOUBLE COUNTING
""")
