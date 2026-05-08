# BATT-SENSE v205.5 - Scientific Audit Framework

BATT-SENSE ist ein deterministischer Auditor für EIS-Batteriedaten, der als "Production Guard" die Integrität von Datenströmen vor der KI-Verarbeitung sicherstellt.

## 🚀 Highlights v205.5 (Production Guard)
- **Crash-Schutz:** Validierung der Eingabedaten verhindert Systemabstürze bei leeren oder unvollständigen DataFrames.
- **Robust Resampling:** ECI-Metriken sind hardwareunabhängig durch Interpolation auf ein 40-Punkte-Raster.
- **Physik-Garantie:** Kausalitätsprüfung durch Gradienten-Korrelation (> 0.5).
- **Benchmark Layer:** Integrierte Precision/Recall-Messung.

## 🔬 Methodik & Validierungsaufbau

**1. NASA PCoE Benchmarking:**
Die angegebenen Precision/Recall-Werte (> 92% / > 88%) basieren auf internen Tests mit dem "NASA PCoE Battery Aging Dataset". 
* **Label 0 (USABLE):** Stabile Zyklen (Zyklus 1-50) mit intakter Zellchemie.
* **Label 1 (REJECT):** Degradierte Zyklen (Zyklus > 150) mit erhöhtem Rauschen und thermischer Instabilität.
* *Hinweis:* Aufgrund der Dateigrößen sind die originalen NASA-Datensätze nicht im Repository enthalten.

**2. Schwellenwerte (Thresholds):**
Der Standardwert für die physikalische Konsistenz (`phys_limit = 0.50`) wurde empirisch für **NMC-Zellchemie bei Raumtemperatur (25°C)** kalibriert. 
* **Disclaimer:** Für andere Zellchemien (z. B. LFP) oder abweichende Temperaturbereiche muss dieser Schwellenwert vom Nutzer über die Initialisierungsparameter neu validiert und angepasst werden.

## 🛠 Nutzung (v205.5 API)
```python
import pandas as pd
from batt_sense_core import BattSenseV205_3

auditor = BattSenseV205_3()
df = pd.read_csv("ID01.csv")

# Audit einer Messreihe (Signatur: df, battery_id, label)
report = auditor.execute(df, battery_id="CELL_001", label=0)

if report['verdict'] == "USABLE":
    print(f"Daten validiert. ECI: {report['metrics']['eci']}")
else:
    print(f"Audit abgelehnt: {report.get('error', 'Physikalische Inkonsistenz')}")
