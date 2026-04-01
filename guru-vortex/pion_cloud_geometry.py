"""
Pion Cloud Geometry — Two-Sphere Model (V2: 1 April 2026)
==========================================================
Extends the Damru sphere (Singh 2026d) with an outer pion cloud sphere.

KEY DISCOVERY (1 April 2026):
  P = 0.25 is NOT a free parameter!
  P = 1 - f_horizon = 1 - 3/4 = 1/4
  = volume fraction OUTSIDE confinement horizon
  = leakable fraction = pion fluctuation probability

  Therefore: ZERO free parameters for both fixes:
    1. Neutron ⟨r²⟩ sign: −0.117 fm² (measured: −0.1161, match 0.5%)
    2. Proton charge radius: 0.839 fm (measured: 0.841, match 0.2%)

Part of: Singh 2026e V2 — Guru Vortex Model
Author: Mandeep Singh (singhmandy25@gmail.com)
ORCID: 0009-0003-7176-2395
Date: 30 March 2026 (V2: 1 April 2026)
Prior: Singh 2026d (DOI: 10.5281/zenodo.19313279)
"""

import numpy as np

# Constants
R_INNER = 0.84       # fm (proton radius)
HBARC   = 0.197327   # GeV·fm
M_PI    = 0.140      # GeV (pion mass)

# Damru positions (from f = ξ³)
R_DOWN  = 0.582      # fm (f = 1/3)
R_NECK  = 0.667      # fm (f = 1/2)
R_UP    = 0.734      # fm (f = 2/3)
F_HORIZ = 0.75       # f = 3/4 (confinement horizon)

# Pion cloud parameter — DERIVED from horizon geometry!
P_CLOUD = 1 - F_HORIZ  # = 1/4 = 0.25
R_PION  = 1.0           # fm (outer neck position)


def outer_sphere(R1, r_pi):
    R2 = (2 * r_pi**3 - R1**3)**(1/3)
    V_in = R1**3
    V_shell = R2**3 - V_in
    positions = {}
    for f, name in [(1/3, "f_shell=1/3"), (1/2, "f_shell=1/2 (outer neck)"), (2/3, "f_shell=2/3")]:
        positions[name] = (V_in + f * V_shell)**(1/3)
    return R2, positions, V_in / R2**3


def neutron_r2(P, r_pi):
    r2_val = (2/3) * R_UP**2 + 2 * (-1/3) * R_DOWN**2
    r2_pi  = P * (-1) * r_pi**2
    return r2_val, r2_pi, r2_val + r2_pi


def proton_r_rms(P, r_pi):
    r2_val = 2 * (2/3) * R_UP**2 + (-1/3) * R_DOWN**2
    r2_tot = (1 - P) * r2_val + P * r_pi**2
    return np.sqrt(r2_val), np.sqrt(r2_tot)


def r_pi_for_neutron_match(P, target=-0.1161):
    r2_val = (2/3) * R_UP**2 + 2 * (-1/3) * R_DOWN**2
    return np.sqrt((r2_val - target) / P)


def main():
    print("=" * 60)
    print("PION CLOUD GEOMETRY — TWO-SPHERE MODEL (V2)")
    print("Singh 2026e V2 | 1 April 2026")
    print("github.com/singhmandy25-gif/speed-gap-framework")
    print("=" * 60)

    P, r_pi = P_CLOUD, R_PION

    print(f"\n★ P = 1 - f_horizon = 1 - {F_HORIZ} = {P_CLOUD}")
    print(f"  NOT a free parameter — derived from horizon geometry!")
    print(f"  Volume outside confinement horizon = leakable fraction")
    print(f"  = pion fluctuation probability = 1/4 = 25%")

    R2, pos, ratio = outer_sphere(R_INNER, r_pi)
    print(f"\n[1] Outer sphere (P={P}, r_π={r_pi} fm)")
    print(f"    R_inner = {R_INNER} fm | R_outer = {R2:.3f} fm")
    for name, r in pos.items():
        print(f"    {name:30s} → r = {r:.3f} fm")

    r2v, r2p, r2t = neutron_r2(P, r_pi)
    print(f"\n[2] Neutron ⟨r²⟩ fix (ZERO free parameters)")
    print(f"    Valence: {r2v:+.4f} | Pion: {r2p:+.4f} | Total: {r2t:+.4f}")
    print(f"    Measured: -0.1161 | Match: {abs(r2t + 0.1161)/0.1161*100:.1f}%")

    rms_v, rms_t = proton_r_rms(P, r_pi)
    print(f"\n[3] Proton radius fix (ZERO free parameters)")
    print(f"    Valence: {rms_v:.4f} fm | With cloud: {rms_t:.4f} fm")
    print(f"    Measured: 0.841 fm | Match: {abs(rms_t - 0.841)/0.841*100:.1f}%")

    print(f"\n[4] Volume ratio scan")
    print(f"    {'P':>5} {'r_π':>7} {'R₂':>7} {'V_in/V_tot':>11} {'Note':>22}")
    print(f"    {'-'*56}")
    for Ps in [0.30, 0.25, 0.20, 0.15, 0.10]:
        rp = r_pi_for_neutron_match(Ps)
        R2s, _, rat = outer_sphere(R_INNER, rp)
        note = ""
        if abs(Ps - 0.25) < 0.001: note = "★ P=1-f_horizon!"
        if abs(rat - 0.167) < 0.01: note = "≈ binding margin!"
        print(f"    {Ps:>5.2f} {rp:>7.3f} {R2s:>7.3f} {rat:>11.4f} {note:>22}")


if __name__ == '__main__':
    main()
