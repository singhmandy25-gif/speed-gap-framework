#!/usr/bin/env python3
"""
CM KG in SPHERICAL JUG — Proton = Finite Box
=============================================
Mandeep Singh | 15 April 2026

PHYSICS:
  Wave TRAPPED inside sphere (radius R)
  NOT free space — CLOSED jug!
  
  Boundary conditions:
    ψ(r=0) = finite (regularity)
    ψ(r=R) = 0     (hard wall = confinement)
  
  Like electron in atom but REVERSED:
    Atom: wave goes 0→∞, decays at ∞
    Proton: wave goes 0→R, ZERO at R (wall)
  
  CM metric inside: W(r) = varies from W_center to W_surface
  W_surface = 1/4 (OE = 3/4, confinement)
  W_center = ??? (depends on model)

KEY QUESTIONS:
  1. Standing wave nodes at f = 1/3 and 2/3?
  2. How many modes fit inside?
  3. l=0 vs l=1 node positions different?

USAGE:
  cd ~/cmb_work && source cmb_env/bin/activate
  python3 -u cm_jug.py 2>&1 | tee rotating_results/jug.txt
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
# W(r) INSIDE proton
# ═══════════════════════════════════════
# Model: W goes from W_center (near 1) to W_surface (= 1/4)
# Using CM exterior formula mapped to interior:
#   Outside: W = (r-r_s)/(r+2r_s) with r_s = 1 (natural units)
#   Inside jug: we need W(0)→something, W(R)→1/4
#
# Several models to test:

def W_linear(r, R):
    """Linear: W goes from 1 at center to 1/4 at surface"""
    return 1.0 - 0.75 * (r / R)

def W_quadratic(r, R):
    """Quadratic: W = 1 - (3/4)(r/R)²"""
    return 1.0 - 0.75 * (r / R)**2

def W_volume(r, R):
    """Volume fraction: W = 1 - (3/4)×f = 1 - (3/4)(r/R)³"""
    return 1.0 - 0.75 * (r / R)**3

def W_CM_interior(r, R):
    """CM-inspired: W = 1/(1 + 3(r/R)²) → W(0)=1, W(R)=1/4"""
    return 1.0 / (1.0 + 3.0 * (r / R)**2)

def W_OE_linear(r, R):
    """OE linear: OE = (3/4)(r/R), so W = 1 - (3/4)(r/R)"""
    return 1.0 - 0.75 * (r / R)

W_MODELS = {
    'linear':    W_linear,
    'quadratic': W_quadratic,
    'volume':    W_volume,
    'CM_interior': W_CM_interior,
}

# ═══════════════════════════════════════
# SOLVER: Shoot from r=0 outward to r=R
# ═══════════════════════════════════════

def shoot_jug(omega, R, l, W_func, mu=1.0, dr_start=0.001):
    """
    Shoot outward from r≈0 to r=R
    Returns: r_array, u_array (u = r×R(r)), u(R)
    
    Equation: u'' + [ω²/W^(2/3) - μ²/W^(1/3) - l(l+1)/r²] u = 0
    Start: u ~ r^(l+1) near origin
    Check: u(R) = 0 for eigenvalue
    """
    r0 = dr_start
    # Initial conditions: u ~ r^(l+1), u' ~ (l+1)r^l
    u0 = r0**(l + 1)
    du0 = (l + 1) * r0**l
    
    def rhs(r, y):
        w = W_func(r, R)
        if w < 0.001:
            w = 0.001
        F = omega**2 * w**(-2.0/3.0) - mu**2 * w**(-1.0/3.0) - l*(l+1) / r**2
        return [y[1], -F * y[0]]
    
    rr = np.linspace(r0, R, 3000)
    try:
        sol = solve_ivp(rhs, (r0, R), [u0, du0], t_eval=rr,
                        method='RK45', rtol=1e-10, atol=1e-13, max_step=R/500)
        if sol.success:
            return sol.t, sol.y[0], sol.y[0][-1]
        return None, None, 1e10
    except:
        return None, None, 1e10

def find_jug_evs(R, l, W_func, mu=1.0, n_max=6):
    """Find eigenvalues where u(R) = 0"""
    # omega must be > 0 and < mu for bound state
    # In jug, omega can be > mu too (standing waves)
    # Scan wide range
    omega_max = mu * 5.0  # can be above mu in confined box
    omegas = np.linspace(0.01, omega_max, 1000)
    
    uR = []
    for om in omegas:
        _, _, val = shoot_jug(om, R, l, W_func, mu)
        uR.append(val)
    uR = np.array(uR)
    
    evs = []
    for i in range(len(uR) - 1):
        if uR[i] * uR[i+1] < 0 and abs(uR[i]) < 1e8 and abs(uR[i+1]) < 1e8:
            try:
                ev = brentq(lambda om: shoot_jug(om, R, l, W_func, mu)[2],
                           omegas[i], omegas[i+1], xtol=1e-10)
                evs.append(ev)
                if len(evs) >= n_max:
                    break
            except:
                pass
    return evs

def analyze_jug(omega, R, l, W_func, mu=1.0):
    """Analyze wavefunction: peaks, nodes, f-values"""
    r_arr, u_arr, _ = shoot_jug(omega, R, l, W_func, mu)
    if r_arr is None:
        return None
    
    r = r_arr
    R_wave = u_arr / r  # R(r) = u/r
    # Avoid division by zero
    R_wave[0] = R_wave[1]
    
    P = R_wave**2 * r**2
    norm = np.trapezoid(P, r)
    if norm > 0:
        P /= norm
        R_wave /= np.sqrt(norm)
    
    # Cumulative probability
    cum = np.zeros_like(r)
    for i in range(1, len(r)):
        cum[i] = np.trapezoid(P[:i+1], r[:i+1])
    if cum[-1] > 0:
        cum /= cum[-1]
    
    # Volume fraction f = (r/R)³
    f_vol = (r / R)**3
    
    # Peak
    peak_idx = np.argmax(P)
    r_peak = r[peak_idx]
    f_peak_prob = cum[peak_idx]          # probability fraction
    f_peak_vol = (r_peak / R)**3         # volume fraction
    
    # W and OE at peak
    w_peak = W_func(r_peak, R)
    oe_peak = 1 - w_peak
    
    # Nodes (zero crossings of R_wave, excluding origin)
    nodes = []
    for i in range(1, len(R_wave) - 1):
        if R_wave[i] * R_wave[i+1] < 0 and r[i] > 0.01 * R:
            rn = r[i] - R_wave[i] * (r[i+1] - r[i]) / (R_wave[i+1] - R_wave[i])
            fn_prob = np.interp(rn, r, cum)
            fn_vol = (rn / R)**3
            wn = W_func(rn, R)
            nodes.append({
                'r': rn, 'r_frac': rn/R,
                'f_prob': fn_prob, 'f_vol': fn_vol,
                'W': wn, 'OE': 1 - wn
            })
    
    return {
        'r_peak': r_peak, 'r_peak_frac': r_peak / R,
        'f_peak_prob': f_peak_prob, 'f_peak_vol': f_peak_vol,
        'w_peak': w_peak, 'oe_peak': oe_peak,
        'nodes': nodes,
        'r': r, 'P': P, 'R_wave': R_wave, 'cum': cum, 'f_vol': f_vol
    }

# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════

log("=" * 70)
log("CM KG in SPHERICAL JUG — Proton Interior")
log("=" * 70)

# Proton parameters
R_proton = 0.84  # fm
mu = 1.0  # natural units (mass scale)

# ═══════════════════════════════════════
# PART A: Test all W models
# ═══════════════════════════════════════
log("\n" + "=" * 70)
log("PART A: Different W(r) models inside proton")
log("=" * 70)

# Use R = 5 in natural units (arbitrary, relative positions matter)
R = 5.0

for model_name, W_func in W_MODELS.items():
    log(f"\n--- Model: {model_name} ---")
    log(f"  W(0) = {W_func(0, R):.4f}, W(R/2) = {W_func(R/2, R):.4f}, W(R) = {W_func(R, R):.4f}")
    
    for l in [0, 1, 2]:
        evs = find_jug_evs(R, l, W_func, mu, n_max=5)
        if not evs:
            log(f"  l={l}: no states")
            continue
        
        log(f"  l={l}: {len(evs)} states")
        for ni, ev in enumerate(evs):
            info = analyze_jug(ev, R, l, W_func, mu)
            if info is None:
                continue
            
            ns = ""
            for nd in info['nodes']:
                d13 = abs(nd['f_vol'] - 1./3.) / (1./3.) * 100
                d23 = abs(nd['f_vol'] - 2./3.) / (2./3.) * 100
                closest = "1/3" if d13 < d23 else "2/3"
                cdist = min(d13, d23)
                ns += f" NODE r/R={nd['r_frac']:.3f} f_vol={nd['f_vol']:.4f}({closest} {cdist:.0f}%)"
            
            d_peak_13 = abs(info['f_peak_vol'] - 1./3.) / (1./3.) * 100
            d_peak_23 = abs(info['f_peak_vol'] - 2./3.) / (2./3.) * 100
            
            log(f"    n={ni+1}: ω={ev:.4f} r_peak/R={info['r_peak_frac']:.3f} "
                f"f_vol={info['f_peak_vol']:.4f}(1/3:{d_peak_13:.0f}% 2/3:{d_peak_23:.0f}%) "
                f"OE@peak={info['oe_peak']:.3f}{ns}")

# ═══════════════════════════════════════
# PART B: Multiple R values (size scan)
# ═══════════════════════════════════════
log("\n" + "=" * 70)
log("PART B: Does jug SIZE matter? (f_vol should be size-independent)")
log("=" * 70)

W_func = W_CM_interior  # best physical model

for R in [2.0, 3.0, 5.0, 8.0, 10.0, 15.0, 20.0]:
    evs = find_jug_evs(R, 0, W_func, mu, n_max=3)
    if evs:
        info = analyze_jug(evs[0], R, 0, W_func, mu)
        if info:
            log(f"  R={R:<6.1f} ω₁={evs[0]:<8.4f} "
                f"r_peak/R={info['r_peak_frac']:.3f} "
                f"f_vol_peak={info['f_peak_vol']:.4f} "
                f"OE@peak={info['oe_peak']:.3f}")

# ═══════════════════════════════════════
# PART C: Key test — nodes at 1/3 and 2/3?
# ═══════════════════════════════════════
log("\n" + "=" * 70)
log("PART C: Do nodes fall at f = 1/3 and f = 2/3?")
log("=" * 70)
log("Target: f_vol = 1/3 = 0.3333 (d quark)")
log("Target: f_vol = 2/3 = 0.6667 (u quark)")
log("Target: f_vol = 1/2 = 0.5000 (neck)")

R = 5.0
W_func = W_CM_interior

for l in [0, 1, 2, 3]:
    evs = find_jug_evs(R, l, W_func, mu, n_max=6)
    if not evs:
        log(f"\n  l={l}: no states")
        continue
    
    log(f"\n  l={l}: {len(evs)} states")
    
    for ni, ev in enumerate(evs):
        info = analyze_jug(ev, R, l, W_func, mu)
        if info is None:
            continue
        
        # Peak volume fraction
        fv = info['f_peak_vol']
        d13 = abs(fv - 1./3.) / (1./3.) * 100
        d23 = abs(fv - 2./3.) / (2./3.) * 100
        d12 = abs(fv - 0.5) / 0.5 * 100
        
        peak_match = ""
        if d13 < 5: peak_match = " ← 1/3 MATCH!"
        elif d23 < 5: peak_match = " ← 2/3 MATCH!"
        elif d12 < 5: peak_match = " ← 1/2 MATCH!"
        
        log(f"    n={ni+1}: f_vol_peak={fv:.4f} "
            f"(1/3:{d13:.1f}% 2/3:{d23:.1f}% 1/2:{d12:.1f}%){peak_match}")
        
        # Check nodes
        for nd in info['nodes']:
            fv_n = nd['f_vol']
            d13n = abs(fv_n - 1./3.) / (1./3.) * 100
            d23n = abs(fv_n - 2./3.) / (2./3.) * 100
            d12n = abs(fv_n - 0.5) / 0.5 * 100
            
            node_match = ""
            if d13n < 5: node_match = " ← 1/3 NODE!"
            elif d23n < 5: node_match = " ← 2/3 NODE!"
            elif d12n < 5: node_match = " ← 1/2 NODE!"
            
            log(f"           node: f_vol={fv_n:.4f} r/R={nd['r_frac']:.3f} "
                f"OE={nd['OE']:.3f} "
                f"(1/3:{d13n:.1f}% 2/3:{d23n:.1f}% 1/2:{d12n:.1f}%){node_match}")

# ═══════════════════════════════════════
# PART D: Wavefunctions plot
# ═══════════════════════════════════════
log("\nGenerating plots...")

R = 5.0
W_func = W_CM_interior

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.patch.set_facecolor('#0a0a14')
fig.suptitle('KG Standing Waves in Proton Jug (CM Metric)',
             color='#f0c040', fontsize=15, fontweight='bold')

for idx, l in enumerate([0, 1, 2, 3]):
    ax = axes[idx // 2][idx % 2]
    ax.set_facecolor('#0f0f1a')
    
    evs = find_jug_evs(R, l, W_func, mu, n_max=4)
    
    colors = ['#f0c040', '#40e0d0', '#ff4060', '#80ff80']
    
    for ni, ev in enumerate(evs[:4]):
        info = analyze_jug(ev, R, l, W_func, mu)
        if info is None:
            continue
        
        r = info['r']
        P = info['P']
        f_vol = (r / R)**3
        
        ax.plot(f_vol, P / max(P), color=colors[ni], linewidth=2,
                label=f'n={ni+1} ω={ev:.2f}')
        
        # Mark nodes
        for nd in info['nodes']:
            ax.axvline(x=nd['f_vol'], color=colors[ni], alpha=0.3, linestyle=':')
    
    # Damru positions
    ax.axvline(x=1./3., color='white', linestyle='--', alpha=0.6)
    ax.axvline(x=2./3., color='white', linestyle='--', alpha=0.6)
    ax.axvline(x=0.5, color='yellow', linestyle=':', alpha=0.3)
    
    if idx == 0:
        ax.text(1./3. + 0.01, 0.9, 'd', color='white', fontsize=12)
        ax.text(2./3. + 0.01, 0.9, 'u', color='white', fontsize=12)
        ax.text(0.5 + 0.01, 0.9, 'neck', color='yellow', fontsize=9)
    
    ax.set_xlabel('f = (r/R)³ (volume fraction)', color='white', fontsize=11)
    ax.set_ylabel('|ψ|² (normalized)', color='white', fontsize=11)
    ax.set_title(f'l = {l}', color='#40e0d0', fontsize=13)
    ax.legend(fontsize=9, facecolor='#1a1a2e', edgecolor='#444', labelcolor='white')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.15)
    ax.set_xlim(0, 1)

plt.tight_layout()
fig.savefig(f'{OUTDIR}/jug_waves.png', dpi=150, bbox_inches='tight', facecolor='#0a0a14')
plt.close()

# Plot 2: W(r) models comparison
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('#0a0a14')
ax.set_facecolor('#0f0f1a')

r_plot = np.linspace(0, R, 200)
f_plot = (r_plot / R)**3

for name, W_func in W_MODELS.items():
    w_vals = [W_func(r, R) for r in r_plot]
    ax.plot(f_plot, w_vals, linewidth=2, label=name)

ax.axhline(y=0.25, color='white', linestyle='--', alpha=0.5)
ax.text(0.02, 0.27, 'W = 1/4 (confinement)', color='white', fontsize=10)
ax.axvline(x=1./3., color='white', linestyle=':', alpha=0.3)
ax.axvline(x=2./3., color='white', linestyle=':', alpha=0.3)

ax.set_xlabel('f = (r/R)³', color='white', fontsize=13)
ax.set_ylabel('W(r)', color='white', fontsize=13)
ax.set_title('W(r) Models Inside Proton', color='#f0c040', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, facecolor='#1a1a2e', edgecolor='#444', labelcolor='white')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.15)

fig.savefig(f'{OUTDIR}/jug_W_models.png', dpi=150, bbox_inches='tight', facecolor='#0a0a14')
plt.close()

# ═══════════════════════════════════════
# PART E: Summary
# ═══════════════════════════════════════
log("\n" + "=" * 70)
log("SUMMARY")
log("=" * 70)
log("Open-space KG (previous): wave free, peaks at f_prob = 1/3")
log("Jug KG (this test):       wave TRAPPED, nodes at f_vol = ???")
log("If nodes at 1/3 and 2/3 → standing wave creates BOTH quark positions")
log("=" * 70)
log("DONE!")
