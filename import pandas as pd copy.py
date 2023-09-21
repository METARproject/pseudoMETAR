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

#supprime les lignes vides
df.dropna()

#supprime les lignes qui commencent par !
df = df[~df['texte'].str.startswith('!')]

df['Nom'] = df['texte'].str.slice(2, 20)
df['Code'] = df['texte'].str.slice(20, 24)
df = df.drop(columns=['texte'])
print(df)
df.to_csv('stations.csv', index=False)