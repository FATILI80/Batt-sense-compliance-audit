import json

# ==========================================
# BATT-SENSE: Regulatory Compliance Module
# Fokus: EU 2023/1542 & DIN DKE SPEC 99100
# ==========================================

class RegulatoryGuard:
    def __init__(self, limits_config=None):
        # Gesetzliche Benchmarks (Ziele für 2031)
        self.limits = limits_config or {
            "min_recycled_cobalt": 0.16,
            "min_recycled_lithium": 0.06,
            "min_recycled_nickel": 0.06,
            "max_co2_threshold": 80.0  # kg CO2e/MWh (Lebenszyklus)
        }

    def run_audit(self, data):
        """Prüft Batterie-Metadaten gegen EU-Verordnung."""
        report = {"id": data["id"], "status": "PASS", "details": []}
        
        # 1. CO2-Audit (Intensität über Lebensdauer)
        total_delivered_energy = data["capacity_kwh"] * data["cycle_life"]
        co2_per_mwh = data["total_co2_kg"] / (total_delivered_energy / 1000)
        
        if co2_per_mwh > self.limits["max_co2_threshold"]:
            report["status"] = "FAIL"
            report["details"].append(f"CO2 Score: {co2_per_mwh:.2f} > {self.limits['max_co2_threshold']}")
        
        # 2. Recycling-Audit
        recycled = data["recycled_content"]
        for metal, rate in recycled.items():
            limit_key = f"min_recycled_{metal}"
            if limit_key in self.limits and rate < self.limits[limit_key]:
                report["status"] = "FAIL"
                report["details"].append(f"Recycled {metal} insufficient: {rate*100}% < {self.limits[limit_key]*100}%")
                
        return report

# ==========================================
# TEST-SUITE (Simulierter Durchlauf)
# ==========================================
if __name__ == "__main__":
    # Beispiel-Daten einer Batterie (NMC Chemie)
    battery_sample = {
        "id": "BAT-99-X-2026",
        "capacity_kwh": 75,
        "cycle_life": 2000,
        "total_co2_kg": 5500,
        "recycled_content": {
            "cobalt": 0.18,   # PASS
            "lithium": 0.04,  # FAIL (Ziel 6%)
            "nickel": 0.10    # PASS
        }
    }

    auditor = RegulatoryGuard()
    report = auditor.run_audit(battery_sample)

    print(f"--- BATT-SENSE COMPLIANCE REPORT ---")
    print(f"ID: {report['id']}")
    print(f"URTEIL: {report['status']}")
    if report['details']:
        for issue in report['details']:
            print(f" - WARNUNG: {issue}")
