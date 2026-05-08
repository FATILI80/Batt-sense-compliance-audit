# BATT-SENSE v205.1 - Compliance Support Architecture

BATT-SENSE ist ein deterministischer Audit-Layer für elektrochemische Impedanzspektroskopie (EIS). Er dient als prozessuales Qualitäts-Gate für Batteriedaten, bevor diese in KI-Diagnosemodelle oder den Digitalen Batteriepass fließen.

## ⚠️ Wichtiger Disclaimer (Haftungsausschluss)
BATT-SENSE prüft die numerische und prozessuale Konsistenz der Daten. Die Ergebnisse (ECI, SoH-Proxy) stellen eine empirische Einschätzung dar und keine absolute physikalische Wahrheit. Dieses Tool ersetzt keine zertifizierte Konformitätsbewertung gemäß der EU-Batterieverordnung 2023/1542. Die Nutzung erfolgt auf eigene Gefahr.

## Kern-Architektur
- **L0 Ingest:** Robuste Vorverarbeitung mit MAD-Filter und Lückenerkennung.
- **L1/L2 Engine:** Empirical Consistency Index (ECI) zur numerischen Prüfung.
- **v205 Compliance Support:** Temperatur-Kompensation (Arrhenius) & SoH-Power-Proxy.
- **Triple-Lock Governance:** Traceability durch Daten-, Config- und Prozedur-Hashes.

## Schnellstart
Um das Audit-Verfahren zu starten, wird der `BattSenseCore` initialisiert. Die Messungen müssen dem **Swallow-27 Protokoll** entsprechen (siehe `SOP_SWALLOW_27.md`).

```python
from batt_sense_core import BattSenseV205_1

# Initialisierung mit dem Standard-Profil
bs = BattSenseV205_1(profile="NMC811_BASELINE_v1")
report = bs.execute(raw_df, temp_c=25.0, soc_pct=90, battery_id="CELL-XYZ")
print(report)

