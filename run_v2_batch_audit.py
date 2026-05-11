from batt_sense_v2_core import BattSenseGuardV205_5
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# BATT-SENSE v2 BATCH RUNNER
# ============================================================

def run_demonstration():
    # 1. Initialisierung des Guards aus der Core-Datei
    guard = BattSenseGuardV205_5()
    
    print(f"--- BATT-SENSE v2 Batch Audit gestartet ({datetime.now().strftime('%H:%M:%S')}) ---")

    # 2. Simulation einer Test-Flotte (Batch)
    # In einem echten Szenario würden hier CSV-Dateien geladen werden
    test_fleet = [
        {
            "id": "ZELLE-LFP-001-OK", 
            "data": pd.DataFrame({
                'freq': np.logspace(3, -1, 15),
                'real': np.linspace(0.05, 0.15, 15),
                'imag': -np.sin(np.linspace(0, np.pi, 15)) * 0.05
            })
        },
        {
            "id": "ZELLE-NMC-999-ERROR", 
            "data": pd.DataFrame({
                'freq': [1000, 500, 100], 
                'real': [0.1, 0.1, 0.1], 
                'imag': [0, 0, 0] # Zu wenig/instabile Daten
            })
        }
    ]

    # 3. Verarbeitung und Reporting
    results = []
    for cell in test_fleet:
        print(f"Prüfe {cell['id']}...")
        report = guard.execute_audit(cell['data'], battery_id=cell['id'])
        results.append(report)
        print(f"  -> Ergebnis: {report['verdict']}")

    # 4. Zusammenfassung als CSV exportieren
    # Wir flachen das Dictionary ab, damit es eine saubere Tabelle gibt
    df_summary = pd.json_normalize(results)
    output_file = "audit_summary_v2.csv"
    df_summary.to_csv(output_file, index=False)
    
    print(f"\n--- Batch abgeschlossen. Bericht gespeichert unter: {output_file} ---")

if __name__ == "__main__":
    run_demonstration()
