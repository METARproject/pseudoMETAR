#####################################################################################
##  Capte la liste des aeroports à jour.
##  Inscrit trois fichiers :
## 1 - stations initiales : fichier txt d'origine
## 2 - stations nettoyées : fichier .CSV contenant la liste nettoyée complete de l'ensemble des stations
## 3 - liste finale : fichier .CSV conrtenant la liste des noms et codes des stations
#####################################################################################

import pandas as pd
import requests
import csv

def airport_list():
    url="https://www.aviationweather.gov/docs/metar/stations.txt"
   
    # Utilisez requests.get() pour télécharger le contenu du fichier depuis l'URL
    response = requests.get(url)
    airport_list = response.text

    # Ouvrir un fichier en mode écriture
    with open('stations_initiales.txt', 'w') as fichier:
        # Écrire des données dans le fichier
        fichier.write(airport_list)

    with open('stations_initiales.txt', 'r') as fichier:
        lignes = fichier.readlines()

    # Créez un DataFrame à partir de la liste des lignes
    df = pd.DataFrame({'texte': lignes})   
    print("DF de base : ", df.count())

    #########################################################################
    # NETTOYAGE DE LA LISTE
    #########################################################################

    #supprime les lignes qui commencent par !
    df = df[~df['texte'].str.startswith('!')]
    print("DF sans ! : ", df.count())

    #supprime les lignes vides
    df.dropna()
    print("DF dopna : ", df.count())

    #supprime les lignes de titre
    masque = df['texte'].str.contains('CD  STATION', case=False)
    df = df[~masque]
    print("DF sans station : ", df.count())

    #supprime les lignes qui ne contiennent pas de lettres
    masque = df['texte'].str.contains('[a-zA-Z]', na=False)
    df = df[masque]
    print("DF sans lettres : ", df.count())

    #supprime les lignes qui ne contiennent pas de lettres
    masque = df['texte'].apply(lambda x: len(str(x)) >= 80)
    df = df[masque]
    print("DF trop courts : ", df.count())


    #########################################################################
    # ENREGISTREMENT DE LA VERSION NETTOYEE
    #########################################################################

    df.to_csv('stations_nettoyees.csv', index=False)

    #########################################################################
    # SUPRESSION DES COLONNES INUTILES
    #########################################################################

    df['Nom'] = df['texte'].str.slice(2, 20)
    df['Code'] = df['texte'].str.slice(20, 24)
    
    df = df.drop(columns=['texte'])
    df.reset_index(drop=True, inplace=True)

    print("Version_finale : ",df)
    df.to_csv('stations_finales.csv', index=False)

    #########################################################################
    # SUPRESSION DES LIGNES SANS CODES (A FAIRE)
    #########################################################################

        

    #retourne la liste des codes OAIC des aéroports sous forme d'une liste permettant d'aller capter les METAR et TAF

    ma_liste = df['Code'].tolist()
    return (ma_liste)

ma_liste=airport_list()
with open("liste_codes.csv", 'w', newline='') as fichier_csv:
    # Créez un objet writer CSV
    writer = csv.writer(fichier_csv)
    # Écrivez la liste dans le fichier CSV en tant que ligne unique
    writer.writerow(ma_liste)

