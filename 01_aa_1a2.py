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
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Search for DATA_START marker
    for idx, line in enumerate(lines):
        if 'DATA_START' in line:
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
    # Try to automatically detect the file format
    print("INFO: DATA_START marker not found. Attempting automatic detection...")
    
    # Analyze first few lines to detect format
    if len(lines) == 0:
        raise ValueError("File is empty.")
    
    # Detect separator from first line
    first_line = lines[0].strip()
    if '\t' in first_line:
        sep = '\t'
    elif ',' in first_line:
        sep = ','
    else:
        sep = '\t'  # default to tab
    
    # Check if first line looks like data (all numeric) or header (contains text)
    first_parts = first_line.split(sep)
    
    # Try to determine if first line is a header or data
    is_header = False
    try:
        # If we can't convert all parts to float, it's likely a header
        for part in first_parts:
            float(part)
    except ValueError:
        is_header = True
    
    if is_header:
        # First line is a header
        col_names = [col.strip() for col in first_parts]
        skiprows = 1
    else:
        # First line is data, generate generic column names
        num_cols = len(first_parts)
        col_names = [f'Column_{i+1}' for i in range(num_cols)]
        skiprows = 0
    
    print(f"INFO: Detected separator: {'TAB' if sep == chr(9) else repr(sep)}")
    print(f"INFO: Detected {len(col_names)} columns: {col_names}")
    print(f"INFO: Data starts at line {skiprows + 1}")
    
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
    print(f"Trennzeichen: {'TAB' if sep == chr(9) else repr(sep)}")
    
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
