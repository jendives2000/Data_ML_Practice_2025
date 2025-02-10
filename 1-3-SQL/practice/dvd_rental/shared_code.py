import re
from datetime import date

import pandas as pd


def execute_stmt(stmt, engine, output_lim=None):
    with engine.connect() as conn:
        # Compile SQL to string
        compiled_sql = str(stmt.compile(engine))

        # Extract limit value from the parameterized SQL or check manually set limits
        limit_match = re.search(
            r"LIMIT \%\((.*?)\)s", compiled_sql
        )  # Regex for SQLAlchemy parameterized limit
        lim_num = None
        if limit_match:
            # Extract the parameter key and resolve its value
            param_key = limit_match.group(1)
            params = stmt.compile(engine).params
            lim_num = params.get(param_key)

        # Execute without limit to get total row count
        stmt_no_limit = stmt.limit(None) if lim_num is not None else stmt
        total_rows = conn.execute(stmt_no_limit).fetchall()  # Fetch all rows

        # Execute the original statement (with limit if applied)
        result = conn.execute(stmt)
        rows = result.fetchall()

        # Print total rows before applying limit
        print(f"\nTotal rows selected: {len(total_rows)}")

        # Print limit information if applicable
        if lim_num:
            print(f"Limit of {lim_num} applied. Rows displayed: {len(rows)}")

        # Print raw SQL query
        print(f"\nRaw SQL query:\n{compiled_sql}\n")

        # Print column names
        print(" | ".join(result.keys()))

        # Print a subset of rows based on output_lim
        rows_to_print = rows[:output_lim] if output_lim else rows
        for row in rows_to_print:
            formatted_row = [
                item.strftime("%Y-%m-%d") if isinstance(item, date) else str(item)
                for item in row
            ]
            print(" | ".join(formatted_row))


# Refactoring subquery function:
def subquery(Func, aliasCol):
    return select(Func(aliasCol)).scalar_subquery()


def alias_and_column(table, alias_name, column_name):
    """
    Create an alias for a table and return the alias along with a specific column.
    # Usage example
    f2, f2rc = alias_and_column(film, "f2", "replacement_cost")

    Parameters:
    - table: The original SQLAlchemy table object.
    - alias_name: The name of the alias for the table.
    - column_name: The name of the column to extract from the alias table.

    Returns:
    - alias_table: The alias of the original table.
    - alias_table_col: The column object from the alias table.
    """
    alias_table = table.alias(alias_name)
    alias_table_col = getattr(alias_table.c, column_name)
    return alias_table, alias_table_col


def sql_2_df(stmt):
    with engine.connect() as conn:
        result = conn.execute(stmt)  # Execute the SQL statement
        rows = result.fetchall()  # Fetch all rows
        columns = result.keys()  # Get column names

    # Convert to a Pandas DataFrame
    return pd.DataFrame(rows, columns=columns)
