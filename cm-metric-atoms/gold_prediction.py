#!/usr/bin/env python3
"""
Z_cross = 1/(√3 α) = 79 = Gold
Wall-orbit crossing: CM-specific prediction
Verifies Singh 2026z, Chapter 8
"""
import numpy as np

alpha = 1/137.036
hc = 197.327
mc2_e = 0.511
a0 = hc/(mc2_e*alpha)

print("="*60)
print("CH8: Z_cross = 79 = GOLD")
print("="*60)

# Derivation
print(f"\n  Wall:  r_wall = 3Zα²a₀ (grows ∝ Z)")
print(f"  Orbit: r_orbit = a₀/Z   (shrinks ∝ 1/Z)")
print(f"\n  Set equal: 3Zα²a₀ = a₀/Z → 3Z²α² = 1")
Z_cross = 1/(np.sqrt(3)*alpha)
print(f"  Z_cross = 1/(√3 × α) = 1/(√3 × {alpha:.6f}) = {Z_cross:.2f}")
print(f"  Nearest integer: {int(round(Z_cross))} = Gold (Au)")

# Full table
print(f"\n{'Z':>4} {'El':>3} {'r_wall':>10} {'r_orbit':>10} {'ratio':>8} {'regime':>20}")
print("-"*60)
for Z,name in [(1,"H"),(6,"C"),(13,"Al"),(26,"Fe"),(47,"Ag"),
               (79,"Au"),(82,"Pb"),(92,"U")]:
    rw = 3*Z*alpha**2*a0
    ro = a0/Z
    rat = rw/ro
    if rat < 0.01: regime = "Wall invisible"
    elif rat < 0.3: regime = "Wall small"
    elif rat < 0.9: regime = "Wall significant"
    elif rat < 1.1: regime = "★ WALL = ORBIT"
    else: regime = "Wall > orbit"
    print(f"{Z:4d} {name:>3} {rw:10.1f} {ro:10.0f} {rat:8.5f} {regime:>20}")

# D-dependent
print(f"\n  Dimension dependence:")
print(f"  {'D':>3} {'Z_cross':>10} {'Element':>10}")
for D in [2,3,4,5]:
    Zd = 1/(np.sqrt(D)*alpha)
    elem = {2:"Californium(97)", 3:"Gold(79)", 4:"Thulium(69)", 5:"Terbium(62)"}
    print(f"  {D:3d} {Zd:10.1f} {elem.get(D,'?'):>10}")

print(f"\n  Only D=3 gives Gold. Z_cross encodes both α AND D.")
