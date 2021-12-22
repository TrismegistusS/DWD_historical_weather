#!/usr/bin/env python
# coding: utf-8

# DWD_hist_weather.py
#
# (c) 2021 Holger Leerhoff
#
# Dieses Modul importiert Daten aus dem umfangreichen OpenData-Angebot
# des Deutschen Wetterdienstes (DWD) in ein Pandas-Dataframe.
#
# Regionalität
#
# Die Auswahl der Wetterstationen erfolgt hier nach Bundesländern. Auf
# Grundlage des Bundeslands werden alle dort befindlichen Wetterstationen
# ermittelt, deren historische und aktuelle Daten heruntergeladen, extrahiert
# und (hier am Beispiel der Temperatur) in ein DataFrame geladen und können
# dann weiter ausgewertet werden.

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import fnmatch

def tageswerte_land(auswertungsland, still=False, protokoll=False):
    """
    Parameters
    ----------
    land : Name of federal state (required)
    still: suppress progess indicators (optional, default: False)
    protokoll: write wetterdaten.csv.gz (optional, default: False)
    Returns
    -------
    Pandas DataFrame with the state's daily average measured values:
    - TempMean, HumidityMean, TempMax, TempMin, SunshineDuration
    """
    DWD_PFAD = 'https://opendata.dwd.de/climate_environment/CDC/' \
               'observations_germany/climate/daily/kl/'
    assert auswertungsland in ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
                    'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
                    'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz',
                    'Saarland', 'Sachsen', 'Sachsen-Anhalt',
                    'Schleswig-Holstein', 'Thüringen'], 'Bitte Namem eines Bundeslands' \
                    ' als Parameter übergeben.'
    # Laden der Wetterstationen vom DWD-OpenData-Server. Infos, Datensatz-
    # beschreibung etc. hier: https://opendata.dwd.de/README.txt
    url = DWD_PFAD + 'historical/KL_Tageswerte_Beschreibung_Stationen.txt'
    stationen = pd.DataFrame()
    stationen = pd.read_fwf(url,
                            encoding='ISO-8859-1',
                            header=None,
                            skiprows=[0, 1],
                            names=['Stations_id', 'von_datum', 'bis_datum',
                                   'Stationshoehe', 'geoBreite', 'geoLaenge',
                                   'Stationsname', 'Bundesland'])
    # Aus dem Datensatz alle Stations-IDs nach Ländern extrahieren und als
    # separate Listen mit den Ländernamen als Schlüssel in dictionary packen.
    stationen_ids = {}
    for land in stationen['Bundesland'].unique():
        stationen_ids[land] = stationen[stationen['Bundesland']
                                        == land]['Stations_id'].tolist()
    # Zusammenstellen der URLs der ZIP-Archive der Wetterstationen vom
    # DWD-OpenData-Server. Aufrufen der html-Seite, parsen mit BeautifulSoup,
    # die entsprechenden URLs in einer Liste speichern.
    stationen_dateinamen = {}
    page = requests.get(DWD_PFAD+'historical').text
    soup = BeautifulSoup(page, 'html.parser')
    for node in soup.find_all('a'):
        if node.get('href').startswith('tageswerte_KL_'):
            stationen_dateinamen[int(node.text[14:19])] = node.text
    # Die Wetterdaten ausgewählter Wetterstationen (als ZIP-Archiv) vom
    # DWD-OpenData-Server ziehen, darin die eigentliche Datendatei finden und
    # deren Inhalte einlesen.
    # Zu allen Wetterstationen eine Datei mit aktuellen Wetterdaten suchen und
    # deren Inhalte einlesen.
    # Error-Handling für Stationen ohne freie / akt. Daten.
    # Hier werden ausgelesen:
    #  - das Tagesmittel der Temperatur in °C (TMK)
    #  - das Tagesmittel der relativen Feuchte in % (UPM)
    #  - das Tagesmaximum der Temeratur in 2m Höhe in °C (TXK)
    #  - das Tagesminimum der Temeratur in 2m Höhe in °C (TNK)
    #  - die tägliche Sonnenscheindauer in h (SDK)
    #  - das Tagesmittel der Windgeschwindigkeit im m/s
    # Im Datensatz sind noch weitere Messwerte vorhanden.
    wetter = pd.DataFrame()
    for station in stationen_ids[auswertungsland]:
        for typ in ['historical', 'recent']:
            try:
                if typ == 'historical':
                    url = DWD_PFAD+'historical/'+stationen_dateinamen[station]
                else:
                    url = DWD_PFAD+'recent/tageswerte_KL_' + \
                                   str(station).zfill(5)+'_akt.zip'
                gezippte_dateien = ZipFile(BytesIO(urlopen(url).read()))
                csv_dateiname = (fnmatch.filter(gezippte_dateien.namelist(),
                                 'produkt*.txt'))
                csv_daten = gezippte_dateien.open(*csv_dateiname)
                wetter = wetter.append(pd.read_csv(csv_daten,
                                                   sep=';',
                                                   usecols=['STATIONS_ID',
                                                            'MESS_DATUM',
                                                            ' TMK',
                                                            ' UPM',
                                                            ' TXK',
                                                            ' TNK',
                                                            ' SDK',
                                                            '  FM'],
                                                   parse_dates=['MESS_DATUM']))
                if not still:
                    print('.', end='')
            except KeyError:  # für die Wetterstation liegen keine Daten vor
                if not still:
                    print('-', end='')
            except IOError:  # für die Wetterstation liegen keine akt. Daten vor
                if not still:
                    print('-', end='')
    # Missings (-999.0) durch System-Missings ersetzen.
    wetter = (wetter.rename(columns={'STATIONS_ID': 'Station',
                                     'MESS_DATUM': 'Datum',
                                     ' TMK': 'TempMean',
                                     ' UPM': 'HumidityMean',
                                     ' TXK': 'TempMax',
                                     ' TNK': 'TempMin',
                                     ' SDK': 'SunshineDuration',
                                     '  FM': 'Windspeed'})
                    .replace(-999.0, np.nan))
    # Protokoll: gegebenenfalls großes DataFrame als komprimiertes csv speichern
    if protokoll:
        wetter.to_csv('./wetterprotokoll.csv.gz', index=False, compression='gzip')
    # Aus Stationsdaten regionale Tagesmittelwerte bilden
    tageswerte = wetter[['Datum', 'TempMean', 'HumidityMean', 'TempMax', 'TempMin',
                         'SunshineDuration', 'Windspeed']].groupby('Datum').mean()
    tageswerte['Jahr'] = tageswerte.index.year
    tageswerte['Monat'] = tageswerte.index.month
    tageswerte['Tag_des_Jahres'] = tageswerte.index.dayofyear
    return tageswerte

def tagestemp_land(auswertungsland, still=False):  # for backwards compatibility
    """
    Parameters
    ----------
    land : Name of federal state (required)
    still: suppress progess indicators (optional, default: False)

    Returns
    -------
    Pandas DataFrame with the state's daily average temeratures
    """
    tageswerte = tageswerte_land(auswertungsland)
    tageswerte = tageswerte[['TempMean', 'Jahr', 'Monat', 'Tag_des_Jahres']]
    tageswerte = tageswerte.rename(columns={'TempMean': 'Temp'})
    return tageswerte

# beim direkten Aufruf mit Land als Parameter jährlichen Temperaturdurchschnitt ausgeben
if __name__ == "__main__":
    import sys
    tageswerte = tageswerte_land(sys.argv[1])
    print(f'\nJähliche Durchschnittstemperturen für {sys.argv[1]}.')
    print(tageswerte.groupby('Jahr')['TempMean'].mean())
        