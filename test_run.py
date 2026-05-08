import pandas as pd
import sys
import os

# Pfad-Korrektur, damit batt_sense_core im Hauptverzeichnis gefunden wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from batt_sense_core import BattSenseV205_3

def main():
    auditor = BattSenseV205_3()
    print("--- BATT-SENSE v205.5 Integration Test ---")

    # 1. Test: Leere Daten (Der Bug-Check für den Production Guard)
    print("\nTest 1: Leerer DataFrame...")
    empty_df = pd.DataFrame()
    report_empty = auditor.execute(empty_df, battery_id="EMPTY_TEST")
    print(f"Ergebnis: {report_empty['verdict']} (Erwartet: INVALID)")

    # 2. Test: Reale Daten (ID01)
    print("\nTest 2: Reale Messdaten (ID01)...")
    try:
        # Pfad geht eine Ebene hoch zu data_samples
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data_samples', 'ID01.csv')
        df = pd.read_csv(data_path)
        report_real = auditor.execute(df, battery_id="ID01_TEST")
        print(f"Ergebnis: {report_real['verdict']} | ECI: {report_real['metrics']['eci']}")
    except Exception as e:
        print(f"Hinweis: Konnte ID01.csv nicht laden ({e}). Prüfe die Ordnerstruktur.")

if __name__ == "__main__":
    main()
