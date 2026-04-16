#!/usr/bin/env python3
"""
CM ROTATING KG — FULL VPS STUDY
=================================
Mandeep Singh | 15 April 2026

USAGE:
  cd ~/cmb_work && source cmb_env/bin/activate
  mkdir -p rotating_results
  nohup python3 cm_rotating_kg.py > rotating_results/log.txt 2>&1 &
  tail -f rotating_results/log.txt

WHAT THIS DOES:
  1. l=0,1,2 eigenvalues at 7 coupling strengths
  2. Wavefunction peak positions → probability fraction f
  3. Node positions → check f=1/3, 2/3 match
  4. Rotation splitting of l=1 (m=-1,0,+1)
  5. ⟨OE⟩ averages for all states
  6. Saves everything

KEY QUESTION: Does wave peak at f=1/3 (Damru d-quark)?
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time

OUTDIR = "rotating_results"
os.makedirs(OUTDIR, exist_ok=True)

def log(msg):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {msg}")

def W_s(r):
    if r <= 1.001: return 0.001
    return (r-1.0)/(r+2.0)

def W_cm(r):
    return np.where(r > 1.001, (r-1.0)/(r+2.0), 0.001)

def shoot_full(omega, mu, l=0, r_max=300.0, r_min=1.5):
    if omega <= 0 or omega >= mu: return None, None, 1e10
    kappa = np.sqrt(mu**2 - omega**2)
    u0 = np.exp(-kappa*r_max); du0 = -kappa*u0
    def rhs(r, y):
        w = W_s(r)
        F = omega**2*w**(-2.0/3.0) - mu**2*w**(-1.0/3.0) - l*(l+1)/r**2
        return [y[1], -F*y[0]]
    rr = np.linspace(r_max, r_min, 6000)
    try:
        sol = solve_ivp(rhs, (r_max, r_min), [u0, du0], t_eval=rr,
                        method='RK45', rtol=1e-10, atol=1e-13, max_step=0.5)
        if sol.success:
            return sol.t, sol.y[0], sol.y[0][-1]
        return None, None, 1e10
    except:
        return None, None, 1e10

def find_evs(mu, l=0, n_max=4):
    omegas = np.linspace(mu*0.01, mu*0.9999, 400)
    uv = [shoot_full(om, mu, l)[2] for om in omegas]
    uv = np.array(uv)
    evs = []
    for i in range(len(uv)-1):
        if uv[i]*uv[i+1] < 0 and abs(uv[i]) < 1e5 and abs(uv[i+1]) < 1e5:
            try:
                ev = brentq(lambda om: shoot_full(om, mu, l)[2],
                           omegas[i], omegas[i+1], xtol=1e-12)
                evs.append(ev)
                if len(evs) >= n_max: break
            except: pass
    return evs

def analyze_wavefunction(omega, mu, l=0):
    """Get peak position, nodes, probability fractions, averages"""
    r_arr, u_arr, _ = shoot_full(omega, mu, l)
    if r_arr is None: return None
    
    r = r_arr[::-1]; u = u_arr[::-1]
    R = u / r
    norm = np.trapezoid(R**2 * r**2, r)
    if norm > 0: R /= np.sqrt(norm)
    
    P = R**2 * r**2
    w = W_cm(r)
    
    # Cumulative probability
    cum_P = np.zeros_like(r)
    for i in range(1, len(r)):
        cum_P[i] = np.trapezoid(P[:i+1], r[:i+1])
    cum_P /= cum_P[-1]
    
    # Peak
    peak_idx = np.argmax(P)
    r_peak = r[peak_idx]
    f_peak = cum_P[peak_idx]
    
    # Nodes (zero crossings)
    nodes = []
    for i in range(len(R)-1):
        if R[i]*R[i+1] < 0 and r[i] > 1.6:
            r_node = r[i] - R[i]*(r[i+1]-r[i])/(R[i+1]-R[i])
            f_node = np.interp(r_node, r, cum_P)
            w_node = W_s(r_node)
            nodes.append({'r': r_node, 'f': f_node, 'W': w_node, 'OE': 1-w_node})
    
    # Averages
    P_total = np.trapezoid(P, r)
    avg_r = np.trapezoid(r * P, r) / P_total
    avg_OE = np.trapezoid((1-w) * P, r) / P_total
    avg_W = np.trapezoid(w * P, r) / P_total
    
    # Proper volume fraction at peak
    proper_P = P * w**(-1.0/3.0)
    cum_proper = np.zeros_like(r)
    for i in range(1, len(r)):
        cum_proper[i] = np.trapezoid(proper_P[:i+1], r[:i+1])
    if cum_proper[-1] > 0:
        cum_proper /= cum_proper[-1]
    f_proper_peak = cum_proper[peak_idx]
    
    return {
        'r_peak': r_peak, 'f_peak': f_peak, 'f_proper_peak': f_proper_peak,
        'avg_r': avg_r, 'avg_OE': avg_OE, 'avg_W': avg_W,
        'nodes': nodes, 'r': r, 'R': R, 'P': P, 'cum_P': cum_P
    }

# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════

log("="*60)
log("CM ROTATING KG — FULL VPS STUDY")
log("="*60)

alpha_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9]
all_data = []

# PART A: Eigenvalues + node positions for l=0,1,2
for alpha_g in alpha_values:
    mu = 2 * alpha_g
    log(f"\nalpha_g = {alpha_g}, mu = {mu}")
    
    for l in [0, 1, 2]:
        evs = find_evs(mu, l=l, n_max=3)
        if not evs:
            log(f"  l={l}: no bound states")
            continue
        
        log(f"  l={l}: {len(evs)} states")
        
        for ni, ev in enumerate(evs):
            info = analyze_wavefunction(ev, mu, l)
            if info is None: continue
            
            be = (1 - ev/mu) * 100
            row = {
                'alpha_g': alpha_g, 'l': l, 'n': ni+1,
                'omega_mu': ev/mu, 'be': be,
                'r_peak': info['r_peak'],
                'f_peak': info['f_peak'],
                'f_proper_peak': info['f_proper_peak'],
                'avg_r': info['avg_r'],
                'avg_OE': info['avg_OE'],
                'nodes': info['nodes']
            }
            all_data.append(row)
            
            node_str = ""
            for nd in info['nodes']:
                node_str += f" NODE r={nd['r']:.1f}(f={nd['f']:.3f})"
            
            log(f"    n={ni+1}: BE={be:.3f}% peak_r={info['r_peak']:.1f} "
                f"f_peak={info['f_peak']:.4f} f_proper={info['f_proper_peak']:.4f} "
                f"<OE>={info['avg_OE']:.4f}{node_str}")

# PART B: Rotation splitting
log("\n" + "="*60)
log("ROTATION SPLITTING (l=1, m=-1,0,+1)")
log("="*60)

for alpha_g in [0.3, 0.5, 0.7]:
    mu = 2 * alpha_g
    evs_l1 = find_evs(mu, l=1, n_max=1)
    if not evs_l1: continue
    
    E0 = evs_l1[0]
    
    # Better rotation estimate: proton spin = hbar/2
    # omega_rot = hbar/(2*I) where I = (2/5)*m*R^2
    # In natural units: omega_rot ~ 5/(4*mu*R_peak^2)
    info = analyze_wavefunction(E0, mu, l=1)
    if info is None: continue
    R_peak = info['r_peak']
    
    omega_rot = 5.0 / (4.0 * mu * R_peak**2)
    
    log(f"\nalpha_g = {alpha_g}: E0/mu = {E0/mu:.6f}, R_peak = {R_peak:.1f}")
    log(f"  omega_rot = {omega_rot:.6f} ({omega_rot/mu*100:.4f}% of mu)")
    
    for m in [-1, 0, 1]:
        E_m = E0 + m * omega_rot
        be_m = (1 - E_m/mu) * 100
        log(f"  m={m:+d}: w/mu={E_m/mu:.6f} B.E.={be_m:.4f}%")
    
    # Mass ratio estimate
    dE = 2 * omega_rot  # splitting between m=+1 and m=-1
    log(f"  total splitting: {dE:.6f} = {dE/mu*100:.4f}% of mu")
    log(f"  if mu=938 MeV: splitting = {dE/mu*938:.2f} MeV")

# PART C: Check f=1/3, 1/2, 2/3 positions
log("\n" + "="*60)
log("KEY TEST: f = 1/3 (d quark), 1/2 (neck), 2/3 (u quark)")
log("="*60)

# C1: f_peak check
log(f"\n--- C1: Where does wave PEAK? ---")
log(f"{'ag':<6}{'l':<4}{'n':<4}{'f_peak':<10}{'diff_1/3':<10}{'diff_2/3':<10}{'closest':<10}")
log("-"*54)
for row in all_data:
    if row['n'] == 1:
        d13 = abs(row['f_peak'] - 1/3) / (1/3) * 100
        d23 = abs(row['f_peak'] - 2/3) / (2/3) * 100
        d12 = abs(row['f_peak'] - 1/2) / (1/2) * 100
        closest = "1/3" if d13 < d23 and d13 < d12 else ("2/3" if d23 < d12 else "1/2")
        marker = " <<<" if min(d13,d23,d12) < 5 else ""
        log(f"{row['alpha_g']:<6}{row['l']:<4}{row['n']:<4}"
            f"{row['f_peak']:<10.4f}{d13:<10.1f}{d23:<10.1f}{closest}{marker}")

# C2: Find r where f = 1/3, 1/2, 2/3 exactly
log(f"\n--- C2: Radius at exact f = 1/3, 1/2, 2/3 positions ---")
log(f"{'ag':<6}{'l':<4}{'n':<4}{'r@f=1/3':<10}{'OE@1/3':<10}{'r@f=1/2':<10}{'OE@1/2':<10}{'r@f=2/3':<10}{'OE@2/3':<10}")
log("-"*64)
for row in all_data:
    if row['n'] != 1: continue
    # Re-analyze to get exact positions
    ev_mu = row['omega_mu'] * 2 * row['alpha_g']
    mu = 2 * row['alpha_g']
    info = analyze_wavefunction(ev_mu, mu, row['l'])
    if info is None: continue
    
    r = info['r']
    cum = info['cum_P']
    w = W_cm(r)
    
    results_f = {}
    for f_target, name in [(1/3, '1/3'), (1/2, '1/2'), (2/3, '2/3')]:
        idx = np.searchsorted(cum, f_target)
        if idx < len(r):
            r_at_f = r[idx]
            w_at_f = W_s(r_at_f)
            oe_at_f = 1 - w_at_f
            results_f[name] = {'r': r_at_f, 'OE': oe_at_f}
        else:
            results_f[name] = {'r': 0, 'OE': 0}
    
    log(f"{row['alpha_g']:<6}{row['l']:<4}{row['n']:<4}"
        f"{results_f['1/3']['r']:<10.2f}{results_f['1/3']['OE']:<10.4f}"
        f"{results_f['1/2']['r']:<10.2f}{results_f['1/2']['OE']:<10.4f}"
        f"{results_f['2/3']['r']:<10.2f}{results_f['2/3']['OE']:<10.4f}")

# C3: Node positions check against 1/3, 2/3
log(f"\n--- C3: Do NODES fall at f = 1/3 or 2/3? ---")
for row in all_data:
    if not row['nodes']: continue
    for nd in row['nodes']:
        d13 = abs(nd['f'] - 1/3) / (1/3) * 100
        d23 = abs(nd['f'] - 2/3) / (2/3) * 100
        d12 = abs(nd['f'] - 1/2) / (1/2) * 100
        closest = min(d13, d23, d12)
        which = "1/3" if d13==closest else ("2/3" if d23==closest else "1/2")
        marker = " <<<" if closest < 10 else ""
        log(f"  ag={row['alpha_g']} l={row['l']} n={row['n']}: "
            f"node r={nd['r']:.1f} f={nd['f']:.4f} OE={nd['OE']:.4f} "
            f"closest={which}({closest:.1f}%){marker}")

# C4: Combined Damru check
log(f"\n--- C4: Damru positions from WAVE probability ---")
log("Damru 2026d: d at f=1/3, neck at f=1/2, u at f=2/3")
log("CM KG wave: where do these fractions fall?")
log(f"\n{'ag':<6}{'l':<4}{'OE@f=1/3':<12}{'match d?':<12}{'OE@f=1/2':<12}{'match neck?':<12}{'OE@f=2/3':<12}{'match u?':<12}")
log("-"*72)
for row in all_data:
    if row['n'] != 1 or row['l'] != 0: continue
    ev_mu = row['omega_mu'] * 2 * row['alpha_g']
    mu = 2 * row['alpha_g']
    info = analyze_wavefunction(ev_mu, mu, 0)
    if info is None: continue
    
    r = info['r']; cum = info['cum_P']; w = W_cm(r)
    
    oe_vals = {}
    for f_target in [1/3, 1/2, 2/3]:
        idx = np.searchsorted(cum, f_target)
        if idx < len(r):
            oe_vals[f_target] = 1 - W_s(r[idx])
        else:
            oe_vals[f_target] = 0
    
    # d quark OE in 2026m = 1/20 = 0.05
    # neck OE = 1/2
    # u quark OE in 2026m = 0 (free)
    d_match = abs(oe_vals[1/3] - 0.05) / 0.05 * 100 if oe_vals[1/3] > 0 else 999
    n_match = abs(oe_vals[1/2] - 0.5) / 0.5 * 100
    u_match = "free" 
    
    log(f"{row['alpha_g']:<6}{row['l']:<4}"
        f"{oe_vals[1/3]:<12.4f}{d_match:<12.1f}"
        f"{oe_vals[1/2]:<12.4f}{n_match:<12.1f}"
        f"{oe_vals[2/3]:<12.4f}{u_match:<12}")

# PART D: Save summary
with open(f"{OUTDIR}/summary.txt", 'w') as f:
    f.write("CM ROTATING KG — RESULTS\n")
    f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M')}\n\n")
    
    f.write(f"{'ag':<6}{'l':<4}{'n':<4}{'w/mu':<10}{'BE%':<8}{'r_peak':<8}"
            f"{'f_peak':<10}{'f_proper':<10}{'<OE>':<8}{'nodes':<30}\n")
    f.write("-"*90 + "\n")
    
    for row in all_data:
        ns = " ".join([f"r={nd['r']:.1f}(f={nd['f']:.3f})" for nd in row['nodes']])
        f.write(f"{row['alpha_g']:<6}{row['l']:<4}{row['n']:<4}"
                f"{row['omega_mu']:<10.6f}{row['be']:<8.3f}{row['r_peak']:<8.1f}"
                f"{row['f_peak']:<10.4f}{row['f_proper_peak']:<10.4f}"
                f"{row['avg_OE']:<8.4f}{ns}\n")

# PART E: Plots
log("\nGenerating plots...")

# Plot 1: f_peak vs alpha_g for each l
fig, ax = plt.subplots(figsize=(10,7))
fig.patch.set_facecolor('#0a0a14')
ax.set_facecolor('#0f0f1a')

for l, col, mk in [(0,'#f0c040','o'), (1,'#40e0d0','s'), (2,'#ff4060','D')]:
    ag_list = [r['alpha_g'] for r in all_data if r['l']==l and r['n']==1]
    fp_list = [r['f_peak'] for r in all_data if r['l']==l and r['n']==1]
    if ag_list:
        ax.plot(ag_list, fp_list, f'{mk}-', color=col, markersize=8,
                linewidth=2, label=f'l={l} ground state')

ax.axhline(y=1/3, color='white', linestyle='--', alpha=0.5, linewidth=2)
ax.text(0.92, 1/3+0.01, 'f = 1/3 (d quark)', color='white', fontsize=10)
ax.axhline(y=2/3, color='white', linestyle=':', alpha=0.3)
ax.text(0.92, 2/3+0.01, 'f = 2/3 (u quark)', color='white', fontsize=9)

ax.set_xlabel('alpha_g', color='white', fontsize=12)
ax.set_ylabel('f_peak (prob fraction at wavefunction peak)', color='white', fontsize=12)
ax.set_title('Does Wave Peak at f = 1/3 (Damru d-quark)?',
             color='#f0c040', fontsize=13, fontweight='bold')
ax.legend(fontsize=11, facecolor='#1a1a2e', edgecolor='#444', labelcolor='white')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.15)
fig.savefig(f'{OUTDIR}/f_peak_vs_alpha.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a14')
plt.close()

# Plot 2: f_peak (probability) vs f_peak (proper volume)
fig, ax = plt.subplots(figsize=(10,7))
fig.patch.set_facecolor('#0a0a14')
ax.set_facecolor('#0f0f1a')

for l, col, mk in [(0,'#f0c040','o'), (1,'#40e0d0','s'), (2,'#ff4060','D')]:
    fp = [r['f_peak'] for r in all_data if r['l']==l and r['n']==1]
    fpp = [r['f_proper_peak'] for r in all_data if r['l']==l and r['n']==1]
    if fp:
        ax.scatter(fp, fpp, c=col, marker=mk, s=100, label=f'l={l}', zorder=3)

ax.plot([0,1],[0,1], 'w--', alpha=0.3, label='f_prob = f_proper')
ax.axvline(x=1/3, color='#f0c040', linestyle=':', alpha=0.5)
ax.axhline(y=1/3, color='#f0c040', linestyle=':', alpha=0.5)
ax.set_xlabel('f_peak (probability)', color='white', fontsize=12)
ax.set_ylabel('f_peak (proper volume)', color='white', fontsize=12)
ax.set_title('Probability vs Proper Volume Fraction at Peak',
             color='#f0c040', fontsize=13, fontweight='bold')
ax.legend(fontsize=11, facecolor='#1a1a2e', edgecolor='#444', labelcolor='white')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.15)
fig.savefig(f'{OUTDIR}/f_prob_vs_proper.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a14')
plt.close()

log(f"\nAll saved in {OUTDIR}/")
log("="*60)
log("DONE!")
log("="*60)
