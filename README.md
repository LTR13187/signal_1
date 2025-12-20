# Numerical Integration of Acceleration Data

## Überblick (Overview)

Dieses Projekt implementiert eine numerische Integration von Beschleunigungsdaten zur Berechnung von Geschwindigkeit und Weg.

This project implements numerical integration of acceleration data to calculate velocity and position.

## Beschreibung (Description)

Das Programm liest Beschleunigungsdaten aus einer CSV-Datei und führt eine numerische Integration durch:
1. **Erste Integration**: Beschleunigung → Geschwindigkeit
2. **Zweite Integration**: Geschwindigkeit → Weg

Die Ergebnisse werden mit den Referenzwerten verglichen und grafisch dargestellt.

The program reads acceleration data from a CSV file and performs numerical integration:
1. **First integration**: Acceleration → Velocity
2. **Second integration**: Velocity → Position

The results are compared with reference values and visualized graphically.

## Datenformat (Data Format)

Die CSV-Datei `avs.csv` enthält folgende Spalten (tab-getrennt):
- **Spalte 1**: Zeit (s)
- **Spalte 2**: Weg (m) - Referenzwert
- **Spalte 3**: Geschwindigkeit (m/s) - Referenzwert
- **Spalte 4**: Beschleunigung (m/s²)

The CSV file `avs.csv` contains the following columns (tab-separated):
- **Column 1**: Time (s)
- **Column 2**: Position (m) - Reference value
- **Column 3**: Velocity (m/s) - Reference value
- **Column 4**: Acceleration (m/s²)

## Installation

```bash
pip install -r requirements.txt
```

## Verwendung (Usage)

```bash
python3 integrate_acceleration.py
```

Das Skript:
1. Liest die Daten aus `avs.csv`
2. Führt die numerische Integration durch (Trapezregel)
3. Passt die Anfangsbedingungen an die Referenzwerte an
4. Berechnet Fehlerstatistiken
5. Erstellt Plots und speichert sie als `integration_results.png`

The script:
1. Reads data from `avs.csv`
2. Performs numerical integration (trapezoidal rule)
3. Adjusts initial conditions to match reference values
4. Calculates error statistics
5. Creates plots and saves them as `integration_results.png`

## Methode (Method)

### Numerische Integration

Die Trapezregel wird verwendet:

```
integral[i] = integral[i-1] + 0.5 * (y[i] + y[i-1]) * dt
```

### Anfangsbedingungen

Die Anfangswerte für Geschwindigkeit und Weg werden aus den Referenzdaten übernommen:
- v(t=0) = v_ref(t=0)
- s(t=0) = s_ref(t=0)

## Ergebnisse (Results)

Die Implementierung erreicht sehr gute Übereinstimmung mit den Referenzwerten:

- **Geschwindigkeit (Velocity)**:
  - RMS Fehler: ~3.56e-02 m/s
  - Max. absoluter Fehler: ~5.03e-02 m/s

- **Weg (Position)**:
  - RMS Fehler: ~8.50e-04 m
  - Max. absoluter Fehler: ~1.39e-03 m

Die Plots zeigen, dass die berechneten Werte (rot gestrichelt) sehr gut mit den Referenzwerten (blau durchgezogen) übereinstimmen.

The implementation achieves very good agreement with reference values. The plots show that the calculated values (red dashed) match the reference values (blue solid) very closely.

## Dateien (Files)

- `avs.csv` - Eingabedaten (Input data)
- `integrate_acceleration.py` - Hauptskript (Main script)
- `requirements.txt` - Python-Abhängigkeiten (Python dependencies)
- `integration_results.png` - Ausgabegrafik (Output plot)
