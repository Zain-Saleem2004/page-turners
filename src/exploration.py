"""Simple exploration: summarize every table of the dataset.

Run from the project root with ``python -m src.exploration``.
"""
import pandas as pd
from src.loading import load_book_tags, load_books, load_ratings, load_tags

def summarize_table(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize each column of a table.

    Args:
        df: Any table.

    Returns:
        One row per column with its data type, number of unique values
        and number of missing values.
    """
    return pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "unique": df.nunique(),
        "missing": df.isna().sum(),
    })


def main() -> None:
    """Print the summary of every table."""
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 120)

    tables = {
        "books": load_books(),
        "ratings": load_ratings(),
        "tags": load_tags(),
        "book_tags": load_book_tags(),
    }
    for name, df in tables.items():
        print(f"== {name}: {df.shape[0]} rows, {df.shape[1]} columns ==")
        print(summarize_table(df))
        print()


if __name__ == "__main__":
    main()