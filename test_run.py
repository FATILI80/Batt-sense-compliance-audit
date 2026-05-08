import pandas as pd
from batt_sense_core import BattSenseV205_3

# Initialisierung des Auditors (v205.5 Standard)
auditor = BattSenseV205_3()

def run_test():
    print("--- BATT-SENSE v205.5 Testlauf ---")
    
    # Test-Daten laden (Beispiel ID01)
    try:
        df = pd.read_csv("data_samples/ID01.csv")
    except FileNotFoundError:
        # Fallback für lokale Tests ohne Ordnerstruktur
        print("Hinweis: data_samples/ID01.csv nicht gefunden. Nutze Dummy-Daten.")
        df = pd.DataFrame({
            'freq': [1000, 100, 10, 1, 0.1],
            'real': [0.01, 0.02, 0.03, 0.04, 0.05],
            'imag': [-0.001, -0.005, -0.01, -0.02, -0.05]
        })

    # Audit ausführen (Signatur-Fix: Keine temp_c / soc_pct mehr)
    report = auditor.execute(df, battery_id="TEST-CELL-01", label=0)

    # Ergebnis-Ausgabe
    print(f"Audit-Urteil: {report['verdict']}")
    if "metrics" in report:
        print(f"ECI: {report['metrics']['eci']}")
        print(f"Phys. Konsistenz: {report['metrics']['phys_consistency']}")
    
    if "error" in report:
        print(f"Fehlermeldung: {report['error']}")

if __name__ == "__main__":
    run_test()
