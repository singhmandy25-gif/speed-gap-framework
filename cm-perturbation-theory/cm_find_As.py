#!/usr/bin/env python3
"""
FIND CM's OWN A_s, n_s, τ
Fix: Ω_m=0.2784, H₀=70.05 (CM derived)
Vary: A_s, n_s, τ (fit to Planck CMB data)

Same method ΛCDM used — just fewer free parameters!

Run: cd ~/cmb_work && source cmb_env/bin/activate
     python3 cm_find_As.py
"""
import numpy as np
from scipy.optimize import minimize
import os

try:
    from classy import Class
except ImportError:
    print("ERROR: CLASS not available. Install with: pip install classy")
    exit(1)

# ═══════════════════════════════════════
# CM FIXED PARAMETERS (derived, not varied)
# ═══════════════════════════════════════
omega_b = 0.02237      # BBN (independent)
omega_cdm = 0.11424    # CM derived from p
h = 0.7005             # CM derived from p

print("="*65)
print("FINDING CM's OWN A_s, n_s, τ")
print("="*65)
print(f"FIXED (CM derived): ω_b={omega_b}, ω_cdm={omega_cdm}, h={h}")
print(f"VARY: A_s, n_s, τ_reio → fit to Planck TT data")
print()

# ═══════════════════════════════════════
# LOAD PLANCK DATA
# ═══════════════════════════════════════
planck_file = os.path.expanduser("~/cmb_work/planck_cl_tt.txt")
if not os.path.exists(planck_file):
    print(f"ERROR: {planck_file} not found!")
    print("Need Planck C_ℓ TT data file.")
    exit(1)

print(f"Loading Planck data from {planck_file}...")
pdata = np.loadtxt(planck_file)
print(f"Loaded {len(pdata)} data points")

# Figure out data format
print(f"First row: {pdata[0]}")
print(f"Columns: {pdata.shape[1] if len(pdata.shape)>1 else 1}")

# Planck data format: typically ℓ, D_ℓ, error_down, error_up
# or ℓ_min, ℓ_max, D_ℓ, error
# Let's check what we have
if pdata.shape[1] >= 3:
    ell_data = pdata[:, 0]
    dl_data = pdata[:, 1]
    if pdata.shape[1] >= 4:
        # Symmetric error = average of up/down
        dl_err = (np.abs(pdata[:, 2]) + np.abs(pdata[:, 3])) / 2
    elif pdata.shape[1] == 3:
        dl_err = np.abs(pdata[:, 2])
    
    # Filter: use ℓ > 30 (avoid low-ℓ cosmic variance)
    mask = ell_data > 30
    ell_data = ell_data[mask]
    dl_data = dl_data[mask]
    dl_err = dl_err[mask]
    
    # Handle zero errors
    dl_err[dl_err < 1] = 100  # large error for missing data
    
    print(f"Using {len(ell_data)} points with ℓ > 30")
    print(f"ℓ range: {ell_data[0]:.0f} to {ell_data[-1]:.0f}")
    print(f"D_ℓ range: {dl_data.min():.1f} to {dl_data.max():.1f}")
else:
    print("ERROR: Cannot parse Planck data format")
    exit(1)

# ═══════════════════════════════════════
# CHI-SQUARED FUNCTION
# ═══════════════════════════════════════
call_count = [0]

def chi2_CM(params):
    """Compute χ² between CLASS(CM) and Planck data"""
    ln_As, n_s, tau = params
    A_s = np.exp(ln_As) * 1e-10
    
    call_count[0] += 1
    
    # Bounds check
    if A_s < 1e-10 or A_s > 5e-9: return 1e10
    if n_s < 0.9 or n_s > 1.05: return 1e10
    if tau < 0.01 or tau > 0.12: return 1e10
    
    try:
        cosmo = Class()
        cosmo.set({
            'output': 'tCl,lCl',
            'lensing': 'yes',
            'l_max_scalars': 2500,
            'omega_b': omega_b,
            'omega_cdm': omega_cdm,
            'h': h,
            'A_s': A_s,
            'n_s': n_s,
            'tau_reio': tau,
        })
        cosmo.compute()
        
        cl = cosmo.lensed_cl(2500)
        ell_theory = np.arange(2, 2501)
        Dl_theory = cl['tt'][2:2501] * ell_theory*(ell_theory+1)/(2*np.pi) * (2.7255e6)**2
        
        # Interpolate to data ℓ values
        Dl_at_data = np.interp(ell_data, ell_theory, Dl_theory)
        
        chi2 = np.sum(((Dl_at_data - dl_data)/dl_err)**2)
        
        cosmo.struct_cleanup()
        cosmo.empty()
        
        if call_count[0] % 10 == 0:
            print(f"  [{call_count[0]}] A_s={A_s:.4e}, n_s={n_s:.4f}, τ={tau:.4f} → χ²={chi2:.1f}")
        
        return chi2
        
    except Exception as e:
        return 1e10

# ═══════════════════════════════════════
# STEP 1: Scan A_s (fix n_s, τ at Planck values)
# ═══════════════════════════════════════
print(f"\n{'='*65}")
print("STEP 1: Scan A_s alone (n_s=0.9649, τ=0.054 fixed)")
print("="*65)

n_s_fixed = 0.9649
tau_fixed = 0.054

As_values = [1.8e-9, 1.9e-9, 2.0e-9, 2.05e-9, 2.1e-9, 2.15e-9, 2.2e-9, 2.3e-9, 2.4e-9]
chi2_values = []

print(f"\n{'A_s':>12} {'ln(10¹⁰A_s)':>14} {'χ²':>10}")
print("-"*40)

for As in As_values:
    ln_As = np.log(As * 1e10)
    c2 = chi2_CM([ln_As, n_s_fixed, tau_fixed])
    chi2_values.append(c2)
    print(f"{As:>12.3e} {ln_As:>14.4f} {c2:>10.1f}")

best_idx = np.argmin(chi2_values)
best_As = As_values[best_idx]
print(f"\nBest A_s (scan) = {best_As:.3e} (χ² = {chi2_values[best_idx]:.1f})")

# ═══════════════════════════════════════
# STEP 2: Fine-tune A_s around best
# ═══════════════════════════════════════
print(f"\n{'='*65}")
print("STEP 2: Fine-tune A_s")
print("="*65)

As_fine = np.linspace(best_As*0.9, best_As*1.1, 11)
chi2_fine = []

for As in As_fine:
    ln_As = np.log(As * 1e10)
    c2 = chi2_CM([ln_As, n_s_fixed, tau_fixed])
    chi2_fine.append(c2)

best_idx2 = np.argmin(chi2_fine)
best_As_fine = As_fine[best_idx2]
print(f"Best A_s (fine) = {best_As_fine:.4e} (χ² = {chi2_fine[best_idx2]:.1f})")

# ═══════════════════════════════════════
# STEP 3: Optimize all three (A_s, n_s, τ)
# ═══════════════════════════════════════
print(f"\n{'='*65}")
print("STEP 3: Optimize A_s, n_s, τ together")
print("="*65)

call_count[0] = 0
x0 = [np.log(best_As_fine * 1e10), 0.9649, 0.054]

result = minimize(chi2_CM, x0, method='Nelder-Mead',
                  options={'maxiter': 200, 'xatol': 0.001, 'fatol': 1.0})

best_lnAs = result.x[0]
best_ns = result.x[1]
best_tau = result.x[2]
best_As_final = np.exp(best_lnAs) * 1e-10

print(f"\n{'='*65}")
print("RESULT: CM's OWN PARAMETERS")
print("="*65)
print(f"  A_s   = {best_As_final:.4e} (Planck ΛCDM: 2.1e-9)")
print(f"  n_s   = {best_ns:.4f}       (Planck ΛCDM: 0.9649)")
print(f"  τ     = {best_tau:.4f}       (Planck ΛCDM: 0.054)")
print(f"  χ²    = {result.fun:.1f}")
print(f"  χ²/N  = {result.fun/len(ell_data):.2f}")

# ═══════════════════════════════════════
# STEP 4: Compare — CM's A_s vs Planck's A_s
# ═══════════════════════════════════════
print(f"\n{'='*65}")
print("COMPARISON: CM vs ΛCDM CLASS output")
print("="*65)

# Run CLASS with best CM params
cosmo_cm = Class()
cosmo_cm.set({
    'output': 'tCl,pCl,lCl,mPk',
    'lensing': 'yes',
    'l_max_scalars': 2500,
    'omega_b': omega_b,
    'omega_cdm': omega_cdm,
    'h': h,
    'A_s': best_As_final,
    'n_s': best_ns,
    'tau_reio': best_tau,
})
cosmo_cm.compute()

# Run CLASS with ΛCDM Planck params
cosmo_lcdm = Class()
cosmo_lcdm.set({
    'output': 'tCl,pCl,lCl,mPk',
    'lensing': 'yes',
    'l_max_scalars': 2500,
    'omega_b': 0.02237,
    'omega_cdm': 0.1200,
    'h': 0.674,
    'A_s': 2.1e-9,
    'n_s': 0.9649,
    'tau_reio': 0.054,
})
cosmo_lcdm.compute()

# Peak comparison
cl_cm = cosmo_cm.lensed_cl(2500)
cl_lcdm = cosmo_lcdm.lensed_cl(2500)

ell = np.arange(2, 2501)
Dl_cm = cl_cm['tt'][2:2501] * ell*(ell+1)/(2*np.pi) * (2.7255e6)**2
Dl_lcdm = cl_lcdm['tt'][2:2501] * ell*(ell+1)/(2*np.pi) * (2.7255e6)**2

peak_ranges = [
    (180, 280), (480, 600), (760, 870),
    (1060, 1200), (1360, 1480), (1660, 1800), (1940, 2100),
]

print(f"\n{'Peak':>5} {'ℓ_CM':>7} {'ℓ_ΛCDM':>8} {'D_CM':>10} {'D_ΛCDM':>10} {'Diff':>8}")
print("-"*55)

for pk, (l_lo, l_hi) in enumerate(peak_ranges):
    i_lo, i_hi = l_lo-2, min(l_hi-2, len(Dl_cm)-1)
    if i_hi >= len(Dl_cm): continue
    
    i_cm = i_lo + np.argmax(Dl_cm[i_lo:i_hi+1])
    i_lcdm = i_lo + np.argmax(Dl_lcdm[i_lo:i_hi+1])
    
    print(f"{pk+1:>5} {ell[i_cm]:>7} {ell[i_lcdm]:>8} {Dl_cm[i_cm]:>10.1f} {Dl_lcdm[i_lcdm]:>10.1f} {(Dl_cm[i_cm]/Dl_lcdm[i_lcdm]-1)*100:>+8.1f}%")

# Key quantities
sigma8_cm = cosmo_cm.sigma8()
sigma8_lcdm = cosmo_lcdm.sigma8()
theta_cm = cosmo_cm.theta_s_100()
theta_lcdm = cosmo_lcdm.theta_s_100()
rs_cm = cosmo_cm.rs_drag()

print(f"\nKey quantities with CM's OWN A_s:")
print(f"  σ₈:    CM = {sigma8_cm:.4f},  ΛCDM = {sigma8_lcdm:.4f}")
print(f"  100θ*: CM = {theta_cm:.4f}, ΛCDM = {theta_lcdm:.4f}")
print(f"  r_s:   CM = {rs_cm:.2f} Mpc")

# S₈ with CM growth correction
S8_cm = sigma8_cm * 0.9793 * (0.2784/0.3)**0.5
print(f"  S₈(CM, with growth correction): {S8_cm:.4f}")
print(f"  DES measured: 0.776 ± 0.017 → {abs(S8_cm-0.776)/0.017:.2f}σ")

print(f"\n{'='*65}")
print("SUMMARY")
print("='*65")
print(f"""
ΛCDM: 6 parameters fitted to CMB
  ω_b, ω_cdm, h, A_s, n_s, τ → all 6 varied

CM:   3 derived + 3 fitted to CMB  
  ω_cdm, h, Ω_m → DERIVED from p = e^(-3/4) (FIXED)
  A_s, n_s, τ → fitted (same method as ΛCDM)
  
  3 fewer free parameters!
  
CM's A_s = {best_As_final:.4e} (vs Planck {2.1e-9:.1e})
CM's n_s = {best_ns:.4f} (vs Planck 0.9649)
CM's τ   = {best_tau:.4f} (vs Planck 0.054)
""")

cosmo_cm.struct_cleanup()
cosmo_lcdm.struct_cleanup()

print("DONE ✅")
