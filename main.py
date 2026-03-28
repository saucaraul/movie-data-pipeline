from src.extract.imdb_extractor import extract_imdb_data
from src.transform.imdb_transformer import transform_imdb_data

if __name__ == "__main__":
    extract_imdb_data()
    transform_imdb_data()
