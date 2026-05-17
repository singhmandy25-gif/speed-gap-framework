#!/usr/bin/env python3
"""
Q = 0 for CM density ρ = A/r² in D = 3
Q_coeff = −(D−1)(D−3)/4 → zero only at D=1 (trivial) and D=3
Verifies Singh 2026z, Chapters 1-2
"""

mp = 938.272   # MeV
Rp = 0.881     # fm
import numpy as np

print("="*60)
print("CH1: Q = 0 for ρ = A/r² in 3D")
print("="*60)

A = mp/(4*np.pi*Rp)
print(f"\nA = mp/(4πRp) = {A:.2f} MeV/fm")
print(f"4πA = {4*np.pi*A:.0f} MeV/fm (flux per shell = constant)")

# Numerical verification: ∇²(1/r) via finite differences
print(f"\nNumerical ∇²(1/r) check:")
for r0 in [0.1, 1.0, 10.0, 100.0]:
    dr = r0 * 1e-4
    f_plus = 1/(r0+dr)
    f_zero = 1/r0
    f_minus = 1/(r0-dr)
    d2f = (f_plus - 2*f_zero + f_minus)/dr**2
    # Spherical: ∇²f = d²f/dr² + (2/r)df/dr
    df = (f_plus - f_minus)/(2*dr)
    laplacian = d2f + 2/r0 * df
    print(f"  r = {r0:6.1f} fm: ∇²(1/r) = {laplacian:.2e} (should be 0)")

print(f"\n{'='*60}")
print("CH2: Q_coeff = −(D−1)(D−3)/4 across dimensions")
print(f"{'='*60}")
print(f"\n{'D':>3} {'(D-1)':>6} {'(D-3)':>6} {'Q_coeff':>10} {'Q=0?':>6}")
print("-"*35)
for D in range(1, 11):
    qc = -(D-1)*(D-3)/4
    is_zero = "★ YES" if abs(qc) < 0.001 else "no"
    print(f"{D:3d} {D-1:6d} {D-3:6d} {qc:10.3f} {is_zero:>6}")

print(f"\nOnly D=1 (trivial) and D=3 give Q=0.")
print(f"D=3 is the unique non-trivial dimension.")
