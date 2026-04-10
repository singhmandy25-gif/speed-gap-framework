#!/usr/bin/env python3
"""
redshift_prediction.py — Verify §3-4 of Singh 2026n
Surface redshift: z_CM = W^(-1/6) - 1 vs z_GR = (1-2ε)^(-1/2) - 1

The CM metric predicts 28-37% LESS surface redshift than GR for
NICER-observed neutron stars. This is EOS-independent.

For J0740+6620: Iron Kα at 5.10 keV (CM) vs 4.57 keV (GR) — 540 eV gap.

Author: Mandeep Singh
"""
import numpy as np

G = 6.674e-8      # cm³/(g·s²)
c = 2.998e10       # cm/s
Msun = 1.989e33    # g
km = 1e5           # cm

def z_GR(eps):
    """GR surface redshift: z = (1-2ε)^(-1/2) - 1"""
    return 1/np.sqrt(1 - 2*eps) - 1

def z_CM(eps):
    """CM surface redshift: z = W^(-1/6) - 1"""
    b2 = 2*eps
    W = (1 - b2) / (1 + 2*b2)
    return W**(-1/6) - 1

print("="*65)
print("§3-4: SURFACE REDSHIFT PREDICTIONS")
print("="*65)

# ── Comparison table ──
print(f"\n── Redshift vs Compactness ──")
print(f"{'ε':>6} {'z_GR':>8} {'z_CM':>8} {'Δz/z_GR':>9} {'Regime':<20}")
for eps, regime in [(0.01,"Earth surface"), (0.05,"White dwarf"), 
                     (0.10,"Heavy WD"), (0.15,"Light NS"),
                     (0.177,"J0030 (NICER)"), (0.184,"J0437 (NICER)"),
                     (0.20,"Typical NS"), (0.245,"J0740 (NICER)"),
                     (0.25,"Near maximum"), (0.30,"Maximum NS")]:
    zg = z_GR(eps)
    zc = z_CM(eps)
    dz = (zc-zg)/zg*100
    print(f"{eps:6.3f} {zg:8.4f} {zc:8.4f} {dz:+8.1f}% {regime:<20}")

# ── Taylor expansion ──
print(f"\n── Taylor: Δz ≈ -2ε² (Eq. 3.6) ──")
print(f"{'ε':>6} {'Δz exact':>12} {'−2ε²':>12} {'Ratio':>8}")
for eps in [0.01, 0.02, 0.05, 0.10, 0.15, 0.20]:
    dz = z_CM(eps) - z_GR(eps)
    approx = -2*eps**2
    print(f"{eps:6.3f} {dz:12.6f} {approx:12.6f} {dz/approx:8.3f}")

# ── NICER pulsars ──
print(f"\n── NICER Pulsar Predictions ──")
pulsars = [
    ("J0030+0451", 1.40, 11.71, "Riley+ 2019"),
    ("J0437-4715", 1.418, 11.36, "Choudhury+ 2024"),
    ("J0740+6620", 2.073, 12.49, "Riley+ 2021"),
]

for name, M, R, ref in pulsars:
    eps = G*M*Msun/(R*km*c**2)
    zg = z_GR(eps); zc = z_CM(eps)
    Eg = 6.4/(1+zg); Ec = 6.4/(1+zc)
    gap = Ec - Eg
    dz_pct = (zc-zg)/zg*100
    
    print(f"\n  {name} (M={M} M☉, R={R} km) [{ref}]")
    print(f"    ε = {eps:.4f}")
    print(f"    z_GR = {zg:.4f},  z_CM = {zc:.4f},  Δz = {dz_pct:+.1f}%")
    print(f"    Iron Kα: GR = {Eg:.2f} keV,  CM = {Ec:.2f} keV")
    print(f"    Gap = {gap:.2f} keV = {gap*1000:.0f} eV")
    if gap*1000 > 100:
        print(f"    XRISM (5 eV): {gap*1000/5:.0f}σ detection")

# ── All spectral lines for J0740 ──
print(f"\n── All Lines for J0740+6620 ──")
eps740 = G*2.073*Msun/(12.49*km*c**2)
zg740 = z_GR(eps740); zc740 = z_CM(eps740)

lines = [("O VIII Lyα", 0.654), ("Iron Kα", 6.400), ("Fe XXV", 6.700),
         ("Fe XXVI", 6.966), ("Iron Kβ", 7.058)]

print(f"  z_GR = {zg740:.4f}, z_CM = {zc740:.4f}")
print(f"  {'Line':<16} {'E_rest':>8} {'E_GR':>8} {'E_CM':>8} {'Gap(eV)':>8}")
for lname, E in lines:
    Eg = E/(1+zg740); Ec = E/(1+zc740)
    print(f"  {lname:<16} {E:8.3f} {Eg:8.3f} {Ec:8.3f} {(Ec-Eg)*1000:8.0f}")

# ── 4U 1820-30 inverse problem ──
print(f"\n── 4U 1820-30: Inverse Problem (§5) ──")
z_obs = 0.72
eps_gr = (1 - 1/(1+z_obs)**2)/2
W_cm = (1+z_obs)**(-6)
eps_cm = (1-W_cm)/(4*W_cm+2)

print(f"  Observed z = {z_obs}")
print(f"  If GR correct:  ε = {eps_gr:.4f} → M = {eps_gr*10*km*c**2/G/Msun:.2f} M☉ at R=10km")
print(f"  If CM correct:  ε = {eps_cm:.4f} → M = {eps_cm*10*km*c**2/G/Msun:.2f} M☉ at R=10km")
print(f"  → If M < 2.5 M☉ confirmed: FAVOURS GR (CM needs >3 M☉)")

print(f"\n{'='*65}")
print(f"PREDICTION: One spectral line measurement decides CM vs GR.")
print(f"{'='*65}")
