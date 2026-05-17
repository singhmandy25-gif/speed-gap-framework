#!/usr/bin/env python3
"""
CM Formula: E = ½mec²(W⁻¹/³ − 1)
Reproduces Table 7.1 of Singh 2026z
Compare: Coulomb vs CM vs Dirac vs NIST measured
"""
import numpy as np

alpha = 1/137.036
mc2 = 511099  # eV

# NIST measured 1s binding energies (eV)
nist = {
    1:13.598, 2:54.418, 3:122.454, 4:217.713, 5:340.226, 6:489.993,
    7:667.046, 8:871.410, 9:1103.117, 10:1362.199,
    11:1648.702, 12:1962.665, 13:2304.141, 14:2673.182, 15:3069.842,
    16:3494.189, 17:3946.296, 18:4426.233,
    20:5469.864, 22:6625.82, 24:7894.81, 26:9277.69,
    28:10775.40, 29:11567.61, 30:12388.93,
    33:15028.44, 36:17936.21,
    42:24465.6, 47:30312.5,
    54:40271.0, 74:79296.0, 79:93460.0, 82:101137.0, 92:131810.0
}

names = {1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",
    9:"F",10:"Ne",11:"Na",12:"Mg",13:"Al",14:"Si",15:"P",
    16:"S",17:"Cl",18:"Ar",20:"Ca",22:"Ti",24:"Cr",26:"Fe",
    28:"Ni",29:"Cu",30:"Zn",33:"As",36:"Kr",
    42:"Mo",47:"Ag",54:"Xe",74:"W",79:"Au",82:"Pb",92:"U"}

def E_coulomb(Z):
    """Bohr formula: E = ½mc²(Zα)²"""
    return 0.5 * mc2 * (Z*alpha)**2

def E_cm(Z):
    """CM formula: E = ½mc²(W⁻¹/³ − 1), W = (1−β²)/(1+2β²)"""
    beta2 = (Z*alpha)**2
    W = (1 - beta2) / (1 + 2*beta2)
    return 0.5 * mc2 * (W**(-1/3) - 1)

def E_dirac(Z):
    """Dirac analytical: E = mc²(1 − √(1−(Zα)²))"""
    return mc2 * (1 - np.sqrt(1 - (Z*alpha)**2))

if __name__ == "__main__":
    print("="*85)
    print("CM FORMULA VERIFICATION — Singh 2026z, Table 7.1")
    print("E = ½mec²(W⁻¹/³ − 1), W = (1−β²)/(1+2β²), β = Zα")
    print("="*85)
    print(f"\n{'Z':>3} {'El':>3} {'NIST':>10} {'Coul':>10} {'CM':>10} {'Dirac':>10} {'Coul%':>8} {'CM%':>8} {'Dir%':>8}")
    print("-"*75)

    cm_beats_c = 0; cm_beats_d = 0
    err_c = []; err_cm = []; err_d = []

    for Z in sorted(nist.keys()):
        Em = nist[Z]
        Ec, Ecm, Ed = E_coulomb(Z), E_cm(Z), E_dirac(Z)
        ec = (Ec-Em)/Em*100; ecm = (Ecm-Em)/Em*100; ed = (Ed-Em)/Em*100
        err_c.append(abs(ec)); err_cm.append(abs(ecm)); err_d.append(abs(ed))
        if abs(ecm) < abs(ec): cm_beats_c += 1
        if abs(ecm) < abs(ed): cm_beats_d += 1
        best = "★" if abs(ecm)<abs(ec) and abs(ecm)<abs(ed) else ""
        print(f"{Z:3d} {names[Z]:>3} {Em:10.1f} {Ec:10.1f} {Ecm:10.1f} {Ed:10.1f} {ec:+7.2f}% {ecm:+7.2f}% {ed:+7.2f}% {best}")

    N = len(nist)
    print(f"\n--- SCORECARD ({N} ions) ---")
    print(f"  CM beats Coulomb:  {cm_beats_c}/{N}")
    print(f"  CM beats Dirac:    {cm_beats_d}/{N}")
    print(f"  Average |error|:   Coul {np.mean(err_c):.3f}%  CM {np.mean(err_cm):.3f}%  Dirac {np.mean(err_d):.3f}%")

    heavy = [Z for Z in nist if Z > 40]
    hc_e = [abs((E_coulomb(Z)-nist[Z])/nist[Z]*100) for Z in heavy]
    hcm_e = [abs((E_cm(Z)-nist[Z])/nist[Z]*100) for Z in heavy]
    hd_e = [abs((E_dirac(Z)-nist[Z])/nist[Z]*100) for Z in heavy]
    print(f"  Heavy (Z>40) avg:  Coul {np.mean(hc_e):.3f}%  CM {np.mean(hcm_e):.3f}%  Dirac {np.mean(hd_e):.3f}%")
    print(f"  Uranium:           Coul {err_c[-1]:.2f}%  CM {err_cm[-1]:.2f}%  Dirac {err_d[-1]:.2f}%")
