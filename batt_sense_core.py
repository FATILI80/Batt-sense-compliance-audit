import numpy as np
import pandas as pd
import hashlib
from scipy.interpolate import interp1d

# BATT-SENSE v205.3: SCIENTIFIC HARDENING
VERSION_LABEL = "v205.3-scientific-baseline"
VERSION_HASH = hashlib.sha256(VERSION_LABEL.encode()).hexdigest()[:8]

class BattSenseV205_3:
    def __init__(self):
        # Kalibrierte Schwellenwerte
        self.mu_limit = 0.85
        self.phys_limit = 0.50
        # Einheitliches Frequenz-Raster für ECI-Vergleichbarkeit
        self.target_log_freq = np.linspace(3, -1, 40) # 1000Hz bis 0.1Hz

    def _get_robust_eci(self, df):
        """Berechnet ECI unabhängig vom Sampling-Schema des Messgeräts."""
        try:
            phase = np.arctan2(-df['imag'], df['real'])
            log_f_source = np.log10(df['freq'])
            
            # Interpolation auf das Standard-Raster (macht NASA/Oxford vergleichbar)
            f_interp = interp1d(log_f_source, phase, bounds_error=False, fill_value="extrapolate")
            uniform_phase = f_interp(self.target_log_freq)
            
            eci = np.mean(np.abs(np.gradient(uniform_phase))) * 15
            return round(float(eci), 4)
        except:
            return 1.0 # Fallback bei Fehlern

    def execute(self, raw_df, battery_id="UNKNOWN", label=None):
        # Datenreinigung (Physik-Schutz: wir lassen die Rohdaten für den Check intakt)
        df = raw_df.dropna().sort_values("freq", ascending=False).reset_index(drop=True)
        
        # 1. Robust ECI
        eci = self._get_robust_eci(df)
        
        # 2. Physikalische Konsistenz
        correlation = np.corrcoef(np.gradient(df['real']), np.gradient(df['imag']))[0, 1]
        phys_consistency = round(float(correlation), 4)

        # 3. Urteil
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
