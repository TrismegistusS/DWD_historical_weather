# DWD_hist_weather.py

#### (c) Holger Leerhoff (2021)

Dieses Notebook importiert Daten aus dem umfangreichen OpenData-Angebot des Deutschen Wetterdienstes (DWD) in ein Pandas-Dataframe.

## Regionalität
Die Auswahl der Wetterstationen erfolgt hier nach Bundesländern. Auf Grundlage des Bundeslands werden alle dort befindlichen Wetterstationen ermittelt, deren historische und aktuelle Daten heruntergeladen, extrahiert und (hier am Beispiel der Temperatur) in ein DataFrame geladen und können dann weiter ausgewertet werden.

## Daten
Hier wird aktuell lediglich die tägliche Temperatur (TMK) der Wetterstationen ausgelesen, Modifikaton für andere Messwerte sind aber leicht möglich. Zwei kleine Beispielauswertungen (Entwicklung der täglichen und jährlichen Durchschnittstemperatur) sind angefügt.

Der Deutsche Wetterdienst (DWD) hat ein großartiges OpenData-Angebot. Richtlinien und Vorgaben für die Datennutzung finden sich auf der Webseite des DWD.

## Zweck
Das Skript ist als Teilprodukt eines größeren Projekts entstanden und kann vielleicht als Grundlage für eigene Projekte dienen. Dazu ist das Skript auch ausführlich kommentiert.
