import os

import pandas as pd

# Checking the OpenAI API key is available
"OPENAI_API_KEY" in os.environ

# Importing the dataset
pathIMDBcsv = "/home/jendives/MLpro/Data_ML_Practice_2025/9-0_Gen_AI/RAG_ChatGPT-API_DuckDB-Vector/Data-In/IMDB.csv"
movies_raw = pd.read_csv(pathIMDBcsv)
movies_raw.head(10)

# Renaming columns into a new movies df
movies = movies_raw.rename(
    columns={
        "primaryTitle": "movie_title",
        "Description": "movie_description",
    }
)

movies.head(1)
