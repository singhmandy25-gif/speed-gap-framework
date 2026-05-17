#!/usr/bin/env python3
"""
Strip geometry: t/w = 8π/9, m×R = (4/3)πℏ/c, particle = sphere
Speed decomposition: v²_fwd + v²_rot = c²
Verifies Singh 2026z, Chapters 3-5
"""
import numpy as np

hc = 197.327    # MeV·fm
mc2_e = 0.511   # MeV electron
mc2_p = 938.272 # MeV proton

print("="*60)
print("CH3: Strip Dimensions — t/w = 8π/9")
print("="*60)

tw = 8*np.pi/9
print(f"\n  t/w = 8π/9 = {tw:.6f}")
print(f"  = (4/3)π × (2/3) = {(4/3)*np.pi * (2/3):.6f}")
print(f"  Sphere packing × virial partition")

# OE wall connection
frac = tw/(1+tw)
print(f"\n  t/(w+t) = {frac:.4f}")
print(f"  OE_wall = 3/4 = {3/4:.4f}")
print(f"  Match: {abs(frac-0.75)/0.75*100:.1f}% difference")

print(f"\n{'='*60}")
print("CH4: Standing Wave — m×R = (4/3)πℏ/c")
print(f"{'='*60}")

N_lam = (4/3)*np.pi
print(f"\n  Wavelengths per circumference = 2πR/λ = 2π/(3/2) = (4/3)π = {N_lam:.4f}")

# Proton
Rp = N_lam * hc / mc2_p
print(f"\n  Proton:")
print(f"    R = (4/3)πℏ/(mpc) = {Rp:.4f} fm")
print(f"    CODATA: 0.8751 ± 0.0006 fm")
print(f"    Error: {(Rp-0.8751)/0.8751*100:.2f}%")

# Electron
Re = N_lam * hc / mc2_e
print(f"\n  Electron:")
print(f"    R = (4/3)πℏ/(mec) = {Re:.0f} fm")
print(f"    Experiments: point-like (< 10⁻³ fm)")
print(f"    Status: open problem (wave extent, not charge radius)")

print(f"\n{'='*60}")
print("CH5: Particle = Sphere + Speed Decomposition")
print(f"{'='*60}")

# Density
Ve = (4/3)*np.pi*Re**3
rho_e = mc2_e/Ve
Vp = (4/3)*np.pi*Rp**3
rho_p = mc2_p/Vp
print(f"\n  Electron: V = {Ve:.4e} fm³, ρ = {rho_e:.4e} MeV/fm³")
print(f"  Proton:   V = {Vp:.4f} fm³, ρ = {rho_p:.1f} MeV/fm³")
print(f"  ρ_p/ρ_e = {rho_p/rho_e:.2e} = (mp/me)⁴ = {(mc2_p/mc2_e)**4:.2e}")

# Speed decomposition
L = np.sqrt((3/2)**2 + (2*np.pi)**2)
v_fwd = (3/2)/L
v_rot = 2*np.pi/L
print(f"\n  Helix path per turn: L/R = {L:.4f}")
print(f"  v_fwd/c = λ/L = {v_fwd:.4f} ({v_fwd**2*100:.1f}% of c²)")
print(f"  v_rot/c = 2πR/L = {v_rot:.4f} ({v_rot**2*100:.1f}% of c²)")
print(f"  v²_fwd + v²_rot = {v_fwd**2 + v_rot**2:.6f} (should be 1.000000)")

# Advance ratio
J = 3/(4*np.pi)
print(f"\n  Advance ratio J = 3/(4π) = {J:.4f}")

# D-dependent advance ratios
print(f"\n  {'D':>3} {'J=D/(4π)':>10} {'v²_fwd':>8} {'v²_rot':>8}")
for D in [2,3,4,5]:
    lR = D/2
    Ld = np.sqrt(lR**2 + (2*np.pi)**2)
    vf = lR/Ld; vr = 2*np.pi/Ld
    print(f"  {D:3d} {D/(4*np.pi):10.4f} {vf**2*100:7.1f}% {vr**2*100:7.1f}%")
