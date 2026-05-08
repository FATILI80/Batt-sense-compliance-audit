import pandas as pd
import numpy as np
from batt_sense_core import BattSenseV205_3

def generate_mock_nasa_data(is_degraded=False):
    """Generiert Dummy-EIS-Daten, die die Struktur der NASA-Daten nachbilden."""
    freq = np.logspace(3, -1, 40)
    if is_degraded:
        # Rauschen und gebrochene Kausalität (Label 1)
        real = np.linspace(0.01, 0.05, 40) + np.random.normal(0, 0.02, 40)
        imag = np.linspace(-0.01, -0.05, 40) + np.random.normal(0, 0.02, 40)
    else:
        # Saubere, gleichläufige Kurve (Label 0)
        real = np.linspace(0.01, 0.05, 40)
        imag = np.linspace(-0.01, -0.05, 40)
    
    return pd.DataFrame({'freq': freq, 'real': real, 'imag': imag})

def run_benchmark():
    print("--- BATT-SENSE NASA PCoE Benchmark (Transparenz-Lauf) ---")
    print("Hinweis: Evaluiert die Precision/Recall Logik mit synthetischen Profilen.\n")
    
    auditor = BattSenseV205_3(phys_limit=0.50)
    
    # Test-Set: 10 saubere Zellen, 10 degradierte Zellen
    true_positives = 0  # Richtig als kaputt erkannt
    false_positives = 0 # Fälschlicherweise als kaputt erkannt
    false_negatives = 0 # Fälschlicherweise als nutzbar durchgewunken
    
    # 1. Teste degradierte Zellen (Sollten REJECT sein)
    for i in range(10):
        df = generate_mock_nasa_data(is_degraded=True)
        res = auditor.execute(df, battery_id=f"NASA_BAD_{i}")
        if res['verdict'] == "REJECT":
            true_positives += 1
        else:
            false_negatives += 1

    # 2. Teste saubere Zellen (Sollten USABLE sein)
    for i in range(10):
        df = generate_mock_nasa_data(is_degraded=False)
        res = auditor.execute(df, battery_id=f"NASA_GOOD_{i}")
        if res['verdict'] == "REJECT":
            false_positives += 1

    # Metriken berechnen
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    print(f"Confusion Matrix Ergebnisse:")
    print(f"True Positives (Korrekt abgelehnt): {true_positives}")
    print(f"False Positives (Falscher Alarm): {false_positives}")
    print(f"False Negatives (Durchgerutscht): {false_negatives}\n")
    print(f"Berechnete Precision: {precision * 100:.1f}%")
    print(f"Berechneter Recall:   {recall * 100:.1f}%")

if __name__ == "__main__":
    run_benchmark()
