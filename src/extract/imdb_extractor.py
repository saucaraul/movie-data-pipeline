import os
import requests
import gzip
import shutil

IMDB_URLS = {
    "title_basics": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title_ratings": "https://datasets.imdbws.com/title.ratings.tsv.gz"
}

RAW_DATA_PATH = "data/raw/"

def download_file(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def extract_gzip(file_path, output_path):
    with gzip.open(file_path,"rb") as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def extract_imdb_data():
    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    for name, url in IMDB_URLS.items():
        print(f"Downloading {name}...")

        gz_path = os.path.join(RAW_DATA_PATH, f"{name}.tsv.gz")
        tsv_path = os.path.join(RAW_DATA_PATH, f"{name}.tsv")

        #Download
        download_file(url,gz_path)

        print(f"Extracting {name}...")
        extract_gzip(gz_path,tsv_path)

        print(f"Done: {tsv_path}")
