#!/usr/bin/env python
# coding: utf-8

# DWD_hist_weather.py
#
# (c) 2021 Holger Leerhoff
#
# Dieses Notebook importiert Daten aus dem umfangreichen OpenData-Angebot
# des Deutschen Wetterdienstes (DWD) in ein Pandas-Dataframe.
#
# Regionalität
#
# Die Auswahl der Wetterstationen erfolgt hier nach Bundesländern. Auf
# Grundlage des Bundeslands werden alle dort befindlichen Wetterstationen
# ermittelt, deren historische und aktuelle Daten heruntergeladen, extrahiert
# und (hier am Beispiel der Temperatur) in ein DataFrame geladen und können
# dann weiter ausgewertet werden.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import fnmatch

DWD_PFAD = 'https://opendata.dwd.de/climate_environment/CDC/' \
           'observations_germany/climate/daily/kl/historical/'

# Hier wird zur Selektion der Wetterstationen das Bundesland im Klartext
# festgelegt.

BUNDESLAND = 'Berlin'

# %% Laden der historischen und aktuellen Wetterstationen vom
# DWD-OpenData-Server. Infos, Datensatzbeschreibung etc. hier:
# https://opendata.dwd.de/climate_environment/CDC/observations_germany/
# climate/daily/kl/historical/

url = DWD_PFAD + 'KL_Tageswerte_Beschreibung_Stationen.txt'
stationen = pd.DataFrame()
stationen = pd.read_fwf(url,
                        encoding='ISO-8859-1',
                        header=None,
                        skiprows=[0, 1],
                        names=['Stations_id', 'von_datum', 'bis_datum',
                               'Stationshoehe', 'geoBreite', 'geoLaenge',
                               'Stationsname', 'Bundesland'])

# Aus dem Datensatz alle Stations-IDs nach Ländern extrahieren und als
# separate Listen mit den Ländernamen als Schlüssel in ein dictionary packen.

wetterstationen_ids = {}
for land in stationen['Bundesland'].unique():
    wetterstationen_ids[land] = stationen[stationen['Bundesland']
                                          == land]['Stations_id'].tolist()

# %% Zusammenstellen der URLs der ZIP-Archive der Wetterstationen vom
# DWD-OpenData-Server. Aufrufen der html-Seite, parsen mit BeautifulSoup,
# die entsprechenden URLs in einer Liste speichern.

wetterstationen_dateinamen = {}
page = requests.get(DWD_PFAD).text
soup = BeautifulSoup(page, 'html.parser')
for node in soup.find_all('a'):
    if node.get('href').startswith('tageswerte_KL_'):
        wetterstationen_dateinamen[int(node.text[14:19])] = node.text

# %% Die Wetterdaten ausgewählter Wetterstationen (als ZIP-Archiv) vom
# DWD-OpenData-Server ziehen, darin die eigentliche Datendatei finden und
# deren Inhalte einlesen.
# Error-Handling für Stationen ohne freie Daten.
# Missings (-999.0 beim DWD) durch System-Missings ersetzen.
# NB: Hier wird die Temperatur (TMK) ausgelesen, Modifikaton für andere
# Messwerte sind leicht möglich.

wetter = pd.DataFrame()
for station in wetterstationen_ids[BUNDESLAND]:
    try:
        url = DWD_PFAD + wetterstationen_dateinamen[station]
        gezippte_dateien = ZipFile(BytesIO(urlopen(url).read()))
        csv_dateiname = fnmatch.filter(gezippte_dateien.namelist(),
                                       "produkt*.txt")
        csv_daten = gezippte_dateien.open(*csv_dateiname)
        wetter = wetter.append(pd.read_csv(csv_daten,
                                           sep=';',
                                           na_values='-999.0',
                                           usecols=['STATIONS_ID',
                                                    'MESS_DATUM',
                                                    ' TMK'],
                                           parse_dates=['MESS_DATUM']))
        print('.', end='')
    except KeyError:  # für die Wetterstation liegen keine Daten vor
        print('-', end='')

wetter = wetter.rename(columns={'STATIONS_ID': 'Station',
                                'MESS_DATUM': 'Datum',
                                ' TMK': 'Temp'})


# %% Statiosdaten nach Tagesmittelwerten zusammenfassen

tageswerte = wetter[['Datum', 'Temp']].groupby('Datum').mean()

tageswerte['Jahr'] = tageswerte.index.year
tageswerte['Monat'] = tageswerte.index.month
tageswerte['Tag'] = tageswerte.index.dayofyear

# =============================================================================
# Beispiel-Auswertungen
#
# =============================================================================

# %% Heatmap der täglichen Durchschnittstemperaturen

ana = tageswerte.pivot(index='Jahr', columns='Tag', values='Temp')

f, ax = plt.subplots(figsize=(20, 10))
sns.heatmap(ana, vmin=-10, vmax=23, cmap="RdBu_r")
ax.axes.set_title("Tagesmitteltemperaturen", y=1.01)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_minor_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# %% Jährliche Durchschnittstemperaturen plus 5-Jahres-Mittel

ana = tageswerte.pivot('Jahr', 'Tag', 'Temp')
ana['Jahresmittel'] = ana.mean(axis=1)
ana['Jahresmittel5'] = ana['Jahresmittel'].rolling(5).mean()

plt.subplots(figsize=(20, 10))
sns.lineplot(data=ana, x='Jahr', y='Jahresmittel')
sns.lineplot(data=ana, x='Jahr', y='Jahresmittel5', color='red')
