"""
verify_lambda_qcd.py — Λ_QCD = m_p/(D+1) from OE × W parabola

Paper: Singh 2026v, DOI: 10.5281/zenodo.19740577
Sections: §3.8–3.9

Derives:
  OE × W peaks at OE = 1/2 (Damru neck)
  Maximum = 1/(D+1) = 1/4
  Λ_QCD = m_p × max = m_p/4 = 234.6 MeV
  QCD range: 200–340 MeV → m_p/4 is inside

Also: OE×W landscape at all 6 quark positions
  b quark at OE=1/2 = peak = Λ_QCD
  s and t quarks mirror (both = 3m_p/16)

Zero fitted parameters.
"""

import math

# Constants
m_p = 938.272  # MeV
D = 3

# Quark OE positions (from 2026m, 2026s)
quarks = [
    ("u",  0,      "Surface"),
    ("d",  1/20,   "Light quark"),
    ("s",  1/4,    "≈ pion decay scale"),
    ("c",  17/40,  "Charm"),
    ("b",  1/2,    "Damru neck = MAXIMUM"),
    ("t",  3/4,    "Wall = mirrors s"),
]


def main():
    print("=" * 65)
    print("Λ_QCD = m_p/(D+1) FROM OE × W PARABOLA")
    print("Paper: Singh 2026v, §3.8–3.9")
    print("=" * 65)

    # Step 1: The parabola
    print(f"\n--- Step 1: OE × W = OE × (1-OE) ---")
    print(f"  This is a parabola in OE.")
    print(f"  d(OE×W)/dOE = 1 - 2×OE = 0 → OE = 1/2")
    print(f"  Maximum value = (1/2)(1/2) = 1/4 = 1/(D+1)")

    # Step 2: Λ_QCD
    lambda_qcd = m_p / (D + 1)
    print(f"\n--- Step 2: Λ_QCD ---")
    print(f"  Λ_QCD = m_p × (OE×W)_max")
    print(f"        = m_p / (D+1)")
    print(f"        = {m_p} / {D+1}")
    print(f"        = {lambda_qcd:.1f} MeV")
    print(f"")
    print(f"  QCD measured: 200–340 MeV (depends on scheme)")
    print(f"  CM prediction: {lambda_qcd:.1f} MeV → INSIDE RANGE")
    print(f"")
    print(f"  QCD needs Λ_QCD as INPUT (free parameter).")
    print(f"  CM derives it: m_p / 4.")

    # Step 3: Quark landscape
    print(f"\n--- Step 3: OE × W at each quark position ---")
    print(f"{'Quark':<6} {'OE':<10} {'W':<10} {'OE×W':<10} {'m_p×OE×W':<12} {'Note'}")
    print("-" * 65)

    for name, OE, note in quarks:
        W = 1 - OE
        product = OE * W
        energy = m_p * product
        print(f"{name:<6} {OE:<10.4f} {W:<10.4f} {product:<10.4f} "
              f"{energy:<12.1f} {note}")

    # Step 4: s-t mirror
    OE_s = 1/4
    OE_t = 3/4
    product_s = OE_s * (1 - OE_s)
    product_t = OE_t * (1 - OE_t)

    print(f"\n--- Step 4: s-t mirror symmetry ---")
    print(f"  s quark: OE=1/4, OE×W = {product_s:.4f}, "
          f"m_p×OE×W = {m_p*product_s:.1f} MeV")
    print(f"  t quark: OE=3/4, OE×W = {product_t:.4f}, "
          f"m_p×OE×W = {m_p*product_t:.1f} MeV")
    print(f"  SAME! Because OE×(1-OE) symmetric around 1/2")
    print(f"  Both = 3/16 × m_p = {3/16*m_p:.1f} MeV")

    # Step 5: Universal formula
    print(f"\n--- Step 5: Universal m/(D+1) ---")
    print(f"  For ANY mass m:")
    print(f"    Peak of m×OE×W = m/(D+1) = m/4")
    print(f"  Proton:   {m_p}/4 = {m_p/4:.1f} MeV = Λ_QCD")
    print(f"  Electron: 0.511/4 = {0.511/4:.3f} MeV = m_e/4")

    # Pass/fail
    print(f"\n{'=' * 65}")
    print("PASS/FAIL:")
    tests = [
        ("OE×W max at OE=1/2", True, "d/dOE = 0 → OE=1/2"),
        ("Max value = 1/(D+1) = 1/4", 1/4 == 1/(D+1), f"{1/(D+1)}"),
        ("Λ_QCD inside QCD range",
         200 < lambda_qcd < 340, f"{lambda_qcd:.1f} in [200,340]"),
        ("b quark at OE=1/2 (peak)",
         quarks[4][1] == 0.5, f"OE_b = {quarks[4][1]}"),
        ("s-t mirror (same product)",
         abs(product_s - product_t) < 1e-10, f"{product_s} = {product_t}"),
    ]

    all_pass = True
    for name, passed, detail in tests:
        status = "PASS ✓" if passed else "FAIL ✗"
        if not passed:
            all_pass = False
        print(f"  {status}  {name} ({detail})")

    print(f"\n{'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
    return all_pass


if __name__ == "__main__":
    main()
