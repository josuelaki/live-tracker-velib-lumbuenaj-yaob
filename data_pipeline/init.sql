DROP TABLE IF EXISTS stations;

CREATE TABLE stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE,
    velos_dispo INTEGER,
    places_dispo INTEGER
);