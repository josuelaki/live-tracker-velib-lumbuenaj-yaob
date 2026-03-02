import requests

def recuperer_donnees_velib():
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100"

    try:
        reponse = requests.get(url, timeout = 10) # Récupération des données vélib

        reponse.raise_for_status()

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
            print(f"Station {nom_station}, il y a {velos_dispo} velos dispo et {places_dispo} places disponible")

