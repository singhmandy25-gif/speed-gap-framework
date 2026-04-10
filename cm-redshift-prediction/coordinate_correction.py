#!/usr/bin/env python3
"""
coordinate_correction.py — Verify §2 of Singh 2026n
Isotropic → circumferential coordinate conversion for CM metric.

The CM metric uses isotropic coordinates:
  ds² = W^(1/3)dt² − W^(−1/3)(dr² + r²dΩ²)

Physical (circumferential) radius:
  R_circ = r × W^(−1/6)

Paper 2026j incorrectly compared CM isotropic r with GR circumferential R.
This script verifies the corrected values.

Author: Mandeep Singh
"""
import numpy as np

def W(beta2):
    """CM compression function"""
    return (1 - beta2) / (1 + 2*beta2)

def R_circ(r_iso, beta2):
    """Circumferential radius from isotropic coordinate"""
    return r_iso * W(beta2)**(-1/6)

print("="*60)
print("§2: COORDINATE CORRECTION VERIFICATION")
print("="*60)

# ── Photon sphere ──
print("\n── Photon Sphere ──")
r_ph = np.sqrt(2)        # CM photon sphere in isotropic coords
b2_ph = 1/r_ph           # β² = r_s/r (natural units, r_s=1)
W_ph = W(b2_ph)
R_ph = R_circ(r_ph, b2_ph)

print(f"  r_isotropic  = {r_ph:.4f} r_s")
print(f"  β²           = {b2_ph:.6f}")
print(f"  W            = {W_ph:.6f}")
print(f"  W^(-1/6)     = {W_ph**(-1/6):.6f}")
print(f"  R_circ       = {R_ph:.4f} r_s")
print(f"  GR (Schw.)   = 1.5000 r_s")
print(f"  Deviation    = {(R_ph/1.5-1)*100:+.1f}% (CM FURTHER)")
print(f"  2026j said   = -5.7% (WRONG, mixed coordinates)")

# ── ISCO ──
print("\n── ISCO ──")
r_isco = 2.811
b2_isco = 1/r_isco
W_isco = W(b2_isco)
R_isco = R_circ(r_isco, b2_isco)

print(f"  r_isotropic  = {r_isco:.4f} r_s")
print(f"  β²           = {b2_isco:.6f}")
print(f"  W            = {W_isco:.6f}")
print(f"  W^(-1/6)     = {W_isco**(-1/6):.6f}")
print(f"  R_circ       = {R_isco:.4f} r_s")
print(f"  GR (Schw.)   = 3.0000 r_s")
print(f"  Deviation    = {(R_isco/3.0-1)*100:+.1f}% (CM FURTHER)")
print(f"  2026j said   = -6.3% (WRONG, mixed coordinates)")

# ── Shadow (coordinate-independent) ──
print("\n── Shadow (coordinate-independent) ──")
b_cm = r_ph / W_ph**(1/3)
b_gr = 3*np.sqrt(3)/2
print(f"  b_crit CM    = {b_cm:.3f} r_s")
print(f"  b_crit GR    = {b_gr:.3f} r_s")
print(f"  Ratio        = {b_cm/b_gr:.3f} (+{(b_cm/b_gr-1)*100:.1f}%)")
print(f"  → UNCHANGED by coordinate correction ✓")

# ── Summary table ──
print("\n── Corrected Table (replaces 2026j Table 6) ──")
print(f"{'Quantity':<25} {'GR':>10} {'CM':>10} {'Deviation':>10} {'Coord-free?':>12}")
print(f"{'Photon sphere (circ.)':<25} {'1.500':>10} {R_ph:10.3f} {(R_ph/1.5-1)*100:+9.1f}% {'No':>12}")
print(f"{'Shadow (impact param.)':<25} {b_gr:10.3f} {b_cm:10.3f} {(b_cm/b_gr-1)*100:+9.1f}% {'YES':>12}")
print(f"{'ISCO (circ.)':<25} {'3.000':>10} {R_isco:10.3f} {(R_isco/3.0-1)*100:+9.1f}% {'No':>12}")
print(f"{'ISCO frequency':<25} {'f_GR':>10} {'0.828':>10} {'-17.2%':>10} {'YES':>12}")
print(f"{'ISCO binding':<25} {'5.72%':>10} {'5.45%':>10} {'-4.7%':>10} {'YES':>12}")
