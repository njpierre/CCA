from sqlalchemy import create_engine
import pandas as pd
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/analytics_db")
engine = create_engine(DATABASE_URL)

#Récupère les données depuis PostgreSQL sous forme de dataframe
def get_data():
    return pd.read_sql("SELECT * FROM data", engine)
