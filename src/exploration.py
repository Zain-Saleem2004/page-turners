"""Simple exploration: summarize every table of the dataset.

Run from the project root with ``python -m src.exploration``.
"""
import pandas as pd
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
