import pandas as pd
from sqlalchemy import create_engine

# Database credetials
DB_USER = "postgres"
DB_PASSWORD = "your_password_here"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "imdb_pipeline"

PROCESSED_DATA_PATH = "data/processed/"

def load_to_postgres():
    """
    Loads processed IMDb data into PostgreSQL database.
    """
    print("Loading processed data...")

    # Load CSV
    df = pd.read_csv(f"{PROCESSED_DATA_PATH}movies.csv")

    print("Connecting to PostgreSQL...")

    # Create connection string
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    print("Writing data to PostgreSQL...")

    # Write to Table
    df.to_sql(
        name = "movies",
        con=engine,
        if_exists="replace",           # Replace if exists
        index=False                    
    )
    print("Data successfully loaded to PostgreSQL!")
