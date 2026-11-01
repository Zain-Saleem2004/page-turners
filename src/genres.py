import pandas as pd

# Tags that describe what a book is. Variants of one genre share a label.
GENRES = {
    "fantasy": ["fantasy", "urban-fantasy", "magic", "sci-fi-fantasy", "fantasy-sci-fi"],
    "young-adult": ["young-adult", "ya", "ya-fiction", "teen"],
    "childrens": ["childrens", "children", "children-s", "children-s-books", "childrens-books", "kids", "middle-grade"],
    "classics": ["classics", "classic"],
    "romance": ["romance", "contemporary-romance", "historical-romance", "paranormal-romance"],
    "mystery": ["mystery", "mysteries", "crime", "mystery-thriller"],
    "thriller": ["thriller", "suspense"],
    "science-fiction": ["science-fiction", "sci-fi", "scifi", "sci-fi-fantasy", "fantasy-sci-fi"],
    "dystopian": ["dystopian", "dystopia"],
    "historical-fiction": ["historical-fiction", "historical"],
    "paranormal": ["paranormal", "supernatural"],
    "horror": ["horror"],
    "contemporary": ["contemporary", "contemporary-fiction"],
    "adventure": ["adventure"],
    "humor": ["humor"],
    "chick-lit": ["chick-lit"],
    "graphic-novels": ["graphic-novels", "graphic-novel", "comics", "manga"],
    "poetry": ["poetry"],
    "literary-fiction": ["literary-fiction"],
    "non-fiction": ["non-fiction", "nonfiction"],
    "history": ["history"],
    "biography": ["biography", "memoir"],
    "philosophy": ["philosophy"],
    "psychology": ["psychology"],
    "science": ["science"],
}

# One row per (tag name, genre).
TAG_GENRE_PAIRS = pd.DataFrame(
    [(tag, genre) for genre, tag_list in GENRES.items() for tag in tag_list],
    columns=["tag_name", "genre"],
)

# A tag counts as evidence of a genre only if at least this many users
# applied it to the book.
MIN_TAG_COUNT = 50


def build_book_genres(books: pd.DataFrame, book_tags: pd.DataFrame,
                      tags: pd.DataFrame,
                      min_count: int = MIN_TAG_COUNT) -> pd.DataFrame:
    """Return one row (book_id, genre) for every genre of every book.

    Args:
        books: Table of books with ``book_id`` and ``goodreads_book_id``.
        book_tags: Table with ``goodreads_book_id``, ``tag_id`` and ``count``.
        tags: Table with ``tag_id`` and ``tag_name``.
        min_count: Minimum number of users that must have applied the tag.

    Returns:
        A table with columns ``book_id`` and ``genre``, without duplicates.
    """
    tag_genre = tags.merge(TAG_GENRE_PAIRS, on="tag_name")[["tag_id", "genre"]]
    genre_rows = (
        book_tags[book_tags["count"] >= min_count]
        .merge(tag_genre, on="tag_id")
        .merge(books[["book_id", "goodreads_book_id"]],
               on="goodreads_book_id", validate="many_to_one")
    )
    return genre_rows[["book_id", "genre"]].drop_duplicates().reset_index(drop=True)


def books_by_genre(books: pd.DataFrame, book_genres: pd.DataFrame) -> pd.DataFrame:
    """Return the books table with one row per (book, genre) pair.

    A book with three genres appears three times, once in each genre.
    """
    return book_genres.merge(books, on="book_id", validate="many_to_one")