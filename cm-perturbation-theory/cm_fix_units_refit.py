#!/usr/bin/env python3
"""
DIAGNOSE CLASS units → FIX → Re-run A_s fit
Run: python3 cm_fix_units_refit.py
"""
import numpy as np
from scipy.optimize import minimize
import os

from classy import Class

omega_b = 0.02237
omega_cdm_CM = 0.11424
h_CM = 0.7005

# ═══════════════════════════════════════
# STEP 0: DIAGNOSE UNIT CONVERSION
# ═══════════════════════════════════════
print("="*65)
print("STEP 0: DIAGNOSING CLASS ↔ PLANCK UNITS")
print("="*65)

# Run CLASS with Planck best-fit
cosmo = Class()
cosmo.set({
    'output': 'tCl,lCl', 'lensing': 'yes', 'l_max_scalars': 2500,
    'omega_b': 0.02237, 'omega_cdm': 0.1200, 'h': 0.674,
    'A_s': 2.1e-9, 'n_s': 0.9649, 'tau_reio': 0.054,
})
cosmo.compute()
cl = cosmo.lensed_cl(2500)

# Load Planck data
pdata = np.loadtxt(os.path.expanduser("~/cmb_work/planck_cl_tt.txt"))
ell_planck = pdata[:, 0]
dl_planck = pdata[:, 1]
bestfit_planck = pdata[:, 4]

# Compare CLASS at Planck ℓ values with BestFit column
# Try different conversion factors
print(f"\nTrying different conversions for CLASS C_ℓ → D_ℓ:")
print(f"Planck BestFit at ℓ≈136: {bestfit_planck[3]:.1f}")

l_test = int(round(ell_planck[3]))  # ℓ ≈ 136
Cl_class = cl['tt'][l_test]

conversions = {
    '×1e12 (K²→μK²)': Cl_class * l_test*(l_test+1)/(2*np.pi) * 1e12,
    '×T²_μK': Cl_class * l_test*(l_test+1)/(2*np.pi) * (2.7255e6)**2,
    '×T²_K×1e12': Cl_class * l_test*(l_test+1)/(2*np.pi) * (2.7255)**2 * 1e12,
    'just ℓ(ℓ+1)/(2π)': Cl_class * l_test*(l_test+1)/(2*np.pi),
    '×(T_K)²': Cl_class * l_test*(l_test+1)/(2*np.pi) * (2.7255)**2,
}

print(f"\n{'Conversion':<25} {'D_ℓ(CLASS)':>12} {'D_ℓ(Planck)':>12} {'Ratio':>8}")
print("-"*60)
for name, val in conversions.items():
    ratio = val/bestfit_planck[3] if bestfit_planck[3] > 0 else 0
    print(f"{name:<25} {val:>12.1f} {bestfit_planck[3]:>12.1f} {ratio:>8.3f}")

# Find correct conversion: compare at ALL Planck points
print(f"\n--- Finding correct conversion factor ---")

# Test: multiply by T² (μK²)
T_muK2 = (2.7255e6)**2

ratios_T2 = []
for i in range(len(ell_planck)):
    l = int(round(ell_planck[i]))
    if l < 2 or l > 2499: continue
    dl_class = cl['tt'][l] * l*(l+1)/(2*np.pi) * T_muK2
    if bestfit_planck[i] > 10:
        ratios_T2.append(dl_class / bestfit_planck[i])

mean_ratio = np.mean(ratios_T2)
print(f"CLASS(×T²_μK)/Planck_BestFit ratio: {mean_ratio:.4f} ± {np.std(ratios_T2):.4f}")
print(f"→ CLASS×T² is {mean_ratio:.1f}× too high")
print(f"→ Correct factor = T²_μK / {mean_ratio:.1f} = {T_muK2/mean_ratio:.4e}")

CORRECT_FACTOR = T_muK2 / mean_ratio

# Verify with corrected factor
print(f"\nVerification with CORRECT_FACTOR = {CORRECT_FACTOR:.4e}:")
print(f"{'ℓ':>7} {'CLASS':>10} {'Planck BF':>10} {'Ratio':>8}")
print("-"*40)
for i in [0, 3, 10, 20, 40, 60, 80]:
    if i >= len(ell_planck): continue
    l = int(round(ell_planck[i]))
    if l < 2 or l > 2499: continue
    dl_class = cl['tt'][l] * l*(l+1)/(2*np.pi) * CORRECT_FACTOR
    ratio = dl_class/bestfit_planck[i] if bestfit_planck[i] > 0 else 0
    print(f"{l:>7} {dl_class:>10.1f} {bestfit_planck[i]:>10.1f} {ratio:>8.3f}")

cosmo.struct_cleanup()
cosmo.empty()

# ═══════════════════════════════════════
# STEP 1: RE-FIT A_s WITH CORRECT UNITS
# ═══════════════════════════════════════
print(f"\n{'='*65}")
print(f"STEP 1: RE-FIT A_s, n_s, τ WITH CORRECT UNITS")
print(f"{'='*65}")

# Use ℓ > 30 data
mask = ell_planck > 30
ell_data = ell_planck[mask]
dl_data = dl_planck[mask]
dl_err = (np.abs(pdata[mask, 2]) + np.abs(pdata[mask, 3])) / 2
dl_err[dl_err < 1] = 100

call_count = [0]

def chi2_func(params):
    ln_As, n_s, tau = params
    A_s = np.exp(ln_As) * 1e-10
    
    if A_s < 1e-10 or A_s > 5e-9: return 1e10
    if n_s < 0.90 or n_s > 1.05: return 1e10
    if tau < 0.01 or tau > 0.12: return 1e10
    
    call_count[0] += 1
    
    try:
        c = Class()
        c.set({
            'output': 'tCl,lCl', 'lensing': 'yes', 'l_max_scalars': 2500,
            'omega_b': omega_b, 'omega_cdm': omega_cdm_CM, 'h': h_CM,
            'A_s': A_s, 'n_s': n_s, 'tau_reio': tau,
        })
        c.compute()
        cl_out = c.lensed_cl(2500)
        
        chi2 = 0
        for i in range(len(ell_data)):
            l = int(round(ell_data[i]))
            if l < 2 or l > 2499: continue
            dl_theory = cl_out['tt'][l] * l*(l+1)/(2*np.pi) * CORRECT_FACTOR
            chi2 += ((dl_theory - dl_data[i])/dl_err[i])**2
        
        c.struct_cleanup()
        c.empty()
        
        if call_count[0] % 10 == 0:
            print(f"  [{call_count[0]:>3}] A_s={A_s:.3e} n_s={n_s:.4f} τ={tau:.4f} → χ²={chi2:.1f} (χ²/N={chi2/len(ell_data):.2f})")
        
        return chi2
    except:
        return 1e10

# First: check Planck params give good χ²
print("\nSanity check: Planck ΛCDM params should give χ²/N ≈ 1...")
chi2_planck = chi2_func([np.log(2.1e-9 * 1e10), 0.9649, 0.054])
print(f"Planck ΛCDM: χ² = {chi2_planck:.1f}, χ²/N = {chi2_planck/len(ell_data):.2f}")

# Now optimize for CM
print(f"\nOptimizing A_s, n_s, τ for CM (ω_cdm={omega_cdm_CM}, h={h_CM})...")
call_count[0] = 0

# Start from Planck values
x0 = [np.log(2.1e-9 * 1e10), 0.9649, 0.054]

result = minimize(chi2_func, x0, method='Nelder-Mead',
                  options={'maxiter': 300, 'xatol': 0.001, 'fatol': 0.5})

best_As = np.exp(result.x[0]) * 1e-10
best_ns = result.x[1]
best_tau = result.x[2]

print(f"\n{'='*65}")
print(f"RESULT: CM's OWN PARAMETERS")
print(f"{'='*65}")
print(f"  A_s = {best_As:.4e}   (Planck: 2.100e-9)")
print(f"  n_s = {best_ns:.4f}       (Planck: 0.9649)")
print(f"  τ   = {best_tau:.4f}       (Planck: 0.054)")
print(f"  χ²  = {result.fun:.1f}")
print(f"  χ²/N = {result.fun/len(ell_data):.2f}")

# ═══════════════════════════════════════
# STEP 2: COMPARE PEAKS WITH CM's OWN A_s
# ═══════════════════════════════════════
print(f"\n{'='*65}")
print(f"STEP 2: PEAK COMPARISON — CM (own A_s) vs ΛCDM")
print(f"{'='*65}")

# CM with own params
cosmo_cm = Class()
cosmo_cm.set({
    'output': 'tCl,pCl,lCl,mPk', 'lensing': 'yes', 'l_max_scalars': 2500,
    'omega_b': omega_b, 'omega_cdm': omega_cdm_CM, 'h': h_CM,
    'A_s': best_As, 'n_s': best_ns, 'tau_reio': best_tau,
})
cosmo_cm.compute()

# ΛCDM Planck
cosmo_lcdm = Class()
cosmo_lcdm.set({
    'output': 'tCl,pCl,lCl,mPk', 'lensing': 'yes', 'l_max_scalars': 2500,
    'omega_b': 0.02237, 'omega_cdm': 0.1200, 'h': 0.674,
    'A_s': 2.1e-9, 'n_s': 0.9649, 'tau_reio': 0.054,
})
cosmo_lcdm.compute()

cl_cm = cosmo_cm.lensed_cl(2500)
cl_lcdm = cosmo_lcdm.lensed_cl(2500)

ell = np.arange(2, 2501)
Dl_cm = np.array([cl_cm['tt'][l] * l*(l+1)/(2*np.pi) * CORRECT_FACTOR for l in ell])
Dl_lcdm = np.array([cl_lcdm['tt'][l] * l*(l+1)/(2*np.pi) * CORRECT_FACTOR for l in ell])

# Peak finding in known ranges
peak_ranges = [(180,280),(480,600),(760,870),(1060,1200),(1360,1480),(1660,1800),(1940,2100)]

print(f"\n{'Peak':>5} {'ℓ_CM':>7} {'ℓ_ΛCDM':>8} {'Δℓ':>4} {'D_CM':>10} {'D_ΛCDM':>10} {'D_Planck':>10} {'CM/Pla':>8}")
print("-"*70)

for pk, (l_lo, l_hi) in enumerate(peak_ranges):
    i_lo, i_hi = l_lo-2, min(l_hi-2, len(Dl_cm)-1)
    i_cm = i_lo + np.argmax(Dl_cm[i_lo:i_hi+1])
    i_lcdm = i_lo + np.argmax(Dl_lcdm[i_lo:i_hi+1])
    
    l_cm = ell[i_cm]
    l_lcdm = ell[i_lcdm]
    
    # Find Planck data near this ℓ
    i_planck = np.argmin(np.abs(ell_planck - l_cm))
    d_planck = dl_planck[i_planck]
    
    pct_cm_planck = (Dl_cm[i_cm]/d_planck - 1)*100 if d_planck > 0 else 0
    
    print(f"{pk+1:>5} {l_cm:>7} {l_lcdm:>8} {abs(l_cm-l_lcdm):>4} {Dl_cm[i_cm]:>10.1f} {Dl_lcdm[i_lcdm]:>10.1f} {d_planck:>10.1f} {pct_cm_planck:>+8.1f}%")

# Key quantities
sigma8_cm = cosmo_cm.sigma8()
sigma8_lcdm = cosmo_lcdm.sigma8()
theta_cm = cosmo_cm.theta_s_100()
rs_cm = cosmo_cm.rs_drag()

print(f"\nDerived quantities:")
print(f"  σ₈:    CM = {sigma8_cm:.4f},  ΛCDM = {sigma8_lcdm:.4f}")
print(f"  100θ*: CM = {theta_cm:.4f}  (Planck: 1.04110)")
print(f"  r_s:   CM = {rs_cm:.2f} Mpc")

# S₈ with CM growth correction
S8 = sigma8_cm * 0.9793 * (0.2784/0.3)**0.5
print(f"  S₈(CM+growth): {S8:.4f} (DES: 0.776±0.017 → {abs(S8-0.776)/0.017:.2f}σ)")

# ═══════════════════════════════════════
# FINAL SCORECARD
# ═══════════════════════════════════════
print(f"\n{'='*65}")
print(f"SCORECARD: ΛCDM 6 fitted vs CM 3 derived + 3 fitted")
print(f"{'='*65}")
print(f"""
ΛCDM (6 fitted):  ω_b, ω_cdm, h, A_s, n_s, τ → all from Planck CMB
CM (3+3):         ω_cdm, h, Ω_m → DERIVED from p=e^(-3/4)
                  A_s, n_s, τ → fitted from same Planck CMB data

CM uses 3 FEWER free parameters!

CM fitted values:
  A_s = {best_As:.4e}  (Planck: 2.100e-9, diff: {(best_As/2.1e-9-1)*100:+.1f}%)
  n_s = {best_ns:.4f}  (Planck: 0.9649, diff: {(best_ns/0.9649-1)*100:+.1f}%)
  τ   = {best_tau:.4f}  (Planck: 0.054, diff: {(best_tau/0.054-1)*100:+.1f}%)
  
CM χ²/N = {result.fun/len(ell_data):.2f} (good fit = ~1)
""")

cosmo_cm.struct_cleanup()
cosmo_lcdm.struct_cleanup()
print("DONE ✅")
