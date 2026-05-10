import pandas as pd
from batt_sense_core import BattSenseV205_3, EmptyDataFrameError, DataFormatError

def main():
    auditor = BattSenseV205_5()
    print("--- BATT-SENSE v205.5 Integration Test (Production Guard) ---")

    # Test 1: Leere Daten (Prüft das Exception-Handling)
    print("\nTest 1: Leerer DataFrame...")
    empty_df = pd.DataFrame()
    try:
        auditor.execute(empty_df, battery_id="EMPTY_TEST")
    except EmptyDataFrameError as e:
        print(f"Ergebnis: Exception korrekt ausgelöst und abgefangen! -> {e}")

    # Test 2: Reale Messdaten (Prüft die Validierung)
    print("\nTest 2: Reale Messdaten (ID01)...")
    try:
        df = pd.read_csv("ID01.csv") 
        report_real = auditor.execute(df, battery_id="ID01_TEST")
        print(f"Ergebnis: {report_real['verdict']} | ECI: {report_real['metrics']['eci']}")
    except FileNotFoundError:
        print("Hinweis: ID01.csv nicht gefunden. Prüfe, ob die Datei im Verzeichnis liegt.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()
