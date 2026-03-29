from src.extract.imdb_extractor import extract_imdb_data
from src.transform.imdb_transformer import transform_imdb_data
from src.load.imdb_loader import load_to_postgres

import os

if __name__ == "__main__":
    if not os.path.exists("data/raw/title_basics.tsv"):
        extract_imdb_data()

    transform_imdb_data()
    load_to_postgres()
