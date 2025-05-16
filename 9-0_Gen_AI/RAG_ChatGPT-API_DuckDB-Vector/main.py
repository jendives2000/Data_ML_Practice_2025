import os
import sys

# ensure the script’s directory is on the import path
sys.path.insert(0, os.path.dirname(__file__))

# Vector database: DuckDB
import duckdb
import pandas as pd

# openai modules:
import tiktoken

# Langchain modules:
from langchain.document_loaders import DataFrameLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DuckDB
from langchain_openai import OpenAIEmbeddings

# from utils:
from utils import count_embeddings

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
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Vectors counting:
n_vectors = count_embeddings(conn, "embeddings")

# Fill the vector DB with data from documents:
if n_vectors > 0:
    docsearch = DuckDB(embedding=embeddings, connection=conn, table_name="embeddings")
else:
    docsearch = DuckDB.from_documents(
        docs, embeddings, connection=conn, table_name="embeddings"
    )

# ==== Testing the RAG ====
# question = "What's a good movie about climate change?"
question = "What’s a the Iron Giant movie?"

# Convert the vector DB to a retriever & target relevant docs to answer a question:
docsearch.similarity_search(question, k=4)

# ==== Chaining Prompts ====
# Prompt Setup:
DOCUMENT_PROMPT = """{page_content}
IMDB link: {source}
=========="""

QUESTION_PROMPT = """
Given the following extracted parts of a movie database and a question, create a final answer with the IMDB link as source ("SOURCE").
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCE" part in your answer.

QUESTION: What’s a good movie about a robot to watch with my kid?
=========
Title: "A.I. Artificial Intelligence"
Genres: Drama, Sci-Fi
Description: A robotic boy, the first programmed to love, David (Haley Joel Osment) is adopted as a test case by a Cybertronics employee (Sam Robards) and his wife (Frances O'Connor). Though he gradually becomes their child, a series of unexpected circumstances make this life impossible for David. Without final acceptance by humans or machines, David embarks on a journey to discover where he truly belongs, uncovering a world in which the line between robot and machine is both vast and profoundly thin.
IMDB link: https://www.imdb.com/title/tt0212720
========
Title: I, Robot
Genres: Action, Mystery, Sci-Fi
Description: In 2035, highly intelligent robots fill public service positions throughout the world, operating under three rules to keep humans safe. Despite his dark history with robotics, Detective Del Spooner (Will Smith) investigates the alleged suicide of U.S. Robotics founder Alfred Lanning (James Cromwell) and believes that a human-like robot (Alan Tudyk) murdered him. With the help of a robot expert (Bridget Moynahan), Spooner discovers a conspiracy that may enslave the human race.
IMDB link: https://www.imdb.com/title/tt0343818
========
Title: The Iron Giant
Genres: Action, Adventure, Animation
Description: In this animated adaptation of Ted Hughes' Cold War fable, a giant alien robot (Vin Diesel) crash-lands near the small town of Rockwell, Maine, in 1957. Exploring the area, a local 9-year-old boy, Hogarth, discovers the robot, and soon forms an unlikely friendship with him. When a paranoid government agent, Kent Mansley, becomes determined to destroy the robot, Hogarth and beatnik Dean McCoppin (Harry Connick Jr.) must do what they can to save the misunderstood machine.
IMDB link: https://www.imdb.com/title/tt0129167
========
FINAL ANSWER: 'The Iron Giant' is an animated movie about a friendship between a robot and a kid. It would be a good movie to watch with a kid.'
SOURCE: https://www.imdb.com/title/tt0129167

QUESTION: {question}
========
{summaries}
FINAL ANSWER:"""

# Creating the prompt template objects: 
document_prompt = PromptTemplate.from_template(DOCUMENT_PROMPT)
question_prompt = PromptTemplate.from_template(QUESTION_PROMPT)

cost
ttal_nber_tokens

movies.head(1)
print(movies.head().iloc[0].page_content)
movies.movie_description.isna
print(docs[:3])
docs
nber_tokens_perdoc
