import numpy as np
import pandas as pd
import hashlib
from scipy.interpolate import interp1d

class BattSenseV205_3:
    def __init__(self):
        self.mu_limit = 0.85
        self.phys_limit = 0.50
        # Ziel-Raster für den ECI-Check (1000Hz bis 0.1Hz, log-skaliert)
        self.target_log_freq = np.linspace(3, -1, 40)

    def _get_robust_eci(self, df):
        """Berechnet ECI auf einem einheitlichen Frequenz-Raster."""
        phase = np.arctan2(-df['imag'], df['real'])
        log_f_source = np.log10(df['freq'])
        
        # Interpolation auf Standard-Raster
        try:
            f_interp = interp1d(log_f_source, phase, bounds_error=False, fill_value="extrapolate")
            uniform_phase = f_interp(self.target_log_freq)
            # Berechnung des Gradienten auf dem uniformen Raster
            eci = np.mean(np.abs(np.gradient(uniform_phase))) * 15 # Skalierungsfaktor angepasst
            return round(float(eci), 4)
        except:
            return 1.0 # Fallback bei korrupten Daten

    def execute(self, raw_df, battery_id="UNKNOWN", label=None):
        # Physik-Check bleibt (Gradienten-Korrelation)
        df = raw_df.dropna().sort_values("freq", ascending=False).reset_index(drop=True)
        
        eci = self._get_robust_eci(df)
        correlation = np.corrcoef(np.gradient(df['real']), np.gradient(df['imag']))[0, 1]
        phys_consistency = round(float(correlation), 4)

        is_stable = eci < self.mu_limit
        is_physical = phys_consistency > self.phys_limit
        verdict = "USABLE" if (is_stable and is_physical) else "REJECT"

        return {
            "battery_id": battery_id,
            "verdict": verdict,
            "eci": eci,
            "phys_consistency": phys_consistency,
            "ground_truth": label # Hier speichern wir das externe Label
        }
