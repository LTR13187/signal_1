#!/usr/bin/env python3
"""
Test script for integrate_acceleration.py

This script tests the numerical integration functionality to ensure
the integration results are correct.
"""

import sys
import os
import numpy as np

# Add current directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from integrate_acceleration import load_data, integrate_acceleration


def test_load_data():
    """Test loading data from CSV file."""
    print("Testing load_data()...")
    
    # Test with avs.csv
    time, acceleration = load_data('avs.csv')
    
    # Verify we got data
    assert len(time) > 0, "No time data loaded"
    assert len(acceleration) > 0, "No acceleration data loaded"
    assert len(time) == len(acceleration), "Time and acceleration arrays have different lengths"
    
    # Verify time is increasing
    assert np.all(np.diff(time) > 0), "Time values are not monotonically increasing"
    
    print(f"  ✓ Loaded {len(time)} data points")
    print(f"  ✓ Time range: {time[0]:.3f} to {time[-1]:.3f} seconds")
    print()


def test_integrate_acceleration():
    """Test numerical integration of acceleration."""
    print("Testing integrate_acceleration()...")
    
    # Load test data
    time, acceleration = load_data('avs.csv')
    
    # Perform integration
    velocity, position = integrate_acceleration(time, acceleration)
    
    # Verify initial conditions
    assert velocity[0] == 0.0, f"Initial velocity should be 0, got {velocity[0]}"
    assert position[0] == 0.0, f"Initial position should be 0, got {position[0]}"
    
    # Verify array lengths
    assert len(velocity) == len(time), "Velocity array has wrong length"
    assert len(position) == len(time), "Position array has wrong length"
    
    # Verify no NaN or Inf values
    assert not np.any(np.isnan(velocity)), "Velocity contains NaN values"
    assert not np.any(np.isnan(position)), "Position contains NaN values"
    assert not np.any(np.isinf(velocity)), "Velocity contains Inf values"
    assert not np.any(np.isinf(position)), "Position contains Inf values"
    
    print(f"  ✓ Initial conditions correct (v0={velocity[0]}, p0={position[0]})")
    print(f"  ✓ Velocity range: [{velocity.min():.2f}, {velocity.max():.2f}]")
    print(f"  ✓ Position range: [{position.min():.2f}, {position.max():.2f}]")
    print(f"  ✓ No NaN or Inf values")
    print()


def test_simple_integration():
    """Test integration with simple known values."""
    print("Testing with simple constant acceleration...")
    
    # Create simple test case: constant acceleration = 10
    time = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    acceleration = np.array([10.0, 10.0, 10.0, 10.0, 10.0])
    
    velocity, position = integrate_acceleration(time, acceleration)
    
    # For constant acceleration a=10, starting from rest:
    # v(t) = 10*t
    # x(t) = 5*t^2
    
    expected_velocity = np.array([0.0, 10.0, 20.0, 30.0, 40.0])
    expected_position = np.array([0.0, 5.0, 20.0, 45.0, 80.0])
    
    # Check velocity (should be close to expected)
    assert np.allclose(velocity, expected_velocity, rtol=0.01), \
        f"Velocity integration incorrect: {velocity} vs expected {expected_velocity}"
    
    # Check position (should be close to expected)
    assert np.allclose(position, expected_position, rtol=0.01), \
        f"Position integration incorrect: {position} vs expected {expected_position}"
    
    print(f"  ✓ Velocity integration correct")
    print(f"  ✓ Position integration correct")
    print()


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running integration tests...")
    print("=" * 60)
    print()
    
    try:
        test_load_data()
        test_integrate_acceleration()
        test_simple_integration()
        
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
