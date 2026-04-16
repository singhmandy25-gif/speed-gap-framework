CLASS Installation Guide — For Reproducing Speed Gap V4 Results
The Speed Gap V4 paper uses the Cosmic Linear Anisotropy Solving System (CLASS) Boltzmann code to verify the CMB angular scale θ*, sound horizon r_s, matter power spectrum, and S_8. This document explains how to install CLASS correctly for bit-level reproducibility of the paper's results.
⚠ Why Exact Version Matters
Different CLASS versions can produce small differences (≤0.1%) in derived quantities like θ*. For bit-level reproducibility of the paper's results:
Paper uses: CLASS v3.3.4 (unmodified)
MD5 checksum of source/background.c: 5156074d51a98395741ac3cf6ff48175
The Speed Gap framework does not modify CLASS source code. All predictions emerge from changed input parameters only — this is required by the differential complementarity principle ΔA+ΔB=0 (derived in Singh 2026g).
Option A: Install via pip (fastest — works 90% of the time)
Bash
Note: On Windows, pip install often fails due to compilation dependencies. Use Option B or WSL (Windows Subsystem for Linux) instead.
Verify installation:
Bash
Expected output:
Code
Option B: Install from Source (most reliable)
This is the recommended method if pip install fails or if you want to verify source integrity.
Prerequisites
Linux or macOS (or Windows WSL)
C compiler (gcc or clang)
Python 3.8+
Make
Step 1: Clone the official repository
Bash
Step 2: Checkout the exact version
Bash
Step 3: Verify source integrity (optional but recommended)
Bash
Expected output:
Code
If the MD5 matches, you have the same source code the paper uses. If not, your checkout is different — use git checkout v3.3.4 again.
Step 4: Compile
Bash
This takes 1–2 minutes. Successful compilation ends with:
Code
Step 5: Install the Python wrapper
Bash
Step 6: Verify
Bash
Option C: Docker (if you hate dependency management)
A pre-built container with CLASS v3.3.4 and all Python dependencies:
Bash
(Note: This exact image may need to be rebuilt — check https://hub.docker.com/u/lesgourg for availability.)
Common Issues
Issue 1: ImportError: libclass.so: cannot open shared object
CLASS shared library not found. Solution:
Bash
Issue 2: classy compilation fails with gcc error
Usually missing C compiler. On Ubuntu:
Bash
On macOS:
Bash
Issue 3: Version mismatch — getting different θ*
If your 100×θ_s differs from the paper's 1.042082 by more than 0.001:
Check CLASS version: python -c "import classy; print(classy.__version__)"
Must be 3.3.4. If different, re-install specific version.
Verify MD5 of background.c.
Verifying Your Setup Is Correct
Run class_verification_v4.py and compare outputs with EXPECTED_OUTPUTS.txt.
All key values should match within:
θ_s:    ±0.0001
r_s:    ±0.05 Mpc
σ_8:    ±0.0001
S_8:    ±0.0001
If your values match, your installation reproduces the paper's results exactly.
Virtual Environment (Recommended)
For clean isolation:
Bash
References & Credits
CLASS official repo: https://github.com/lesgourg/class_public
CLASS paper: Blas, D., Lesgourgues, J., Tram, T. (2011). JCAP 07, 034. arXiv:1104.2933
CLASS documentation: https://github.com/lesgourg/class_public/wiki
CLASS is released under the MIT License and is not modified in the Speed Gap framework. All credit for the Boltzmann solver goes to its developers.
Why We Don't Bundle CLASS
CLASS source code is not included in this repository because:
CLASS is actively maintained — we want users to always get the latest bug fixes and improvements
License integrity — we respect CLASS's own licensing and attribution
Size — CLASS source + compiled binaries are ~50 MB
Platform differences — compiled binaries differ by OS/architecture
Instead, we provide:
Exact version number (v3.3.4)
MD5 checksum of source file
Expected outputs (see EXPECTED_OUTPUTS.txt)
Complete install instructions (this file)
This is standard practice for reproducible computational physics.
Contact
If you encounter installation issues, please:
Check your CLASS version: python -c "import classy; print(classy.__version__)"
Verify MD5 of background.c
Run class_verification_v4.py and compare with EXPECTED_OUTPUTS.txt
For framework-specific questions:
Email: singhmandy25@gmail.com
GitHub Issues: https://github.com/singhmandy25-gif/speed-gap-framework/issues
