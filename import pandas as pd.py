import pandas as pd
import requests
from datetime import date, time
import shutil, os
import csv

list=["LFBI","PATE","KGNB","OIMJ","EVRA"]

def airport_list():
    url="https://www.aviationweather.gov/docs/metar/stations.txt"
   
    # Utilisez requests.get() pour télécharger le contenu du fichier depuis l'URL
    response = requests.get(url)
    contenu_fichier = response.text
    return(contenu_fichier)



def get_metar(ma_liste):
    nom_fichier = '20230921_liste_METAR.txt'
    with open(nom_fichier, 'w') as fichier:
        
        for airport in ma_liste:
            chain="https://beta.aviationweather.gov/cgi-bin/data/metar.php?ids=" + airport + "&hours=500"
            data=requests.get(chain)
            result=data.text
            print(result)
            fichier.write(result)



airport_list=airport_list()
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

ma_liste = df['Code'].tolist()

get_metar(ma_liste)