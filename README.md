# DWD_hist_weather.py

#### (c) Holger Leerhoff (2021)

*A simple and lightweight Python module importing data from the Deutscher Wetterdienst's open data service into a Pandas DataFrame. I suspect most people interested in this script are speaking German. Should there be need for an English version please open an issue. Thanks!*

Dieses Python-Modul importiert Daten aus dem umfangreichen OpenData-Angebot des Deutschen Wetterdienstes (DWD) in ein Pandas-Dataframe.

## Regionalität
Die Zusammenstellung der Wetterstationen erfolgt nach Bundesländern. Auf Grundlage des Bundeslands werden alle dort befindlichen Wetterstationen ermittelt, eine Reihe deren tagesgenauer Messwerte heruntergeladen und können dann weiter ausgewertet werden.

## Daten
Es werden sowohl die historischen (bis vor 500 Tagen) als auch die aktuellen Daten (die letzten 500 Tage) verarbeitet, in der Regel bekommt man also *sehr* lange Zeitreihen bis ins 19. Jahrhundert zurück.

Aktuell werden ausgelesen:
    - das Tagesmittel der Temperatur in °C (TMK)
    - das Tagesmittel der relativen Feuchte in % (UPM)
    - das Tagesmaximum der Temeratur in 2m Höhe in °C (TXK)
    - das Tagesminimum der Temeratur in 2m Höhe in °C (TNK)
    - die tägliche Sonnenscheindauer in h (SDK)

Im DWD-Datensatz sind noch weitere Messwerte vorhanden, Modifikationen für andere/zusätzliche Messwerte sind leicht möglich.

Richtlinien und Vorgaben für die Datennutzung des DWD, etwa die Zitierweise, finden sich auf deren Homepage.

Bei häufigem Einsatz empfiehlt es sich möglicherweise, die Wetterdaten etwa als pickle zwischenzuspeichern, um die DWD-Server zu schonen. Im Beispiel-Notebook ist das implementiert.

## Zweck
Das Modul ist als Teilprodukt eines größeren Projekts entstanden und kann so wie es ist benutzt werden oder als Grundlage für eigene Projekte dienen. Das Skript ist ausführlich kommentiert. Zwei kleine Beispielauswertungen (langfristige Entwicklung der täglichen und jährlichen Durchschnittstemperatur) finden sich exemplarisch im Beispiel-Notebook.
