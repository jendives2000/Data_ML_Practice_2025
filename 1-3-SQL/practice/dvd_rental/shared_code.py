from datetime import date
import pandas as pd

def execute_stmt(stmt, engine):
    with engine.connect() as conn:
        result = conn.execute(stmt)
        rows = result.fetchall()  # Fetch all rows to calculate total count

        # Print the total number of rows returned
        print(f"\nTotal rows returned: {len(rows)}")

        print(
            f"\nRaw SQL query:\n{stmt.compile(engine)}\n"
        )  # Show the equivalent raw-like SQL query

        # Print column names
        print(
            " | ".join(result.keys())
        )  # result.keys() returns a list of column names as strings

        for row in rows:
            formatted_row = [  # if date, format as Y-M-D, else as string
                item.strftime("%Y-%m-%d") if isinstance(item, date) else str(item)
                for item in row
            ]
            print(" | ".join(formatted_row))  # Separate columns with " | "


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
