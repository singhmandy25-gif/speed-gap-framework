"""
Cornell Potential Wavefunction Check — Singh 2026d Verification
===============================================================
Solves radial Schrödinger equation with Cornell potential:
  V(r) = -4αs/(3r) + σ·r

Checks where the ground state radial probability r²|ψ|² peaks
and compares with Damru Geometry Neck position (0.667 fm).

Result: Ground state peak at r = 0.696 fm vs Neck = 0.667 fm → 4.3% match
        Excited state node at r = 0.618 fm vs d-quark = 0.582 fm → 6.2% match

Note: Uses non-relativistic Schrödinger equation with constituent
quark mass. A full relativistic treatment (Dirac equation) would
be more rigorous but qualitative conclusions are expected to hold.

Author: Mandeep Singh (singhmandy25@gmail.com)
Paper:  Singh 2026d — Damru Geometry
"""

import numpy as np
from scipy.linalg import eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Physical constants
HBARC = 0.197327  # GeV·fm

# Standard QCD parameters
ALPHA_S = 0.39     # strong coupling at ~1 GeV scale
SIGMA = 0.18       # string tension (GeV²)
M_Q = 0.336        # constituent quark mass (GeV) ≈ M_proton/3

# Damru predictions
R_DOWN = 0.582     # fm (f = 1/3)
R_NECK = 0.667     # fm (f = 1/2)
R_UP   = 0.734     # fm (f = 2/3)


def solve_cornell(alpha_s, sigma, m_q, l=0, Nr=500, r_max=3.0, n_states=5):
    """Solve radial Schrödinger with Cornell potential using matrix method.
    
    V(r) = -(4/3) × αs × ℏc / r + (σ/ℏc) × r
    
    Returns: r (array), eigenvalues (array), eigenvectors (matrix)
    """
    dr = r_max / Nr
    r = np.linspace(dr, r_max, Nr)
    
    # Cornell potential in GeV
    V = -(4/3) * alpha_s * HBARC / r + (sigma / HBARC) * r
    if l > 0:
        V += l * (l + 1) * HBARC**2 / (2 * m_q * r**2)
    
    # Hamiltonian matrix (three-point stencil for kinetic energy)
    T_coeff = HBARC**2 / (2 * m_q * dr**2)
    H = np.zeros((Nr, Nr))
    for i in range(Nr):
        H[i, i] = 2 * T_coeff + V[i]
        if i > 0:
            H[i, i-1] = -T_coeff
        if i < Nr - 1:
            H[i, i+1] = -T_coeff
    
    eigenvalues, eigenvectors = eigh(H, subset_by_index=[0, n_states - 1])
    return r, eigenvalues, eigenvectors


def find_peak(r, psi):
    """Find peak of r²|ψ|² (radial probability density)."""
    r2psi2 = r**2 * psi**2
    peak_idx = np.argmax(r2psi2)
    return r[peak_idx]


def find_nodes(r, psi):
    """Find zero crossings of wavefunction."""
    sign_changes = np.where(np.diff(np.sign(psi)))[0]
    return [r[i] for i in sign_changes]


def main():
    print("Solving Cornell potential (matrix method)...")
    r, E_vals, psi_all = solve_cornell(ALPHA_S, SIGMA, M_Q)
    
    # Ground state
    psi0 = psi_all[:, 0]
    r_peak = find_peak(r, psi0)
    
    # First excited state
    psi1 = psi_all[:, 1]
    nodes_1 = find_nodes(r, psi1)
    
    print(f"\nEnergy eigenvalues:")
    for i, E in enumerate(E_vals):
        print(f"  E_{i} = {E:.4f} GeV")
    
    print(f"\nGround state peak: r = {r_peak:.3f} fm")
    print(f"Damru Neck:        r = {R_NECK} fm")
    print(f"Match: {abs(r_peak - R_NECK)/R_NECK*100:.1f}%")
    
    if nodes_1:
        print(f"\nFirst excited node: r = {nodes_1[0]:.3f} fm")
        print(f"Damru d-quark:      r = {R_DOWN} fm")
        print(f"Match: {abs(nodes_1[0] - R_DOWN)/R_DOWN*100:.1f}%")
    
    # Parameter sensitivity scan
    print(f"\n{'='*65}")
    print(f"PARAMETER SCAN")
    print(f"{'='*65}")
    print(f"{'αs':>6} {'σ':>8} {'m_q':>8} {'r_peak':>10} {'node(E₁)':>10}")
    print(f"{'-'*65}")
    
    params = [
        (0.30, 0.18, 0.336, "low αs"),
        (0.39, 0.18, 0.336, "STANDARD"),
        (0.50, 0.18, 0.336, "high αs"),
        (0.39, 0.12, 0.336, "low σ"),
        (0.39, 0.25, 0.336, "high σ"),
        (0.39, 0.18, 0.220, "light quark"),
        (0.39, 0.18, 0.500, "heavy quark"),
    ]
    
    for a, s, m, label in params:
        r2, E2, psi2 = solve_cornell(a, s, m)
        pk = find_peak(r2, psi2[:, 0])
        nd = find_nodes(r2, psi2[:, 1])
        nd_str = f"{nd[0]:.3f}" if nd else "—"
        print(f"{a:>6.2f} {s:>8.2f} {m:>8.3f} {pk:>10.3f} {nd_str:>10}  {label}")
    
    print(f"\nDamru zone: {R_DOWN}–{R_UP} fm")
    
    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(11, 10), gridspec_kw={'hspace': 0.3})
    
    # Panel A: Ground state
    ax = axes[0]
    r2psi2 = r**2 * psi0**2
    r2psi2 = r2psi2 / np.max(r2psi2)
    ax.plot(r, r2psi2, 'b-', linewidth=2.5, label=f'Ground state r²|ψ₀|² (peak = {r_peak:.3f} fm)')
    ax.fill_between(r, r2psi2, alpha=0.1, color='blue')
    
    for ri, label, color in [(R_DOWN, f'd: {R_DOWN}', '#e84040'), 
                              (R_NECK, f'Neck: {R_NECK}', '#c9a84c'),
                              (R_UP, f'u: {R_UP}', '#2e7d32')]:
        ax.axvline(ri, color=color, linestyle='--', linewidth=2, alpha=0.8, label=f'Damru {label} fm')
    
    ax.plot(r_peak, 1.0, 'b*', markersize=15)
    ax.set_xlabel('r (fm)', fontsize=11)
    ax.set_ylabel('r²|ψ(r)|²', fontsize=11)
    ax.set_title(f'Ground State — Cornell Potential (αs={ALPHA_S}, σ={SIGMA}, m_q={M_Q} GeV)', fontsize=12)
    ax.legend(fontsize=9)
    ax.set_xlim(0, 2.5)
    ax.grid(True, alpha=0.3)
    
    # Panel B: Excited state
    ax = axes[1]
    psi1_n = psi1 / np.max(np.abs(psi1))
    ax.plot(r, psi1_n, 'r-', linewidth=2.5, label='First excited ψ₁(r)')
    ax.axhline(0, color='gray', linewidth=0.5)
    
    for ri, label, color in [(R_DOWN, f'd: {R_DOWN}', '#e84040'),
                              (R_NECK, f'Neck: {R_NECK}', '#c9a84c'),
                              (R_UP, f'u: {R_UP}', '#2e7d32')]:
        ax.axvline(ri, color=color, linestyle='--', linewidth=2, alpha=0.8, label=f'Damru {label} fm')
    
    if nodes_1:
        ax.axvline(nodes_1[0], color='black', linestyle=':', linewidth=2)
        ax.annotate(f'Node = {nodes_1[0]:.3f} fm', (nodes_1[0], -0.5),
                    ha='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('r (fm)', fontsize=11)
    ax.set_ylabel('ψ₁(r)', fontsize=11)
    ax.set_title('First Excited State — Where is the Node?', fontsize=12)
    ax.legend(fontsize=9)
    ax.set_xlim(0, 2.5)
    ax.grid(True, alpha=0.3)
    
    plt.savefig('cornell_wavefunction.png', dpi=150, bbox_inches='tight')
    print("\nSaved: cornell_wavefunction.png")


if __name__ == '__main__':
    main()
