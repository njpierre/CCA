
# Projet Cloud Computing : Dashboard des ventes d'une entreprise

Ce projet est une application d'analyse de données utilisant **Flask** pour les API et **Dash** pour l'affichage des graphiques interactifs. Les données sont stockées dans une base de données **PostgreSQL**, et un pipeline ETL permet de les charger automatiquement.
Ces données sont fictives et ne servent qu'à montrer comment mettre en place une application dans un docker.

## Installation & Exécution

###  **Prérequis**
- **Docker** installé sur votre ordinateur
- **Docker Compose** pour gérer les services

### **Coment Démarrer l'application**

1. **Cloner le projet**
   
   `git clone https://github.com/njpierre/CCA`
   
   `cd CCA`

3. **Lancer Docker Compose**
   
   `docker-compose up --build`
   

###  **Accès à l'application**

 **Copier l'URL :**  `http://localhost:5000/dash/` 


##  **Architecture des Services**

### **Services Déployés**

1. **PostgreSQL (db)** : Stocke les données.
2. **ETL (etl)** : Charge "data.csv" dans PostgreSQL.
3. **Analytics (analytics)** : Fournit les API Flask & le Dashboard Dash.

### **Structure du projet**


 **CCA**/
│──  **docker-compose.yml**      : Configuration des services Docker

│──  **services**/

│   ├──  **db**/                 : Service de base de données PostgreSQL

│   │   ├──  **init.sql**         : Script SQL pour créer la table

│   │   ├──  **data.csv**         : Fichier de données

│   ├──  **etl**/                : Pipeline ETL

│   │   ├──  **etl.py**           : Script pour charger les données

│   ├──  **analytics**/          : Service Flask & Dash

│   │   ├──  **app.py**          : Serveur Flask & Dash

│   │   ├──  **layout.py**       : Layout de l'interface Dash

│   │   ├──  **callbacks.py**    : Callbacks pour interactivité Dash

## **Débogage & Résolution des Problèmes**
 
### **Vérifier si les conteneurs tournent**
 
`docker ps -a`
 
###  **Voir les logs des services**
 
`docker logs -f cca-analytics-1  # Logs du service Analytics`
 
###  **Se connecter à PostgreSQL**
 
`docker exec -it cca-db-1 psql -U user -d analytics_db`
 
###  **Supprimer et reconstruire les volumes (si problème de données)**
 
`docker compose down -v`
 
`docker compose up --build`
