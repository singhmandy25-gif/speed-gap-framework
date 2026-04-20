"""
baryon_meson_pattern.py — Singh 2026t, Chapter 4
Tests R = (4/3)π × λ_C (baryons) and R = e^(-3/4) × λ_C (mesons)
on all hadrons with measured charge radii.

Author: Mandeep Singh | ORCID: 0009-0003-7176-2395
"""

import numpy as np

hbar_c = 197.3269804  # MeV·fm
p = np.exp(-3/4)      # = 0.47237 (confinement transmission)
baryon_factor = (4/3) * np.pi  # = 4.18879
meson_factor = p               # = 0.47237

print("=" * 70)
print("  Singh 2026t Ch 4 — Baryon–Meson Pattern Verification")
print("=" * 70)

print(f"\n  Baryon factor: (4/3)π = {baryon_factor:.5f}")
print(f"  Meson factor:  e^(-3/4) = {meson_factor:.5f}")

# ═══ BARYONS ═══
print(f"\n  ═══ BARYONS: R = (4/3)π × λ_C ═══\n")
print(f"  {'Particle':<12} {'Quarks':<8} {'Mass MeV':<10} {'λ_C fm':<10} {'R_pred fm':<10} {'R_meas fm':<10} {'Error':<8} {'Pass?':<6}")
print(f"  {'─'*74}")

baryons = [
    ("Proton",    "uud",   938.272,  0.877,  "stable"),
    ("Neutron",   "udd",   939.565,  0.862,  "878 s"),
    ("Δ(1232)",   "uuu*",  1232.0,   0.84,   "5e-24 s"),
]

baryon_pass = 0
baryon_total = 0
for name, quarks, mass, R_meas, lifetime in baryons:
    lC = hbar_c / mass
    R_pred = baryon_factor * lC
    err = (R_pred / R_meas - 1) * 100
    passed = abs(err) < 5
    if passed: baryon_pass += 1
    baryon_total += 1
    mark = "✓" if passed else "✗"
    print(f"  {name:<12} {quarks:<8} {mass:<10.1f} {lC:<10.5f} {R_pred:<10.4f} {R_meas:<10.3f} {err:>+6.1f}%  {mark}")

# ═══ MESONS ═══
print(f"\n  ═══ MESONS: R = e^(-3/4) × λ_C ═══\n")
print(f"  {'Particle':<12} {'Quarks':<8} {'Mass MeV':<10} {'λ_C fm':<10} {'R_pred fm':<10} {'R_meas fm':<10} {'Error':<8} {'Pass?':<6}")
print(f"  {'─'*74}")

mesons = [
    ("π±",     "ud̄",   139.570,  0.659,  "2.6e-8 s"),
    ("K±",     "us̄",   493.677,  0.560,  "1.2e-8 s"),
    ("ρ(770)", "uū+dd̄",775.26,  0.75,   "4.5e-24 s"),
    ("J/ψ",    "cc̄",   3096.9,   0.25,   "7.1e-21 s"),
]

meson_pass = 0
meson_total = 0
for name, quarks, mass, R_meas, lifetime in mesons:
    lC = hbar_c / mass
    R_pred = meson_factor * lC
    err = (R_pred / R_meas - 1) * 100
    passed = abs(err) < 5
    if passed: meson_pass += 1
    meson_total += 1
    mark = "✓" if passed else "✗"
    print(f"  {name:<12} {quarks:<8} {mass:<10.1f} {lC:<10.5f} {R_pred:<10.4f} {R_meas:<10.3f} {err:>+6.1f}%  {mark}")

# ═══ R/λ_C LANDSCAPE ═══
print(f"\n  ═══ R/λ_C LANDSCAPE ═══\n")
print(f"  {'Particle':<12} {'R_meas/λ_C':<12} {'Closest to':<16} {'Distance':<12}")
print(f"  {'─'*52}")

all_particles = [
    ("Proton",    938.272,  0.877),
    ("Neutron",   939.565,  0.862),
    ("Δ(1232)",   1232.0,   0.84),
    ("π±",        139.570,  0.659),
    ("K±",        493.677,  0.560),
    ("ρ(770)",    775.26,   0.75),
    ("J/ψ",       3096.9,   0.25),
]

for name, mass, R_meas in all_particles:
    lC = hbar_c / mass
    ratio = R_meas / lC
    dist_baryon = abs(ratio - baryon_factor)
    dist_meson = abs(ratio - meson_factor)
    closest = "(4/3)π" if dist_baryon < dist_meson else "e^(-3/4)"
    dist = min(dist_baryon, dist_meson)
    print(f"  {name:<12} {ratio:<12.3f} {closest:<16} {dist:<12.3f}")

# ═══ REVERSE TEST ═══
print(f"\n  ═══ REVERSE TEST: Mass from Radius ═══\n")
print(f"  {'Particle':<10} {'R fm':<8} {'m(baryon) MeV':<14} {'m(meson) MeV':<14} {'m_actual MeV':<13} {'Best':<8}")
print(f"  {'─'*67}")

for name, mass, R_meas in [("Proton",938.272,0.877), ("Neutron",939.565,0.862),
                             ("Pion",139.570,0.659), ("Kaon",493.677,0.560)]:
    m_baryon = baryon_factor * hbar_c / R_meas
    m_meson = meson_factor * hbar_c / R_meas
    err_b = abs(m_baryon/mass - 1)
    err_m = abs(m_meson/mass - 1)
    best = "Baryon" if err_b < err_m else ("Meson" if err_m < 0.05 else "Neither")
    print(f"  {name:<10} {R_meas:<8.3f} {m_baryon:<14.1f} {m_meson:<14.1f} {mass:<13.1f} {best:<8}")

# ═══ PREDICTIONS ═══
print(f"\n  ═══ PREDICTIONS: Unmeasured Baryon Radii ═══\n")
print(f"  {'Baryon':<10} {'Quarks':<8} {'Mass MeV':<10} {'R_pred fm':<10} {'Lifetime':<14}")
print(f"  {'─'*52}")

predictions = [
    ("Λ",     "uds",  1115.68, "2.6e-10 s"),
    ("Σ⁺",    "uus",  1189.37, "8.0e-11 s"),
    ("Σ⁰",    "uds",  1192.64, "7.4e-20 s"),
    ("Ξ⁰",    "uss",  1314.86, "2.9e-10 s"),
    ("Ξ⁻",    "dss",  1321.71, "1.6e-10 s"),
    ("Ω⁻",    "sss",  1672.45, "8.2e-11 s"),
]

for name, quarks, mass, lifetime in predictions:
    lC = hbar_c / mass
    R_pred = baryon_factor * lC
    print(f"  {name:<10} {quarks:<8} {mass:<10.2f} {R_pred:<10.4f} {lifetime:<14}")

# ═══ SCORECARD ═══
total_pass = baryon_pass + meson_pass
total_test = baryon_total + meson_total

print(f"\n{'=' * 70}")
print(f"  SCORECARD")
print(f"{'=' * 70}")
print(f"""
  Baryons tested:  {baryon_pass}/{baryon_total} pass (stable nucleons ✓, resonance ✗)
  Mesons tested:   {meson_pass}/{meson_total} pass (pion ✓, others ✗)
  Total:           {total_pass}/{total_test} pass
  
  Pattern boundary:
    WORKS:  Stable + lightest + u,d quarks only
    FAILS:  Resonances, strange quarks, heavy quarks, spin-1
    
  Free parameters: ZERO
""")
