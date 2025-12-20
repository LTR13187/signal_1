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
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If the CSV file has incorrect format
    """
    try:
        # Read CSV file (tab-separated, 4 columns: time, position, velocity, acceleration)
        data = pd.read_csv(filename, sep='\t', header=None, 
                           names=['time', 'position_ref', 'velocity_ref', 'acceleration'])
        
        # Validate that we have the expected number of columns
        if len(data.columns) != 4:
            raise ValueError(f"CSV file should have 4 columns, but has {len(data.columns)}")
        
        # Validate that we have some data
        if len(data) == 0:
            raise ValueError("CSV file is empty")
            
        return data
        
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file '{filename}' not found. Please ensure the file exists.")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV file '{filename}': {str(e)}")


def integrate_trapezoidal(y, x):
    """
    Perform numerical integration using the trapezoidal rule.
    
    Uses vectorized NumPy operations for efficiency.
    
    Args:
        y: Array of values to integrate
        x: Array of x-values (e.g., time)
        
    Returns:
        Array of integrated values
    """
    # Calculate step sizes
    dx = np.diff(x)
    
    # Calculate average values between consecutive points
    y_avg = 0.5 * (y[1:] + y[:-1])
    
    # Cumulative sum with initial value of 0
    integrated = np.concatenate([[0], np.cumsum(y_avg * dx)])
    
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


def plot_results(data, velocity_calc, position_calc, output_file='integration_results.png'):
    """
    Plot the calculated and reference values for comparison.
    
    Args:
        data: DataFrame with reference data
        velocity_calc: Calculated velocity values
        position_calc: Calculated position values
        output_file: Path to save the output plot (default: 'integration_results.png')
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
    plt.savefig(output_file, dpi=150)
    print(f"Plot saved as '{output_file}'")
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
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Numerische Integration von Beschleunigungsdaten'
    )
    parser.add_argument(
        '--input', '-i',
        default='avs.csv',
        help='Pfad zur CSV-Datei mit Beschleunigungsdaten (default: avs.csv)'
    )
    parser.add_argument(
        '--output', '-o',
        default='integration_results.png',
        help='Pfad zur Ausgabedatei für Plots (default: integration_results.png)'
    )
    args = parser.parse_args()
    
    print("Numerische Integration von Beschleunigungsdaten")
    print("="*60)
    
    # Load data
    print(f"\nLade Daten aus '{args.input}'...")
    try:
        data = load_data(args.input)
        print(f"Daten geladen: {len(data)} Datenpunkte")
    except (FileNotFoundError, ValueError) as e:
        print(f"Fehler beim Laden der Daten: {str(e)}")
        return
    
    # Perform integration
    print("\nFühre numerische Integration durch...")
    velocity_calc, position_calc = integrate_acceleration(data)
    print("Integration abgeschlossen")
    
    # Calculate and display errors
    calculate_errors(data, velocity_calc, position_calc)
    
    # Plot results
    print("\nErstelle Plots...")
    plot_results(data, velocity_calc, position_calc, output_file=args.output)
    
    print("\nFertig!")


if __name__ == "__main__":
    main()
