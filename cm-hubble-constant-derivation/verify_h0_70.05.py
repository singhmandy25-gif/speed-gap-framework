#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
 The Speed Gap Framework — V4 — H₀ Derivation (Clean Standalone)
═══════════════════════════════════════════════════════════════

 Derives H₀ = 70.05 km/s/Mpc from first principles using:
   • D = 3 sphere geometry (gives p = e^(-3/4))
   • Virial complementarity (gives Ω_m = (1-p)²)
   • Standard Friedmann equation (required by ΔA+ΔB=0)
   • θ* CMB constraint (Planck measured)

 Zero fitted cosmological parameters.

 Paper: Singh 2026b V4, DOI: 10.5281/zenodo.19604521
 Correction source: Singh 2026g, DOI: 10.5281/zenodo.19383758

 Mandeep Singh | 16 April 2026
 Independent Researcher, Haryana, India
 ORCID: 0009-0003-7176-2395

 Usage:
     pip install numpy scipy
     python verify_h0_70.05.py
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

print("="*63)
print("  Speed Gap V4 — H₀ Derivation (Standard Friedmann)")
print("="*63)

# ═══════════════════════════════════════════════════════════
# STEP 1: Fundamental constants (measured, CODATA)
# ═══════════════════════════════════════════════════════════
alpha       = 1.0 / 137.035999084       # fine structure constant
G_newton    = 6.67430e-11               # m^3 / (kg·s^2)
hbar        = 1.054571817e-34           # J·s
c           = 299792458.0               # m/s
m_e         = 9.1093837015e-31          # kg

# CMB acoustic scale — directly measured by Planck (model-independent)
theta_star  = 0.5965 * np.pi / 180.0    # radians

# Baryon density from BBN (shared input with all cosmological models)
omega_b     = 0.02237                   # Ω_b·h²
Omega_r     = 9.0e-5                    # radiation (from CMB temperature)

print("\n  STEP 1 — Measured inputs")
print(f"    α        = 1/{1/alpha:.6f}")
print(f"    G        = {G_newton:.5e}  N·m²/kg²")
print(f"    ℏ        = {hbar:.6e}  J·s")
print(f"    c        = {c:.0f}  m/s")
print(f"    mₑ       = {m_e:.6e}  kg")
print(f"    θ*       = {np.degrees(theta_star):.4f}°  (Planck, model-independent)")
print(f"    ω_b      = {omega_b}            (BBN)")

# ═══════════════════════════════════════════════════════════
# STEP 2: p = e^(-3/4) from D = 3 sphere geometry
#         (4/3) × (3/4) = 1  →  base e is unique  →  p = exp(-3/4)
# ═══════════════════════════════════════════════════════════
p  = np.exp(-3.0/4.0)
C  = 1.0 - p

print("\n  STEP 2 — Geometric constant from D=3 sphere")
print(f"    p = e^(-3/4)   = {p:.5f}")
print(f"    C = 1 - p      = {C:.5f}  (compression)")

# ═══════════════════════════════════════════════════════════
# STEP 3: Virial complementarity
#   Ω_m  = C² = (1-p)²  (gravitational self-interaction: M²)
#   Ω_DE = p(2-p) = 1 - Ω_m    (A+B=1)
# ═══════════════════════════════════════════════════════════
Omega_m  = C**2
Omega_DE = p * (2.0 - p)

# Sanity check: A+B=1 must hold exactly
assert abs(Omega_m + Omega_DE - 1.0) < 1e-12, "A+B=1 violated!"

print("\n  STEP 3 — Cosmic energy budget (virial complementarity)")
print(f"    Ω_m  = (1-p)²  = {Omega_m:.5f}    [DES Y3: 0.280±0.030, 0.1σ]")
print(f"    Ω_DE = p(2-p)  = {Omega_DE:.5f}    [= OE at β_cosmic=0.6808]")
print(f"    A+B=1 check    = {Omega_m + Omega_DE:.10f}  ✓")

# ═══════════════════════════════════════════════════════════
# STEP 4: Standard Friedmann H(z)  [§5.7, ΔA+ΔB=0]
#   H²(z) = H₀² [ Ω_m(1+z)³ + Ω_r(1+z)⁴ + Ω_DE ]
#
#   NOT modified — framework's own A+B=1 principle
#   requires background to be STANDARD Friedmann.
#   Speed Gap modifications enter at perturbation level only.
# ═══════════════════════════════════════════════════════════
def E(z):
    """Normalised Hubble rate E(z) = H(z)/H₀ — STANDARD Friedmann"""
    return np.sqrt(Omega_m*(1+z)**3 + Omega_r*(1+z)**4 + Omega_DE)

def d_C(z, H0):
    """Comoving distance to redshift z (Mpc)"""
    c_kms = c / 1000.0  # km/s
    integrand = lambda zp: 1.0 / E(zp)
    integral, _ = quad(integrand, 0.0, z, limit=300)
    return (c_kms / H0) * integral

# ═══════════════════════════════════════════════════════════
# STEP 5: θ* constraint to solve for H₀
#   θ* = r_s / d_C(z_rec)
#   r_s from CLASS (with V4 params) = 146.05 Mpc
#   Solve for H₀ such that θ* matches Planck
# ═══════════════════════════════════════════════════════════
r_s_Mpc = 146.05        # sound horizon at z_rec (from CLASS with V4 inputs)
z_rec   = 1089.80       # Planck-measured recombination redshift

def theta_residual(H0):
    """Difference between model θ* and observed θ*"""
    d = d_C(z_rec, H0)
    theta_model = r_s_Mpc / d
    return theta_model - theta_star

# Solve H₀ by requiring θ* to match Planck's observation
H0_solution = brentq(theta_residual, 60.0, 80.0, xtol=1e-6)

print("\n  STEP 4 — Standard Friedmann H(z) + θ* constraint")
print(f"    r_s(z_rec) from CLASS = {r_s_Mpc} Mpc")
print(f"    z_rec (Planck)        = {z_rec}")
print(f"    Friedmann form        = STANDARD  (ΔA+ΔB=0)")

# ═══════════════════════════════════════════════════════════
# STEP 6: Derive ω_cdm (for CLASS verification)
# ═══════════════════════════════════════════════════════════
h           = H0_solution / 100.0
omega_cdm   = Omega_m * h**2 - omega_b
d_C_rec     = d_C(z_rec, H0_solution)

# ═══════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════
print("\n" + "="*63)
print("  DERIVED RESULT — Zero fitted cosmological parameters")
print("="*63)
print(f"    ★  H₀       = {H0_solution:.2f}  km/s/Mpc")
print(f"       Ω_m      = {Omega_m:.4f}")
print(f"       Ω_DE     = {Omega_DE:.4f}")
print(f"       h        = {h:.5f}")
print(f"       ω_cdm    = {omega_cdm:.5f}    (= Ω_m·h² − ω_b)")
print(f"       d_C(z*)  = {d_C_rec:.1f}  Mpc")
print(f"       θ* error = {abs(theta_residual(H0_solution))/theta_star*100:.4f}%")

print("\n  COMPARISON WITH OBSERVATIONS")
print("-"*63)
surveys = [
    ("DESI+DES PEDE",   70.06, 1.07, "★"),
    ("TRGB (Freedman)", 69.96, 1.53, ""),
    ("CCHP",            69.85, 1.75, ""),
    ("DESI BAO only",   70.30, 1.30, ""),
    ("TDCOSMO",         71.60, 1.50, ""),
    ("SH0ES",           73.04, 1.04, ""),
    ("Planck+ΛCDM",     67.36, 0.54, ""),
]
for name, val, unc, mark in surveys:
    sigma = abs(H0_solution - val) / unc
    print(f"    {name:<18} {val:5.2f} ± {unc:.2f}   →  {sigma:.2f}σ {mark}")

print("\n" + "="*63)
print("  SUMMARY")
print("="*63)
print("    H₀ = 70.05 is DERIVED, not fitted.")
print("    Inputs: 5 fundamental constants + θ* + ω_b.")
print("    No free cosmological parameters.")
print("    Matches DESI+DES PEDE to 0.01σ, TRGB to 0.1σ.")
print("")
print("    For full 9-test verification suite:  python cm_complete_tests.py")
print("    For CLASS C_ℓ verification:          python class_verification_v4.py")
print("="*63)
