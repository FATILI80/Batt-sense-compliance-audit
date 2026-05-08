# BATT-SENSE v205.2 - Deterministic Integrity Auditor

BATT-SENSE ist ein spezialisierter Audit-Layer für die elektrochemische Impedanzspektroskopie (EIS). Das System dient als "Gatekeeper" für Batteriedaten, um deren physikalische Konsistenz und Signalqualität sicherzustellen, bevor sie in Diagnose-Modelle oder digitale Batteriepässe einfließen.

## 🎯 Fokus: Datenintegrität statt Schätzung
Im Gegensatz zu herkömmlichen Modellen verzichtet BATT-SENSE v205.2 bewusst auf spekulative SoH-Schätzungen. Stattdessen liefert es ein deterministisches Audit-Urteil basierend auf der Signaltheorie und physikalischen Kausalität.

## Kern-Features (v205.2 Calibrated)
- **ECI (Empirical Consistency Index):** Quantifiziert das Signalrauschen in der Phasenebene.
- **Physical Correlation Check:** Validiert die Kausalität zwischen Real- und Imaginärteil (optimiert für reale NMC-Labordaten, Schwellenwert > 0.5).
- **Triple-Lock Traceability:** Garantierte Reproduzierbarkeit durch Hashing von Rohdaten, Konfiguration und Algorithmus-Version.
- **Compliance-Ready:** Entwickelt mit Blick auf die Anforderungen der EU-Batterieverordnung 2023/1542 (Batteriepass 2027).

## Architektur & Nutzung
Das System basiert auf dem **Swallow-27 Protokoll** (siehe `SOP_SWALLOW_27.md`), welches eine Stabilisierungszeit von 27 Sekunden vor der Messung vorschreibt.

### Schnellstart (Python)
```python
from batt_sense_core import BattSenseV205_1

# Initialisierung des Auditors
auditor = BattSenseV205_1()

# Audit ausführen
report = auditor.execute(raw_df, temp_c=25.0, soc_pct=90, battery_id="CELL-001")

if report.verdict == "USABLE":
    print(f"Daten validiert. Integrity Score: {report.integrity_score}")
else:
    print(f"Audit fehlgeschlagen: {report.flags}")
