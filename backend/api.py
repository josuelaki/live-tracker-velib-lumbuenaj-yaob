import sqlite3

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def root():
    return {"Hello" : "World"}


@app.get("/stations")
def get_stations():
    connect = sqlite3.connect("../data_pipeline/velib.db")
    connect.row_factory = sqlite3.Row
    curseur = connect.cursor()
    requete = "SELECT * FROM stations"
    curseur.execute(requete)

    data = curseur.fetchall()
    connect.close

    stations = [dict(ligne) for ligne in data]

    return stations