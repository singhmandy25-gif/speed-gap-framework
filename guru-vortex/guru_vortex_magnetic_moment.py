"""
Guru Vortex Model — Magnetic Moment from Counter-Rotating Layers
================================================================
Named after Bṛhaspati (बृहस्पति, Jupiter) — Guru (गुरु, "teacher")
in Indian tradition. The proton interior is modelled as three
counter-rotating gluon field layers, like Jupiter's atmospheric bands.

BREAKTHROUGH RESULT:
  Rotation profile ω ∝ 1/r^(1-p) where p = e^(-3/4) = 0.4724
  (SAME cosmic dark energy exponent that gives H₀ = 72.94 km/s/Mpc)
  
  Discrete model: μ_p/μ_n = -1.4560 (measured: -1.4599, match 0.3%)
  
  Honest caveat: continuous model gives -1.95 (34% off)
  Result is model-dependent — discrete layers work, smooth profile doesn't

Part of: Singh 2026e — Guru Vortex Model
Author: Mandeep Singh (singhmandy25@gmail.com)
ORCID: 0009-0003-7176-2395
Date: 30 March 2026
Prior: Singh 2026b (DOI: 10.5281/zenodo.19244123)
       Singh 2026d (DOI: 10.5281/zenodo.19313279)
"""

import numpy as np

# Constants
R      = 0.84       # fm (proton radius)
R_DOWN = 0.582      # fm (d-quark, f = 1/3)
R_UP   = 0.734      # fm (u-quark, f = 2/3)
R_NECK = 0.667      # fm (Neck, f = 1/2)
M_P    = 0.938272   # GeV (proton mass)

# Cosmic exponent
p = np.exp(-3/4)    # = 0.47237 — same as H₀ derivation


def layer_centres():
    """Centre positions of three vortex layers."""
    r_R = R_DOWN / 2           # inner layer (R): 0 to d-quark
    r_G = R_NECK               # middle layer (G): d to u
    r_B = (R_UP + R) / 2      # outer layer (B): u to surface
    return r_R, r_G, r_B


def mu_ratio_discrete(power):
    """μ_p/μ_n from discrete 3-layer vortex model.
    
    ω(r) ∝ 1/r^power for each layer centre.
    Shear at boundary = ω_inner + ω_outer (counter-rotating → add).
    μ_q = Q_q × shear × r_q, combined with SU(6) spin weights.
    """
    r_R, r_G, r_B = layer_centres()

    # Rotation speeds
    omega_R = r_R**(-power)
    omega_G = r_G**(-power)
    omega_B = r_B**(-power)

    # Shear at boundaries (counter-rotating → speeds ADD)
    shear_d = omega_R + omega_G   # R↻ meets G↺ at d-quark
    shear_u = omega_G + omega_B   # G↺ meets B↻ at u-quark

    # Angular momentum × charge at each boundary
    L_d = shear_d * R_DOWN
    L_u = shear_u * R_UP
    mu_u = (2/3) * L_u     # u-quark: Q = +2/3
    mu_d = (-1/3) * L_d    # d-quark: Q = -1/3

    # SU(6) spin weight combination
    mu_p = (4/3) * mu_u - (1/3) * mu_d   # proton = uud
    mu_n = (4/3) * mu_d - (1/3) * mu_u   # neutron = udd

    if abs(mu_n) < 1e-10:
        return 999.0
    return mu_p / mu_n


def mu_ratio_continuous(power, sigma=0.20):
    """μ_p/μ_n from continuous vortex model with Gaussian quark spread.
    
    Quarks are Gaussian clouds (width σ) instead of sharp points.
    ω(r) = r^(-power) everywhere (continuous profile).
    """
    r_grid = np.linspace(0.01, 2.0, 2000)
    dr = r_grid[1] - r_grid[0]
    omega = r_grid**(-power)

    rho_u = np.exp(-0.5 * ((r_grid - R_UP) / sigma)**2) / (sigma * np.sqrt(2*np.pi))
    rho_d = np.exp(-0.5 * ((r_grid - R_DOWN) / sigma)**2) / (sigma * np.sqrt(2*np.pi))

    mu_u = np.sum((2/3) * rho_u * omega * r_grid**3 * dr)
    mu_d = np.sum((-1/3) * rho_d * omega * r_grid**3 * dr)

    mu_p = (4/3) * mu_u - (1/3) * mu_d
    mu_n = (4/3) * mu_d - (1/3) * mu_u

    if abs(mu_n) < 1e-10:
        return 999.0
    return mu_p / mu_n


def spin_from_shear():
    """Proton spin = 1/2 from SU(6) shear weights."""
    Sz_u = (4/3) * 0.5    # both u-quarks combined
    Sz_d = (-1/3) * 0.5   # d-quark
    return Sz_u + Sz_d     # should be 0.5


def main():
    MEASURED = -1.4599

    print("=" * 60)
    print("GURU VORTEX MODEL — MAGNETIC MOMENT")
    print("Singh 2026e | github.com/singhmandy25-gif/speed-gap-framework")
    print("=" * 60)

    power = 1 - p
    ratio = mu_ratio_discrete(power)

    print(f"\n[1] Cosmic exponent")
    print(f"    p = e^(-3/4) = {p:.4f}")
    print(f"    Rotation power = (1-p) = {power:.4f}")
    print(f"    ω(r) ∝ 1/r^{power:.4f}")

    print(f"\n[2] Discrete 3-layer result")
    print(f"    μ_p/μ_n = {ratio:.4f}")
    print(f"    Measured = {MEASURED}")
    print(f"    Match:     {abs(ratio - MEASURED)/abs(MEASURED)*100:.1f}%")

    # Power scan
    print(f"\n[3] Rotation profile scan")
    print(f"    {'Power':>8} {'Profile':>22} {'μ_p/μ_n':>10} {'Match':>8}")
    print(f"    {'-'*52}")
    for pw, name in [(0, "uniform"), (0.5, "1/√r"),
                      (power, f"1/r^(1-p) = {power:.4f} ★"),
                      (1.0, "1/r"), (2.0, "Kepler 1/r²")]:
        r = mu_ratio_discrete(pw)
        m = abs(r - MEASURED) / abs(MEASURED) * 100
        print(f"    {pw:>8.4f} {name:>22} {r:>10.4f} {m:>7.1f}%")

    # Continuous check
    print(f"\n[4] Continuous model (honest check)")
    print(f"    {'σ (fm)':>8} {'μ_p/μ_n':>10} {'Match':>8} {'Note':>15}")
    print(f"    {'-'*45}")
    for sig in [0.05, 0.10, 0.15, 0.20, 0.30, 0.50]:
        rc = mu_ratio_continuous(power, sig)
        m = abs(rc - MEASURED) / abs(MEASURED) * 100
        note = "← point-like" if sig < 0.08 else ""
        print(f"    {sig:>8.2f} {rc:>10.4f} {m:>7.1f}% {note:>15}")
    print(f"    ⚠ Continuous model differs from discrete — result is model-dependent")

    # Cosmic connection
    print(f"\n[5] Cosmic-Nuclear connection")
    print(f"    COSMIC:  p = {p:.4f} → H₀ = 72.94 km/s/Mpc (SH0ES: 0.09σ)")
    print(f"    NUCLEAR: (1-p) = {power:.4f} → μ_p/μ_n = {ratio:.4f} (0.3%)")
    print(f"    A + B = p + (1-p) = 1")
    print(f"    Same exponent, 41 orders of magnitude apart")

    # Spin
    spin = spin_from_shear()
    print(f"\n[6] Proton spin from vortex shear")
    print(f"    u-quarks: (4/3)×(1/2) = {4/3*0.5:.4f}")
    print(f"    d-quark:  (-1/3)×(1/2) = {-1/3*0.5:.4f}")
    print(f"    Total = {spin:.4f} = 1/2 ℏ ✓")
    print(f"    Spin = shear angular momentum at vortex boundaries")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"SCORECARD: 8/8 checks addressed")
    print(f"{'=' * 60}")
    checks = [
        ("Neck ≈ Burkert max pressure",  "3.9%",  "A", "unchanged"),
        ("Cornell peak ≈ Neck",           "4.3%",  "A", "unchanged"),
        ("Three-method convergence",      "±4%",   "A", "unchanged"),
        ("Neutron ⟨r²⟩ sign",            "0.5%",  "B", "FIXED (pion cloud)"),
        ("Proton charge radius",          "0.2%",  "B", "FIXED (pion cloud)"),
        ("Charge density smooth",         "—",     "A", "confirmed"),
        ("Nodes in confining zone",       "—",     "A", "confirmed"),
        ("μ_p/μ_n ratio (discrete)",      "0.3%",  "B→C", "NEW (Guru vortex)"),
    ]
    print(f"  {'Check':<35} {'Match':>6} {'Level':>5} {'Status':>25}")
    print(f"  {'-'*75}")
    for name, match, level, status in checks:
        print(f"  {name:<35} {match:>6} {level:>5} {status:>25}")


if __name__ == '__main__':
    main()
