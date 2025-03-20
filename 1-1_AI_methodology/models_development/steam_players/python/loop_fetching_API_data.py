import os
import time
from pathlib import Path

import dotenv
import duckdb
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from shared_code_2 import (
    append_to_csv,
    setup_duckdb,
    steamid_from_accountid,
)

# Load environment variables
current_dir = os.getcwd()
env_path = Path(current_dir).parents[3] / ".env"
print(f".env file exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

# --- Configuration ---
API_KEY = os.getenv("STEAM_API_KEY")
if not API_KEY:
    raise ValueError("STEAM_API_KEY not found in environment variables.")

BASE_URL = os.getenv("BASE_URL")
API_CALL_LIMIT = 99990
CSV_FILE = "../data_in/public_profiles.csv"

# API call counter
api_calls = 0
sleep_time = 1  # Adjust if needed


def fetch_player_summaries(steam_ids):
    """Fetch player summaries for a list of SteamID64 values."""
    global api_calls
    steam_ids_str = ",".join(str(sid) for sid in steam_ids)
    params = {"key": API_KEY, "steamids": steam_ids_str}
    response = requests.get(BASE_URL, params=params)
    api_calls += 1

    # Print API call stats
    print(f"✅ API calls made: {api_calls}, calls left: {API_CALL_LIMIT - api_calls}")

    # Stop execution when reaching a multiple of 1850
    if api_calls % 1850 == 0:
        print(
            f"\n\n🚨 1850 calls reached.\n\tStopping before Short-Term Limit is reached.\n"
        )
        exit()  # Stop the script immediately

    if response.status_code == 200:
        players = response.json().get("response", {}).get("players", [])
        return [
            p for p in players if p.get("communityvisibilitystate") == 3
        ]  # Only public profiles
    else:
        print(f"⚠️ Error {response.status_code}: {response.text}")
        return []


def main():
    """Main function to run API calls continuously until limit is reached."""
    global api_calls
    start_account_id = 50000000
    batch_size = 100

    try:
        while api_calls < API_CALL_LIMIT:
            steam_ids = [
                steamid_from_accountid(start_account_id + i) for i in range(batch_size)
            ]
            public_players = fetch_player_summaries(steam_ids)

            if public_players:
                df = pd.DataFrame(public_players)

                # Ensure correct column structure
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

                for col in expected_columns:
                    if col not in df.columns:
                        df[col] = np.nan

                df = df[expected_columns]  # Ensure correct order

                # ✅ Debugging Information Before Insert
                print("\n🔹 **DEBUG: DataFrame Before Insert** 🔹")
                print(f"Columns in DataFrame: {df.columns.tolist()}")
                if not df.empty:
                    print("\n🔹 **First Row Values:** 🔹", df.iloc[0].to_dict())

                # ✅ Open connection for each insert, then close it
                con = setup_duckdb()
                con.register("temp_df", df)
                con.execute("INSERT INTO public_profiles SELECT * FROM temp_df")
                con.close()  # Close after each call

                # Append to CSV
                append_to_csv(df, CSV_FILE)

            # Sleep to allow CSV writing
            time.sleep(sleep_time)

            # Move to next batch
            start_account_id += batch_size

    except KeyboardInterrupt:
        print("\n🛑 Manually stopped by user.")

    print(f"\n✅ Finished after {api_calls} API calls.")


if __name__ == "__main__":
    main()
