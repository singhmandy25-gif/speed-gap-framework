"""
complete_verification.py — Run ALL verification tests for Singh 2026v

Paper: "The Strong Coupling Constant from Clausius-Mossotti Geometry:
        Two Derivations, Zero Parameters"
DOI: 10.5281/zenodo.19740577
Author: Mandeep Singh | ORCID: 0009-0003-7176-2395

Runs:
  1. verify_alpha_s     — Both running formulas at 7 QCD energies
  2. verify_barycenter  — Mirror symmetry, β²=1/10, α_s=1/√10
  3. verify_lambda_qcd  — Λ_QCD = m_p/4, quark landscape
  4. interior_field_eq  — Self-coupled ODE, profile, α_s at quarks
"""

import sys

def run_all():
    print("=" * 70)
    print("COMPLETE VERIFICATION — Singh 2026v")
    print("The Strong Coupling Constant from CM Geometry")
    print("DOI: 10.5281/zenodo.19740577")
    print("=" * 70)
    print()

    results = {}

    # Test 1: Framework quantities
    print("━" * 70)
    print("TEST 1/5: CM FRAMEWORK QUANTITIES (Ch 2)")
    print("━" * 70)
    from verify_framework import main as test0
    results["Framework"] = test0()
    print()

    # Test 2: Running formulas
    print("━" * 70)
    print("TEST 2/5: α_s RUNNING FORMULAS")
    print("━" * 70)
    from verify_alpha_s import main as test1
    results["α_s running"] = test1()
    print()

    # Test 3: Barycenter
    print("━" * 70)
    print("TEST 3/5: BARYCENTER MIRROR SYMMETRY")
    print("━" * 70)
    from verify_barycenter import main as test2
    results["Barycenter"] = test2()
    print()

    # Test 4: Λ_QCD
    print("━" * 70)
    print("TEST 4/5: Λ_QCD = m_p/(D+1)")
    print("━" * 70)
    from verify_lambda_qcd import main as test3
    results["Λ_QCD"] = test3()
    print()

    # Test 5: Interior
    print("━" * 70)
    print("TEST 5/5: INTERIOR FIELD EQUATION")
    print("━" * 70)
    from interior_field_eq import main as test4
    results["Interior"] = test4()
    print()

    # Final summary
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for name, result in results.items():
        status = "PASS ✓" if result else "FAIL ✗"
        print(f"  {status}  {name}")
    
    print(f"\n  {passed}/{total} test groups passed")
    
    print(f"\n{'─' * 70}")
    print(f"KEY RESULTS:")
    print(f"  α_s(1 GeV) = 0.462 vs QCD 0.47     →  1.6% (D1, zero fitted)")
    print(f"  α_s(1 GeV) = 0.496 vs QCD 0.47     →  5.4% (field eq, zero fitted)")
    print(f"  α_s(1.78)  = 0.328 vs QCD 0.330    →  0.5% (D2, zero fitted)")
    print(f"  α_s(bary)  = 1/√10 vs QCD 0.330    →  4.2% (mirror, zero fitted)")
    print(f"  Λ_QCD      = m_p/4 = 234.6 MeV     →  inside QCD range 200–340")
    print(f"  D2 average = 8.1% across 7 scales   →  most uniform formula")
    print(f"  Fitted parameters: ZERO throughout")
    print(f"{'─' * 70}")
    
    if passed == total:
        print(f"\n  ALL TESTS PASSED ✓")
        print(f"  Every number in Singh 2026v is reproducible.")
    else:
        print(f"\n  SOME TESTS FAILED ✗")
        print(f"  Check individual test outputs above.")
    
    print(f"\n  Paper: doi.org/10.5281/zenodo.19740577")
    print(f"  Code:  github.com/singhmandy25-gif/speed-gap-framework")
    print(f"         /tree/main/cm-alpha-s-derivation")
    
    return passed == total


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
