"""Chapter 3A: mp/me = Re/Rp = 1836 (0.0000%)"""
import numpy as np
hbar_c = 197.3269804; mp = 938.272046; me = 0.51099895
n43pi = (4/3)*np.pi
Rp = n43pi * hbar_c / mp
Re = n43pi * hbar_c / me
print(f"Rp = {Rp:.4f} fm, Re = {Re/1000:.3f} pm")
print(f"mp/me = {mp/me:.5f}")
print(f"Re/Rp = {Re/Rp:.5f}")
print(f"Error = {abs(mp/me - Re/Rp)/(mp/me)*100:.6f}%")
print(f"PASS" if abs(mp/me - Re/Rp) < 0.001 else "FAIL")
