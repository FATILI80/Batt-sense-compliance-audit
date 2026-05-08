import pandas as pd
import sys
import os

# Pfad anpassen, damit der Core gefunden wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from batt_sense_core import BattSenseV205_1

def run_system_check():
    # Beispiel-Daten (NMC-Charakteristik)
    data = {
        "freq": [1000, 100, 10, 1, 0.1],
        "real": [0.0142, 0.0145, 0.0150, 0.0160, 0.0180],
        "imag": [-0.0001, -0.0010, -0.0050, -0.0100, 0.0]
    }
    df = pd.DataFrame(data)
    
    bs = BattSenseV205_1()
    print("--- BATT-SENSE SYSTEM CHECK ---")
    try:
        report = bs.execute(df, temp_c=25.0, soc_pct=100, battery_id="INTERNAL-TEST-001")
        print(report)
    except Exception as e:
        print(f"Fehler beim Systemcheck: {e}")

if __name__ == "__main__":
    run_system_check()
