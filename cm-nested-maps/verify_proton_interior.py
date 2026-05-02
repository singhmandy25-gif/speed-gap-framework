"""Chapter 2B: ρ,f,T table + E×T=h + frequency ratio=9"""
import numpy as np
mp_J = 938.272e6 * 1.602176634e-19
hbar = 1.054571817e-34; h = 6.62607015e-34

f0 = mp_J/(2*np.pi*hbar)
T0 = 1/f0
print(f"f₀ = {f0:.2e} Hz, T₀ = {T0:.2e} s, f₀×T₀ = {f0*T0:.4f}")

table = [
    ("d quark",  6.81e23, 1.47e-24),
    ("midpoint", 3.03e23, 3.30e-24),
    ("u quark",  1.70e23, 5.88e-24),
    ("wall",     7.57e22, 1.32e-23),
]
print(f"\n{'Position':<12} {'f':<12} {'T(paper)':<12} {'1/f':<12} {'f×T':<8} {'OK?'}")
all_ok = True
for name,f,T in table:
    correct_T = 1/f
    fT = f*T
    ok = abs(fT - 1.0) < 0.02
    if not ok: all_ok = False
    print(f"{name:<12} {f:<12.2e} {T:<12.2e} {correct_T:<12.2e} {fT:<8.4f} {'✓' if ok else '✗'}")

print(f"\nf(d)/f(wall) = {6.81e23/7.57e22:.1f} (should be 9)")
print(f"\n{'ALL PASS' if all_ok else 'SOME FAIL'}")
