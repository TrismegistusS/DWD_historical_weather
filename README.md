# DWD_hist_weather.py

#### (c) Holger Leerhoff (2021)

Dieses Python-Skript importiert Daten aus dem umfangreichen OpenData-Angebot des Deutschen Wetterdienstes (DWD) in ein Pandas-Dataframe.

## Regionalität
Die Zusammenstellung der Wetterstationen erfolgt hier nach Bundesländern. Auf Grundlage des Bundeslands werden alle dort befindlichen Wetterstationen ermittelt, deren Daten heruntergeladen, extrahiert und (hier am Beispiel der Temperatur) und können dann weiter ausgewertet werden.

## Daten
- es wird aktuell nur die tägliche Temperatur (TMK) der Wetterstationen ausgelesen, Modifikaton für andere Messwerte (Druck, Niederschlag, Sonnenscheindauer etc.) sind leicht möglich
- es werden aktuell nur deren historische (bis vor 500 Tagen) Daten verarbeitet; eine Umstellung auf die aktuellen Daten (die letzten 500 Tage) ist leicht möglich

Richtlinien und Vorgaben für die Datennutzung des DWD, etwa die Zitierweise, finden sich auf deren Homepage.

## Zweck
Das Skript ist als Teilprodukt eines größeren Projekts entstanden und kann vielleicht als Grundlage für eigene Projekte dienen. DasSkript ist ausführlich kommentiert. Zwei kleine Beispielauswertungen (langfristige Entwicklung der täglichen und jährlichen Durchschnittstemperatur) sind angefügt.
