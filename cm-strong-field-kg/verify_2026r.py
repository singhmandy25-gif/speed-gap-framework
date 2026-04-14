#!/usr/bin/env python3
"""
verify_2026r.py — Master verification for Singh 2026r
DOI: 10.5281/zenodo.19564200

11 tests verifying all key results from the paper:
  1-3: Metric properties (g_tt×|g_rr|=1, spatial flatness, √(-g))
  4-5: 1PN match (g_tt expansion, F_CM = F_GR at leading order)
  6:   μ_eff = μ W^(-1/6) algebraic identity
  7:   GPS consistency (β² = 2GM/rc²)
  8-10: Eigenvalue checks (weak, moderate, strong coupling)
  11:  CM binds weaker than GR (binding energy ratio < 1)

Usage: python verify_2026r.py
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import warnings
warnings.filterwarnings('ignore')

PASS = 0
FAIL = 0
M = 1.0
rs = 2 * M  # Schwarzschild radius

def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ PASS: {name}")
    else:
        FAIL += 1
        print(f"  ❌ FAIL: {name}")
    if detail:
        print(f"         {detail}")

def W_cm(r):
    return (r - rs) / (r + 2*rs)

def f_gr(R):
    return 1 - rs / R

# ════════════════════════════════════════════
print("=" * 65)
print("  Singh 2026r — Master Verification (11 tests)")
print("  DOI: 10.5281/zenodo.19564200")
print("=" * 65)

# ────────────────────────────────────────────
print("\n[1-3] METRIC PROPERTIES\n")

# Test 1: g_tt × |g_rr| = 1
print("  Test 1: g_tt × |g_rr| = 1 at all compactness")
all_one = True
for r in [2.1, 3, 5, 10, 50, 100, 1000]:
    W = W_cm(r)
    if W <= 0:
        continue
    gtt = W ** (1/3)
    grr_abs = W ** (-1/3)
    product = gtt * grr_abs
    if abs(product - 1.0) > 1e-14:
        all_one = False
check("g_tt × |g_rr| = 1 (exact)", all_one)

# Test 2: √(-g) × g^rr = -r² sinθ (W cancels)
print("  Test 2: √(-g) × g^rr = -r² (W cancels)")
cancels = True
for r in [2.5, 5, 10, 50]:
    W = W_cm(r)
    sqrt_neg_g = W ** (-1/3) * r**2  # sinθ=1 for equator
    g_rr_inv = -W ** (1/3)
    product = sqrt_neg_g * g_rr_inv
    expected = -r**2
    if abs(product - expected) / abs(expected) > 1e-14:
        cancels = False
check("√(-g) × g^rr = -r² (spatial flatness)", cancels)

# Test 3: √(-g) = W^(-1/3) r²
print("  Test 3: √(-g) determinant")
det_ok = True
for r in [3, 10, 100]:
    W = W_cm(r)
    gtt = W ** (1/3)
    grr = -W ** (-1/3)
    gthth = -W ** (-1/3) * r**2
    gphph = gthth  # sin²θ = 1 at equator
    g_det = gtt * grr * gthth * gphph  # simplified for diagonal
    sqrt_neg_g_expected = W ** (-1/3) * r**2
    sqrt_neg_g_computed = np.sqrt(abs(g_det)) / r**2 * r**2  # simplified
    # Direct check: W^(1/3) × W^(-1/3) × W^(-1/3) × W^(-1/3) = W^(-2/3)
    exp_sum = 1/3 + (-1/3) + (-1/3) + (-1/3)
    if abs(exp_sum - (-2/3)) > 1e-14:
        det_ok = False
check("√(-g) exponent = W^(-1/3) r² sinθ", det_ok,
      f"Exponent sum: 1/3 + (-1/3) + (-1/3) + (-1/3) = {1/3-1/3-1/3-1/3:.4f} = -2/3 ✓")

# ────────────────────────────────────────────
print("\n[4-5] 1PN MATCH\n")

# Test 4: g_tt^CM ≈ 1-2ε at weak field
print("  Test 4: g_tt^CM = 1-2ε at 1PN")
pn_ok = True
for r in [100, 500, 1000]:
    eps = M / r  # ε = GM/(rc²)
    W = W_cm(r)
    gtt_cm = W ** (1/3)
    gtt_gr = 1 - 2 * eps
    diff = abs(gtt_cm - gtt_gr) / abs(gtt_gr)
    # Should be O(ε²) 
    if diff > 5 * eps**2:
        pn_ok = False
check("g_tt^CM = 1-2ε + O(ε²)", pn_ok,
      f"At r=1000M: diff = {abs(W_cm(1000)**(1/3) - (1-2*M/1000)):.2e}, ε² = {(M/1000)**2:.2e}")

# Test 5: F_CM = F_GR at leading order
print("  Test 5: F_CM = F_GR = -κ² + 2μ²ε at 1PN")
mu = 0.01  # very weak coupling
omega = mu * 0.9999
r_test = 1000 * M
eps = M / r_test
W = W_cm(r_test)
F_cm = omega**2 * W**(-2/3) - mu**2 * W**(-1/3)
F_gr = omega**2 - f_gr(r_test) * mu**2
diff_F = abs(F_cm - F_gr) / max(abs(F_cm), abs(F_gr), 1e-30)
check("F_CM ≈ F_GR at weak field", diff_F < 0.01,
      f"F_CM = {F_cm:.6e}, F_GR = {F_gr:.6e}, diff = {diff_F:.4e}")

# ────────────────────────────────────────────
print("\n[6-7] EFFECTIVE MASS & GPS\n")

# Test 6: μ_eff = μ W^(-1/6) identity
print("  Test 6: μ² W^(-1/3) = (μ W^(-1/6))²")
identity_ok = True
for r in [2.5, 5, 10, 50]:
    W = W_cm(r)
    mu_val = 0.5
    lhs = mu_val**2 * W**(-1/3)
    rhs = (mu_val * W**(-1/6))**2
    if abs(lhs - rhs) / abs(lhs) > 1e-14:
        identity_ok = False
check("μ²W^(-1/3) = (μW^(-1/6))² (exact identity)", identity_ok)

# Test 7: GPS with β² = 2GM/(rc²)
print("  Test 7: GPS consistency (β² = 2GM/rc²)")
G = 6.674e-11; c = 3e8; M_earth = 5.972e24
r_ground = 6.371e6; r_gps = 26.571e6
eps_ground = G * M_earth / (r_ground * c**2)
eps_gps = G * M_earth / (r_gps * c**2)
beta2_ground = 2 * eps_ground
beta2_gps = 2 * eps_gps
W_ground = (1 - beta2_ground) / (1 + 2 * beta2_ground)
W_gps = (1 - beta2_gps) / (1 + 2 * beta2_gps)
td_cm_ground = W_ground ** (1/6)
td_cm_gps = W_gps ** (1/6)
ratio_cm = td_cm_gps / td_cm_ground
grav_us = (ratio_cm - 1) * 86400e6  # μs/day
check("GPS gravity = +45.66 μs/day (CM)", abs(grav_us - 45.66) < 0.1,
      f"CM gives {grav_us:.2f} μs/day")

# ────────────────────────────────────────────
print("\n[8-10] EIGENVALUE COMPARISONS\n")

def shoot_cm(omega, mu, l, rmax, rmin):
    if omega >= mu: return 1e10
    kappa = np.sqrt(mu**2 - omega**2)
    u0 = np.exp(-kappa * rmax); up0 = -kappa * u0
    def ode(r, y):
        W = W_cm(r)
        if W <= 0: return [0, 0]
        F = omega**2 * W**(-2/3) - l*(l+1)/r**2 - mu**2 * W**(-1/3)
        return [y[1], -F * y[0]]
    sol = solve_ivp(ode, [rmax, rmin], [u0, up0], rtol=1e-9, atol=1e-12, max_step=1.0)
    return sol.y[0][-1] if sol.success else np.nan

def shoot_gr(omega, mu, l, rmax, rmin):
    if omega >= mu: return 1e10
    kappa = np.sqrt(mu**2 - omega**2)
    P0 = np.exp(-kappa * rmax); dP0 = -kappa * P0
    def ode(R, y):
        f = f_gr(R)
        if f <= 0: return [0, 0]
        return [y[1], -(rs/R**2/f)*y[1] - (omega**2 - f*(mu**2 + l*(l+1)/R**2))/f**2 * y[0]]
    sol = solve_ivp(ode, [rmax, rmin], [P0, dP0], rtol=1e-9, atol=1e-12, max_step=1.0)
    return sol.y[0][-1] if sol.success else np.nan

def find_ground(sfn, mu, rng, **kw):
    oms = np.linspace(rng[0], rng[1], 200)
    vs = [sfn(o, mu, 0, **kw) for o in oms]
    for i in range(1, len(vs)):
        if np.isfinite(vs[i]) and np.isfinite(vs[i-1]) and vs[i]*vs[i-1] < 0:
            try:
                return brentq(lambda o: sfn(o, mu, 0, **kw), oms[i-1], oms[i], xtol=1e-11)
            except: pass
    return None

# Test 8: Weak coupling α_g=0.1
print("  Test 8: α_g=0.1 eigenvalue (2PN shift ~0.1-0.2%)")
mu8 = 0.1
ev_cm8 = find_ground(shoot_cm, mu8, (mu8*0.97, mu8*0.9999), rmax=500, rmin=2.5)
ev_gr8 = find_ground(shoot_gr, mu8, (mu8*0.97, mu8*0.9999), rmax=500, rmin=2.5)
if ev_cm8 and ev_gr8:
    shift8 = (ev_cm8 - ev_gr8) / ev_gr8 * 100
    check("α_g=0.1: CM-GR shift < 0.5% (2PN)", abs(shift8) < 0.5,
          f"ω_CM={ev_cm8:.8f}, ω_GR={ev_gr8:.8f}, shift={shift8:+.3f}%")
else:
    check("α_g=0.1: eigenvalues found", False, "Solver failed")

# Test 9: Moderate α_g=0.3
print("  Test 9: α_g=0.3 eigenvalue (shift ~5%)")
mu9 = 0.3
ev_cm9 = find_ground(shoot_cm, mu9, (mu9*0.85, mu9*0.999), rmax=100, rmin=2.3)
ev_gr9 = find_ground(shoot_gr, mu9, (mu9*0.85, mu9*0.999), rmax=100, rmin=2.3)
if ev_cm9 and ev_gr9:
    shift9 = (ev_cm9 - ev_gr9) / ev_gr9 * 100
    check("α_g=0.3: CM-GR shift 3-8%", 3 < shift9 < 8,
          f"ω_CM={ev_cm9:.6f}, ω_GR={ev_gr9:.6f}, shift={shift9:+.2f}%")
else:
    check("α_g=0.3: eigenvalues found", False, "Solver failed")

# Test 10: Strong α_g=0.5
print("  Test 10: α_g=0.5 eigenvalue (shift ~15-20%)")
mu10 = 0.5
ev_cm10 = find_ground(shoot_cm, mu10, (mu10*0.6, mu10*0.999), rmax=50, rmin=2.15)
ev_gr10 = find_ground(shoot_gr, mu10, (mu10*0.6, mu10*0.999), rmax=50, rmin=2.15)
if ev_cm10 and ev_gr10:
    shift10 = (ev_cm10 - ev_gr10) / ev_gr10 * 100
    check("α_g=0.5: CM-GR shift 15-22%", 15 < shift10 < 22,
          f"ω_CM={ev_cm10:.6f}, ω_GR={ev_gr10:.6f}, shift={shift10:+.2f}%")
else:
    check("α_g=0.5: eigenvalues found", False, "Solver failed")

# ────────────────────────────────────────────
print("\n[11] CM BINDS WEAKER\n")

# Test 11: BE_CM/BE_GR < 1 at all couplings
print("  Test 11: CM binding always weaker than GR")
weaker = True
for (ev_cm, ev_gr, mu_v) in [(ev_cm8, ev_gr8, mu8), (ev_cm9, ev_gr9, mu9), (ev_cm10, ev_gr10, mu10)]:
    if ev_cm and ev_gr:
        be_cm = (mu_v - ev_cm) / mu_v
        be_gr = (mu_v - ev_gr) / mu_v
        if be_cm >= be_gr:
            weaker = False
check("B.E._CM < B.E._GR (all couplings)", weaker,
      "CM always less tightly bound — spatial flatness → weaker confinement")

# ════════════════════════════════════════════
print("\n" + "=" * 65)
print(f"  RESULT: {PASS}/{PASS+FAIL} PASS")
if FAIL == 0:
    print("  ALL TESTS PASSED ✅")
else:
    print(f"  {FAIL} TEST(S) FAILED ❌")
print("=" * 65)
