import os

import duckdb


def steamid_from_accountid(account_id):
    """Convert a 32-bit account ID to a 64-bit SteamID."""
    return account_id + 76561197960265728


def setup_duckdb():
    """Create a DuckDB connection and a table for storing public profiles if it doesn't exist."""
    con = duckdb.connect(database="steam_profiles.duckdb", read_only=False)

    # Drop table if it exists
    con.execute("DROP TABLE IF EXISTS public_profiles")

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS public_profiles (
        steamid TEXT,
        personaname TEXT,
        profileurl TEXT,
        avatar TEXT,
        avatarmedium TEXT,
        avatarfull TEXT,
        communityvisibilitystate INTEGER,
        personastate INTEGER,
        lastlogoff BIGINT,
        commentpermission INTEGER,
        realname TEXT,
        primaryclanid TEXT,
        timecreated BIGINT,
        loccountrycode TEXT,
        locstatecode TEXT,
        loccityid INTEGER
    );
    """
    con.execute(create_table_sql)
    return con


def append_to_csv(df, csv_file):
    """Append the DataFrame to a CSV file."""
    header = not os.path.exists(csv_file)
    df.to_csv(csv_file, mode="a", header=header, index=False)
