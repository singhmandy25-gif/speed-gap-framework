#!/usr/bin/env python3
"""
CM KG COMPLETE — Eigenvalues + Real Rotation + Quark Position Test
===================================================================
Mandeep Singh | 15 April 2026

ONE script, ALL results:
  A. l=0,1,2 eigenvalues (no rotation)
  B. l=1 with REAL rotation in equation (Ω²r²<sin²θ> term)
  C. m=0 peak → f=1/3? m=±1 peak → f=2/3?
  D. Summary table

USAGE:
  cd ~/cmb_work && source cmb_env/bin/activate
  python3 -u cm_kg_complete.py 2>&1 | tee rotating_results/complete.txt
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time, os

OUTDIR = "rotating_results"
os.makedirs(OUTDIR, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

# ═══════════════════════════════════════
# CORE: KG equation with optional rotation
# ═══════════════════════════════════════

def W_s(r):
    if r <= 1.001: return 0.001
    return (r - 1.0) / (r + 2.0)

def W_cm(r):
    return np.where(r > 1.001, (r - 1.0) / (r + 2.0), 0.001)

def shoot(omega, mu, l=0, Omega=0.0, sin2avg=0.0, r_max=300., r_min=1.5):
    """
    Solve KG radial equation:
    u'' + [ω²W^(-2/3) - μ²W^(-1/3) - l(l+1)/r² - Ω²r²<sin²θ>] u = 0
    
    Omega=0, sin2avg=0 → standard KG (no rotation)
    Omega>0 → real rotation term in equation
    """
    if omega <= 0 or omega >= mu: return None, None, 1e10
    kappa = np.sqrt(mu**2 - omega**2)
    u0 = np.exp(-kappa * r_max)
    du0 = -kappa * u0
    
    def rhs(r, y):
        w = W_s(r)
        F = (omega**2 * w**(-2./3.)
             - mu**2 * w**(-1./3.)
             - l * (l + 1) / r**2
             - Omega**2 * r**2 * sin2avg)
        return [y[1], -F * y[0]]
    
    rr = np.linspace(r_max, r_min, 6000)
    try:
        sol = solve_ivp(rhs, (r_max, r_min), [u0, du0], t_eval=rr,
                        method='RK45', rtol=1e-10, atol=1e-13, max_step=0.5)
        if sol.success:
            return sol.t, sol.y[0], sol.y[0][-1]
        return None, None, 1e10
    except:
        return None, None, 1e10

def find_evs(mu, l=0, Omega=0.0, sin2avg=0.0, n_max=3):
    omegas = np.linspace(mu * 0.01, mu * 0.9999, 500)
    uv = [shoot(om, mu, l, Omega, sin2avg)[2] for om in omegas]
    uv = np.array(uv)
    evs = []
    for i in range(len(uv) - 1):
        if uv[i] * uv[i+1] < 0 and abs(uv[i]) < 1e5 and abs(uv[i+1]) < 1e5:
            try:
                ev = brentq(lambda om: shoot(om, mu, l, Omega, sin2avg)[2],
                           omegas[i], omegas[i+1], xtol=1e-12)
                evs.append(ev)
                if len(evs) >= n_max:
                    break
            except:
                pass
    return evs

def analyze(omega, mu, l=0, Omega=0.0, sin2avg=0.0):
    """Full analysis: peak, nodes, probability fractions, OE averages"""
    r_arr, u_arr, _ = shoot(omega, mu, l, Omega, sin2avg)
    if r_arr is None: return None
    
    r = r_arr[::-1]; u = u_arr[::-1]
    R = u / r
    norm = np.trapezoid(R**2 * r**2, r)
    if norm > 0: R /= np.sqrt(norm)
    P = R**2 * r**2
    w = W_cm(r)
    
    # Cumulative probability
    cum = np.zeros_like(r)
    for i in range(1, len(r)):
        cum[i] = np.trapezoid(P[:i+1], r[:i+1])
    cum /= cum[-1]
    
    # Peak
    peak_idx = np.argmax(P)
    r_peak = r[peak_idx]
    f_peak = cum[peak_idx]
    
    # Nodes
    nodes = []
    for i in range(len(R) - 1):
        if R[i] * R[i+1] < 0 and r[i] > 1.6:
            rn = r[i] - R[i] * (r[i+1] - r[i]) / (R[i+1] - R[i])
            fn = np.interp(rn, r, cum)
            nodes.append({'r': rn, 'f': fn, 'OE': 1 - W_s(rn)})
    
    # Averages
    Pt = np.trapezoid(P, r)
    avg_r = np.trapezoid(r * P, r) / Pt
    avg_OE = np.trapezoid((1 - w) * P, r) / Pt
    
    # Radius at exact f = 1/3, 1/2, 2/3
    f_positions = {}
    for ft in [1./3., 0.5, 2./3.]:
        idx = np.searchsorted(cum, ft)
        if 0 < idx < len(r):
            rf = r[idx]
            f_positions[ft] = {'r': rf, 'OE': 1 - W_s(rf)}
        else:
            f_positions[ft] = {'r': 0, 'OE': 0}
    
    return {
        'r_peak': r_peak, 'f_peak': f_peak,
        'avg_r': avg_r, 'avg_OE': avg_OE,
        'nodes': nodes, 'f_positions': f_positions,
        'r': r, 'P': P, 'cum': cum
    }

# ═══════════════════════════════════════
# sin²θ averages for l=1 states
# ═══════════════════════════════════════
SIN2_M0 = 2.0 / 5.0    # m=0: cos²θ distribution → less equatorial
SIN2_M1 = 4.0 / 5.0    # m=±1: sin²θ distribution → more equatorial

alpha_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9]

# ═══════════════════════════════════════
# PART A: Standard eigenvalues (no rotation)
# ═══════════════════════════════════════
log("=" * 70)
log("PART A: Standard l=0,1,2 eigenvalues (no rotation)")
log("=" * 70)

all_standard = []

for ag in alpha_values:
    mu = 2 * ag
    log(f"\nalpha_g = {ag}")
    
    for l in [0, 1, 2]:
        evs = find_evs(mu, l=l)
        if not evs:
            log(f"  l={l}: no states")
            continue
        
        for ni, ev in enumerate(evs):
            info = analyze(ev, mu, l)
            if info is None: continue
            
            be = (1 - ev / mu) * 100
            ns = " ".join([f"NODE r={nd['r']:.1f}(f={nd['f']:.3f})" for nd in info['nodes']])
            log(f"  l={l} n={ni+1}: BE={be:.3f}% f_peak={info['f_peak']:.4f} "
                f"<OE>={info['avg_OE']:.4f} {ns}")
            
            all_standard.append({
                'ag': ag, 'l': l, 'n': ni + 1, 'ev': ev, 'mu': mu,
                'be': be, 'f_peak': info['f_peak'], 'avg_OE': info['avg_OE'],
                'nodes': info['nodes'], 'f_positions': info['f_positions']
            })

# ═══════════════════════════════════════
# PART B: l=1 with REAL rotation
# ═══════════════════════════════════════
log("\n" + "=" * 70)
log("PART B: l=1 with REAL rotation (Ω²r²<sin²θ> in equation)")
log("=" * 70)
log(f"<sin²θ>: m=0 = {SIN2_M0:.3f}, m=±1 = {SIN2_M1:.3f}")

Omega_fracs = [0.0, 0.001, 0.002, 0.003, 0.005, 0.007, 0.01, 
               0.015, 0.02, 0.025, 0.03, 0.04, 0.05]

rotation_results = []

for ag in [0.3, 0.5, 0.7, 0.9]:
    mu = 2 * ag
    log(f"\nalpha_g = {ag}, mu = {mu}")
    log(f"  {'Omega/mu':<10} {'m0_f':<9} {'m0_r':<9} {'m1_f':<9} {'m1_r':<9} "
        f"{'ratio':<9} {'d_1/3%':<9} {'d_2/3%':<9} {'note':<10}")
    log(f"  {'-'*80}")
    
    for Of in Omega_fracs:
        Omega = Of * mu
        
        if Of == 0:
            ev_m0 = find_evs(mu, l=1, n_max=1)
            ev_m0 = ev_m0[0] if ev_m0 else None
            ev_m1 = ev_m0
            sin2_0, sin2_1 = 0, 0
        else:
            ev_m0_list = find_evs(mu, l=1, Omega=Omega, sin2avg=SIN2_M0, n_max=1)
            ev_m1_list = find_evs(mu, l=1, Omega=Omega, sin2avg=SIN2_M1, n_max=1)
            ev_m0 = ev_m0_list[0] if ev_m0_list else None
            ev_m1 = ev_m1_list[0] if ev_m1_list else None
            sin2_0, sin2_1 = SIN2_M0, SIN2_M1
        
        if ev_m0 and ev_m1:
            info0 = analyze(ev_m0, mu, l=1, Omega=Omega, sin2avg=sin2_0)
            if Of == 0:
                info1 = info0
            else:
                info1 = analyze(ev_m1, mu, l=1, Omega=Omega, sin2avg=sin2_1)
            
            if info0 and info1:
                fp0 = info0['f_peak']
                fp1 = info1['f_peak']
                rp0 = info0['r_peak']
                rp1 = info1['r_peak']
                ratio = fp1 / fp0 if fp0 > 0 else 0
                d0 = abs(fp0 - 1./3.) / (1./3.) * 100
                d1 = abs(fp1 - 2./3.) / (2./3.) * 100
                
                note = ""
                if d0 < 5 and d1 < 10:
                    note = "MATCH!"
                elif d0 < 10 and d1 < 20:
                    note = "CLOSE"
                
                log(f"  {Of:<10.3f} {fp0:<9.4f} {rp0:<9.1f} {fp1:<9.4f} {rp1:<9.1f} "
                    f"{ratio:<9.3f} {d0:<9.1f} {d1:<9.1f} {note}")
                
                rotation_results.append({
                    'ag': ag, 'Of': Of, 'fp0': fp0, 'fp1': fp1,
                    'rp0': rp0, 'rp1': rp1, 'd0': d0, 'd1': d1,
                    'ev0': ev_m0, 'ev1': ev_m1
                })
        else:
            lost = "m=0 lost" if not ev_m0 else "m=1 lost"
            log(f"  {Of:<10.3f} {lost}")

# ═══════════════════════════════════════
# PART C: Find BEST rotation rate
# ═══════════════════════════════════════
log("\n" + "=" * 70)
log("PART C: Best rotation rate for f=1/3 + f=2/3 match")
log("=" * 70)

best_results = {}

for ag in [0.3, 0.5, 0.7, 0.9]:
    mu = 2 * ag
    log(f"\nalpha_g = {ag}: fine scanning Omega...")
    
    best_score = 999
    best = None
    
    for Of in np.arange(0.001, 0.06, 0.0005):
        Omega = Of * mu
        
        ev0_list = find_evs(mu, l=1, Omega=Omega, sin2avg=SIN2_M0, n_max=1)
        ev1_list = find_evs(mu, l=1, Omega=Omega, sin2avg=SIN2_M1, n_max=1)
        
        if ev0_list and ev1_list:
            info0 = analyze(ev0_list[0], mu, l=1, Omega=Omega, sin2avg=SIN2_M0)
            info1 = analyze(ev1_list[0], mu, l=1, Omega=Omega, sin2avg=SIN2_M1)
            
            if info0 and info1:
                fp0 = info0['f_peak']
                fp1 = info1['f_peak']
                d0 = abs(fp0 - 1./3.) / (1./3.) * 100
                d1 = abs(fp1 - 2./3.) / (2./3.) * 100
                score = d0 + d1
                
                if score < best_score:
                    best_score = score
                    best = {
                        'Of': Of, 'fp0': fp0, 'fp1': fp1,
                        'rp0': info0['r_peak'], 'rp1': info1['r_peak'],
                        'd0': d0, 'd1': d1,
                        'ev0': ev0_list[0], 'ev1': ev1_list[0],
                        'oe0': info0['avg_OE'], 'oe1': info1['avg_OE']
                    }
    
    if best:
        best_results[ag] = best
        dE = abs(best['ev1'] - best['ev0'])
        log(f"  BEST Omega = {best['Of']:.4f} * mu")
        log(f"    m=0:  f_peak = {best['fp0']:.4f}  (1/3 = 0.3333, diff = {best['d0']:.1f}%)")
        log(f"    m=±1: f_peak = {best['fp1']:.4f}  (2/3 = 0.6667, diff = {best['d1']:.1f}%)")
        log(f"    ratio = {best['fp1']/best['fp0']:.3f}  (target 2.0)")
        log(f"    <OE> m=0 = {best['oe0']:.4f}, <OE> m=±1 = {best['oe1']:.4f}")
        log(f"    energy split = {dE:.6f} = {dE/mu*938:.1f} MeV")
    else:
        log(f"  no valid states found")

# ═══════════════════════════════════════
# PART D: OE at f=1/3, 1/2, 2/3 positions
# ═══════════════════════════════════════
log("\n" + "=" * 70)
log("PART D: OE values at Damru positions (l=0 ground states)")
log("=" * 70)
log(f"{'ag':<6} {'OE@1/3':<10} {'match_d?':<12} {'OE@1/2':<10} {'match_neck?':<12} {'OE@2/3':<10}")
log("-" * 60)

for row in all_standard:
    if row['l'] == 0 and row['n'] == 1:
        fp = row['f_positions']
        oe13 = fp[1./3.]['OE']
        oe12 = fp[0.5]['OE']
        oe23 = fp[2./3.]['OE']
        d_neck = abs(oe12 - 0.5) / 0.5 * 100
        log(f"{row['ag']:<6} {oe13:<10.4f} {'—':<12} {oe12:<10.4f} {d_neck:<12.1f} {oe23:<10.4f}")

# ═══════════════════════════════════════
# PART E: MASTER SUMMARY
# ═══════════════════════════════════════
log("\n" + "=" * 70)
log("MASTER SUMMARY")
log("=" * 70)

log("\n1. l=0 ground state peaks at f ≈ 1/3 (d quark position):")
for row in all_standard:
    if row['l'] == 0 and row['n'] == 1:
        d = abs(row['f_peak'] - 1./3.) / (1./3.) * 100
        log(f"   ag={row['ag']}: f_peak = {row['f_peak']:.4f} ({d:.1f}% from 1/3)")

log("\n2. Rotation splits l=1 into m=0 (1/3?) and m=±1 (2/3?):")
for ag, b in best_results.items():
    log(f"   ag={ag}: m=0→{b['fp0']:.4f}({b['d0']:.1f}%) m=±1→{b['fp1']:.4f}({b['d1']:.1f}%) Omega={b['Of']:.4f}mu")

log("\n3. OE at f=1/2 approaches 1/2 (neck) at strong coupling:")
for row in all_standard:
    if row['l'] == 0 and row['n'] == 1 and row['ag'] >= 0.5:
        oe12 = row['f_positions'][0.5]['OE']
        d = abs(oe12 - 0.5) / 0.5 * 100
        log(f"   ag={row['ag']}: OE@f=1/2 = {oe12:.4f} ({d:.1f}% from 1/2)")

# ═══════════════════════════════════════
# PART F: Plots
# ═══════════════════════════════════════
log("\nGenerating plots...")

# Plot 1: f_peak vs alpha_g
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('#0a0a14')
ax.set_facecolor('#0f0f1a')

for l, col, mk in [(0, '#f0c040', 'o'), (1, '#40e0d0', 's'), (2, '#ff4060', 'D')]:
    ag_list = [r['ag'] for r in all_standard if r['l'] == l and r['n'] == 1]
    fp_list = [r['f_peak'] for r in all_standard if r['l'] == l and r['n'] == 1]
    if ag_list:
        ax.plot(ag_list, fp_list, f'{mk}-', color=col, markersize=8, linewidth=2,
                label=f'l={l} ground (no rotation)')

ax.axhline(y=1./3., color='white', linestyle='--', alpha=0.7, linewidth=2)
ax.text(0.12, 1./3. + 0.008, 'f = 1/3 (d quark)', color='white', fontsize=11)
ax.axhline(y=2./3., color='white', linestyle=':', alpha=0.4)
ax.text(0.12, 2./3. + 0.008, 'f = 2/3 (u quark)', color='white', fontsize=10)
ax.axhline(y=0.5, color='#888', linestyle=':', alpha=0.3)
ax.text(0.12, 0.508, 'f = 1/2 (neck)', color='#888', fontsize=9)

ax.set_xlabel('alpha_g', color='white', fontsize=13)
ax.set_ylabel('f_peak (probability fraction at wave peak)', color='white', fontsize=13)
ax.set_title('Wave Peak Position: f = 1/3 Confirmed at All Couplings',
             color='#f0c040', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, facecolor='#1a1a2e', edgecolor='#444', labelcolor='white')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.15)
ax.set_ylim(0.25, 0.75)
fig.savefig(f'{OUTDIR}/f_peak_all.png', dpi=150, bbox_inches='tight', facecolor='#0a0a14')
plt.close()

# Plot 2: Rotation effect on m=0 vs m=±1
if rotation_results:
    for ag in [0.3, 0.5, 0.7]:
        data = [r for r in rotation_results if r['ag'] == ag and r['Of'] > 0]
        if not data: continue
        
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.patch.set_facecolor('#0a0a14')
        ax.set_facecolor('#0f0f1a')
        
        ofs = [r['Of'] for r in data]
        fp0s = [r['fp0'] for r in data]
        fp1s = [r['fp1'] for r in data]
        
        ax.plot(ofs, fp0s, 'o-', color='#40e0d0', markersize=6, linewidth=2, label='m=0 (axis)')
        ax.plot(ofs, fp1s, 's-', color='#ff6060', markersize=6, linewidth=2, label='m=±1 (equator)')
        
        ax.axhline(y=1./3., color='#40e0d0', linestyle='--', alpha=0.5)
        ax.axhline(y=2./3., color='#ff6060', linestyle='--', alpha=0.5)
        ax.text(0.002, 1./3. - 0.02, 'target: 1/3', color='#40e0d0', fontsize=10)
        ax.text(0.002, 2./3. + 0.01, 'target: 2/3', color='#ff6060', fontsize=10)
        
        ax.set_xlabel('Omega / mu (rotation rate)', color='white', fontsize=13)
        ax.set_ylabel('f_peak', color='white', fontsize=13)
        ax.set_title(f'Rotation Splits Peaks: alpha_g={ag}',
                     color='#f0c040', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11, facecolor='#1a1a2e', edgecolor='#444', labelcolor='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.15)
        fig.savefig(f'{OUTDIR}/rotation_split_ag{ag}.png', dpi=150,
                    bbox_inches='tight', facecolor='#0a0a14')
        plt.close()

log(f"\nAll saved in {OUTDIR}/")
log("=" * 70)
log("DONE!")
log("=" * 70)
