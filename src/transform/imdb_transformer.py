import os
import pandas as pd

# Paths for input (raw data) and output (processed data)
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"

def transform_imdb_data():
    """
    This function:
    1. Loads raw IMDb datasets
    2. Cleans and filters the data
    3. Merges datasets
    4. Saves a processed dataset ready for analysis
    """
    # Ensure processed folder exists
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

    print("Loading IMDb datasets...")

    # Load title.basics dataset
    basics = pd.read_csv(
        f"{RAW_DATA_PATH}title_basics.tsv",
        sep= "\t",                          # TSV = Tab Separated Values
        dtype= str,                         # Load everything as string to avoid type issues
        low_memory= False                   # Prevent pandas warnings for large files
    )

    # Load title.ratings dataset
    ratings = pd.read_csv(
        f"{RAW_DATA_PATH}title_ratings.tsv",
        sep= "\t",
        dtype= str
    )
    print("Cleaning data...")

    # Replace IMDb null values (\N) with actual None/NaN
    basics.replace("\\N", None, inplace=True)
    ratings.replace("\\N", None, inplace=True)

    print("Filtering movies...")

    # Keep only movies and exclude adult content
    movies = basics[
        (basics['titleType'] == 'movie') &      # Only movies
        (basics['isAdult'] == '0')              # Exclude adult content
    ][['tconst', 'primaryTitle', 'startYear', 'genres']] # Select relevant columns

    print("Converting data types...")

    # Convert columns to proper data types
    movies['startYear'] = pd.to_numeric(movies['startYear'], errors='coerce') # Convert to numeric, set errors to NaN
    ratings['averageRating'] = pd.to_numeric(ratings['averageRating'], errors='coerce')
    ratings['numVotes'] = pd.to_numeric(ratings['numVotes'], errors='coerce')

    print("Merging datasets...")

    # Merge movies with ratings using tconst (unique ID)
    movies_with_ratings = movies.merge(
        ratings,
        on= 'tconst',
        how= 'left'              # Keep all movies, even those without ratings
    )

    print("Applying filters...")

    #Remove movies with very low number of votes (low quality data)
    movies_with_ratings = movies_with_ratings[
        movies_with_ratings['numVotes'] >= 1000
    ]

    print("Saving processed data...")

    # Save final dataset to CSV
    output_path = f"{PROCESSED_DATA_PATH}movies.csv"
    movies_with_ratings.to_csv(output_path, index=False)

    print(f"Transformation completed! File saved at: {output_path}")
    