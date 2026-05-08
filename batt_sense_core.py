import numpy as np
import pandas as pd
import hashlib
import json
from dataclasses import dataclass
from typing import List, Dict, Tuple, Any
import time

# BATT-SENSE v205.1: INTEGRITY AUDITOR
VERSION_LABEL = "v205.1-integrity-auditor"
VERSION_HASH = hashlib.sha256(VERSION_LABEL.encode()).hexdigest()[:8]

@dataclass
class ComplianceAuditResult:
    battery_id: str
    verdict: str
    integrity_score: float
    metrics: Dict[str, float]
    metadata: Dict[str, Any]
    flags: List[str]
    audit_trail: Dict[str, str]

class BattSenseV205_1:
    def __init__(self):
        self.mu_limit = 0.85
        self.min_samples = 12

    def execute(self, raw_df: pd.DataFrame, temp_c: float, soc_pct: float, battery_id: str):
        # 1. Daten-Check (L0)
        df = raw_df.dropna(subset=["freq", "real", "imag"]).sort_values("freq", ascending=False).reset_index(drop=True)
        
        # 2. Rausch-Check (ECI)
        phase = np.arctan2(-df['imag'], df['real'])
        eci = round(float(np.mean(np.abs(np.gradient(phase, np.log10(df['freq'])))) * 5), 4)
        
        # 3. NEU: Konsistenz-Check (Physik-Check)
        # Wir schauen, ob Real- und Imaginärteil logisch zusammenpassen
        correlation = np.corrcoef(np.gradient(df['real']), np.gradient(df['imag']))[0, 1]
        phys_consistency = round(float(correlation), 4)

        # 4. Urteilsbildung
        is_stable = eci < self.mu_limit
        is_physical = phys_consistency > 0.7  # Ein Wert unter 0.7 deutet auf Messfehler hin
        
        verdict = "USABLE" if (is_stable and is_physical) else "REJECT"
        
        flags = []
        if not is_stable: flags.append("HIGH_NOISE_DETECTED")
        if not is_physical: flags.append("PHYSICAL_INCONSISTENCY_DETECTED")

        # 5. Governance (Hashing)
        c_hash = hashlib.sha256(df.round(8).to_json(orient="split").encode()).hexdigest()[:16]

        return ComplianceAuditResult(
            battery_id=battery_id,
            verdict=verdict,
            integrity_score=round(1.0 - (eci/5), 4),
            metrics={"eci": eci, "phys_consistency": phys_consistency},
            metadata={"temp_c": temp_c, "soc_pct": soc_pct},
            flags=flags,
            audit_trail={"data_hash": c_hash, "proc_hash": VERSION_HASH}
        )
