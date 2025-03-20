import os
import time
from pathlib import Path

import dotenv
import duckdb
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
from shared_code_2 import (
    append_to_csv,
    setup_duckdb,
    steamid_from_accountid,
)

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
API_CALL_LIMIT = int(os.getenv("API_CALL_LIMIT"))
CSV_FILE = "../data_in/public_profiles.csv"

# Global API call counter
api_calls = 0


def fetch_player_summaries(steam_ids):
    """Fetch player summaries for a list of SteamID64 values."""
    global api_calls
    steam_ids_str = ",".join(str(sid) for sid in steam_ids)
    params = {"key": API_KEY, "steamids": steam_ids_str}
    response = requests.get(BASE_URL, params=params)
    api_calls += 1

    # Print API call stats after this request.
    print(f"API calls made: {api_calls}, calls left: {API_CALL_LIMIT - api_calls}")

    if response.status_code == 200:
        players = response.json().get("response", {}).get("players", [])
        # Filter for public profiles: communityvisibilitystate == 3
        public_players = [
            player for player in players if player.get("communityvisibilitystate") == 3
        ]
        return public_players
    else:
        print("Error:", response.status_code, response.text)
        return []


def main():
    # Set up DuckDB connection and CSV file
    con = setup_duckdb()

    # Define the range of account IDs to fetch
    start_account_id = 50000000  # Example starting account ID; adjust as needed.
    end_account_id = start_account_id + 200  # Demo range for 200 accounts.
    batch_size = 100  # API allows up to 100 Steam IDs per request.

    # Create a list of 32-bit account IDs
    account_ids = list(range(start_account_id, end_account_id))

    for i in range(0, len(account_ids), batch_size):
        batch = account_ids[i : i + batch_size]
        steam_ids = [steamid_from_accountid(acc) for acc in batch]
        public_players = fetch_player_summaries(steam_ids)

        if public_players:
            # Convert the list of dicts into a DataFrame.
            df = pd.DataFrame(public_players)

            # Ensure the DataFrame has only the expected columns**
            expected_columns = [
                "steamid",
                "personaname",
                "profileurl",
                "avatar",
                "avatarmedium",
                "avatarfull",
                "communityvisibilitystate",
                "personastate",
                "lastlogoff",
                "commentpermission",
                "realname",
                "primaryclanid",
                "timecreated",
                "loccountrycode",
                "locstatecode",
                "loccityid",
            ]

            # Ensure all expected columns exist; fill missing ones with NaN
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = np.nan  # or use None

            # Reorder columns to match DuckDB table schema
            df = df[expected_columns]

            # ✅ Debugging Information Before Insert
            print("\n🔹 **DEBUG: DataFrame Before Insert** 🔹")
            print(f"Number of columns supplied: {len(df.columns)}")
            print(f"Expected columns: {len(expected_columns)}")
            print(f"Columns in DataFrame: {df.columns.tolist()}")
            if not df.empty:
                print("\n🔹 **First Row Values:** 🔹")
                print(
                    df.iloc[0].to_dict()
                )  # Print the first row's dictionary representation

            # Now insert into DuckDB
            con.register("temp_df", df)
            con.execute("INSERT INTO public_profiles SELECT * FROM temp_df")
            # Append the data to a CSV file.
            append_to_csv(df, CSV_FILE)

        # Pause between requests to stay within rate limits.
        time.sleep(1)

    print("Finished fetching data.")
    con.close()


if __name__ == "__main__":
    main()
