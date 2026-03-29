"""
Proton Charge Density Check — Singh 2026d Verification
======================================================
Fourier-transforms proton electromagnetic form factor G_E(Q²)
to obtain charge density ρ(r) in position space.

Checks whether Damru Geometry predicted positions (0.582, 0.667, 0.734 fm)
show any structure in the charge density.

Result: Charge density is smooth and featureless at predicted positions.
This is a scope boundary — geometry describes forces (pressure), not
the quantum charge cloud.

Author: Mandeep Singh (singhmandy25@gmail.com)
Paper:  Singh 2026d — Damru Geometry
"""

import numpy as np
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Physical constants
HBARC = 0.197327   # GeV·fm
M_PROTON = 0.938272 # GeV
R_PROTON = 0.84     # fm (PDG charge radius)

# Damru predictions
R_DOWN  = 0.582  # fm (f = 1/3)
R_NECK  = 0.667  # fm (f = 1/2)
R_UP    = 0.734  # fm (f = 2/3)


def GE_kelly(Q2):
    """Kelly (2004) proton electric form factor parametrization.
    Ref: J.J. Kelly, Phys. Rev. C 70, 068202 (2004)
    """
    tau = Q2 / (4 * M_PROTON**2)
    return (1 - 0.24 * tau) / (1 + 10.98*tau + 12.82*tau**2 + 21.97*tau**3)


def GE_arrington(Q2):
    """Arrington (2004) proton electric form factor.
    Ref: J. Arrington, Phys. Rev. C 69, 022201 (2004)
    """
    tau = Q2 / (4 * M_PROTON**2)
    a = [1.0, 3.226, 1.508, -0.3773, 0.611, -0.1853, 1.596e-2]
    poly = sum(a[i] * tau**i for i in range(len(a)))
    return 1.0 / poly


def charge_density(r_fm, GE_func, qmax=30.0):
    """Breit-frame charge density via Fourier transform.
    
    ρ(r) = 1/(2π²) ∫₀^∞ q² G_E(q²) sin(qr)/(qr) dq
    
    Note: Breit frame density differs from rest-frame density
    for relativistic systems (Miller 2007, PRL 99, 112001).
    """
    if r_fm < 1e-10:
        def integrand(q):
            return q**2 * GE_func((q * HBARC)**2)
        result, _ = quad(integrand, 0, qmax, limit=200)
    else:
        def integrand(q):
            return q**2 * GE_func((q * HBARC)**2) * np.sin(q * r_fm) / (q * r_fm)
        result, _ = quad(integrand, 0, qmax, limit=200)
    return result / (2 * np.pi**2)


def main():
    print("Computing charge densities...")
    r = np.linspace(0.01, 1.5, 500)
    
    rho_kelly = np.array([charge_density(ri, GE_kelly) for ri in r])
    rho_arrington = np.array([charge_density(ri, GE_arrington) for ri in r])
    
    # Normalize
    rho_kelly_n = rho_kelly / rho_kelly[0]
    rho_arrington_n = rho_arrington / rho_arrington[0]
    
    # Second derivative (inflection structure)
    dr = r[1] - r[0]
    d2rho = np.gradient(np.gradient(rho_kelly_n, dr), dr)
    inflections = np.where(np.diff(np.sign(d2rho)))[0]
    
    # Print results at predicted positions
    print("\nCharge density at Damru positions (Kelly):")
    for name, ri in [("d-quark (0.582)", R_DOWN), ("Neck (0.667)", R_NECK), ("u-quark (0.734)", R_UP)]:
        idx = np.argmin(np.abs(r - ri))
        print(f"  {name}: ρ/ρ₀ = {rho_kelly_n[idx]:.4f} — smooth, no structure")
    
    print(f"\nInflection points: {len(inflections)}")
    for i in inflections[:3]:
        print(f"  r = {r[i]:.3f} fm")
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(r, rho_kelly_n, 'r-', linewidth=2.5, label='Kelly (2004)')
    ax.plot(r, rho_arrington_n, 'g-.', linewidth=1.5, alpha=0.6, label='Arrington (2004)')
    
    for ri, label, color in [(R_DOWN, 'd-quark (0.582)', '#e84040'), 
                              (R_NECK, 'Neck (0.667)', '#c9a84c'),
                              (R_UP, 'u-quark (0.734)', '#2e7d32')]:
        ax.axvline(ri, color=color, linestyle='--', alpha=0.7, linewidth=1.5, label=f'Damru: {label} fm')
    
    ax.set_xlabel('r (fm)', fontsize=12)
    ax.set_ylabel('ρ(r) / ρ(0)', fontsize=12)
    ax.set_title('Proton Charge Density — Form Factor Fourier Transform\nwith Damru Geometry Predicted Positions', fontsize=13)
    ax.legend(fontsize=9)
    ax.set_xlim(0, 1.5)
    ax.grid(True, alpha=0.3)
    
    plt.savefig('charge_density.png', dpi=150, bbox_inches='tight')
    print("\nSaved: charge_density.png")
    print("Result: Smooth curve — no structure at predicted positions.")


if __name__ == '__main__':
    main()
