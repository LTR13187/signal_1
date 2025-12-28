#!/usr/bin/env python3
"""
Script to process CSV files with optional DATA_START marker.
Handles files with or without the DATA_START marker gracefully.
"""

import sys
import csv


def get_data_start_info(file_path):
    """
    Get information about where the data starts in a CSV file.
    
    Looks for DATA_START marker. If not found, attempts to automatically
    detect the data format by analyzing the file structure.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        tuple: (skiprows, col_names, sep) where:
            - skiprows: number of rows to skip before data
            - col_names: list of column names or None
            - sep: separator character (e.g., '\t', ',')
    """
    data_start_idx = None
    
    # Read file and look for DATA_START marker
    # Only read first 100 lines to avoid memory issues with large files
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            lines.append(line)
            if i >= 100:  # Limit to first 100 lines for header detection
                break
    
    # Search for DATA_START marker (case-insensitive)
    for idx, line in enumerate(lines):
        if line.strip().lower() == "data_start":
            data_start_idx = idx
            break
    
    # If DATA_START marker was found
    if data_start_idx is not None:
        # The header is the line immediately after DATA_START
        header_line = lines[data_start_idx + 1].strip()
        
        # Detect separator (try tab first, then comma)
        if '\t' in header_line:
            sep = '\t'
        elif ',' in header_line:
            sep = ','
        else:
            sep = '\t'  # default to tab
        
        col_names = [col.strip() for col in header_line.split(sep)]
        skiprows = data_start_idx + 2  # Skip to the line after the header
        
        return skiprows, col_names, sep
    
    # Fallback: No DATA_START marker found
    print("ERROR: The line 'data_start' is missing in the specified file. Ensure that the 'data_start' indicator exists to mark the beginning of the dataset, or adjust the script to handle your file's structure.")
    
    # Analyze first few lines to detect format
    if len(lines) == 0:
        raise ValueError("File is empty.")
    
    # Count total lines in the file for validation
    with open(file_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
    
    # Offer user the option to manually specify the starting row
    user_input = input("The 'data_start' line was not found. Enter the row number where data starts (starting from 0): ")
    
    # Validate the user input
    try:
        skiprows = int(user_input.strip())
    except ValueError:
        raise ValueError("ERROR: Invalid input. Please enter a valid integer for the row number.")
    
    # Validate that the row number is within range
    if skiprows < 0:
        raise ValueError("ERROR: Row number cannot be negative.")
    if skiprows >= total_lines:
        raise ValueError(f"ERROR: Row number {skiprows} is out of range. The file has only {total_lines} lines.")
    
    # Detect separator from the specified starting line
    data_line = None
    if skiprows < len(lines):
        data_line = lines[skiprows].strip()
    else:
        # Read the specific line if not in our cached lines
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == skiprows:
                    data_line = line.strip()
                    break
    
    # Ensure data_line was found
    if data_line is None:
        raise ValueError(f"ERROR: Could not read line {skiprows} from the file.")
    
    if '\t' in data_line:
        sep = '\t'
    elif ',' in data_line:
        sep = ','
    else:
        sep = '\t'  # default to tab
    
    # Generate generic column names based on the data line
    data_parts = data_line.split(sep)
    num_cols = len(data_parts)
    col_names = [f'Column_{i+1}' for i in range(num_cols)]
    
    print(f"INFO: Using row {skiprows} as data start")
    print(f"INFO: Detected separator: {'TAB' if sep == '\t' else repr(sep)}")
    print(f"INFO: Detected {len(col_names)} columns")
    
    return skiprows, col_names, sep


# Main execution
if __name__ == "__main__":
    # Get file path from user
    file_path = input("Dateipfad eingeben: ").strip()
    
    # Get data start information
    try:
        skiprows, col_names, sep = get_data_start_info(file_path)
    except Exception as e:
        print(f"Fehler beim Ermitteln der Datenstart-Informationen: {e}")
        sys.exit(1)
    
    print(f"Automatisch gefundene Datenzeile: {skiprows+1}")
    print(f"Spalten: {col_names}")
    print(f"Trennzeichen: {'TAB' if sep == '\t' else repr(sep)}")
    
    # Read and display first few rows of data
    try:
        import pandas as pd
        df = pd.read_csv(file_path, sep=sep, skiprows=skiprows, names=col_names)
        print(f"\nErfolgreich geladen: {len(df)} Zeilen")
        print("\nErste 5 Zeilen:")
        print(df.head())
    except ImportError:
        # If pandas is not available, use basic CSV reading
        print("\nPandas not available, using basic CSV reading...")
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=sep)
            # Skip rows
            for _ in range(skiprows):
                next(reader)
            # Display first 5 data rows
            print("\nErste 5 Zeilen:")
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                print(f"  {dict(zip(col_names, row))}")
    except Exception as e:
        print(f"Fehler beim Laden der Daten: {e}")
        sys.exit(1)
    
    print("\nDaten erfolgreich verarbeitet!")
