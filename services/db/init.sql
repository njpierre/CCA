CREATE TABLE IF NOT EXISTS data (
    id SERIAL PRIMARY KEY,
    "Date" DATE,
    "Produit" TEXT,
    "Catégorie" TEXT,
    "Prix" INT, 
    "Quantité" INT,
    "Total" INT
);

COPY data(Date, Produit, Catégorie, Prix, Quantité, Total)
FROM '/docker-entrypoint-initdb.d/data.csv'
DELIMITER ';' 
CSV HEADER;