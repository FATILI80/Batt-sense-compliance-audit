# BATT-SENSE v205.3 - Scientific Audit Framework

BATT-SENSE ist ein deterministischer Auditor für EIS-Batteriedaten. 

## Highlights v205.3 (Scientific Hardening)
- **Robust Resampling:** ECI-Metriken sind jetzt über verschiedene Datensätze (NASA PCoE, Oxford, CALCE) hinweg vergleichbar.
- **Benchmark Execution Layer:** Integrierte Funktionen zur Berechnung von Precision und Recall gegen Ground-Truth Labels.
- **Physik-Garantie:** Validierung der Kausalität durch Gradienten-Korrelation (> 0.5).

## Validierung
Das System wurde erfolgreich gegen reale Labordaten kalibriert. Die aktuelle Version minimiert False-Positives durch ein frequenz-normalisiertes Audit-Verfahren.

## Struktur
- `batt_sense_core.py`: Mathematischer Kern (v205.3)
- `tests/benchmark_engine.py`: Statistische Auswertung von Testreihen.
- `SOP_SWALLOW_27.md`: Messvorschrift.
