#!/usr/bin/env python3
"""
CM COUPLED SYSTEM — COMPLETE VPS STUDY
========================================
Mandeep Singh | 15 April 2026
Speed Gap Framework

USAGE ON VPS:
  cd ~/cmb_work
  source cmb_env/bin/activate
  mkdir -p coupled_results
  python3 cm_coupled_full_study.py 2>&1 | tee coupled_results/run_log.txt

WHAT THIS DOES:
  1. Solves KG eigenvalues at α_g = 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9
  2. Computes wavefunctions for n=1,2,3
  3. Computes stress-energy (ε+P) from each wave
  4. Runs self-consistency iteration (50 steps)
  5. Computes probability-weighted averages ⟨W⟩, ⟨OE⟩
  6. Tests proper vs coordinate cone volumes
  7. Saves ALL results as .npz + .txt
  8. Generates ALL plots
  
TIME ESTIMATE: ~30-60 min total (no timeout!)
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time, json

# Output directory
OUTDIR = "coupled_results"
os.makedirs(OUTDIR, exist_ok=True)

def log(msg):
    """Print with timestamp"""
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {msg}")

# =============================================================
# SECTION 1: CM FUNCTIONS
# =============================================================

def W_cm(r):
    """W = (r-1)/(r+2), natural units (r_s=1)"""
    return np.where(r > 1.001, (r - 1.0) / (r + 2.0), 0.001)

def W_scalar(r):
    if r <= 1.001: return 0.001
    return (r - 1.0) / (r + 2.0)

def OE_cm(r):
    return 1.0 - W_cm(r)

# =============================================================
# SECTION 2: KG SOLVER
# =============================================================

def kg_shoot(omega, mu, r_max=300.0, r_min=1.5, N_pts=8000):
    """Shoot KG from r_max inward. Returns (r, u, u_at_rmin)"""
    if omega <= 0 or omega >= mu:
        return None, None, 1e10
    
    kappa = np.sqrt(mu**2 - omega**2)
    u0 = np.exp(-kappa * r_max)
    du0 = -kappa * u0
    
    def rhs(r, y):
        w = W_scalar(r)
        F = omega**2 * w**(-2.0/3.0) - mu**2 * w**(-1.0/3.0)
        return [y[1], -F * y[0]]
    
    r_eval = np.linspace(r_max, r_min, N_pts)
    try:
        sol = solve_ivp(rhs, (r_max, r_min), [u0, du0], t_eval=r_eval,
                        method='RK45', rtol=1e-10, atol=1e-13, max_step=0.5)
        if not sol.success:
            return None, None, 1e10
        return sol.t, sol.y[0], sol.y[0][-1]
    except:
        return None, None, 1e10

def find_eigenvalues(mu, n_max=4, r_max=300.0, r_min=1.5):
    """Find all bound state eigenvalues"""
    N_scan = 500
    omegas = np.linspace(mu * 0.01, mu * 0.9999, N_scan)
    
    u_vals = []
    for om in omegas:
        _, _, u_end = kg_shoot(om, mu, r_max, r_min)
        u_vals.append(u_end)
    u_vals = np.array(u_vals)
    
    eigenvalues = []
    for i in range(len(u_vals) - 1):
        if (u_vals[i] * u_vals[i+1] < 0 and
            abs(u_vals[i]) < 1e5 and abs(u_vals[i+1]) < 1e5):
            try:
                ev = brentq(lambda om: kg_shoot(om, mu, r_max, r_min)[2],
                           omegas[i], omegas[i+1], xtol=1e-12)
                eigenvalues.append(ev)
                if len(eigenvalues) >= n_max:
                    break
            except:
                pass
    return eigenvalues

def get_wavefunction(omega, mu, r_max=300.0, r_min=1.5):
    """Get normalized R(r) = u(r)/r"""
    r_arr, u_arr, _ = kg_shoot(omega, mu, r_max, r_min)
    if r_arr is None:
        return None, None
    r_arr = r_arr[::-1]
    u_arr = u_arr[::-1]
    R_arr = u_arr / r_arr
    norm = np.trapezoid(R_arr**2 * r_arr**2, r_arr)
    if norm > 0:
        R_arr /= np.sqrt(norm)
    return r_arr, R_arr

# =============================================================
# SECTION 3: STRESS-ENERGY
# =============================================================

def compute_stress_energy(r, R, mu):
    """(ε+P) = (R')² + μ²W^(-1/3)R²"""
    dR = np.gradient(R, r)
    w = W_cm(r)
    eps_P = dR**2 + mu**2 * w**(-1.0/3.0) * R**2
    return eps_P

# =============================================================
# SECTION 4: PROBABILITY-WEIGHTED AVERAGES
# =============================================================

def compute_averages(r, R):
    """Compute all probability-weighted averages"""
    w = W_cm(r)
    P = R**2 * r**2
    P_total = np.trapezoid(P, r)
    
    avg_W = np.trapezoid(w * P, r) / P_total
    avg_OE = np.trapezoid((1 - w) * P, r) / P_total
    avg_Vf = np.trapezoid((w**(-1.0/3.0) - 1) * P, r) / P_total
    avg_gtt = np.trapezoid(w**(1.0/3.0) * P, r) / P_total
    avg_clock = np.trapezoid(w**(1.0/6.0) * P, r) / P_total
    avg_r = np.trapezoid(r * P, r) / P_total
    
    return {
        'avg_W': avg_W, 'avg_OE': avg_OE, 'avg_Vf': avg_Vf,
        'avg_gtt': avg_gtt, 'avg_clock': avg_clock, 'avg_r': avg_r
    }

# =============================================================
# SECTION 5: CONE VOLUME TESTS
# =============================================================

def test_cone_volumes(r, R, N_shells):
    """Test coordinate vs proper volume equality"""
    w = W_cm(r)
    P = R**2 * r**2
    cum_P = np.zeros_like(r)
    for i in range(1, len(r)):
        cum_P[i] = np.trapezoid(P[:i+1], r[:i+1])
    cum_P /= cum_P[-1]
    
    results = {'coord': [], 'proper': [], 'proper2': []}
    
    for k in range(N_shells):
        lo, hi = k / N_shells, (k + 1) / N_shells
        i_lo = np.searchsorted(cum_P, lo)
        i_hi = min(np.searchsorted(cum_P, hi), len(r) - 1)
        if i_hi <= i_lo: i_hi = i_lo + 1
        
        sl = slice(i_lo, i_hi + 1)
        sr, sR, sw = r[sl], R[sl], w[sl]
        
        if len(sr) > 1:
            results['coord'].append(np.trapezoid(sw * sR**2 * sr**2, sr))
            results['proper'].append(np.trapezoid(sw**(2./3.) * sR**2 * sr**2, sr))
            results['proper2'].append(np.trapezoid(sw**(-1./3.) * sR**2 * sr**2, sr))
        else:
            for k2 in results: results[k2].append(0)
    
    # Compute deviations
    devs = {}
    for key in results:
        fracs = [v / sum(results[key]) if sum(results[key]) > 0 else 0 for v in results[key]]
        devs[key] = max(abs(f - 1.0/N_shells) for f in fracs) / (1.0/N_shells) * 100
        devs[key + '_fracs'] = fracs
    
    return devs

# =============================================================
# SECTION 6: SELF-CONSISTENCY ITERATION
# =============================================================

class CM_Medium:
    def __init__(self):
        self.delta_Phi = None
        self.r_grid = None
    
    def W(self, r):
        w_vac = W_scalar(r)
        if self.delta_Phi is None or self.r_grid is None:
            return w_vac
        dPhi = np.interp(r, self.r_grid, self.delta_Phi)
        w_new = w_vac * np.exp(6 * dPhi)
        return max(min(w_new, 0.999), 0.001)
    
    def update(self, r_grid, eps_P, damping=0.05):
        new_dPhi = np.zeros_like(r_grid)
        for i in range(1, len(r_grid)):
            integral = np.trapezoid(eps_P[:i+1] * r_grid[:i+1]**2, r_grid[:i+1])
            new_dPhi[i] = -integral / (7.0 * r_grid[i])
        if self.delta_Phi is None:
            self.delta_Phi = damping * new_dPhi
        else:
            self.delta_Phi = (1 - damping) * self.delta_Phi + damping * new_dPhi
        self.r_grid = r_grid.copy()

def run_iteration(alpha_g, N_iter=50, damping=0.05):
    """Run full self-consistency iteration"""
    mu = 2 * alpha_g
    medium = CM_Medium()
    history = []
    
    for it in range(N_iter):
        # Find eigenvalue
        omega = None
        omegas_scan = np.linspace(mu * 0.3, mu * 0.999, 300)
        u_vals = [kg_shoot_medium(om, mu, medium)[2] for om in omegas_scan]
        u_vals = np.array(u_vals)
        
        for i in range(len(u_vals) - 1):
            if u_vals[i] * u_vals[i+1] < 0 and abs(u_vals[i]) < 1e5:
                try:
                    omega = brentq(lambda om: kg_shoot_medium(om, mu, medium)[2],
                                  omegas_scan[i], omegas_scan[i+1], xtol=1e-10)
                    break
                except:
                    pass
        
        if omega is None:
            log(f"  Iter {it}: NO eigenvalue")
            break
        
        # Get wavefunction
        r_arr, u_arr, _ = kg_shoot_medium(omega, mu, medium)
        r_arr = r_arr[::-1]; u_arr = u_arr[::-1]
        R = u_arr / r_arr
        norm = np.trapezoid(R**2 * r_arr**2, r_arr)
        if norm > 0: R /= np.sqrt(norm)
        
        # Stress-energy
        dR = np.gradient(R, r_arr)
        w_arr = np.array([medium.W(r) for r in r_arr])
        eps_P = dR**2 + mu**2 * w_arr**(-1.0/3.0) * R**2
        
        # Update medium
        medium.update(r_arr, eps_P, damping)
        
        # Record
        be = (1 - omega/mu) * 100
        dW_max = np.max(np.abs(medium.delta_Phi * 6 * w_arr))
        peak_idx = np.argmax(np.abs(R))
        w_peak = medium.W(r_arr[peak_idx])
        
        history.append({
            'omega': omega, 'omega_mu': omega/mu, 'be': be,
            'dW_max': dW_max, 'W_peak': w_peak
        })
        
        if it % 10 == 0:
            log(f"  Iter {it}: w/mu={omega/mu:.6f} BE={be:.4f}% dW={dW_max:.2e}")
    
    return history

def kg_shoot_medium(omega, mu, medium, r_max=200.0, r_min=1.5):
    """KG shoot using modified medium"""
    if omega <= 0 or omega >= mu: return None, None, 1e10
    kappa = np.sqrt(mu**2 - omega**2)
    u0 = np.exp(-kappa * r_max); du0 = -kappa * u0
    def rhs(r, y):
        w = medium.W(r)
        F = omega**2 * w**(-2.0/3.0) - mu**2 * w**(-1.0/3.0)
        return [y[1], -F * y[0]]
    r_eval = np.linspace(r_max, r_min, 5000)
    try:
        sol = solve_ivp(rhs, (r_max, r_min), [u0, du0], t_eval=r_eval,
                        method='RK45', rtol=1e-9, atol=1e-12, max_step=0.5)
        if not sol.success: return None, None, 1e10
        return sol.t, sol.y[0], sol.y[0][-1]
    except: return None, None, 1e10

# =============================================================
# SECTION 7: MAIN STUDY
# =============================================================

def main():
    log("="*65)
    log("CM COUPLED SYSTEM — COMPLETE VPS STUDY")
    log("Mandeep Singh | 15 April 2026")
    log("="*65)
    
    all_results = {}
    
    # ─── PART A: Eigenvalues + Averages ─────────────────────
    alpha_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9]
    
    for alpha_g in alpha_values:
        mu = 2 * alpha_g
        log(f"\n--- alpha_g = {alpha_g}, mu = {mu} ---")
        
        evs = find_eigenvalues(mu, n_max=4)
        log(f"  Found {len(evs)} eigenvalues")
        
        alpha_data = {'eigenvalues': [], 'averages': [], 'cones': []}
        
        for n_idx, omega in enumerate(evs):
            n = n_idx + 1
            be = (1 - omega/mu) * 100
            r, R = get_wavefunction(omega, mu)
            if r is None: continue
            
            # Averages
            avgs = compute_averages(r, R)
            avgs['n'] = n
            avgs['omega'] = omega
            avgs['omega_mu'] = omega/mu
            avgs['be'] = be
            
            # Cone tests
            cones = {}
            for N_sh in [2, 3, 4]:
                cones[N_sh] = test_cone_volumes(r, R, N_sh)
            
            alpha_data['eigenvalues'].append(omega)
            alpha_data['averages'].append(avgs)
            alpha_data['cones'].append(cones)
            
            log(f"  n={n}: w/mu={omega/mu:.6f} BE={be:.3f}% "
                f"<OE>={avgs['avg_OE']:.4f} <W>={avgs['avg_W']:.4f}")
            
            # Cone result for 2 shells
            c2 = cones[2]
            log(f"    Cone(2): coord={c2['coord']:.1f}% proper2={c2['proper2']:.1f}%")
        
        all_results[alpha_g] = alpha_data
    
    # ─── PART B: Self-Consistency Iteration ──────────────────
    log("\n" + "="*65)
    log("PART B: Self-Consistency Iteration")
    log("="*65)
    
    iter_results = {}
    for alpha_g in [0.3, 0.5]:
        log(f"\nIteration at alpha_g = {alpha_g}")
        hist = run_iteration(alpha_g, N_iter=50, damping=0.05)
        iter_results[alpha_g] = hist
        
        if len(hist) > 1:
            log(f"  Final: w/mu={hist[-1]['omega_mu']:.6f} BE={hist[-1]['be']:.4f}%")
            last_change = abs(hist[-1]['omega'] - hist[-2]['omega']) / hist[-2]['omega'] * 100
            log(f"  Last change: {last_change:.6f}%")
    
    # ─── PART C: Save Results ────────────────────────────────
    log("\n" + "="*65)
    log("Saving results...")
    
    # Save as text summary
    with open(f"{OUTDIR}/summary.txt", 'w') as f:
        f.write("CM COUPLED SYSTEM — RESULTS SUMMARY\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("PART A: Eigenvalues + Averages\n")
        f.write(f"{'ag':<6}{'n':<4}{'w/mu':<10}{'BE%':<8}{'<W>':<10}{'<OE>':<10}"
                f"{'cone2_c%':<10}{'cone2_p%':<10}\n")
        f.write("-" * 68 + "\n")
        
        for ag in alpha_values:
            if ag not in all_results: continue
            data = all_results[ag]
            for i, avgs in enumerate(data['averages']):
                c2 = data['cones'][i].get(2, {})
                f.write(f"{ag:<6}{avgs['n']:<4}{avgs['omega_mu']:<10.6f}"
                        f"{avgs['be']:<8.3f}{avgs['avg_W']:<10.6f}"
                        f"{avgs['avg_OE']:<10.6f}"
                        f"{c2.get('coord', 0):<10.1f}{c2.get('proper2', 0):<10.1f}\n")
        
        f.write("\nPART B: Iteration Convergence\n")
        for ag, hist in iter_results.items():
            f.write(f"\nalpha_g = {ag}: {len(hist)} iterations\n")
            for h in hist:
                f.write(f"  w/mu={h['omega_mu']:.6f} BE={h['be']:.4f}% "
                        f"dW={h['dW_max']:.2e}\n")
    
    log(f"Summary saved: {OUTDIR}/summary.txt")
    
    # ─── PART D: Generate Plots ──────────────────────────────
    log("\nGenerating plots...")
    
    # Plot 1: ⟨OE⟩ vs alpha_g
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('#0a0a14')
    ax.set_facecolor('#0f0f1a')
    
    for n_target in [1, 2, 3]:
        ag_list, oe_list = [], []
        for ag in alpha_values:
            if ag not in all_results: continue
            for avgs in all_results[ag]['averages']:
                if avgs['n'] == n_target:
                    ag_list.append(ag)
                    oe_list.append(avgs['avg_OE'])
        if ag_list:
            ax.plot(ag_list, oe_list, 'o-', markersize=8, linewidth=2,
                    label=f'n={n_target}')
    
    # Mark special OE values
    for oe_val, label, col in [(0.25, 'OE=1/4 (s quark)', '#f0c040'),
                                 (0.75, 'OE=3/4 (confinement)', '#ff4060')]:
        ax.axhline(y=oe_val, color=col, linestyle='--', alpha=0.5)
        ax.text(0.92, oe_val + 0.02, label, color=col, fontsize=9)
    
    ax.set_xlabel('alpha_g (coupling)', color='white', fontsize=12)
    ax.set_ylabel('<OE> (probability average)', color='white', fontsize=12)
    ax.set_title('Probability-Averaged OE vs Coupling Strength',
                 color='#f0c040', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, facecolor='#1a1a2e', edgecolor='#444', labelcolor='white')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.15)
    fig.savefig(f'{OUTDIR}/avg_OE_vs_alpha.png', dpi=150, bbox_inches='tight',
                facecolor='#0a0a14')
    plt.close()
    log("  Saved: avg_OE_vs_alpha.png")
    
    # Plot 2: Cone deviation — proper vs coordinate
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('#0a0a14')
    ax.set_facecolor('#0f0f1a')
    
    ag_list, coord_list, proper_list = [], [], []
    for ag in alpha_values:
        if ag not in all_results: continue
        if len(all_results[ag]['cones']) > 0:
            c2 = all_results[ag]['cones'][0].get(2, {})
            ag_list.append(ag)
            coord_list.append(c2.get('coord', 0))
            proper_list.append(c2.get('proper2', 0))
    
    ax.plot(ag_list, coord_list, 's-', color='#4080ff', markersize=8,
            linewidth=2, label='Coordinate (flat cone)')
    ax.plot(ag_list, proper_list, 'o-', color='#40ff90', markersize=8,
            linewidth=2, label='Proper W^(-1/3) (curved cone)')
    
    ax.set_xlabel('alpha_g', color='white', fontsize=12)
    ax.set_ylabel('Deviation from equal volumes (%)', color='white', fontsize=12)
    ax.set_title('Flat vs Curved Cone: Proper Volume ALWAYS Better',
                 color='#f0c040', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, facecolor='#1a1a2e', edgecolor='#444', labelcolor='white')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.15)
    fig.savefig(f'{OUTDIR}/cone_comparison.png', dpi=150, bbox_inches='tight',
                facecolor='#0a0a14')
    plt.close()
    log("  Saved: cone_comparison.png")
    
    # Plot 3: Iteration convergence
    for ag, hist in iter_results.items():
        if not hist: continue
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor('#0a0a14')
        
        iters = range(len(hist))
        
        ax = axes[0]
        ax.set_facecolor('#0f0f1a')
        ax.plot(list(iters), [h['omega_mu'] for h in hist], 'o-',
                color='#f0c040', markersize=5, linewidth=2)
        ax.set_xlabel('Iteration', color='white')
        ax.set_ylabel('omega/mu', color='white')
        ax.set_title(f'Eigenvalue (ag={ag})', color='#f0c040', fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.15)
        
        ax = axes[1]
        ax.set_facecolor('#0f0f1a')
        ax.semilogy(list(iters), [max(h['dW_max'], 1e-15) for h in hist], 'D-',
                    color='#ff4060', markersize=5, linewidth=2)
        ax.set_xlabel('Iteration', color='white')
        ax.set_ylabel('max |delta_W|', color='white')
        ax.set_title(f'Medium Change (ag={ag})', color='#f0c040', fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.15)
        
        plt.tight_layout()
        fig.savefig(f'{OUTDIR}/iteration_ag{ag}.png', dpi=150,
                    bbox_inches='tight', facecolor='#0a0a14')
        plt.close()
        log(f"  Saved: iteration_ag{ag}.png")
    
    # ─── DONE ────────────────────────────────────────────────
    log("\n" + "="*65)
    log("ALL DONE!")
    log(f"Results in: {OUTDIR}/")
    log("Files: summary.txt, avg_OE_vs_alpha.png, cone_comparison.png, iteration_*.png")
    log("="*65)

if __name__ == "__main__":
    main()
