
# Projet Cloud Computing : Dashboard des ventes d'une entreprise

Ce projet est une application d'analyse de données utilisant **Flask** et **Dash** pour l'affichage des graphiques interactifs. Les données sont stockées dans une base de données **PostgreSQL**, et un pipeline ETL permet de les charger automatiquement.
Ces données sont fictives et ne servent qu'à montrer comment mettre en place une application dans un docker.

## Installation & Exécution

###  **Prérequis**
- **Docker** installé sur votre ordinateur
- **Docker Compose** pour gérer les services

### **Coment Démarrer l'application**

1. **Cloner le projet**
   ```sh
   git clone https://github.com/njpierre/CCA
   
   cd CCA
   ```
3. **Lancer Docker Compose**
   ```sh
   docker compose up --build
   ```
   

###  **Accès à l'application**

 **Copier l'URL :**  `http://localhost:5000/dash/` 


##  **Architecture des Services**

### **Services Déployés**

1. **PostgreSQL (db)** : Stocke les données.
2. **ETL (etl)** : Charge "data.csv" dans PostgreSQL.
3. **Analytics (analytics)** : Fournit les API Flask & le Dashboard Dash.

### **Structure du projet**


 ```
CCA/
│── docker-compose.yml       # Configuration Docker
│
├── services/
│   ├── db/                  # Service de base de données
│   │   ├── data.csv         # Données brutes
│   │   ├── database.db      # Base de données SQLite
│   │   ├── Dockerfile       # Image Docker pour la base de données
│   │   ├── init.sql         # Script d'initialisation de la DB
│   │
│   ├── etl/                 # Service ETL pour transformation des données
│   │   ├── etl.py           # Script ETL principal
│   │   ├── requirements.txt # Dépendances pour l'ETL
│   │   ├── Dockerfile       # Image Docker pour l'ETL
│   │
│   ├── analytics/           # Service Analytics pour le dashboard
│   │   ├── app.py           # Point d'entrée principal
│   │   ├── database.py      # Connexion à la base de données
│   │   ├── server.py        # Serveur Flask
│   │   ├── layout.py        # Définition du layout Dash
│   │   ├── callbacks.py     # Gestion des callbacks Dash
│   │   ├── charts.py        # Génération des graphiques
│   │   ├── requirements.txt # Dépendances pour Analytics
│   │   ├── Dockerfile       # Image Docker pour Analytics
│   │
│── .git/                    # Référentiel Git
│── README.md                 # Documentation du projet
```

## **Débogage & Résolution des Problèmes**
 
### **Vérifier si les conteneurs tournent**
```sh
docker ps -a
```
 
###  **Voir les logs des services**
```sh
docker logs -f cca-analytics-1  # Logs du service Analytics
```
 
###  **Se connecter à PostgreSQL**
```sh
docker exec -it cca-db-1 psql -U user -d analytics_db
```
 
###  **Supprimer et reconstruire les volumes (si problème de données)**
 ```sh
docker compose down
 
docker compose up --build
```
