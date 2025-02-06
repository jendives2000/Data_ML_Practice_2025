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
