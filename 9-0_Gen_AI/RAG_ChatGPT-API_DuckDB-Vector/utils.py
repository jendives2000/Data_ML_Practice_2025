# Function to count vectors in an embedding:
def count_embeddings(conn, table_name="embeddings"):
    table_exist = conn.execute(
        f"""
                               select count(*)
                               from information_schema.tables
                               where table_name = '{table_name}'
                               """
    ).fetchone()[0]
    if not table_exist:
        return 0

    row_count = conn.execute(
        f"""
                             select count(*)
                             from {table_name}
                             """
    ).fetchone()[0]
    return row_count
