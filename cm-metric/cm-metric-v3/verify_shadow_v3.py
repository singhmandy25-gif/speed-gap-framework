"""
Singh 2026j V3 — Shadow Size Verification
CM metric: ds² = W^(1/3)c²dt² - W^(-1/3)(dr² + r²dΩ²)
W = (1-β²)/(1+2β²), β² = 2GM/(rc²)

Verifies: Shadow +10% larger than GR
Compares: M87* and SgrA* with EHT observations
"""
import numpy as np

G = 6.674e-11; c = 3e8; M_sun = 1.989e30

# CM Weight function
def W(beta2):
    return (1 - beta2) / (1 + 2*beta2)

# === PHOTON SPHERE ===
# Condition: d/dr[W^(2/3)/r²] = 0 → ε² = 1/8 → ε = 1/(2√2)
epsilon_ph = 1 / (2 * np.sqrt(2))
beta2_ph = 2 * epsilon_ph  # = 1/√2
r_ph = 1 / (2 * epsilon_ph)  # in r_s units = √2

W_ph = W(beta2_ph)
W_ph_13 = W_ph**(1/3)

# Critical impact parameter (coordinate-independent)
b_CM = r_ph / W_ph_13
b_GR = 3 * np.sqrt(3) / 2

# Circumferential radius
R_ph_circ = r_ph * W_ph**(-1/6)

print("=== PHOTON SPHERE ===")
print(f"  r_ph (isotropic)      = {r_ph:.4f} r_s = √2 r_s")
print(f"  R_ph (circumferential) = {R_ph_circ:.4f} r_s")
print(f"  GR photon sphere       = 1.5000 r_s")
print(f"  Circumferential: {(R_ph_circ/1.5 - 1)*100:+.1f}% (34% further)")
print(f"  W at photon sphere     = {W_ph:.5f}")
print(f"  b_CM = {b_CM:.3f} r_s")
print(f"  b_GR = {b_GR:.3f} r_s")
print(f"  Ratio: {b_CM/b_GR:.3f} = +{(b_CM/b_GR-1)*100:.1f}% (shadow)")

# === EHT COMPARISON ===
print("\n=== EHT COMPARISON ===")

targets = [
    ("M87*",  6.5e9,  16.8e6 * 3.0857e16, 42, 3),   # D in meters
    ("SgrA*", 4.0e6,  8.277e3 * 3.0857e16, 48.7, 7),
]

for name, M_msun, D, obs, err in targets:
    M = M_msun * M_sun
    r_s = 2*G*M / c**2
    theta_GR = 2 * b_GR * r_s / D * 206265e6  # micro-arcsec
    theta_CM = 2 * b_CM * r_s / D * 206265e6
    sigma_GR = abs(theta_GR - obs) / err
    sigma_CM = abs(theta_CM - obs) / err
    winner = "CM closer" if sigma_CM < sigma_GR else "GR closer"
    
    print(f"\n  {name}:")
    print(f"    GR: {theta_GR:.1f} μas ({sigma_GR:.2f}σ)")
    print(f"    CM: {theta_CM:.1f} μas ({sigma_CM:.2f}σ)")
    print(f"    Observed: {obs} ± {err} μas")
    print(f"    → {winner}")

print("\n=== PHYSICAL REASON ===")
print("  GR: radial stretch only (rubber band)")
print("  CM: all directions equally (balloon)")
print("  Angular stretch → bigger orbit circumference → bigger shadow")
