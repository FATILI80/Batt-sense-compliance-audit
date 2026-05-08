# Scientific Limitations & Disclaimers

BATT-SENSE v205.5 ist als numerischer Audit-Layer konzipiert. Um Overclaiming zu vermeiden und wissenschaftliche Integrität zu wahren, werden hier die expliziten Grenzen des Frameworks dokumentiert.

## 1. Kein Ersatz für den Kramers-Kronig (KK) Test
Der Empirical Consistency Index (ECI) und die Gradienten-Korrelation messen numerische Glätte, Phasen-Jitter und Sampling-Stabilität. **Sie validieren keine Elektrochemie.** BATT-SENSE ist kein zertifizierter Lin-KK Test. Physikalisch inkonsistente Daten, die zufällig glatt verlaufen, können als False Negatives durch das Raster fallen.

## 2. Keine State of Health (SOH) Diagnose
Dieses Framework trifft **keine** Aussagen über den Gesundheitszustand, die Degradation oder die Lebensdauer der Batterie. Es prüft ausschließlich die Integrität des Datensatzes vor der Weitergabe an eine KI-Pipeline.

## 3. Heuristische Schwellenwerte
Der Threshold für die Gradienten-Korrelation (`> 0.5`) ist ein empirischer Richtwert, der für NMC-Zellen bei Raumtemperatur kalibriert wurde. Er stellt keine universelle physikalische Konstante dar. Für andere Zellchemien, extreme Temperaturen oder spezifische Niederfrequenz-Strukturen (z.B. ausgeprägte Warburg-Tails) muss dieser Wert vom Nutzer neu validiert werden.

## 4. Hardware-Abhängigkeit
Das Framework wurde primär gegen synthetische und referenzierte Daten (NASA PCoE) gebenchmarkt. Die Robustheit gegenüber spezifischem Hardware-Rauschen (z.B. von Arbin, BioLogic, Gamry oder Neware Messgeräten) sowie elektromagnetischen Interferenzen (EMI) im Feld ist derzeit explorativ und bedarf weiterer Validierung durch reale Hardware-Injections.

---
*Status: Dieses Projekt ist ein Proof of Concept. Es besitzt keine regulatorische Zertifizierung für industrielle oder sicherheitskritische Batterie-Diagnostik.*
