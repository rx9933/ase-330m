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

# Trim state (from problem statement)
v_trim = 42.0  # m/s
alpha_trim = 0.0  # rad
q_trim = 0.0  # rad/s
theta_trim = 0.0  # rad
beta_trim = 0.0  # rad
p_trim = 0.0  # rad/s
r_trim = 0.0  # rad/s
phi_trim = 0.0  # rad

def load_and_process_maneuver(filename, maneuver_name):
    """
    Load CSV data and compute perturbation states
    
    CSV columns: Time, V_mps, alt_m, pitch_deg, q_degps, alpha_deg, 
                 vpath_deg, beta_deg, p_degps, r_degps, roll_deg
    """
    # Load data
    df = pd.read_csv(filename)
    
    # Convert from degrees to radians where needed
    # States needed: V (already m/s), alpha (rad), q (rad/s), theta (rad) - longitudinal
    #                beta (rad), p (rad/s), r (rad/s), phi (rad) - lateral
    
    time = df['Time'].values
    
    # Longitudinal states
    V_abs = df['V_mps'].values  # m/s
    alpha_abs = np.radians(df['alpha_deg'].values)  # rad
    q_abs = np.radians(df['q_degps'].values)  # rad/s
    theta_abs = np.radians(df['pitch_deg'].values)  # rad
    
    # Lateral states
    beta_abs = np.radians(df['beta_deg'].values)  # rad
    p_abs = np.radians(df['p_degps'].values)  # rad/s
    r_abs = np.radians(df['r_degps'].values)  # rad/s
    phi_abs = np.radians(df['roll_deg'].values)  # rad
    
    # Compute perturbation states
    lon_per = np.column_stack([
        V_abs - v_trim,           # δv
        alpha_abs - alpha_trim,   # δα
        q_abs - q_trim,           # δq
        theta_abs - theta_trim    # δθ
    ])
    
    lat_per = np.column_stack([
        beta_abs - beta_trim,     # δβ
        p_abs - p_trim,           # δp
        r_abs - r_trim,           # δr
        phi_abs - phi_trim        # δφ
    ])
    
    # Absolute states (already in correct units)
    lon_abs = np.column_stack([V_abs, alpha_abs, q_abs, theta_abs])
    lat_abs = np.column_stack([beta_abs, p_abs, r_abs, phi_abs])
    
    return time, lon_abs, lat_abs, lon_per, lat_per

# Load both maneuvers
print("Loading maneuver data...")
t1, lon_abs1, lat_abs1, lon_per1, lat_per1 = load_and_process_maneuver('maneuver_1.csv', 'Maneuver 1')
t2, lon_abs2, lat_abs2, lon_per2, lat_per2 = load_and_process_maneuver('maneuver_2.csv', 'Maneuver 2')

print(f"Maneuver 1: {len(t1)} data points, time range: {t1[0]:.2f} to {t1[-1]:.2f} seconds")
print(f"Maneuver 2: {len(t2)} data points, time range: {t2[0]:.2f} to {t2[-1]:.2f} seconds")

# Plot function for perturbation states
def plot_perturbation_states(t, lon_per, lat_per, title, ax_lon, ax_lat, t_offset=0):
    """Plot longitudinal and lateral perturbation states"""
    
    # Adjust time to start from 0 for easier comparison
    t_adj = t #- t[0]
    
    # Longitudinal states
    lon_labels = [r'$\delta v$ (m/s)', r'$\delta \alpha$ (rad)', 
                  r'$\delta q$ (rad/s)', r'$\delta \theta$ (rad)']
    for i, label in enumerate(lon_labels):
        ax_lon[i].plot(t_adj, lon_per[:, i], 'b-', linewidth=1.5)
        ax_lon[i].set_ylabel(label)
        ax_lon[i].grid(True, alpha=0.3)
        ax_lon[i].axhline(y=0, color='k', linestyle='--', alpha=0.5)
    
    ax_lon[-1].set_xlabel('Time from start (s)')
    
    # Lateral states
    lat_labels = [r'$\delta \beta$ (rad)', r'$\delta p$ (rad/s)', 
                  r'$\delta r$ (rad/s)', r'$\delta \phi$ (rad)']
    for i, label in enumerate(lat_labels):
        ax_lat[i].plot(t_adj, lat_per[:, i], 'r-', linewidth=1.5)
        ax_lat[i].set_ylabel(label)
        ax_lat[i].grid(True, alpha=0.3)
        ax_lat[i].axhline(y=0, color='k', linestyle='--', alpha=0.5)
    
    ax_lat[-1].set_xlabel('Time from start (s)')
    
    ax_lon[0].set_title(f'{title} - Longitudinal States')
    ax_lat[0].set_title(f'{title} - Lateral States')
def main():
    # Create plots for both maneuvers
    fig1 = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(4, 2, figure=fig1, hspace=0.3, wspace=0.3)

    # Maneuver 1
    ax_lon1 = [fig1.add_subplot(gs[i, 0]) for i in range(4)]
    ax_lat1 = [fig1.add_subplot(gs[i, 1]) for i in range(4)]
    plot_perturbation_states(t1, lon_per1, lat_per1, 'Maneuver 1', 
                            ax_lon1, ax_lat1)

    plt.suptitle('Test Flight 1: Maneuver Data\nPerturbation States from Trim', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()

    fig2 = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(4, 2, figure=fig2, hspace=0.3, wspace=0.3)

    # Maneuver 2
    ax_lon2 = [fig2.add_subplot(gs[i, 0]) for i in range(4)]
    ax_lat2 = [fig2.add_subplot(gs[i, 1]) for i in range(4)]
    plot_perturbation_states(t2, lon_per2, lat_per2, 'Maneuver 2', 
                            ax_lon2, ax_lat2)

    plt.suptitle('Test Flight 2: Maneuver Data\nPerturbation States from Trim', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Create detailed comparison plots
    fig3, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Airspeed perturbations
    axes[0, 0].plot(t1 - t1[0], lon_per1[:, 0], 'b-', label='Maneuver 1', linewidth=1.5)
    axes[0, 0].plot(t2 - t2[0], lon_per2[:, 0], 'r-', label='Maneuver 2', linewidth=1.5)
    axes[0, 0].axhline(y=0, color='k', linestyle='--', alpha=0.7)
    axes[0, 0].set_ylabel(r'$\delta v$ (m/s)')
    axes[0, 0].set_xlabel('Time from start (s)')
    axes[0, 0].set_title('Forward Speed Perturbation')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Angle of attack perturbations
    axes[0, 1].plot(t1 - t1[0], np.degrees(lon_per1[:, 1]), 'b-', label='Maneuver 1', linewidth=1.5)
    axes[0, 1].plot(t2 - t2[0], np.degrees(lon_per2[:, 1]), 'r-', label='Maneuver 2', linewidth=1.5)
    axes[0, 1].axhline(y=0, color='k', linestyle='--', alpha=0.7)
    axes[0, 1].set_ylabel(r'$\delta \alpha$ (deg)')
    axes[0, 1].set_xlabel('Time from start (s)')
    axes[0, 1].set_title('Angle of Attack Perturbation')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: Pitch rate perturbations
    axes[1, 0].plot(t1 - t1[0], np.degrees(lon_per1[:, 2]), 'b-', label='Maneuver 1', linewidth=1.5)
    axes[1, 0].plot(t2 - t2[0], np.degrees(lon_per2[:, 2]), 'r-', label='Maneuver 2', linewidth=1.5)
    axes[1, 0].axhline(y=0, color='k', linestyle='--', alpha=0.7)
    axes[1, 0].set_ylabel(r'$\delta q$ (deg/s)')
    axes[1, 0].set_xlabel('Time from start (s)')
    axes[1, 0].set_title('Pitch Rate Perturbation')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Pitch angle perturbations
    axes[1, 1].plot(t1 - t1[0], np.degrees(lon_per1[:, 3]), 'b-', label='Maneuver 1', linewidth=1.5)
    axes[1, 1].plot(t2 - t2[0], np.degrees(lon_per2[:, 3]), 'r-', label='Maneuver 2', linewidth=1.5)
    axes[1, 1].axhline(y=0, color='k', linestyle='--', alpha=0.7)
    axes[1, 1].set_ylabel(r'$\delta \theta$ (deg)')
    axes[1, 1].set_xlabel('Time from start (s)')
    axes[1, 1].set_title('Pitch Angle Perturbation')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle('Longitudinal Perturbation States Comparison', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Lateral states comparison
    fig4, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Sideslip angle perturbations
    axes[0, 0].plot(t1 - t1[0], np.degrees(lat_per1[:, 0]), 'b-', label='Maneuver 1', linewidth=1.5)
    axes[0, 0].plot(t2 - t2[0], np.degrees(lat_per2[:, 0]), 'r-', label='Maneuver 2', linewidth=1.5)
    axes[0, 0].axhline(y=0, color='k', linestyle='--', alpha=0.7)
    axes[0, 0].set_ylabel(r'$\delta \beta$ (deg)')
    axes[0, 0].set_xlabel('Time from start (s)')
    axes[0, 0].set_title('Sideslip Angle Perturbation')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Roll rate perturbations
    axes[0, 1].plot(t1 - t1[0], np.degrees(lat_per1[:, 1]), 'b-', label='Maneuver 1', linewidth=1.5)
    axes[0, 1].plot(t2 - t2[0], np.degrees(lat_per2[:, 1]), 'r-', label='Maneuver 2', linewidth=1.5)
    axes[0, 1].axhline(y=0, color='k', linestyle='--', alpha=0.7)
    axes[0, 1].set_ylabel(r'$\delta p$ (deg/s)')
    axes[0, 1].set_xlabel('Time from start (s)')
    axes[0, 1].set_title('Roll Rate Perturbation')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: Yaw rate perturbations
    axes[1, 0].plot(t1 - t1[0], np.degrees(lat_per1[:, 2]), 'b-', label='Maneuver 1', linewidth=1.5)
    axes[1, 0].plot(t2 - t2[0], np.degrees(lat_per2[:, 2]), 'r-', label='Maneuver 2', linewidth=1.5)
    axes[1, 0].axhline(y=0, color='k', linestyle='--', alpha=0.7)
    axes[1, 0].set_ylabel(r'$\delta r$ (deg/s)')
    axes[1, 0].set_xlabel('Time from start (s)')
    axes[1, 0].set_title('Yaw Rate Perturbation')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Roll angle perturbations
    axes[1, 1].plot(t1 - t1[0], np.degrees(lat_per1[:, 3]), 'b-', label='Maneuver 1', linewidth=1.5)
    axes[1, 1].plot(t2 - t2[0], np.degrees(lat_per2[:, 3]), 'r-', label='Maneuver 2', linewidth=1.5)
    axes[1, 1].axhline(y=0, color='k', linestyle='--', alpha=0.7)
    axes[1, 1].set_ylabel(r'$\delta \phi$ (deg)')
    axes[1, 1].set_xlabel('Time from start (s)')
    axes[1, 1].set_title('Roll Angle Perturbation')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle('Lateral-Directional Perturbation States Comparison', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Print statistical summary
    print("\n" + "=" * 80)
    print("PERTURBATION STATES STATISTICAL SUMMARY")
    print("=" * 80)

    print("\nManeuver 1 - Longitudinal Perturbations:")
    print(f"  δv: mean={np.mean(lon_per1[:,0]):.4f} m/s, std={np.std(lon_per1[:,0]):.4f} m/s")
    print(f"  δα: mean={np.mean(lon_per1[:,1]):.4f} rad, std={np.std(lon_per1[:,1]):.4f} rad")
    print(f"  δq: mean={np.mean(lon_per1[:,2]):.4f} rad/s, std={np.std(lon_per1[:,2]):.4f} rad/s")
    print(f"  δθ: mean={np.mean(lon_per1[:,3]):.4f} rad, std={np.std(lon_per1[:,3]):.4f} rad")

    print("\nManeuver 1 - Lateral Perturbations:")
    print(f"  δβ: mean={np.mean(lat_per1[:,0]):.4f} rad, std={np.std(lat_per1[:,0]):.4f} rad")
    print(f"  δp: mean={np.mean(lat_per1[:,1]):.4f} rad/s, std={np.std(lat_per1[:,1]):.4f} rad/s")
    print(f"  δr: mean={np.mean(lat_per1[:,2]):.4f} rad/s, std={np.std(lat_per1[:,2]):.4f} rad/s")
    print(f"  δφ: mean={np.mean(lat_per1[:,3]):.4f} rad, std={np.std(lat_per1[:,3]):.4f} rad")

    print("\nManeuver 2 - Longitudinal Perturbations:")
    print(f"  δv: mean={np.mean(lon_per2[:,0]):.4f} m/s, std={np.std(lon_per2[:,0]):.4f} m/s")
    print(f"  δα: mean={np.mean(lon_per2[:,1]):.4f} rad, std={np.std(lon_per2[:,1]):.4f} rad")
    print(f"  δq: mean={np.mean(lon_per2[:,2]):.4f} rad/s, std={np.std(lon_per2[:,2]):.4f} rad/s")
    print(f"  δθ: mean={np.mean(lon_per2[:,3]):.4f} rad, std={np.std(lon_per2[:,3]):.4f} rad")

    print("\nManeuver 2 - Lateral Perturbations:")
    print(f"  δβ: mean={np.mean(lat_per2[:,0]):.4f} rad, std={np.std(lat_per2[:,0]):.4f} rad")
    print(f"  δp: mean={np.mean(lat_per2[:,1]):.4f} rad/s, std={np.std(lat_per2[:,1]):.4f} rad/s")
    print(f"  δr: mean={np.mean(lat_per2[:,2]):.4f} rad/s, std={np.std(lat_per2[:,2]):.4f} rad/s")
    print(f"  δφ: mean={np.mean(lat_per2[:,3]):.4f} rad, std={np.std(lat_per2[:,3]):.4f} rad")

    print("\n" + "=" * 80)

    fig1.savefig('p1/man1_long_lat.png', dpi=300, bbox_inches='tight')
    fig2.savefig('p1/man2_long_lat.png', dpi=300, bbox_inches='tight')
    fig3.savefig('p1/long_comparisions.png', dpi=300, bbox_inches='tight')
    fig4.savefig('p1/lat_comparision.png', dpi=300, bbox_inches='tight')
    plt.show()
if __name__=='main':
    main()