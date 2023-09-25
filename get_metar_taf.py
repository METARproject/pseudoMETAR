#####################################################################################
## prends en entrée la liste produite par "get_airport_list"
## Capte les METAR et TAF des aeroports contenus dans la liste pour les 21 derniers jours
##  Inscrit deux fichiers :
## 1 - liste_METAR.txt
## 2 - liste_TAF.txt
#####################################################################################


import pandas as pd
import requests
from datetime import date, time
import shutil, os
import csv


def get_metar(ma_liste):
    nom_fichier = '20230924_liste_METAR.txt'
    with open(nom_fichier, 'w') as fichier:
        
        for airport in ma_liste:
            chain="https://beta.aviationweather.gov/cgi-bin/data/metar.php?ids=" + airport + "&hours=500"
            data=requests.get(chain)
            result=data.text
            if result=="":
                result=airport+" : Pas de Metars dans les 21 derniers jours"
            print(result)
            fichier.write(result)

def get_taf(ma_liste):
    nom_fichier = '20230925_liste_TAF.txt'
    with open(nom_fichier, 'w') as fichier:
        
        for airport in ma_liste:
            chain="https://beta.aviationweather.gov/cgi-bin/data/taf.php?ids=" + airport + "&hours=500"
            data=requests.get(chain)
            result=data.text
            if result=="":
                result=airport+" : Pas de TAF dans les 21 derniers jours"
            print(result)
            fichier.write(result)


nom_fichier_csv = 'ma_liste.csv'
# Initialisez une liste vide pour stocker les données
ma_liste = []
# Ouvrez le fichier CSV en mode lecture
#le fichier liste de codes2 ets une copie du fichier liste de codes dont j'ai enlevé les lignes vides avec excel à la main
with open("liste_codes.csv", 'r') as fichier_csv:
    # Créez un objet reader CSV
    reader = csv.reader(fichier_csv)
        # Parcourez les lignes du fichier CSV et ajoutez-les à la liste
    for ligne in reader:
        ma_liste.extend(ligne)

get_metar(ma_liste)
get_taf(ma_liste)