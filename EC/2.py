## Note this code has been inserted into '2+3.ipynb'

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import os

# Create output directory
os.makedirs('p1', exist_ok=True)

# Define the longitudinal and lateral matrices 
Alon = np.array([
    [-0.1589, -8.9574, 0.0000, -9.8067],
    [-0.0091, -0.6650, 0.9708, 0.0000],
    [-0.0803, -10.7564, -3.6285, 0.0000],
    [0.0000, 0.0000, 1.0000, 0.0000]
])

Alat = np.array([
    [-0.1011, -0.0014, -0.9919, 0.2118],
    [-11.9041, -7.4078, 1.5131, 0.0000],
    [4.1901, -0.2279, -0.7520, 0.0000],
    [0.0000, 1.0000, 0.0000, 0.0000]
])

# Trim state
v_trim = 42.0  # m/s
alpha_trim = 0.0  # rad
q_trim = 0.0  # rad/s
theta_trim = 0.0  # rad
beta_trim = 0.0  # rad
p_trim = 0.0  # rad/s
r_trim = 0.0  # rad/s
phi_trim = 0.0  # rad

print("\n" + "=" * 80)
print("PART 1: EIGENVALUE AND EIGENVECTOR ANALYSIS")
print("=" * 80)

# Longitudinal analysis
print("\n" + "-" * 60)
print("LONGITUDINAL DYNAMICS (Pitch Plane)")
print("-" * 60)

# Compute eigenvalues and eigenvectors for longitudinal system
eigenvalues_lon, eigenvectors_lon = np.linalg.eig(Alon)

print("\nEigenvalues:")
for i, eig in enumerate(eigenvalues_lon):
    print(f"  λ{i+1} = {eig.real:.6f} + {eig.imag:.6f}j")
    print(f"       Magnitude: {np.abs(eig):.6f} rad/s")
    if np.abs(eig.imag) > 1e-6:
        damping = -eig.real / np.abs(eig)
        print(f"       Damping ratio: {damping:.6f}")
    print()

# Identify the modes
print("\nMode Identification:")
print("  Mode 1 & 2: Typically represent the Short Period mode (fast, well-damped)")
print("  Mode 3 & 4: Typically represent the Phugoid mode (slow, lightly damped)")

# Sort eigenvalues by magnitude to identify modes
sorted_indices_lon = np.argsort(np.abs(eigenvalues_lon))
print("\nSorted eigenvalues by magnitude:")
for idx in sorted_indices_lon:
    eig = eigenvalues_lon[idx]
    if np.abs(eig.imag) > 1e-6:
        print(f"  λ = {eig.real:.6f} ± {eig.imag:.6f}i, |λ| = {np.abs(eig):.6f} rad/s")
    else:
        print(f"  λ = {eig.real:.6f}, |λ| = {np.abs(eig):.6f} rad/s")

# Display eigenvectors
print("\nEigenvectors (columns correspond to eigenvalues in order):")
print("States: [δv, δα, δq, δθ]")
for i in range(4):
    print(f"\nEigenvector for λ{i+1} = {eigenvalues_lon[i].real:.6f} + {eigenvalues_lon[i].imag:.6f}j:")
    vec = eigenvectors_lon[:, i]
    print(f"  δv:  {vec[0].real:.6f} + {vec[0].imag:.6f}j")
    print(f"  δα:  {vec[1].real:.6f} + {vec[1].imag:.6f}j")
    print(f"  δq:  {vec[2].real:.6f} + {vec[2].imag:.6f}j")
    print(f"  δθ:  {vec[3].real:.6f} + {vec[3].imag:.6f}j")

# Lateral analysis
print("\n" + "-" * 60)
print("LATERAL-DIRECTIONAL DYNAMICS (Roll/Yaw Plane)")
print("-" * 60)

# Compute eigenvalues and eigenvectors for lateral system
eigenvalues_lat, eigenvectors_lat = np.linalg.eig(Alat)

print("\nEigenvalues:")
for i, eig in enumerate(eigenvalues_lat):
    print(f"  λ{i+1} = {eig.real:.6f} + {eig.imag:.6f}j")
    print(f"       Magnitude: {np.abs(eig):.6f} rad/s")
    if np.abs(eig.imag) > 1e-6:
        damping = -eig.real / np.abs(eig)
        print(f"       Damping ratio: {damping:.6f}")

    print()

# Identify the modes
print("\nMode Identification:")
print("  Mode 1: Typically represents the Roll mode (real, fast)")
print("  Mode 2 & 3: Typically represent the Dutch Roll mode (oscillatory)")
print("  Mode 4: Typically represents the Spiral mode (real, slow)")

# Sort eigenvalues by magnitude to identify modes
sorted_indices_lat = np.argsort(np.abs(eigenvalues_lat))
print("\nSorted eigenvalues by magnitude:")
for idx in sorted_indices_lat:
    eig = eigenvalues_lat[idx]
    if np.abs(eig.imag) > 1e-6:
        print(f"  λ = {eig.real:.6f} ± {eig.imag:.6f}i, |λ| = {np.abs(eig):.6f} rad/s")
    else:
        print(f"  λ = {eig.real:.6f}, |λ| = {np.abs(eig):.6f} rad/s")

# Display eigenvectors
print("\nEigenvectors (columns correspond to eigenvalues in order):")
print("States: [δβ, δp, δr, δφ]")
for i in range(4):
    print(f"\nEigenvector for λ{i+1} = {eigenvalues_lat[i].real:.6f} + {eigenvalues_lat[i].imag:.6f}j:")
    vec = eigenvectors_lat[:, i]
    print(f"  δβ:  {vec[0].real:.6f} + {vec[0].imag:.6f}j")
    print(f"  δp:  {vec[1].real:.6f} + {vec[1].imag:.6f}j")
    print(f"  δr:  {vec[2].real:.6f} + {vec[2].imag:.6f}j")
    print(f"  δφ:  {vec[3].real:.6f} + {vec[3].imag:.6f}j")

# =============================================================================
# SAVE EIGENVALUE / EIGENVECTOR RESULTS
# =============================================================================

output_file = 'p2/eigen_analysis.txt'

with open(output_file, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("EIGENVALUE AND EIGENVECTOR ANALYSIS\n")
    f.write("=" * 80 + "\n\n")

    # ---------------- LONGITUDINAL ----------------
    f.write("-" * 60 + "\n")
    f.write("LONGITUDINAL DYNAMICS (Pitch Plane)\n")
    f.write("-" * 60 + "\n\n")

    f.write("Eigenvalues:\n")
    for i, eig in enumerate(eigenvalues_lon):
        f.write(f"λ{i+1}: {eig.real:.6f} {'+' if eig.imag>=0 else '-'} {abs(eig.imag):.6f}j\n")
        f.write(f"     |λ| = {np.abs(eig):.6f} rad/s\n")
        if np.abs(eig.imag) > 1e-6:
            damping = -eig.real / np.abs(eig)
            f.write(f"     ζ = {damping:.6f}\n")
        f.write("\n")

    f.write("Eigenvectors (States: [δv, δα, δq, δθ]):\n")
    for i in range(4):
        vec = eigenvectors_lon[:, i]
        f.write(f"\nMode {i+1} (λ{i+1}):\n")
        f.write(f"  δv:  {vec[0].real:.6f} + {vec[0].imag:.6f}j\n")
        f.write(f"  δα:  {vec[1].real:.6f} + {vec[1].imag:.6f}j\n")
        f.write(f"  δq:  {vec[2].real:.6f} + {vec[2].imag:.6f}j\n")
        f.write(f"  δθ:  {vec[3].real:.6f} + {vec[3].imag:.6f}j\n")

    # ---------------- LATERAL ----------------
    f.write("\n" + "-" * 60 + "\n")
    f.write("LATERAL-DIRECTIONAL DYNAMICS (Roll/Yaw Plane)\n")
    f.write("-" * 60 + "\n\n")

    f.write("Eigenvalues:\n")
    for i, eig in enumerate(eigenvalues_lat):
        f.write(f"λ{i+1}: {eig.real:.6f} {'+' if eig.imag>=0 else '-'} {abs(eig.imag):.6f}j\n")
        f.write(f"     |λ| = {np.abs(eig):.6f} rad/s\n")
        if np.abs(eig.imag) > 1e-6:
            damping = -eig.real / np.abs(eig)
            f.write(f"     ζ = {damping:.6f}\n")
        f.write("\n")

    f.write("Eigenvectors (States: [δβ, δp, δr, δφ]):\n")
    for i in range(4):
        vec = eigenvectors_lat[:, i]
        f.write(f"\nMode {i+1} (λ{i+1}):\n")
        f.write(f"  δβ:  {vec[0].real:.6f} + {vec[0].imag:.6f}j\n")
        f.write(f"  δp:  {vec[1].real:.6f} + {vec[1].imag:.6f}j\n")
        f.write(f"  δr:  {vec[2].real:.6f} + {vec[2].imag:.6f}j\n")
        f.write(f"  δφ:  {vec[3].real:.6f} + {vec[3].imag:.6f}j\n")

print(f"\nSaved eigen analysis to: {output_file}")