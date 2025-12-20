#!/usr/bin/env python3
"""
Numerical Integration of Acceleration Data

This script reads acceleration data from a CSV file and performs numerical
integration to calculate velocity and position. The results are then compared
with reference values from the CSV file.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def load_data(filename):
    """
    Load data from CSV file.
    
    The CSV file is expected to have the following columns:
    - Column 0: Time (Zeit)
    - Column 1: Position (Weg)
    - Column 2: Velocity (Geschwindigkeit)
    - Column 3: Acceleration (Beschleunigung)
    
    Args:
        filename: Path to the CSV file
        
    Returns:
        DataFrame with columns: time, position_ref, velocity_ref, acceleration
    """
    # Read CSV file, skip the first column (line numbers)
    data = pd.read_csv(filename, sep='\t', header=None, 
                       names=['time', 'position_ref', 'velocity_ref', 'acceleration'])
    return data


def integrate_trapezoidal(y, x):
    """
    Perform numerical integration using the trapezoidal rule.
    
    Args:
        y: Array of values to integrate
        x: Array of x-values (e.g., time)
        
    Returns:
        Array of integrated values
    """
    integrated = np.zeros(len(y))
    for i in range(1, len(y)):
        dx = x[i] - x[i-1]
        integrated[i] = integrated[i-1] + 0.5 * (y[i] + y[i-1]) * dx
    return integrated


def integrate_acceleration(data):
    """
    Integrate acceleration to get velocity and position.
    
    Args:
        data: DataFrame with time and acceleration columns
        
    Returns:
        DataFrame with calculated velocity and position
    """
    time = data['time'].values
    acceleration = data['acceleration'].values
    
    # Integrate acceleration to get velocity
    velocity_calc = integrate_trapezoidal(acceleration, time)
    
    # Integrate velocity to get position
    position_calc = integrate_trapezoidal(velocity_calc, time)
    
    # Adjust initial conditions to match reference values
    # Get initial values from reference data
    v0_ref = data['velocity_ref'].iloc[0]
    s0_ref = data['position_ref'].iloc[0]
    
    # Add initial velocity offset
    velocity_calc = velocity_calc + v0_ref
    
    # Add initial position offset
    position_calc = position_calc + s0_ref
    
    return velocity_calc, position_calc


def plot_results(data, velocity_calc, position_calc):
    """
    Plot the calculated and reference values for comparison.
    
    Args:
        data: DataFrame with reference data
        velocity_calc: Calculated velocity values
        position_calc: Calculated position values
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    time = data['time'].values
    
    # Plot acceleration
    axes[0].plot(time, data['acceleration'], 'b-', label='Beschleunigung (Reference)', linewidth=1.5)
    axes[0].set_xlabel('Zeit (s)')
    axes[0].set_ylabel('Beschleunigung (m/s²)')
    axes[0].set_title('Beschleunigung vs. Zeit')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Plot velocity
    axes[1].plot(time, data['velocity_ref'], 'b-', label='Geschwindigkeit (Reference)', linewidth=1.5)
    axes[1].plot(time, velocity_calc, 'r--', label='Geschwindigkeit (Berechnet)', linewidth=1.5, alpha=0.7)
    axes[1].set_xlabel('Zeit (s)')
    axes[1].set_ylabel('Geschwindigkeit (m/s)')
    axes[1].set_title('Geschwindigkeit vs. Zeit')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # Plot position
    axes[2].plot(time, data['position_ref'], 'b-', label='Weg (Reference)', linewidth=1.5)
    axes[2].plot(time, position_calc, 'r--', label='Weg (Berechnet)', linewidth=1.5, alpha=0.7)
    axes[2].set_xlabel('Zeit (s)')
    axes[2].set_ylabel('Weg (m)')
    axes[2].set_title('Weg vs. Zeit')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig('integration_results.png', dpi=150)
    print("Plot saved as 'integration_results.png'")
    plt.show()


def calculate_errors(data, velocity_calc, position_calc):
    """
    Calculate and display error statistics.
    
    Args:
        data: DataFrame with reference data
        velocity_calc: Calculated velocity values
        position_calc: Calculated position values
    """
    velocity_error = velocity_calc - data['velocity_ref'].values
    position_error = position_calc - data['position_ref'].values
    
    print("\n" + "="*60)
    print("Fehlerstatistik (Error Statistics)")
    print("="*60)
    print("\nGeschwindigkeit (Velocity):")
    print(f"  Mittlerer Fehler (Mean Error):          {np.mean(velocity_error):.6e}")
    print(f"  RMS Fehler (RMS Error):                 {np.sqrt(np.mean(velocity_error**2)):.6e}")
    print(f"  Maximaler absoluter Fehler (Max Error): {np.max(np.abs(velocity_error)):.6e}")
    
    print("\nWeg (Position):")
    print(f"  Mittlerer Fehler (Mean Error):          {np.mean(position_error):.6e}")
    print(f"  RMS Fehler (RMS Error):                 {np.sqrt(np.mean(position_error**2)):.6e}")
    print(f"  Maximaler absoluter Fehler (Max Error): {np.max(np.abs(position_error)):.6e}")
    print("="*60)


def main():
    """Main function to execute the integration and plotting."""
    print("Numerische Integration von Beschleunigungsdaten")
    print("="*60)
    
    # Load data
    print("\nLade Daten aus 'avs.csv'...")
    data = load_data('avs.csv')
    print(f"Daten geladen: {len(data)} Datenpunkte")
    
    # Perform integration
    print("\nFühre numerische Integration durch...")
    velocity_calc, position_calc = integrate_acceleration(data)
    print("Integration abgeschlossen")
    
    # Calculate and display errors
    calculate_errors(data, velocity_calc, position_calc)
    
    # Plot results
    print("\nErstelle Plots...")
    plot_results(data, velocity_calc, position_calc)
    
    print("\nFertig!")


if __name__ == "__main__":
    main()
