import os
import time
from pathlib import Path

import dotenv
import duckdb
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file located in parent directories
# Get the current working directory
current_dir = os.getcwd()

# Construct the path to the .env file
env_path = Path(current_dir).parents[3] / ".env"
print(f".env file exists: {env_path.exists()}")

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)


# --- Configuration ---
# Retrieve the API key from environment variables
API_KEY = os.getenv("STEAM_API_KEY")
if not API_KEY:
    raise ValueError("STEAM_API_KEY not found in environment variables.")

BASE_URL = os.getenv("BASE_URL")
API_CALL_LIMIT = os.getenv("API_CALL_LIMIT")
CSV_FILE = "public_profiles.csv"

# Global API call counter
api_calls = 0
