"""Chapter 4: Double slit 5 tests — OE+W=1, dark=0, bright=4x, energy, bounds"""
import numpy as np
lam=500e-9; d=0.1e-3; L=1.0; k=2*np.pi/lam
y = np.linspace(-5e-3, 5e-3, 100000)
I0 = 1.0
I = 4*I0*np.cos(k*d*y/(2*L))**2
OE = I/I.max(); W = 1-OE

t1 = np.max(np.abs(OE+W-1)) < 1e-14
dark_idx = np.argmin(np.abs(y - lam*L/(2*d)))
t2 = OE[dark_idx] < 1e-6
t3 = abs(I.max()/I0 - 4) < 0.001
t4 = abs(np.trapezoid(I,y)/(2*np.trapezoid(np.ones_like(y)*I0,y))*100 - 100) < 0.01
t5 = OE.min() >= 0 and OE.max() <= 1.0001

tests = [("OE+W=1",t1),("dark=0",t2),("bright=4x",t3),("energy",t4),("bounds",t5)]
for name,t in tests:
    print(f"  {name}: {'PASS' if t else 'FAIL'}")
print(f"\n{sum(t for _,t in tests)}/5 PASS")
