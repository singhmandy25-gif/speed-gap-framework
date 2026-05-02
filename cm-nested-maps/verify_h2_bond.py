"""Chapter 6: H₂ bond = √2 × a₀ = 74.8 pm (0.9%)"""
import numpy as np
a0 = 52.9177
R_pred = np.sqrt(2) * a0
R_meas = 74.14
err = abs(R_pred-R_meas)/R_meas*100
print(f"Predicted: √2 × {a0} = {R_pred:.2f} pm")
print(f"Measured: {R_meas} pm")
print(f"Error: {err:.1f}%")
print(f"{'PASS' if err < 1.5 else 'FAIL'}")
