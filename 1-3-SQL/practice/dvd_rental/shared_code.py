import re
from datetime import date

import pandas as pd


def extract_limit_from_sql(stmt, engine):
    """Extrait la valeur de la clause LIMIT si elle existe dans la requête SQL compilée."""
    compiled_sql = str(stmt.compile(engine))
    limit_match = re.search(r"LIMIT \%\((.*?)\)s", compiled_sql)

    if limit_match:
        param_key = limit_match.group(1)
        params = stmt.compile(engine).params
        return params.get(param_key), compiled_sql
    return None, compiled_sql


def execute_query(stmt, engine, lim_num):
    """Exécute la requête avec et sans limite pour obtenir le total de lignes et les résultats."""
    with engine.connect() as conn:
        stmt_no_limit = stmt.limit(None) if lim_num is not None else stmt
        total_rows = conn.execute(stmt_no_limit).fetchall()  # Nombre total de lignes
        result = conn.execute(stmt)
        rows = result.fetchall()
    return total_rows, rows, result


def format_rows_as_strings(rows):
    """Convertit les données en chaînes de caractères pour assurer une sortie uniforme."""
    return [
        [
            str(item)
            if not isinstance(item, (date, float))
            else (
                item.strftime("%Y-%m-%d") if isinstance(item, date) else f"{item:.2f}"
            )
            for item in row
        ]
        for row in rows
    ]


def calculate_column_widths(col_names, rows_str):
    """Détermine dynamiquement la largeur maximale de chaque colonne pour un affichage aligné."""
    return [
        max(
            len(col_names[i]),
            max(len(row[i]) for row in rows_str) if rows_str else len(col_names[i]),
        )
        for i in range(len(col_names))
    ]


def display_results(compiled_sql, total_rows, rows_str, col_names, col_widths, lim_num):
    """Affiche les résultats formatés avec un alignement correct des colonnes."""
    print(f"\nTotal rows selected: {len(total_rows)}")
    if lim_num:
        print(f"Limit of {lim_num} applied. Rows displayed: {len(rows_str)}")

    print(f"\nRaw SQL query:\n{compiled_sql}\n")

    # Affichage de l'en-tête avec alignement
    header = " | ".join(
        col_names[i].ljust(col_widths[i]) for i in range(len(col_names))
    )
    print(header)
    print("-" * len(header))  # Ligne de séparation

    # Affichage des lignes formatées
    for row in rows_str:
        formatted_row = " | ".join(
            row[i].ljust(col_widths[i]) for i in range(len(col_names))
        )
        print(formatted_row)


def execute_stmt(stmt, engine, output_lim=None):
    """Fonction principale qui orchestre l'exécution et l'affichage de la requête SQL."""
    lim_num, compiled_sql = extract_limit_from_sql(stmt, engine)
    total_rows, rows, result = execute_query(stmt, engine, lim_num)

    col_names = [str(col) for col in result.keys()]
    rows_str = format_rows_as_strings(rows)
    rows_to_print = rows_str[:output_lim] if (output_lim and rows_str) else rows_str
    col_widths = calculate_column_widths(col_names, rows_str)

    display_results(
        compiled_sql, total_rows, rows_to_print, col_names, col_widths, lim_num
    )


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
