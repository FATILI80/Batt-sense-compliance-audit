import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

class BattSenseError(Exception):
    """Basis-Exception für BATT-SENSE Fehler."""
    pass

class BattSenseV205_5:
    """
    BATT-SENSE Core Audit Engine (v205.5 - Clean Version)
    Fokus: Datenintegrität und physikalische Plausibilität von EIS-Daten.
    """
    def __init__(self, mu_limit=0.85, phys_limit=0.50):
        self.mu_limit = mu_limit
        self.phys_limit = phys_limit

    def _validate_input(self, df, battery_id):
        """Prüft die Struktur der Eingangsdaten."""
        if df is None or df.empty:
            raise BattSenseError(f"[{battery_id}] DataFrame ist leer.")
        
        required_cols = ['freq', 'real', 'imag']
        if not all(col in df.columns for col in required_cols):
            raise BattSenseError(f"[{battery_id}] Fehlende Spalten. Erforderlich: {required_cols}")
        
        # Schutz vor ungültigen Frequenzen für Log-Berechnungen
        if (df['freq'] <= 0).any():
             raise BattSenseError(f"[{battery_id}] Ungültige Frequenzwerte (<= 0) gefunden.")
        
        return df.sort_values('freq', ascending=False)

    def _calculate_eci(self, df):
        """
        Berechnet den Electrical Consistency Index (ECI).
        Heuristische Bewertung der Phasenstabilität über das Frequenzspektrum.
        """
        phase = np.angle(df['real'] + 1j*df['imag'], deg=True)
        log_freq = np.log10(df['freq'])
        
        # Interpolation auf einheitliches Raster (40 Punkte)
        # Verhindert Fehler bei unterschiedlichen Messauflösungen
        f_interp = interp1d(log_freq, phase, kind='linear', fill_value="extrapolate")
        target_log_freq = np.linspace(log_freq.max(), log_freq.min(), 40)
        uniform_phase = f_interp(target_log_freq)
        
        # ECI = Mittlerer Gradient der Phase (ohne künstliche Skalierung)
        eci = np.mean(np.abs(np.gradient(uniform_phase)))
        return float(eci)

    def execute(self, raw_df, battery_id="UNKNOWN", label=None):
        """
        Führt das vollständige Audit durch.
        label: Erwartetes Ergebnis für den Benchmark (0=USABLE, 1=REJECT).
        """
        try:
            df = self._validate_input(raw_df, battery_id)
            
            # 1. Stabilitäts-Check
            eci = self._calculate_eci(df)
            
            # 2. Physik-Check (Gradienten-Korrelation)
            # Schutz vor NaN bei konstanten Werten
            corr_matrix = np.corrcoef(np.gradient(df['real']), np.gradient(df['imag']))
            correlation = corr_matrix[0, 1]
            phys_consistency = 0.0 if np.isnan(correlation) else round(float(correlation), 4)

            # 3. Entscheidungs-Logik (Binär nach SOP)
            # Wichtig: ECI Limit muss ggf. angepasst werden, da *15 entfernt wurde.
            # Ein ECI von 0.056 (alt) entsprach ca. 0.85 (alt mit *15). 
            # Wir nutzen hier 0.1 als neuen, ehrlichen Schwellenwert.
            is_stable = eci < 0.1 
            is_physical = phys_consistency > self.phys_limit
            
            verdict = "USABLE" if (is_stable and is_physical) else "REJECT"

            return {
                "battery_id": battery_id,
                "eci": round(eci, 4),
                "phys_consistency": phys_consistency,
                "verdict": verdict,
                "ground_truth": label
            }

        except Exception as e:
            # Explizite Fehlermeldung statt magischer Zahlen
            raise BattSenseError(f"Audit-Fehler bei {battery_id}: {str(e)}")

# Benchmark-Klasse für die automatisierte Validierung
class BattSenseBenchmark:
    def __init__(self, auditor):
        self.auditor = auditor
        self.results = []

    def add_test_case(self, df, battery_id, expected_label):
        try:
            # Übergabe des Labels an die execute-Methode
            report = self.auditor.execute(df, battery_id=battery_id, label=expected_label)
            self.results.append(report)
        except Exception as e:
            print(f"Benchmark-Warnung für {battery_id}: {e}")

    def evaluate(self):
        tp = fp = tn = fn = 0
        for r in self.results:
            flagged = 1 if r["verdict"] == "REJECT" else 0
            actual = r.get("ground_truth")
            
            if actual is None: continue

            if flagged == 1 and actual == 1: tp += 1
            elif flagged == 1 and actual == 0: fp += 1
            elif flagged == 0 and actual == 1: fn += 1
            elif flagged == 0 and actual == 0: tn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        print("\n--- BATT-SENSE VALIDATION REPORT ---")
        print(f"Precision: {precision:.2%}")
        print(f"Recall:    {recall:.2%}")
        print(f"Stats:     TP={tp}, FP={fp}, TN={tn}, FN={fn}")
        return {"precision": precision, "recall": recall}
