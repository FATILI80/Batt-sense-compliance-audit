# BATT-SENSE v205.5 - Scientific Audit Framework (Proof of Concept)

BATT-SENSE ist ein deterministischer Auditor für EIS-Batteriedaten. Dieses Projekt (Alpha-Status) demonstriert einen Pre-Validation-Layer, um die Integrität von Datenströmen vor der KI-Verarbeitung zu prüfen.

## 🚀 Highlights v205.5
- **Crash-Schutz:** Validierung der Eingabedaten verhindert Systemabstürze.
- **Robust Resampling:** Hardwareunabhängige ECI-Metriken durch Interpolation auf ein 40-Punkte-Raster.
- **Gradienten-Korrelation:** Prüfung der Gleichläufigkeit von Real- und Imaginärteil (Default-Threshold > 0.5 für NMC-Chemie).

## 🔬 Methodik & NASA-Validierung
Die ursprünglichen Tests (>92% Precision) wurden gegen das NASA PCoE Battery Dataset gefahren. Da diese Rohdaten zu groß für GitHub sind, beinhaltet dieses Repository das Skript `nasa_benchmark.py`, welches die Evaluationslogik (Precision/Recall Matrix) anhand von synthetischen/reduzierten Profilen transparent macht. 

* **Label 0 (USABLE):** Stabile Zyklen (intakte Zellchemie).
* **Label 1 (REJECT):** Degradierte Zyklen (Rauschen/Instabilität).
* *Disclaimer:* Der Schwellenwert von 0.5 ist empirisch für NMC bei 25°C ermittelt und muss für andere Chemien kalibriert werden.

## 📂 Struktur
- `batt_sense_core.py`: Kern-Logik mit Exception-Handling.
- `nasa_benchmark.py`: Transparenz-Skript für die Metrik-Berechnung.
- `test_run.py`: Lokaler Integrationstest.
- `SOP_SWALLOW_27.md`: Verfahrensanweisung.
