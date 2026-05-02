"""Chapter 5B: A(Fe) = (mp/me)(4/3)πα = 56.13 (0.2%) + ΔA check"""
import numpy as np
mp_me = 1836.15267343; n43pi = (4/3)*np.pi; alpha = 1/137.035999084
A_pred = mp_me * n43pi * alpha
print(f"A(Fe) predicted = {A_pred:.2f}")
print(f"A(Fe) measured  = 56")
print(f"Error = {abs(A_pred-56)/56*100:.1f}%")
print(f"{'PASS' if abs(A_pred-56)/56*100 < 0.5 else 'FAIL'}")

# ΔA + 6(Zα)² with charge radius r₀=1.08
amu=931.494; r0=1.08; A=56; Z=26
flux_nuc = amu/(r0*A**(1/3))
flux_free = 938.272/0.881  # = 1065
delta_A = 1 - flux_nuc/flux_free
shell = 6*(Z*alpha)**2
total = delta_A + shell
print(f"\nΔA (r₀=1.08) = {delta_A:.3f}")
print(f"6(Zα)² = {shell:.3f}")
print(f"Sum = {total:.3f}")
print(f"Match to 1: {abs(total-1)*100:.1f}%")

# Also with matter radius
r0m=1.25
flux_m = amu/(r0m*A**(1/3))
delta_m = 1 - flux_m/flux_free
total_m = delta_m + shell
print(f"\nWith r₀=1.25: sum = {total_m:.3f} ({abs(total_m-1)*100:.1f}% from 1)")
