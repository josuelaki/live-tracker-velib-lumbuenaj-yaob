import sqlite3
import asyncio
import sys
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_pipeline import data_recupereation_donnees as upd

async def recup_data():
    upd.initialiser_bdd()
    while True:
        donnees = upd.recuperer_donnees_velib()
        upd.sauvegarder_donnees(donnees)

        await asyncio.sleep(5)

@asynccontextmanager
async def boucle(app: FastAPI):
    task = asyncio.create_task(recup_data())
    yield
    task.cancel()

app = FastAPI(lifespan=boucle)

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