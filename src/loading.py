# Load the goodbooks CSV files from the local folder.
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def _read_csv(filename: str, data_dir: Path = DATA_DIR, dtype: dict | None = None) -> pd.DataFrame:
    """Read one dataset CSV and check that it is usable.

    Args:
        filename: Name of the file inside ``data_dir``; must be a key of
            ``REQUIRED_COLUMNS``.
        data_dir: Folder containing the dataset files.
        dtype: Optional column types passed to ``pandas.read_csv``.

    Returns:
        The file content as a DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or lacks expected columns.
    """
    path = data_dir / filename
    if not path.is_file():
        raise FileNotFoundError(
            f"{path} not found. Download the dataset first (see the README)."
        )

    try:
        df = pd.read_csv(path, dtype=dtype)
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"{path} is empty.") from error
    if df.empty:
        raise ValueError(f"{path} contains a header but no rows.")

    return df


def load_books(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load book metadata (one row per book, 10,000 rows)."""
    return _read_csv("books.csv", data_dir)


def load_ratings(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load the user ratings sample (about 6 million rows).

    Small integer types are used to reduce memory: ``book_id`` never
    exceeds 10,000 and ``rating`` is between 1 and 5.
    """
    dtypes = {"user_id": "int32", "book_id": "int16", "rating": "int8"}
    return _read_csv("ratings.csv", data_dir, dtype=dtypes)


def load_tags(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load the tag dictionary (tag_id -> tag_name)."""
    return _read_csv("tags.csv", data_dir)


def load_book_tags(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load how many users applied each tag to each book.

    Links to books through ``goodreads_book_id``, not ``book_id``.
    """
    return _read_csv("book_tags.csv", data_dir)

def load_to_read(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load how many users applied each tag to each book.

    Links to books through ``goodreads_book_id``, not ``book_id``.
    """
    return _read_csv("to_read.csv", data_dir)