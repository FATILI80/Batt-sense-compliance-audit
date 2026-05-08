import numpy as np
import pandas as pd
import hashlib
from scipy.interpolate import interp1d

# BATT-SENSE v205.5: PRODUCTION GUARD
VERSION_LABEL = "v205.5-production-guard"

class BattSenseV205_3:
    def __init__(self):
        self.mu_limit = 0.85
        self.phys_limit = 0.50
        self.target_log_freq = np.linspace(3, -1, 40)

    def execute(self, raw_df, battery_id="UNKNOWN", label=None):
        # --- TEST 3 FIX: Input Validation ---
        if raw_df is None or raw_df.empty or len(raw_df) < 5:
            return {
                "battery_id": battery_id,
                "verdict": "INVALID",
                "metrics": {"eci": 1.0, "phys_consistency": 0.0},
                "error": "Insufficient or empty data",
                "ground_truth": label
            }

        try:
            df = raw_df.dropna().sort_values("freq", ascending=False).reset_index(drop=True)
            
            # Robust ECI (v205.3 logic)
            phase = np.arctan2(-df['imag'], df['real'])
            log_f_source = np.log10(df['freq'])
            f_interp = interp1d(log_f_source, phase, bounds_error=False, fill_value="extrapolate")
            uniform_phase = f_interp(self.target_log_freq)
            eci = round(float(np.mean(np.abs(np.gradient(uniform_phase))) * 15), 4)
            
            # Physics Check
            correlation = np.corrcoef(np.gradient(df['real']), np.gradient(df['imag']))[0, 1]
            phys_consistency = round(float(correlation), 4)

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
            return {"battery_id": battery_id, "verdict": "ERROR", "error": str(e)}
