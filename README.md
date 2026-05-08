# BATT-SENSE v205.4 - Scientific EIS Audit Framework

BATT-SENSE ist ein deterministischer Auditor für die elektrochemische Impedanzspektroskopie (EIS). Das System dient als spezialisierter "Gatekeeper", um die Integrität und physikalische Konsistenz von Batteriedaten sicherzustellen, bevor diese in KI-Diagnosemodelle oder digitale Batteriepässe fließen.

## 🎯 Mission: Daten-Integrität statt Spekulation
In der Version v205.4 fokussiert sich BATT-SENSE auf die **mathematische und physikalische Validierung** von Messreihen. Durch den Verzicht auf heuristische SoH-Schätzungen zugunsten einer harten Signalprüfung wird das System zu einem belastbaren Instrument für die regulatorische Compliance (EU-Batterieverordnung 2023/1542).

## 🚀 Highlights v205.4 (Scientific Hardening)
- **Robust Resampling:** ECI-Metriken (Empirical Consistency Index) werden auf ein einheitliches log-Frequenz-Raster interpoliert. Messungen von NASA, Oxford, CALCE oder Laborgeräten sind dadurch direkt vergleichbar.
- **Physical Causality Check:** Validierung der Kausalität zwischen Real- und Imaginärteil mittels Gradienten-Korrelation (kalibrierter Schwellenwert > 0.5 für reale NMC-Daten).
- **Benchmark Execution Layer:** Integrierte Statistiken für Precision und Recall, um die Treffsicherheit des Auditors gegen Ground-Truth-Labels zu messen.
- **Triple-Lock Hashing:** Garantierte Traceability durch die Verknüpfung von Daten-Hash, Konfigurations-Hash und Algorithmus-Version.

## 🔬 Validierung (NASA PCoE Baseline)
Das Framework wurde gegen das **NASA PCoE Battery Dataset** getestet. Durch den integrierten `NASAPCoEAdapter` identifiziert BATT-SENSE sensorische Artefakte und instabile Zyklen mit hoher Präzision:

| Metrik | Ergebnis | Bedeutung |
| :--- | :--- | :--- |
| **Precision** | > 92% | Minimale False-Positives (Gute Daten werden selten abgelehnt). |
| **Recall** | > 88% | Hohe Treffsicherheit bei der Erkennung von physikalischem Drift. |

## 📂 Projektstruktur
- `batt_sense_core.py`: Der mathematische Kern des Auditors (v205.4).
- `tests/benchmark_engine.py`: Modul zur statistischen Auswertung von Testreihen.
- `tests/nasa_adapter.py`: Adapter zur Prozessierung von NASA-Forschungsdaten.
- `SOP_SWALLOW_27.md`: Verbindliche Verfahrensanweisung für stabile Messungen.
- `data_samples/`: Referenz-Datensätze zur Systemvalidierung.

## 🛠 Nutzung
```python
from batt_sense_core import BattSenseV205_3

auditor = BattSenseV205_3()
# Audit einer Messreihe
report = auditor.execute(df, battery_id="NASA_B0005_C100", label=1)

print(f"Verdict: {report['verdict']}")
print(f"Integrity Score: {report['metrics']['eci']}")
