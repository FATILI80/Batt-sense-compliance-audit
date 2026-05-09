import pandas as pd
import numpy as np
from batt_sense_core import BattSenseV205_3

def generate_mock_nasa_data(is_degraded=False, seed=None):
    """Generiert deterministische Dummy-EIS-Daten für Benchmarks."""
    if seed is not None:
        np.random.seed(seed)
        
    freq = np.logspace(3, -1, 40)
    
    if is_degraded:
        # Rauschen und gebrochene Kausalität (Label 1 -> REJECT)
        real = np.linspace(0.01, 0.05, 40) + np.random.normal(0, 0.02, 40)
        imag = np.linspace(-0.01, -0.05, 40) + np.random.normal(0, 0.02, 40)
    else:
        # Saubere, gleichläufige Kurve (Label 0 -> USABLE)
        real = np.linspace(0.01, 0.05, 40)
        imag = np.linspace(-0.01, -0.05, 40)
    
    # Sicherstellen, dass die Spaltennamen exakt dem API-Vertrag entsprechen
    return pd.DataFrame({'freq': freq, 'real': real, 'imag': imag})

def run_benchmark(n_samples_per_class=10):
    print("--- BATT-SENSE NASA PCoE Benchmark (Scientific Edition) ---")
    print(f"Generiere und validiere {n_samples_per_class * 2} synthetische Profile...\n")
    
    auditor = BattSenseV205_3(phys_limit=0.50)
    
    # Confusion Matrix Zähler
    true_positives = 0  # Defekt -> korrekt als REJECT erkannt
    false_positives = 0 # Sauber -> fälschlich als REJECT erkannt
    true_negatives = 0  # Sauber -> korrekt als USABLE erkannt
    false_negatives = 0 # Defekt -> fälschlich als USABLE durchgewunken
    errors = 0          # Code-Abstürze beim Audit
    
    # 1. Teste degradierte Zellen (Sollten REJECT sein)
    for i in range(n_samples_per_class):
        df = generate_mock_nasa_data(is_degraded=True, seed=i)
        try:
            res = auditor.execute(df, battery_id=f"NASA_BAD_{i}")
            if res['verdict'] == "REJECT":
                true_positives += 1
            else:
                false_negatives += 1
        except Exception:
            errors += 1

    # 2. Teste saubere Zellen (Sollten USABLE sein)
    for i in range(n_samples_per_class):
        # Offset für den Seed, damit saubere Profile unabhängig gewürfelt werden
        df = generate_mock_nasa_data(is_degraded=False, seed=i+1000)
        try:
            res = auditor.execute(df, battery_id=f"NASA_GOOD_{i}")
            if res['verdict'] == "REJECT":
                false_positives += 1
            else:
                true_negatives += 1
        except Exception:
            errors += 1

    # Berechnung der Metriken mit Schutz vor Division durch Null
    total_valid = (true_positives + false_positives + true_negatives + false_negatives)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    accuracy = (true_positives + true_negatives) / total_valid if total_valid > 0 else 0.0

    # Formatierter Output
    print("=== CONFUSION MATRIX ===")
    print(f"True Positives (Korrekt abgelehnt):  {true_positives}")
    print(f"True Negatives (Korrekt akzeptiert): {true_negatives}")
    print(f"False Positives (Falscher Alarm):    {false_positives}")
    print(f"False Negatives (Durchgerutscht):    {false_negatives}")
    
    if errors > 0:
        print(f"⚠️ Unerwartete Audit-Fehler:          {errors}")

    print("\n=== PERFORMANCE METRIKEN ===")
    print(f"Precision (Vorhersagegenauigkeit): {precision * 100:.1f}%")
    print(f"Recall (Erkennungsrate defekt):    {recall * 100:.1f}%")
    print(f"Accuracy (Gesamte Trefferquote):   {accuracy * 100:.1f}%\n")

if __name__ == "__main__":
    # Du kannst hier die Zahl beliebig erhöhen (z.B. 100) für massivere Stresstests
    run_benchmark(n_samples_per_class=10)
