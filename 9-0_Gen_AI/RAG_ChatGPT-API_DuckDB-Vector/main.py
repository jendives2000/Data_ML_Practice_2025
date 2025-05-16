import os

# Vector database: DuckDB
import duckdb
import pandas as pd

# openai modules:
import tiktoken

# Langchain modules:
from langchain.document_loaders import DataFrameLoader
from langchain_community.vectorstores import DuckDB
from langchain_openai import OpenAIEmbeddings

# Checking the OpenAI API key is available
"OPENAI_API_KEY" in os.environ

# ==== PREP ====

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
movies = movies[["movie_title", "movie_description", "source", "genres"]]


# ==== Langchain Document Setup ====
# adding a page content col to DF:
movies["page_content"] = (
    "Title: " + movies.movie_title + "\n" + "Genres: " + movies.genres + "\n"
    "Description: " + movies.movie_description
)

# limiting movies DF to 2 cols (ensuring dataloader sees them as non-metadata)
movies_for_loader = movies[["page_content", "source"]]

# loading the data into the langchain document:
docs = DataFrameLoader(movies_for_loader, page_content_column="page_content").load()

# ==== Estimating cost of vector embedding ====
# Creating the encoder:
encoder = tiktoken.encoding_for_model("text-embedding-3-large")

# list of the number of tokens of each document:
nber_tokens_perdoc = [len(encoder.encode(doc.page_content)) for doc in docs]

# Total nber of tokens:
ttal_nber_tokens = sum(nber_tokens_perdoc)

# Cost:
cost_permillion_token = 0.13
cost_pertoken = cost_permillion_token / 1_000_000
cost = round(ttal_nber_tokens * cost_pertoken, 3)

# ==== Vector Database Setup: DuckDB ====
# DuckDB Database creation:
conn = duckdb.connect("embeddings.db")

# embedding object:
embedding = OpenAIEmbeddings(model="text-embedding-3-large")

cost
ttal_nber_tokens

movies.head(1)
print(movies.head().iloc[0].page_content)
movies.movie_description.isna
print(docs[:3])
docs
nber_tokens_perdoc
