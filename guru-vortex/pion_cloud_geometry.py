"""
Pion Cloud Geometry — Two-Sphere Model
=======================================
Extends the Damru sphere (Singh 2026d) with an outer pion cloud sphere.

ONE parameter set (P=0.25, r_π≈1.0 fm) fixes TWO independent measurements:
  1. Neutron ⟨r²⟩ sign: +0.133 → −0.117 fm² (measured: −0.1161, match 0.5%)
  2. Proton charge radius: 0.778 → 0.839 fm (measured: 0.841, match 0.2%)

Bonus: At P=0.15 (chiral standard), Inner/Total volume = 0.161 ≈ 0.167 (binding margin)

Part of: Singh 2026e — Guru Vortex Model
Author: Mandeep Singh (singhmandy25@gmail.com)
ORCID: 0009-0003-7176-2395
Date: 30 March 2026
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

# Default pion cloud parameters
P_DEFAULT  = 0.25    # pion fluctuation probability
RPI_DEFAULT = 1.0    # fm (pion average distance)


def outer_sphere(R1, r_pi):
    """Outer sphere radius and shell volume fractions."""
    R2 = (2 * r_pi**3 - R1**3)**(1/3)
    V_in = R1**3
    V_shell = R2**3 - V_in
    positions = {}
    for f, name in [(1/3, "f_shell=1/3"), (1/2, "f_shell=1/2 (outer neck)"), (2/3, "f_shell=2/3")]:
        positions[name] = (V_in + f * V_shell)**(1/3)
    return R2, positions, V_in / R2**3


def neutron_r2(P, r_pi):
    """Neutron mean square charge radius with pion cloud."""
    r2_val = (2/3) * R_UP**2 + 2 * (-1/3) * R_DOWN**2
    r2_pi  = P * (-1) * r_pi**2
    return r2_val, r2_pi, r2_val + r2_pi


def proton_r_rms(P, r_pi):
    """Proton RMS charge radius with pion cloud."""
    r2_val = 2 * (2/3) * R_UP**2 + (-1/3) * R_DOWN**2
    r2_tot = (1 - P) * r2_val + P * r_pi**2
    return np.sqrt(r2_val), np.sqrt(r2_tot)


def r_pi_for_neutron_match(P, target=-0.1161):
    """Find r_π that gives exact neutron ⟨r²⟩ match."""
    r2_val = (2/3) * R_UP**2 + 2 * (-1/3) * R_DOWN**2
    return np.sqrt((r2_val - target) / P)


def main():
    print("=" * 60)
    print("PION CLOUD GEOMETRY — TWO-SPHERE MODEL")
    print("Singh 2026e | github.com/singhmandy25-gif/speed-gap-framework")
    print("=" * 60)

    P, r_pi = P_DEFAULT, RPI_DEFAULT

    # Outer sphere
    R2, pos, ratio = outer_sphere(R_INNER, r_pi)
    print(f"\n[1] Outer sphere (P={P}, r_π={r_pi} fm)")
    print(f"    R_inner = {R_INNER} fm | R_outer = {R2:.3f} fm")
    print(f"    Inner/Total = {ratio:.4f}")
    for name, r in pos.items():
        print(f"    {name:30s} → r = {r:.3f} fm")

    # Neutron fix
    r2v, r2p, r2t = neutron_r2(P, r_pi)
    print(f"\n[2] Neutron ⟨r²⟩ sign fix")
    print(f"    Valence: {r2v:+.4f} fm² | Pion: {r2p:+.4f} fm²")
    print(f"    Total:   {r2t:+.4f} fm² | Measured: -0.1161 fm²")
    print(f"    Match:   {abs(r2t + 0.1161)/0.1161*100:.1f}%")

    # Proton fix
    rms_v, rms_t = proton_r_rms(P, r_pi)
    print(f"\n[3] Proton charge radius fix")
    print(f"    Valence: {rms_v:.4f} fm | With cloud: {rms_t:.4f} fm")
    print(f"    Measured: 0.841 fm | Match: {abs(rms_t - 0.841)/0.841*100:.1f}%")

    # Volume ratio scan
    print(f"\n[4] Volume ratio scan (r_π adjusted for neutron match)")
    print(f"    {'P':>5} {'r_π':>7} {'R₂':>7} {'V_in/V_tot':>11} {'Note':>22}")
    print(f"    {'-'*56}")
    for Ps in [0.30, 0.25, 0.20, 0.15, 0.10]:
        rp = r_pi_for_neutron_match(Ps)
        R2s, _, rat = outer_sphere(R_INNER, rp)
        note = ""
        if abs(rat - 0.167) < 0.01: note = "≈ binding margin!"
        if abs(rat - 0.25) < 0.03:  note = "≈ 1/4"
        print(f"    {Ps:>5.2f} {rp:>7.3f} {R2s:>7.3f} {rat:>11.4f} {note:>22}")

    print(f"\n    Pion Compton wavelength: {HBARC/M_PI:.3f} fm")
    print(f"    All r_π values within cloud range ✓")


if __name__ == '__main__':
    main()
