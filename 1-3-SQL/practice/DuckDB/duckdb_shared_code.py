def custom_duckdb_conn(memory_limit="10GB", threads=12):
    """
    Create a custom DuckDB connection with specified memory limit and number of threads.

    Parameters:
    memory_limit (str): The maximum amount of system memory to use (default is "10GB").
    threads (int): The number of CPU threads to use for parallel execution (default is 12).

    Example:
    new_conn = custom_duckdb_conn(memory_limit="5GB", threads=6)

    Returns:
    duckdb.DuckDBPyConnection: A DuckDB connection object with the specified configuration.
    """
    return duckdb.connect(config={"memory_limit": memory_limit, "threads": threads})


def execute_stmt(stmt, db):
    """
    Executes a given SQL statement on the specified DuckDB database.

    Parameters:
    stmt (str): The SQL statement to execute.
    db: The name of the DuckDB database file. With the extension .duckdbb

    Example:
    execute_stmt(stmt, mydb.duckdb)
    Declare stmt first
    """
    with duckdb.connect(database=f"{db}") as conn:
        conn.sql(stmt)


def check_extensions(conn):
    """
    Check and return the loaded extensions for the given DuckDB connection.

    Parameters:
    conn (duckdb.DuckDBPyConnection): The DuckDB connection object.

    Example: check_extensions(my_conn)

    Returns:
    DataFrame: A DataFrame containing the loaded extensions.
    """
    return conn.sql(
        """
        select *
        from duckdb_extensions()
        where loaded = true
        """
    )


def install_load_ext(db, extension):
    """
    Install and load a DuckDB extension for a given database connection.

    Example: install_load_ext(mydb, spatial)

    Parameters:
    db (duckdb.DuckDBPyConnection): The DuckDB database connection object.
    extension: The name of the extension to install and load.
    """
    db.install_extension(f"{extension}")
    db.load_extension(f"{extension}")
