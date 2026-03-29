"""
Proton Pressure Distribution Check — Singh 2026d Verification
=============================================================
Computes pressure distribution from Burkert et al. (Nature 2018) D-term
parametrization and compares with Damru Geometry predicted Neck position.

Result: Maximum confining pressure at r = 0.641 fm
        Damru Neck prediction at r = 0.667 fm
        Match: 3.9% — independent verification.

Ref: Burkert, Elouadrhiri, Girod. Nature 557, 396 (2018)

Author: Mandeep Singh (singhmandy25@gmail.com)
Paper:  Singh 2026d — Damru Geometry
"""

import numpy as np
from scipy.integrate import quad
from scipy.interpolate import UnivariateSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Physical constants
HBARC = 0.197327
M_PROTON = 0.938272
R_PROTON = 0.84

# Burkert D-term parameters (tripole fit to DVCS data)
D1 = -1.47          # dimensionless
MD2 = 1.39           # GeV² (mass parameter squared)

# Damru predictions
R_DOWN = 0.582
R_NECK = 0.667
R_UP   = 0.734


def D_tripole(Q2):
    """Tripole D-term form factor.
    D(t) = d₁ / (1 + Q²/M_D²)³ where t = -Q²
    Parameters from Burkert et al. (2018) DVCS fit.
    """
    return D1 / (1 + Q2 / MD2)**3


def D_tilde(r_fm, qmax=40.0):
    """Fourier transform of D-term to position space.
    D̃(r) = 1/(2π²) ∫₀^∞ q² D(-q²) sin(qr)/(qr) dq
    """
    if r_fm < 1e-10:
        def integrand(q):
            return q**2 * D_tripole((q * HBARC)**2)
        result, _ = quad(integrand, 0, qmax, limit=300)
    else:
        def integrand(q):
            return q**2 * D_tripole((q * HBARC)**2) * np.sin(q * r_fm) / (q * r_fm)
        result, _ = quad(integrand, 0, qmax, limit=300)
    return result / (2 * np.pi**2)


def main():
    print("Computing D-tilde(r) and pressure distribution...")
    r = np.linspace(0.01, 2.0, 600)
    Dt = np.array([D_tilde(ri) for ri in r])
    
    # Pressure via derivatives of D-tilde
    # p(r) = (1/6Mp) × [d²D̃/dr² + (2/r) dD̃/dr]
    spl = UnivariateSpline(r, Dt, s=0)
    dDt = spl.derivative()(r)
    d2Dt = spl.derivative(n=2)(r)
    pressure = (1.0 / (6.0 * M_PROTON)) * (d2Dt + 2.0 * dDt / r)
    
    # Find zero crossing
    sign_changes = np.where(np.diff(np.sign(pressure)))[0]
    r_zero = None
    if len(sign_changes) > 0:
        i = sign_changes[0]
        r_zero = r[i] - pressure[i] * (r[i+1] - r[i]) / (pressure[i+1] - pressure[i])
    
    # Find maximum confinement (most negative pressure)
    min_idx = np.argmin(pressure)
    r_max_conf = r[min_idx]
    
    # Print results
    print(f"\nPressure zero crossing:     r = {r_zero:.4f} fm")
    print(f"Maximum confinement:        r = {r_max_conf:.4f} fm")
    print(f"Damru Neck prediction:      r = {R_NECK:.3f} fm")
    print(f"Match: {abs(r_max_conf - R_NECK)/R_NECK*100:.1f}%")
    
    print(f"\nPressure at Damru positions:")
    for name, ri in [("d-quark", R_DOWN), ("Neck", R_NECK), ("u-quark", R_UP)]:
        idx = np.argmin(np.abs(r - ri))
        zone = "ATTRACTIVE (confining)" if pressure[idx] < 0 else "REPULSIVE"
        print(f"  {name} ({ri} fm): p = {pressure[idx]:.4f} GeV/fm³ — {zone}")
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    r2p = r**2 * pressure
    
    ax.fill_between(r, r2p, 0, where=(r2p > 0), color='#e84040', alpha=0.15, label='Repulsive')
    ax.fill_between(r, r2p, 0, where=(r2p < 0), color='#4a9eff', alpha=0.15, label='Attractive (confining)')
    ax.plot(r, r2p, 'k-', linewidth=2.5)
    ax.axhline(0, color='gray', linewidth=0.5)
    
    for ri, label, color in [(R_DOWN, f'd-quark ({R_DOWN})', '#e84040'),
                              (R_NECK, f'Neck ({R_NECK})', '#c9a84c'),
                              (R_UP, f'u-quark ({R_UP})', '#2e7d32')]:
        ax.axvline(ri, color=color, linestyle='--', alpha=0.8, linewidth=2, label=f'Damru: {label} fm')
    
    ax.plot(r_max_conf, r[min_idx]**2 * pressure[min_idx], 'k*', markersize=12)
    ax.annotate(f'Max confinement\n{r_max_conf:.3f} fm', 
                (r_max_conf, r[min_idx]**2 * pressure[min_idx]), fontsize=9, fontweight='bold')
    
    ax.set_xlabel('r (fm)', fontsize=12)
    ax.set_ylabel('r² × p(r) (GeV/fm)', fontsize=12)
    ax.set_title('Proton Pressure Distribution (Burkert 2018) + Damru Predictions\n'
                 f'Max confinement ({r_max_conf:.3f} fm) vs Neck ({R_NECK} fm) = {abs(r_max_conf-R_NECK)/R_NECK*100:.1f}% match',
                 fontsize=13)
    ax.legend(fontsize=9)
    ax.set_xlim(0, 1.5)
    ax.grid(True, alpha=0.3)
    
    plt.savefig('pressure_distribution.png', dpi=150, bbox_inches='tight')
    print("\nSaved: pressure_distribution.png")


if __name__ == '__main__':
    main()
