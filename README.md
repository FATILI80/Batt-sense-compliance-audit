# BATT-SENSE Compliance Audit 🛡️
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
