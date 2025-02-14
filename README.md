
# Projet Cloud Computing - Pipeline d'Analyse de Données
```
# 📌 Projet CCA - Flask & Dash avec PostgreSQL

Ce projet est une application d'analyse de données utilisant **Flask** pour les API et **Dash** pour l'affichage des graphiques interactifs. Les données sont stockées dans une base de données **PostgreSQL**, et un pipeline ETL permet de les charger automatiquement.

---

## 🚀 Installation & Exécution

### 🔧 **Prérequis**
- `Docker` installé sur votre machine
- `Docker Compose` pour gérer les services

### 📦 **Démarrer l'application**

1. **Cloner le projet**
   ```sh
   git clone <repo-url>
   cd <nom_du_dossier>
   ```
2. **Lancer Docker Compose**
   ```sh
   docker-compose up --build
   ```

📌 **Attends quelques secondes** que tous les services démarrent.

### 🖥 **Accès à l'application**

| Fonctionnalité | URL |
|--------------|----|
| **Dashboard Dash (graphiques)** | `[http://localhost:5000/dash/]` |
| **API Flask - Récupérer les données** | `[http://localhost:5000/data]` |
| **API Flask - Statistiques générales** | `[http://localhost:5000/stats]` |
| **API Flask - Statistiques par colonne** | ``http://localhost:5000/stats/<nom_colonne>`` |
| **Liste des colonnes de la table** | `[http://localhost:5000/columns]` |

---

## 🛠 **Architecture des Services**

### 📌 **Services Déployés**

1. **PostgreSQL (`db`)** 📊 - Stocke les données.
2. **ETL (`etl`)** 🔄 - Charge `data.csv` dans PostgreSQL.
3. **Analytics (`analytics`)** 📈 - Fournit les API Flask & le Dashboard Dash.

### 📂 **Structure du projet**

```
📁 CCA/
│── 📄 docker-compose.yml      # Configuration des services Docker
│── 📁 services/
│   ├── 📁 db/                 # Service de base de données PostgreSQL
│   │   ├── 📄 init.sql         # Script SQL pour créer la table
│   │   ├── 📄 data.csv         # Fichier de données
│   ├── 📁 etl/                # Pipeline ETL
│   │   ├── 📄 etl.py           # Script pour charger les données
│   ├── 📁 analytics/          # Service Flask & Dash
│   │   ├── 📄 app.py          # Serveur Flask & Dash
│   │   ├── 📄 layout.py       # Layout de l'interface Dash
│   │   ├── 📄 callbacks.py    # Callbacks pour interactivité Dash
```

---

## 🔍 **Débogage & Résolution des Problèmes**

### 📌 **Vérifier si les conteneurs tournent**

```sh
docker ps -a
```

### 📌 **Voir les logs des services**

```sh
docker logs -f cca-analytics-1  # Logs du service Analytics
```

### 📌 **Se connecter à PostgreSQL**

```sh
docker exec -it cca-db-1 psql -U user -d analytics_db
```

### 📌 **Supprimer et reconstruire les volumes (si problème de données)**

```sh
docker compose down -v

docker compose up --build
```
