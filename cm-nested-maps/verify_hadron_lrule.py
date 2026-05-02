"""Chapter 7A: R/λ_C = (l+1)/3 × (4/3)π — 5 hadrons"""
import numpy as np
n43pi = (4/3)*np.pi; hbar_c = 197.3269804

particles = [
    ("Kaon",   493.677, 0.560, 0),
    ("rho",    775.26,  0.730, 1),
    ("Proton", 938.272, 0.877, 2),
    ("Delta", 1232.0,   0.840, 3),
    ("J/psi", 3096.9,   0.440, 4),
]
print(f"{'Particle':<10} {'l':<4} {'Pred':<8} {'Meas':<8} {'Err':<8} {'Status'}")
for name,mass,R,l in particles:
    lam = hbar_c/mass
    meas = R/lam
    pred = (l+1)/3*n43pi
    err = abs(pred-meas)/meas*100
    print(f"{name:<10} {l:<4} {pred:<8.3f} {meas:<8.3f} {err:<8.1f}% {'PASS' if err<7 else 'FAIL'}")

# Pion separate
pion_ratio = 0.659/(hbar_c/139.570)
print(f"\nPion: R/λ = {pion_ratio:.4f}, e^(-3/4) = {np.exp(-3/4):.4f}, err = {abs(pion_ratio-np.exp(-3/4))/np.exp(-3/4)*100:.1f}%")
