import numpy as np
import pandas as pd
import hashlib
import json
from dataclasses import dataclass
from typing import List, Dict, Tuple, Any
import time

# BATT-SENSE v205.1: COMPLIANCE SUPPORT ARCHITECTURE
VERSION_LABEL = "v205.1-compliance-support-beta"
VERSION_HASH = hashlib.sha256(VERSION_LABEL.encode()).hexdigest()[:8]

@dataclass
class ComplianceAuditResult:
    battery_id: str
    verdict: str
    soh_proxy_pct: float
    metrics: Dict[str, float]
    metadata: Dict[str, Any]
    flags: List[str]
    audit_trail: Dict[str, str]

class CalibrationRegistry:
    _PROFILES = {
        "NMC811_BASELINE_v1": {
            "min_samples": 12,
            "mu_limit": 0.85,
            "rs_nominal_25c": 0.0142, 
            "arrhenius_beta": 3000,
            "soh_caution_limit": 80.0
        }
    }
    @classmethod
    def get_config(cls, profile_name: str):
        cfg = cls._PROFILES.get(profile_name)
        if not cfg: raise ValueError(f"ERR_PROFILE_NOT_FOUND: {profile_name}")
        cfg_hash = hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:8]
        return cfg, cfg_hash

class DataIngestV205_1:
    def __init__(self, config: Dict): self.cfg = config
    def prepare(self, raw_df: pd.DataFrame, temp_c: float, soc_pct: float, battery_id: str):
        if not (0 <= soc_pct <= 100): raise ValueError("INVALID_SOC")
        df = raw_df.dropna(subset=["freq", "real", "imag"]).sort_values("freq", ascending=False).reset_index(drop=True)
        if len(df) < self.cfg["min_samples"]: raise ValueError("INSUFFICIENT_DATA")
        z_abs = np.sqrt(df['real']**2 + df['imag']**2)
        median_z = z_abs.median()
        mad_z = (z_abs - median_z).abs().median()
        if mad_z > 0:
            z_mod = (z_abs - median_z).abs() / (1.4826 * mad_z)
            df = df[z_mod <= 3.5].reset_index(drop=True)
        return df, {"temp_c": temp_c, "soc_pct": soc_pct, "battery_id": battery_id}

class SoHEngineV205_1:
    def __init__(self, config: Dict): self.cfg = config
    def process_indicators(self, df: pd.DataFrame, temp_c: float) -> Tuple[float, float]:
        rs_measured = float(df.iloc[0]['real'])
        t_ref_k, t_meas_k = 298.15, temp_c + 273.15
        beta = self.cfg.get("arrhenius_beta", 3000)
        rs_norm = rs_measured / np.exp(beta * (1/t_meas_k - 1/t_ref_k))
        soh_proxy = max(0, min(100, round((2 - (rs_norm / self.cfg["rs_nominal_25c"])) * 100, 1)))
        return soh_proxy, round(rs_norm, 5)

class BattSenseV205_1:
    def __init__(self, profile="NMC811_BASELINE_v1"):
        self.cfg, self.cfg_hash = CalibrationRegistry.get_config(profile)
        self.ingest = DataIngestV205_1(self.cfg)
        self.engine = SoHEngineV205_1(self.cfg)
    def execute(self, raw_df: pd.DataFrame, temp_c: float, soc_pct: float, battery_id: str):
        df, meta = self.ingest.prepare(raw_df, temp_c, soc_pct, battery_id)
        phase = np.arctan2(-df['imag'], df['real'])
        eci = round(float(np.mean(np.abs(np.gradient(phase, np.log10(df['freq'])))) * 5), 4)
        soh_p, rs_n = self.engine.process_indicators(df, temp_c)
        is_consistent = eci < self.cfg["mu_limit"]
        verdict = "REJECT" if not is_consistent else "USABLE" if soh_p >= self.cfg["soh_caution_limit"] else "CAUTION"
        c_hash = hashlib.sha256(df.round(8).to_json(orient="split").encode()).hexdigest()[:16]
        return ComplianceAuditResult(battery_id, verdict, soh_p, {"eci": eci, "rs_norm_25c": rs_n}, meta, 
                                     [] if is_consistent else ["NUMERICAL_INSTABILITY"],
                                     {"data_hash": c_hash, "cfg_hash": self.cfg_hash, "proc_hash": VERSION_HASH})
