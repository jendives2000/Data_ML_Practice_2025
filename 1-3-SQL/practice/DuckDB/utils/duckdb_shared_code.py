import duckdb
import sqlparse


def custom_conn_conf(memory_limit="5GB", threads=4):
    """
    Create a custom DuckDB connection with specified memory limit and number of threads.

    Parameters:
    memory_limit (str): The maximum amount of system memory to use (default is "5GB").
    threads (int): The number of CPU threads to use for parallel execution (default is 4).

    Example:
    new_conn = custom_conn_conf(memory_limit="10GB", threads=6)

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
    with db.connect() as conn:
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


def convert_2rawSQL(relation):
    """
    Convert a DuckDB relation object to a formatted raw SQL query string.

    Parameters:
    relation (duckdb.DuckDBPyRelation): The DuckDB relation object to convert.

    Example: convert_2rawSQL(my_relation_object)

    Returns:
    str: The formatted raw SQL query string.
    """
    # Get the raw SQL query
    relation1 = relation.sql_query()

    # Check if there is a FROM clause with a path to a file
    if "FROM read_csv_auto(" in relation1:
        # Find the start of the file path
        start_idx = relation1.find("FROM read_csv_auto([") + len("FROM read_csv_auto([")
        # Find the end of the file path
        end_idx = relation1.find("]", start_idx)
        # Extract the full file path
        full_path = relation1[start_idx:end_idx]
        # Extract the file name from the full path
        file_name = full_path.split("\\")[-1]
        # Replace the full path with the file name in the raw SQL
        relation2 = relation1.replace(full_path, file_name)

    # Format the raw SQL for better readability
    formatted_sql = sqlparse.format(relation2, reindent=True)

    print(formatted_sql)


def shell_commd(stmt):
    """
    Execute a DuckDB SQL statement using the system shell command.

    Parameters:
    stmt (str): The SQL statement to execute.

    Example:
    shell_commd('''SELECT * FROM my_table''')

    This function collapses all whitespace in the SQL statement into single spaces
    and then executes it using the DuckDB command-line interface.
    """
    # Collapse all whitespace (including newlines) into single spaces
    cleaned_stmt = " ".join(stmt.split())
    get_ipython().system(f'duckdb ../databases/mydatabase.duckdb -c "{cleaned_stmt}"')


def table_fromCSV(table_name: str, csv_file: str):
    shell_commd(
        f"create or replace table {table_name} as select * from read_csv('../data/data_in/{csv_file}')"
    )


# refactored logic to create ENUM with an RO:
def create_enum(col, db, enum_name):
    """
    Create an ENUM type in DuckDB from unique values in a specified column.

    Parameters:
    col (str): The column name to extract unique values from.
    db (str): The name of the DuckDB relation (table).
    enum_name (str): The name of the ENUM type to be created.
    """
    # extracting the unique values from the specified column
    col_forEnum = duckdb.sql(
        f"""
        select distinct {col}
        from {db}
        """
    ).fetchall()

    # Build a comma-separated list of ENUM values
    col_enum_val = ", ".join(f"'{v[0]}'" for v in col_forEnum)

    # create the ENUM type
    duckdb.sql(f"create type {enum_name} as enum ({col_enum_val});")


# refactoring the code to turn a variable into a pandas dataframe:
def var_to_df(var):
    """
    Convert a SQL result set to a pandas DataFrame.

    Parameters:
    var (sql.run.resultset.ResultSet): The SQL result set to convert.

    Returns:
    pandas.DataFrame: The converted pandas DataFrame.
    """
    return var.DataFrame()


import plotly.express as px
import plotly.io as pio


def init_plotly_template():
    mycolor = "rgb(160, 160, 160)"
    my_plot_1 = dict(
        layout=dict(
            title_font_size=35,
            title_font_color=mycolor,  # Grey in RGB
            font=dict(size=25, color=mycolor),  # Grey in RGB
            plot_bgcolor="black",
            paper_bgcolor="black",
            xaxis=dict(tickangle=-45, tickfont=dict(color=mycolor)),  # Grey in RGB
        )
    )
    # Register your custom template with Plotly
    pio.templates["BlackBG_Yellow2Grey_font"] = my_plot_1
    # Set it as the default for all new figures
    pio.templates.default = "BlackBG_Yellow2Grey_font"
