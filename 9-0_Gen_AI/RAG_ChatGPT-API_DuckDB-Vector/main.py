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

# adding a source column that gives a URL pointing to the movie page:
movies["source"] = "https://www.imdb.com/title/" + movies["tconst"]

# using only the movies type (from col titleType):
movies = movies[movies["titleType"] == "movie"]

# replacing N/A in movie_description with "No description"
movies.movie_description = movies.movie_description.fillna("No description")

# limiting the DF movies to only 4 col: 
movies = movies[
    ["movie_title",
    "movie_description",
    "source",
    "genres"]    
    ]

movies.head(1)
movies.movie_description.isna
