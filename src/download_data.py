"""Download the goodbooks-10k CSV files into the local data/ folder."""

from pathlib import Path
from urllib.error import URLError
from urllib.request import urlretrieve

BASE_URL = "https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master"
FILES = ["books.csv", "ratings.csv", "tags.csv", "book_tags.csv"]
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def download_file(filename: str, data_dir: Path = DATA_DIR) -> Path:
    """Download one dataset file, unless it is already present.

    Args:
        filename: Name of the CSV file in the goodbooks-10k repository.
        data_dir: Folder where the file is saved.

    Returns:
        Path of the local file.

    Raises:
        ConnectionError: If the download fails.
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    destination = data_dir / filename
    if destination.exists():
        print(f"{filename} already present, skipping.")
        return destination

    print(f"Downloading {filename}...")
    try:
        urlretrieve(f"{BASE_URL}/{filename}", destination)
    except URLError as error:
        destination.unlink(missing_ok=True)  # remove a partial file
        raise ConnectionError(f"Could not download {filename}: {error}") from error
    return destination


def main() -> None:
    """Download every file the project needs."""
    for filename in FILES:
        download_file(filename)
    print("Done.")


if __name__ == "__main__":
    main()