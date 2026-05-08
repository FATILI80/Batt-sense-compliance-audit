# SOP: BATT-SENSE Swallow-27 Verfahren

Dieses Dokument definiert die verbindlichen Handlungsschritte zur Datenerhebung für die BATT-SENSE v205.1 Engine.

## 1. Das Swallow-Prinzip (Stabilisierung)
Um Messartefakte durch elektrochemische Instabilität (Drift) zu vermeiden:
- Die Zelle muss vor dem EIS-Sweep **mindestens 27 Sekunden** im stromlosen Zustand (OCV) ruhen.
- Die Temperaturmessung muss direkt am Zellgehäuse erfolgen (mittig).

## 2. Parameter-Vorgaben
- **Frequenzbereich:** 10 kHz bis 0.1 Hz (Minimum).
- **Amplitude:** Max. 5% des Nennstroms (Linearitätsgebot).
- **Metadaten-Pflicht:** `temp_c`, `soc_pct`, `battery_id`.

## 3. Akzeptanz-Matrix (Audit)
- **USABLE:** ECI < 0.85 UND SoH-Proxy >= 80%
- **CAUTION:** ECI < 0.85 UND SoH-Proxy < 80%
- **REJECT:** ECI >= 0.85 ODER Stability Variance > 0.0004 Ohm
