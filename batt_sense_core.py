import numpy as np
import pandas as pd
import hashlib
from scipy.interpolate import interp1d

# BATT-SENSE v205.5: PRODUCTION GUARD
VERSION_LABEL = "v205.5-production-guard"

# --- Eigene Exceptions (Production Grade Fehlerkultur) ---
class BattSenseError(Exception):
    """Basis-Exception für alle BATT-SENSE Fehler."""
    pass

class EmptyDataFrameError(BattSenseError):
    """Wird geworfen, wenn keine Daten übergeben werden."""
    pass

class DataFormatError(BattSenseError):
    """Wird geworfen, wenn essentielle Spalten ('freq', 'real', 'imag') fehlen."""
    pass

class BattSenseV205_5:
    def __init__(self, mu_limit=0.85, phys_limit=0.50):
        # Schwellenwerte können jetzt bei Initialisierung überschrieben werden
        self.mu_limit = mu_limit
        self.phys_limit = phys_limit
        self.target_log_freq = np.linspace(3, -1, 40)

    def execute(self, raw_df, battery_id="UNKNOWN", label=None):
        # 1. Strenge Input-Validierung (Fail Fast Mechanismus)
        if raw_df is None or raw_df.empty or len(raw_df) < 5:
            raise EmptyDataFrameError(f"[{battery_id}] DataFrame ist leer oder hat zu wenig Datenpunkte (min. 5).")
        
        required_columns = {'freq', 'real', 'imag'}
        if not required_columns.issubset(raw_df.columns):
            raise DataFormatError(f"[{battery_id}] Fehlende Spalten. Erwartet: {required_columns}")

        try:
            # 2. Datenbereinigung
            df = raw_df.dropna(subset=['freq', 'real', 'imag']).sort_values("freq", ascending=False).reset_index(drop=True)
            
            # 3. Robust ECI Berechnung
            phase = np.arctan2(-df['imag'], df['real'])
            log_f_source = np.log10(df['freq'])
            f_interp = interp1d(log_f_source, phase, bounds_error=False, fill_value="extrapolate")
            uniform_phase = f_interp(self.target_log_freq)
            eci = round(float(np.mean(np.abs(np.gradient(uniform_phase))) * 15), 4)
            
            # 4. Physics Check
            correlation = np.corrcoef(np.gradient(df['real']), np.gradient(df['imag']))[0, 1]
            phys_consistency = round(float(correlation), 4)

            # 5. Audit Entscheidung
            is_stable = eci < self.mu_limit
            is_physical = phys_consistency > self.phys_limit
            verdict = "USABLE" if (is_stable and is_physical) else "REJECT"

            return {
                "battery_id": battery_id,
                "verdict": verdict,
                "metrics": {"eci": eci, "phys_consistency": phys_consistency},
                "ground_truth": label,
                "audit_hash": hashlib.sha256(df.to_json().encode()).hexdigest()[:12]
            }
        except Exception as e:
            # Unerwartete Berechnungsfehler als Basis-Exception weitergeben
            raise BattSenseError(f"[{battery_id}] Interner Berechnungsfehler: {str(e)}")
