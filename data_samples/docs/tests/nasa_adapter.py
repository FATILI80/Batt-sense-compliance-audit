import pandas as pd
import numpy as np
from benchmark_engine import BattSenseBenchmark

class NASAPCoEAdapter:
    """
    Adapter für das NASA PCoE Battery Dataset. 
    Konvertiert NASA-Strukturen in BATT-SENSE Audit-Objekte.
    """
    def __init__(self, auditor):
        self.benchmark = BattSenseBenchmark(auditor)

    def process_nasa_batch(self, nasa_raw_data_list):
        """
        nasa_raw_data_list: Liste von Dictionaries mit 'cycle', 'data', 'health_label'
        Label 0: Nominaler Zyklus (Early Life)
        Label 1: Artefakt/Degradation (End of Life / Sensor Drift)
        """
        for entry in nasa_raw_data_list:
            df = entry['data'] # Erwartet Spalten: freq, real, imag
            battery_id = f"NASA_B0005_Cycle_{entry['cycle']}"
            
            # Wir jagen die NASA-Daten durch den Benchmark
            self.benchmark.run_test_case(df, battery_id, entry['health_label'])

    def get_final_report(self):
        return self.benchmark.get_statistics()

# Beispiel für die Nutzung (Simulation)
if __name__ == "__main__":
    # HIER: Update auf Version 5
    from batt_sense_core import BattSenseV205_5
    
    # HIER: Korrekter Aufruf mit phys_limit
    auditor = BattSenseV205_5(phys_limit=0.50)
    adapter = NASAPCoEAdapter(auditor)
    
    # Dummy-Daten zur Demonstration der NASA-Logik
    fake_nasa_data = [{
        'cycle': 500, 
        'data': pd.DataFrame({'freq': [100, 10, 1], 'real': [0.02, 0.03, 0.05], 'imag': [-0.001, -0.01, -0.05]}),
        'health_label': 1 # Wir markieren diesen späten Zyklus als 'kritisch'
    }]
    
    adapter.process_nasa_batch(fake_nasa_data)
    stats = adapter.get_final_report()
    print(f"NASA Validation Success: {stats}")
