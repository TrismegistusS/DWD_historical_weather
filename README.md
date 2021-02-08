# DWD_hist_weather.py

#### (c) Holger Leerhoff (2021)

*This Python script imports data from the Deutscher Wetterdienst's open data service into a Pandas dataframe. I suspect most people interested in this script are speaking German. Should there be need for an English version please open an issue. Thanks!*

Dieses Python-Skript importiert Daten aus dem umfangreichen OpenData-Angebot des Deutschen Wetterdienstes (DWD) in ein Pandas-Dataframe.

## Regionalität
Die Zusammenstellung der Wetterstationen erfolgt hier nach Bundesländern. Auf Grundlage des Bundeslands werden alle dort befindlichen Wetterstationen ermittelt, deren tagesgenaue Daten (hier am Beispiel der Temperatur)  heruntergeladen und und können dann weiter ausgewertet werden.

## Daten
- es wird aktuell nur die tägliche Temperatur (TMK) der Wetterstationen ausgelesen, Modifikationen für andere/zusätzliche Messwerte (Druck, Niederschlag, Sonnenscheindauer etc.) sind leicht möglich
- es werden aktuell nur historische (bis vor 500 Tagen) Daten verarbeitet; eine Umstellung auf aktuelle Daten (die letzten 500 Tage) ist leicht möglich

Richtlinien und Vorgaben für die Datennutzung des DWD, etwa die Zitierweise, finden sich auf deren Homepage.

## Zweck
Das Skript ist als Teilprodukt eines größeren Projekts entstanden und soll als Grundlage für eigene Projekte dienen. Das Skript ist ausführlich kommentiert. Zwei kleine Beispielauswertungen (langfristige Entwicklung der täglichen und jährlichen Durchschnittstemperatur) sind angefügt.
