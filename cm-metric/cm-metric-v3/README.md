# CM Metric V3 — Verification Scripts

**Paper:** Singh 2026j V3, DOI: 10.5281/zenodo.20134529  
**Date:** 12 May 2026

## Scripts

| Script | What it verifies |
|---|---|
| `verify_shadow_v3.py` | Shadow +10%, M87*/SgrA* comparison |
| `verify_isco_v3.py` | ISCO radius, frequency, binding energy |
| `verify_qpo_v3.py` | QPO mass estimates, 4 X-ray binaries |
| `verify_spin_v3.py` | Spin β² method, rotation comparison |

## Requirements
```
python3, numpy, scipy
```

## Run
```bash
python3 verify_shadow_v3.py
python3 verify_isco_v3.py
python3 verify_qpo_v3.py
python3 verify_spin_v3.py
```

## Key Results (V3 new findings)
- CM ISCO frequency (1819/M Hz) matches QPOs within 3-37%
- Kerr ISCO frequency overshoots by 17-232% (spin amplification)
- CM ISCO nearly spin-independent (±2%) vs Kerr (5.4× variation)
- GRO J1655-40: CM 3% off vs GR 148% off (best result)
