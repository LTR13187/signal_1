# Signal Data Processing Tool

## Problem / Problem

The original script expected all CSV files to contain a `DATA_START` marker line, which caused it to fail when processing files without this marker.

**Error message:**
```
ValueError: DATA_START line not found in file.
```

## Solution / Lösung

The updated `01_aa_1a2.py` script now includes intelligent automatic detection:

1. **With DATA_START marker**: If the file contains a `DATA_START` line, the script processes it as before, reading the header from the line after DATA_START.

2. **Without DATA_START marker**: If no marker is found, the script automatically:
   - Detects the separator (tab or comma)
   - Determines if the first line is a header or data
   - Generates generic column names if needed
   - Processes the file successfully

## Usage / Verwendung

```bash
python3 01_aa_1a2.py
```

The script will prompt you for a file path:
```
Dateipfad eingeben: /path/to/your/file.csv
```

## Supported Formats / Unterstützte Formate

### Format 1: With DATA_START marker
```
Metadata line 1
Metadata line 2
DATA_START
Column1	Column2	Column3	Column4
0.000	0.2	0	-4176.81658254102
0.001	0.19791	-4.162	-4133.27
...
```

### Format 2: Without DATA_START marker (like avs.csv)
```
0.000	0.2	0	-4176.81658254102
0.001	0.19791	-4.162	-4133.27
...
```

### Format 3: CSV with header, no marker
```
Time,Value1,Value2,Value3
0.000,0.2,0,-4176.81658254102
0.001,0.19791,-4.162,-4133.27
...
```

## Example Output / Beispielausgabe

```
Dateipfad eingeben: avs.csv
INFO: DATA_START marker not found. Attempting automatic detection...
INFO: Detected separator: TAB
INFO: Detected 4 columns: ['Column_1', 'Column_2', 'Column_3', 'Column_4']
INFO: Data starts at line 1
Automatisch gefundene Datenzeile: 1
Spalten: ['Column_1', 'Column_2', 'Column_3', 'Column_4']
Trennzeichen: TAB

Erste 5 Zeilen:
  {'Column_1': '0.000', 'Column_2': '0.2', 'Column_3': '0', 'Column_4': '-4176.81658254102'}
  ...

Daten erfolgreich verarbeitet!
```

## Technical Details / Technische Details

The script uses the following detection logic:
1. Search for `DATA_START` marker in the file
2. If found: use the format specified after the marker
3. If not found: 
   - Detect separator (tab or comma)
   - Check if first line is numeric (data) or text (header)
   - Process accordingly

The solution is backward compatible and handles all existing files with DATA_START markers while also supporting files without markers.
