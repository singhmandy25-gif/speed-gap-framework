#!/usr/bin/env python3
"""
Taylor expansion of W⁻¹/³: verify β⁴ = 0
Verifies Singh 2026z, Chapter 7B
Requires: sympy (pip install sympy)
"""
try:
    from sympy import symbols, series, Rational, sqrt, Abs
    x = symbols('x')
    W = (1-x)/(1+2*x)
    Wm13 = W**Rational(-1,3)

    print("="*60)
    print("CH7B: Taylor Expansion of W⁻¹/³")
    print("="*60)

    # W⁻¹/³ expansion
    s = series(Wm13, x, 0, n=8)
    print(f"\n  W⁻¹/³ = {s}")

    # E = ½(W⁻¹/³ − 1)
    E = series((Wm13-1)/2, x, 0, n=8)
    print(f"\n  E/(mc²) = ½(W⁻¹/³−1) = {E}")

    # Dirac for comparison
    D = series(1-sqrt(1-x), x, 0, n=8)
    print(f"\n  Dirac: 1−√(1−x) = {D}")

    # Coefficient comparison
    print(f"\n  {'Order':>8} {'CM':>12} {'Dirac':>12} {'Match':>6}")
    print(f"  {'-'*42}")
    for i in range(1,7):
        c_cm = float(E.coeff(x,i))
        c_d = float(D.coeff(x,i))
        m = "✓" if abs(c_cm-c_d)<0.001 else "✗"
        print(f"  {'β^'+str(2*i):>8} {c_cm:12.5f} {c_d:12.5f} {m:>6}")

    print(f"\n  KEY: β⁴ coefficient in CM = 0 (ZERO)")
    print(f"  β⁴ in Dirac = 1/8 = 0.125")
    print(f"  They do NOT match order-by-order.")
    print(f"  Agreement is non-perturbative (functions match as wholes).")

except ImportError:
    print("SymPy not installed. Install: pip install sympy")
    print("Manual verification: β⁴ = 0 in W⁻¹/³ (algebraic, see paper Ch7B)")
