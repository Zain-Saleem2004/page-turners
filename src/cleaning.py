"""Clean the raw goodbooks-10k tables."""

import pandas as pd


def normalize_language(codes: pd.Series) -> pd.Series:
    """Merge English variants into 'eng' and label missing codes 'unknown'.

    Args:
        codes: Language codes such as 'eng', 'en-US', 'fre' (may contain NaN).

    Returns:
        A Series of the same length with normalized codes.
    """
    return codes.str.replace(r"^en-.*$", "eng", regex=True).fillna("unknown")


def extract_main_author(authors: pd.Series) -> pd.Series:
    """Return the first person listed in each ``authors`` entry.

    Args:
        authors: Strings such as 'J.K. Rowling, Mary GrandPré'.

    Returns:
        A Series with only the first name of each entry, without extra spaces.
    """
    return authors.str.split(",").str[0].str.strip()


def clean_books(books: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the books table (the input is not modified).

    Steps:
        - publication year converted to the nullable integer type ``Int64``
        - ``main_author`` added (first name in ``authors``)
        - ``language`` added (English variants merged, missing -> 'unknown')
        - ``isbn``, ``isbn13`` and ``language_code`` dropped

    Args:
        books: The raw table from ``loading.load_books``.

    Returns:
        The cleaned table.
    """
    return books.assign(
        original_publication_year=books["original_publication_year"].astype("Int64"),
        main_author=extract_main_author(books["authors"]),
        language=normalize_language(books["language_code"]),
    ).drop(columns=["isbn", "isbn13", "language_code"])