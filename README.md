# BATT-SENSE Compliance Audit 🛡️
## Repository Struktur

Dieses Projekt bietet zwei Ansätze zur Batterie-Diagnose:

* **v1 (Standard):** `batt_sense_core.py` & `run_audit.py`
    * Leichtgewichtiges Skript für schnelle Einzel-Audits. Ideal für explorative Datenanalyse.
* **v2 (Enterprise):** `batt_sense_v2_core.py` & `run_v2_batch_audit.py`
    * Modulare Architektur mit strikter Trennung von Logik und Validierung.
    * Integrierter Trace-Logger und automatisierte Batch-Verarbeitung für industrielle Testreihen.
    * Exportiert detaillierte Audit-Reports als CSV.

**Version: v205.5-production-guard**

Dieses Repository fungiert als strenger **"digitaler Türsteher"** für Batterie-Impedanzdaten. Es filtert unphysikalischen Datenmüll heraus und stellt die Qualität von Messungen sicher, bevor diese in komplexe ML-Pipelines oder Analysen fließen.

## Der Unterschied: BATT-SENSE vs. klassische Methoden
Während etablierte wissenschaftliche Ansätze wie die Kramers-Kronig-Transformation (K-K) lediglich prüfen, ob Daten physikalisch möglich ("wahr") sind, geht dieses Compliance-Audit-Tool einen entscheidenden Schritt weiter – es prüft, ob die Daten **"gut genug"** für industrielle Standards sind.

* **Ganzheitliche Audit-Prüfung:** Das Tool prüft neben der physikalischen Konsistenz auch die Einhaltung von Spezifikationsgrenzen (Compliance).
* **Rausch- und Artefakt-Erkennung:** Es filtert spezifisch nach Messfehlern, die durch die Sensorik selbst (z. B. Sense-Leitungen) entstehen.
* **Automatisierung für große Datensätze:** Optimiert für den Einsatz in Produktionslinien, um Tausende von Messungen automatisch zu sortieren und fehlerhafte Datensätze frühzeitig (Fail-Fast) abzufangen.

## Key Features (v205.5)
- ✅ **Fail-Fast Validierung:** Sofortiger Abbruch bei leeren Daten oder fehlenden Spalten.
- ✅ **Physikalischer Check:** Korrelationsprüfung zwischen Real- und Imaginärteil-Gradienten.
- ✅ **NaN-Protection:** Integrierter Schutz vor mathematischen Fehlern bei Frequenzen ≤ 0.
- ✅ **ECI-Metrik:** Berechnung des Electrochemical Integrity Index zur Stabilitätsprüfung.

---

## Schnellstart & Verwendung

### Installation
Stellen Sie sicher, dass die grundlegenden mathematischen Bibliotheken installiert sind:
```bash
pip install numpy pandas scipy
import pandas as pd
from batt_sense_core import BattSenseV205_5

# 1. Messdaten laden
df = pd.read_csv("messdaten.csv")

# 2. Auditor initialisieren (Schwellenwerte können hier angepasst werden)
auditor = BattSenseV205_5(phys_limit=0.50, mu_limit=0.85)

# 3. Audit ausführen
try:
    report = auditor.execute(df, battery_id="BAT-001")
    
    # 4. Ergebnis auswerten
    print("=== AUDIT REPORT ===")
    print(f"Ergebnis: {report['verdict']}") # Gibt "USABLE" oder "REJECT" zurück
    print(f"Physikalische Konsistenz: {report['metrics']['phys_consistency']}")
    print(f"ECI (Signalstabilität): {report['metrics']['eci']}")

except Exception as e:
    print(f"Fehler beim Audit: {e}")
 BATT-SENSE schließt die Lücke zwischen reiner Forschung (wie Lin-KK) und hardwaregebundener Hersteller-Software durch eine unabhängige, softwarebasierte Prüfung. Es vereinheitlicht verschiedene Datenquellen und prüft sie gegen vordefinierte Compliance-Regeln.
​Status: Proof of Concept. Entwickelt für die industrielle Qualitätssicherung von EIS-Daten.
## Validierung & Stress-Test (NASA Dataset ID54)

Um die Zuverlässigkeit von **BATT-SENSE v2** zu demonstrieren, wurde das System mit realen Labordaten (NASA PCoE) sowie manipulierten Fehler-Daten getestet:

| Test-Szenario | ECI-Stabilität (Ziel < 0.85) | Physik-Check (Ziel > 0.50) | Urteil |
| :--- | :--- | :--- | :--- |
| **Original NASA ID54** | **0.068** ✅ | **0.554** ✅ | **USABLE** |
| **Manipuliert (Rauschen)**| **9.447** ❌ | **0.164** ❌ | **REJECT** |

### Analyse
1. **Präzision:** Der `StabilityValidator` erkennt selbst feinste Unregelmäßigkeiten. Bei realen, gesunden Daten liegt der ECI-Wert nahe 0.
2. **Sicherheit:** Bei simuliertem Messrauschen (Wackelkontakt/EMV-Störung) schlägt das System sofort Alarm und verhindert die Weiterverarbeitung fehlerhafter Daten.

