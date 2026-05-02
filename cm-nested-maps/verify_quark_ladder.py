"""Chapter 7B: e→u→d→s step-by-step + ratio m_s/m_d = e³"""
import numpy as np
me = 0.51099895; n43pi = (4/3)*np.pi; e34 = np.exp(3/4)
pdg = {'u':2.16, 'd':4.67, 's':93.4}

m_u = me * n43pi
m_d = m_u * e34
print("Step-by-step:")
print(f"  m_u = me×(4/3)π = {m_u:.2f} MeV (PDG {pdg['u']}, err {abs(m_u-pdg['u'])/pdg['u']*100:.1f}%)")
print(f"  m_d = m_u×e^(3/4) = {m_d:.2f} MeV (PDG {pdg['d']}, err {abs(m_d-pdg['d'])/pdg['d']*100:.1f}%)")

ratio = pdg['s']/pdg['d']
print(f"\nRatio test (genuine result):")
print(f"  m_s/m_d = {ratio:.2f}")
print(f"  e³ = {np.exp(3):.2f}")
print(f"  Error = {abs(ratio-np.exp(3))/np.exp(3)*100:.1f}%")

print(f"\nWith PDG m_d: m_s = {pdg['d']*np.exp(3):.1f} (err {abs(pdg['d']*np.exp(3)-93.4)/93.4*100:.1f}%)")
print(f"With pred m_d: m_s = {m_d*np.exp(3):.1f} (err {abs(m_d*np.exp(3)-93.4)/93.4*100:.1f}%)")
