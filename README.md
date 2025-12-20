# Numerical Integration of Acceleration Data

This repository contains a Python script for performing numerical integration on acceleration data to derive velocity and position.

## Files

- `integrate_acceleration.py` - Main script for numerical integration
- `test_integration.py` - Test script to verify the integration functionality
- `avs.csv` - Sample acceleration data file

## Description

The `integrate_acceleration.py` script performs numerical integration on acceleration data:

1. Reads time and acceleration data from a CSV file
2. Integrates acceleration to obtain velocity using the trapezoidal rule
3. Integrates velocity to obtain position using the trapezoidal rule
4. Displays interactive plots of acceleration, velocity, and position

The script starts with zero initial conditions (velocity = 0, position = 0) and uses the trapezoidal rule for numerical integration.

## Requirements

- Python 3.x
- NumPy
- Matplotlib

Install dependencies:
```bash
pip install numpy matplotlib
```

## Usage

Run the script with a CSV file containing time and acceleration data:

```bash
python3 integrate_acceleration.py <filepath>
```

Example:
```bash
python3 integrate_acceleration.py avs.csv
```

The script will:
1. Load the time and acceleration data from the CSV file
2. Perform numerical integration to compute velocity and position
3. Display three plots showing:
   - Acceleration vs Time
   - Velocity vs Time (from integration)
   - Position vs Time (from integration)

### Command-line Options

```bash
python3 integrate_acceleration.py --help
```

Shows usage information and available options.

## CSV File Format

The CSV file should contain at least 2 columns:
- Column 1: Time values
- Last column: Acceleration values

The script uses tab-separated values. If your CSV file has more columns, the script will use the first column for time and the last column for acceleration.

Example format:
```
0.000	0.2	0	-4176.81658254102
0.001	0.19791522372053	-4.16229359183563	-4133.27794186613
0.002	0.191704357803475	-8.23781267418677	-4003.56970309466
...
```

## Integration Method

The script uses the **trapezoidal rule** for numerical integration, which provides a good balance between accuracy and computational efficiency:

- **Velocity Integration**: `v[i] = v[i-1] + 0.5 * (a[i-1] + a[i]) * dt`
- **Position Integration**: `x[i] = x[i-1] + 0.5 * (v[i-1] + v[i]) * dt`

Where:
- `v` = velocity
- `a` = acceleration
- `x` = position
- `dt` = time step

## Features

- **No reference values required**: The script only needs time and acceleration data
- **Zero initial conditions**: Integration starts from rest (v₀ = 0, x₀ = 0)
- **Interactive plotting**: Plots are displayed in a window (not saved to files)
- **Robust error handling**: Validates input data and provides clear error messages
- **Flexible CSV reading**: Works with CSV files containing additional columns

## Testing

Run the test script to verify the integration functionality:

```bash
python3 test_integration.py
```

The test script verifies:
- Data loading from CSV files
- Correct initial conditions
- Numerical integration accuracy
- No NaN or Inf values in results

## Changes from Previous Version

This script includes the following improvements:

- ✓ Removed all dependencies on reference values (`position_ref`, `velocity_ref`)
- ✓ Updated to read only time and acceleration from CSV files
- ✓ Adjusted integration to work from acceleration data alone
- ✓ Removed plots related to reference values
- ✓ Changed plotting to display interactively only (no file saving)
- ✓ Updated documentation and help text to reflect these changes
