#!/usr/bin/env python3
"""
Numerical Integration Script for Acceleration Data

This script performs numerical integration on acceleration data to derive
velocity and position. It reads time and acceleration data from a CSV file,
integrates the acceleration to obtain velocity, and then integrates velocity
to obtain position.

The script plots the acceleration, velocity, and position results for
visualization.
"""

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt


def load_data(filepath):
    """
    Load time and acceleration data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file containing time and acceleration data
        
    Returns:
        tuple: (time, acceleration) arrays
        
    Raises:
        ValueError: If the CSV file doesn't contain exactly 2 or more columns
        FileNotFoundError: If the specified file doesn't exist
    """
    try:
        # Load the CSV file
        data = np.loadtxt(filepath, delimiter='\t')
        
        # Validate that we have at least 2 columns
        if data.ndim == 1:
            raise ValueError("CSV file must contain at least 2 columns (time and acceleration)")
        
        if data.shape[1] < 2:
            raise ValueError("CSV file must contain at least 2 columns (time and acceleration)")
        
        # Extract time (first column) and acceleration (last column)
        time = data[:, 0]
        acceleration = data[:, -1]
        
        print(f"Loaded {len(time)} data points")
        print(f"Time range: {time[0]:.3f} to {time[-1]:.3f} seconds")
        
        return time, acceleration
        
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error loading data from {filepath}: {str(e)}")


def integrate_acceleration(time, acceleration):
    """
    Integrate acceleration data to obtain velocity and position.
    
    Uses the trapezoidal rule for numerical integration with zero initial conditions.
    
    Args:
        time (np.ndarray): Time array
        acceleration (np.ndarray): Acceleration array
        
    Returns:
        tuple: (velocity, position) arrays
    """
    # Initialize arrays with zero initial conditions
    velocity = np.zeros_like(acceleration)
    position = np.zeros_like(acceleration)
    
    # Integrate acceleration to get velocity using trapezoidal rule
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        velocity[i] = velocity[i-1] + 0.5 * (acceleration[i-1] + acceleration[i]) * dt
    
    # Integrate velocity to get position using trapezoidal rule
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        position[i] = position[i-1] + 0.5 * (velocity[i-1] + velocity[i]) * dt
    
    return velocity, position


def plot_results(time, acceleration, velocity, position):
    """
    Plot acceleration, velocity, and position data.
    
    Creates a figure with three subplots showing the acceleration, velocity,
    and position over time. Displays the plots interactively.
    
    Args:
        time (np.ndarray): Time array
        acceleration (np.ndarray): Acceleration array
        velocity (np.ndarray): Velocity array (from integration)
        position (np.ndarray): Position array (from integration)
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    fig.suptitle('Numerical Integration of Acceleration Data', fontsize=14, fontweight='bold')
    
    # Plot acceleration
    axes[0].plot(time, acceleration, 'b-', linewidth=1.5, label='Acceleration')
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Acceleration')
    axes[0].set_title('Acceleration vs Time')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Plot velocity
    axes[1].plot(time, velocity, 'g-', linewidth=1.5, label='Velocity (integrated)')
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Velocity')
    axes[1].set_title('Velocity vs Time (from Integration)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # Plot position
    axes[2].plot(time, position, 'r-', linewidth=1.5, label='Position (integrated)')
    axes[2].set_xlabel('Time (s)')
    axes[2].set_ylabel('Position')
    axes[2].set_title('Position vs Time (from Integration)')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()
    
    plt.tight_layout()
    plt.show()


def main():
    """
    Main function to run the numerical integration script.
    
    Parses command-line arguments, loads data, performs integration,
    and displays plots.
    """
    parser = argparse.ArgumentParser(
        description='Perform numerical integration on acceleration data. '
                    'Reads time and acceleration from a CSV file, integrates to obtain '
                    'velocity and position, and displays the results as plots.'
    )
    parser.add_argument(
        'filepath',
        type=str,
        help='Path to the CSV file containing time and acceleration data'
    )
    
    args = parser.parse_args()
    
    try:
        # Load data
        print(f"Loading data from: {args.filepath}")
        time, acceleration = load_data(args.filepath)
        
        # Perform integration
        print("Performing numerical integration...")
        velocity, position = integrate_acceleration(time, acceleration)
        
        # Display results
        print("Integration complete. Displaying plots...")
        plot_results(time, acceleration, velocity, position)
        
        print("Done!")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
