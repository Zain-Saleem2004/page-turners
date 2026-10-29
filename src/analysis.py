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