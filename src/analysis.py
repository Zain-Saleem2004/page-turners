"""Simple analysis of the cleaned books table."""
import numpy as np
import pandas as pd
from scipy import stats

STAR_COLUMNS = ["ratings_1", "ratings_2", "ratings_3", "ratings_4", "ratings_5"]

ERA_BINS = [-np.inf, 1900, 1950, 1980, 2000, 2010, np.inf]
ERA_LABELS = ["before 1900", "1900-1949", "1950-1979",
              "1980-1999", "2000-2009", "2010-2017"]


def rating_distribution(books: pd.DataFrame) -> pd.Series:
    """Share of each star rating (1-5) among all ratings of all books."""
    totals = books[STAR_COLUMNS].sum().to_numpy()
    return pd.Series(totals / totals.sum(), index=[1, 2, 3, 4, 5], name="share")


def assign_era(books: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``books`` with an ``era`` column (missing if no year)."""
    years = books["original_publication_year"].astype("float64")
    era = pd.cut(years, bins=ERA_BINS, labels=ERA_LABELS, right=False)
    return books.assign(era=era)


def summarize_by_group(books: pd.DataFrame, by: str) -> pd.DataFrame:
    """Number of books, mean and median average rating for each group."""
    return (
        books.groupby(by, observed=True)["average_rating"]
        .agg(n_books="count", mean_rating="mean", median_rating="median")
    )


def popularity_rating_correlation(books: pd.DataFrame) -> tuple[float, float]:
    """Spearman correlation between number of ratings and average rating."""
    result = stats.spearmanr(books["work_ratings_count"], books["average_rating"])
    return float(result.statistic), float(result.pvalue)


EXCLUDED_AUTHORS = {"Anonymous", "Unknown"}
def author_trends(books: pd.DataFrame, min_books: int = 8,
                  min_span: int = 5) -> pd.DataFrame:
    """Measure how each author's ratings change with publication year.
    For every author with enough dated books, a straight line is fitted to
    average rating against publication year.
    Args:
        books: Cleaned table with ``main_author``, ``original_publication_year``
            and ``average_rating``.
        min_books: Minimum number of dated books an author needs.
        min_span: Minimum number of years between the first and last book.

    Returns:
        One row per author: number of books, first and last year, mean rating,
        ``slope_per_decade`` (change in stars per 10 years) and its p-value.
    """
    dated = books.dropna(subset=["original_publication_year"])
    dated = dated[~dated["main_author"].isin(EXCLUDED_AUTHORS)]
    rows = []
    for author, group in dated.groupby("main_author"):
        years = group["original_publication_year"].astype("float64")
        if len(group) < min_books or years.max() - years.min() < min_span:
            continue
        fit = stats.linregress(years, group["average_rating"])
        rows.append({
            "author": author,
            "n_books": len(group),
            "first_year": int(years.min()),
            "last_year": int(years.max()),
            "mean_rating": group["average_rating"].mean(),
            "slope_per_decade": fit.slope * 10,
            "p_value": fit.pvalue,
        })
    return pd.DataFrame(rows).set_index("author")