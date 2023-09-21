import pandas as pd
import requests
from datetime import date, time
import shutil, os

list=["LFBI","PATE","KGNB","OIMJ","EVRA"]

def airport_list():
    url="https://www.aviationweather.gov/docs/metar/stations.txt"
   
    # Utilisez requests.get() pour télécharger le contenu du fichier depuis l'URL
    response = requests.get(url)
    contenu_fichier = response.text
    return(contenu_fichier)



def get_metar(list):
    METAR=[]

    for airport in list:
        chain="https://beta.aviationweather.gov/cgi-bin/data/metar.php?ids=" + airport + "&hours=500"
        data=requests.get(chain)
        result=data.text
        return result

airport_list=airport_list()
# Ouvrir un fichier en mode écriture
with open('stations.txt', 'w') as fichier:
    # Écrire des données dans le fichier
    fichier.write(airport_list)

with open('stations.txt', 'r') as fichier:
    lignes = fichier.readlines()

# Créez un DataFrame à partir de la liste des lignes
df = pd.DataFrame({'texte': lignes})   

#supprime les lignes de moins de 45 caracteres
df.dropna()

#supprime les lignes de moins de 45 caracteres
df = df[df['texte'].apply(lambda x: len(x) >= 45)]
df.reset_index(drop=True, inplace=True)

#supprime les lignes qui commencent par !
df = df[~df['texte'].str.startswith('!')]

#supprime les lignes dont le premier mot contient plus de deux caracteres
df = df[df['texte'].apply(lambda x: len(x.split()[0]) <= 2)]
df.reset_index(drop=True, inplace=True)

# supprimer les lignes qui commencentt par CD STATION
masque = ~df['texte'].str.startswith('CD STATION')
# Appliquez le masque pour filtrer les lignes du DataFrame
df = df[masque]
# Réindexez le DataFrame résultant
df.reset_index(drop=True, inplace=True)

print(df)