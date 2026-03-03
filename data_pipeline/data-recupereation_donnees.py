import requests
import sqlite3

def recuperer_donnees_velib():
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100"

    try:
        reponse = requests.get(url, timeout = 10) # Récupération des données vélib, au cas ou sécurité 10s 

        reponse.raise_for_status() # Vérifie que le code de retour de la request est bien 200 sinon lève l'erreur

        print("Connexion réussie ! \n")
        donnees = reponse.json() # Conversion des données brute en json()

        liste_stations = donnees["results"] # On récupère que la partie results dans donnees 
        donnees_nettoye = []

        # Pour chaque stations dans la donnees on récupère le nom de la station 
        # le nombre de vélos dispo et de places dispo
        for station in liste_stations: 
            nom_station = station["name"]
            velos_dispo = station["numbikesavailable"]
            places_dispo = station["numdocksavailable"]

            donnees_nettoye.append({
                "nom" : nom_station,
                "velos_dispo" : velos_dispo,
                "places_dispo" : places_dispo
            })

        return donnees_nettoye
        
    except requests.exceptions.RequestException as erreur:
        print(f"Erreur critique lors de la connexion de l'API : {erreur}")
        return None

def initialiser_bdd():
    connexion = sqlite3.connect("velib.db")
    curseur = connexion.cursor()

    with open("init.sql", "r") as fichier_sql:
        requete_creation = fichier_sql.read()

    curseur.executescript(requete_creation)

    connexion.commit()
    connexion.close()

def sauvegarder_donnees(donnees):
    connexion = sqlite3.connect("velib.db")
    curseur = connexion.cursor()

    for station in donnees:
        requete = "INSERT INTO stations (nom, velos_dispo, places_dispo) VALUES (?, ?, ?)"
        valeurs = (station["nom"], station["velos_dispo"], station["places_dispo"])

        curseur.execute(requete, valeurs)

    connexion.commit()
    connexion.close()

if __name__ == "__main__":
    initialiser_bdd()
    mes_stations = recuperer_donnees_velib()
    
    if mes_stations:
        sauvegarder_donnees(mes_stations)
        print("PIPELINE TERMINÉ")
    else:
        print("ÉCHEC DU PIPELINE")