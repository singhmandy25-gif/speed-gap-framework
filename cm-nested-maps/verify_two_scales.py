"""Chapter 3B: R_orb/R_int = 3/(4πα) = 32.7 (algebraically exact)"""
import numpy as np
alpha = 1/137.035999084; hbar_c = 197.3269804; me = 0.51099895
n43pi = (4/3)*np.pi
R_int = n43pi * hbar_c / me
R_orb = (1/alpha) * hbar_c / me
ratio = R_orb / R_int
formula = 3/(4*np.pi*alpha)
print(f"R_int = {R_int/1000:.3f} pm, R_orb = {R_orb/1000:.2f} pm")
print(f"R_orb/R_int = {ratio:.4f}")
print(f"3/(4πα)     = {formula:.4f}")
print(f"Difference  = {abs(ratio-formula):.2e}")
print(f"PASS (algebraically exact)" if abs(ratio-formula) < 1e-8 else "FAIL")
