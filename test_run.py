import pandas as pd
from batt_sense_core import BattSenseV205_3

def main():
    # Initialisierung des Auditors v205.5
    auditor = BattSenseV205_3()
    print("--- BATT-SENSE v205.5 Integration Test (Root-Check) ---")

    # Test 1: Leere Daten (Der Bug-Check für den Production Guard)
    print("\nTest 1: Leerer DataFrame...")
    empty_df = pd.DataFrame()
    report_empty = auditor.execute(empty_df, battery_id="EMPTY_TEST")
    print(f"Ergebnis: {report_empty['verdict']} (Erwartet: INVALID)")

    # Test 2: Reale Messdaten (Prüfung der CSV-Anbindung)
    print("\nTest 2: Reale Messdaten (ID01)...")
    try:
        # Da die CSV direkt im Hauptverzeichnis liegt:
        df = pd.read_csv("ID01.csv") 
        report_real = auditor.execute(df, battery_id="ID01_TEST")
        print(f"Ergebnis: {report_real['verdict']} | ECI: {report_real['metrics']['eci']}")
    except Exception as e:
        print(f"Hinweis: Konnte ID01.csv nicht laden ({e}).")

if __name__ == "__main__":
    main()
