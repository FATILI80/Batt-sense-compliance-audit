import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import logging
from datetime import datetime

class BattSenseLogger:
    @staticmethod
    def get_logger():
        logger = logging.getLogger("BATT-SENSE-GUARD")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

class PhysicalValidator:
    @staticmethod
    def check_consistency(df):
        try:
            grad_real = np.gradient(df['real'])
            grad_imag = np.gradient(df['imag'])
            correlation = np.corrcoef(grad_real, grad_imag)[0, 1]
            return round(float(correlation), 4)
        except: return 0.0

class StabilityValidator:
    def __init__(self, target_log_freq):
        self.target_log_freq = target_log_freq

    def calculate_eci(self, df):
        try:
            phase = np.arctan2(-df['imag'], df['real'])
            log_f_source = np.log10(df['freq'])
            f_interp = interp1d(log_f_source, phase, bounds_error=False, fill_value="extrapolate")
            uniform_phase = f_interp(self.target_log_freq)
            eci = np.mean(np.abs(np.gradient(uniform_phase))) * 15
            return round(float(eci), 4)
        except: return 99.0

class BattSenseGuardV205_5:
    def __init__(self, mu_limit=0.85, phys_limit=0.50):
        self.mu_limit = mu_limit
        self.phys_limit = phys_limit
        self.logger = BattSenseLogger.get_logger()
        self.target_log_freq = np.linspace(3, -1, 40)
        self.stability_engine = StabilityValidator(self.target_log_freq)
        self.phys_engine = PhysicalValidator()

    def validate_input(self, df):
        if df is None or df.empty: return False, "Leer"
        if not {'freq', 'real', 'imag'}.issubset(df.columns): return False, "Spalten fehlen"
        if (df['freq'] <= 0).any(): return False, "Frequenz <= 0"
        return True, "OK"

    def execute_audit(self, raw_df, battery_id="UNKNOWN"):
        is_valid, msg = self.validate_input(raw_df)
        if not is_valid: return {"battery_id": battery_id, "verdict": "REJECT", "reason": msg}

        df = raw_df.dropna().sort_values("freq", ascending=False).reset_index(drop=True)
        eci = self.stability_engine.calculate_eci(df)
        phys = self.phys_engine.check_consistency(df)
        
        verdict = "USABLE" if (eci < self.mu_limit and phys > self.phys_limit) else "REJECT"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "battery_id": battery_id,
            "verdict": verdict,
            "metrics": {"eci": eci, "phys_consistency": phys}
        }
