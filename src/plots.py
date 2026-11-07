import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

def plot_rating_distribution(distribution: pd.Series) -> plt.Figure:
    """Bar chart of the share of each star rating."""
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(distribution.index, distribution.to_numpy() * 100)
    ax.bar_label(bars, fmt="%.1f%%")
    ax.set_xlabel("Stars")
    ax.set_ylabel("Share of all ratings (%)")
    ax.set_title("How readers rate books")
    return fig


def plot_popularity_vs_rating(books: pd.DataFrame) -> plt.Figure:
    """Scatter plot of number of ratings (log scale) against average rating."""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(books["work_ratings_count"], books["average_rating"],
               s=6, alpha=0.3)
    ax.set_xscale("log")
    ax.set_xlabel("Number of ratings (log scale)")
    ax.set_ylabel("Average rating")
    ax.set_title("Popularity vs appreciation")
    return fig


def plot_rating_by_era(books: pd.DataFrame, show_outliers: bool = False) -> plt.Figure:
    """Box plot of book average ratings for each publication era."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(data=books, x="era", y="average_rating", ax=ax, showfliers=show_outliers)
    ax.set_xlabel("Era")
    ax.set_ylabel("Average rating")
    ax.set_xlabel("Era of first publication")
    ax.set_ylabel("Average rating")
    ax.set_title("Do older books get different ratings?")
    return fig

def plot_rating_by_genre(genre_books: pd.DataFrame, show_outliers: bool = False) -> plt.Figure:
    """Horizontal box plot of book average ratings per genre."""
    order = (
        genre_books.groupby("genre")["average_rating"].median().sort_values(ascending=False).index
    )
    fig, ax = plt.subplots(figsize=(8, 9))
    sns.boxplot(data=genre_books, x="average_rating", y="genre",
                order=order, ax=ax, showfliers=show_outliers)
    ax.set_xlabel("Average rating of the book")
    ax.set_ylabel("")
    ax.set_title("How are books rated in each genre?")
    return fig

def plot_author_timeline(books: pd.DataFrame, author: str) -> plt.Figure:
    """Scatter plot of one author's book ratings by publication year, with trend line."""
    data = books[books["main_author"] == author].dropna(
        subset=["original_publication_year"])
    years = data["original_publication_year"].astype("float64")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(years, data["average_rating"])
    slope, intercept = np.polyfit(years, data["average_rating"], 1)
    line_x = np.array([years.min(), years.max()])
    ax.plot(line_x, slope * line_x + intercept, linestyle="--",
            label=f"trend: {slope * 10:+.3f} stars per decade")
    ax.set_xlabel("Year of first publication")
    ax.set_ylabel("Average rating")
    ax.set_title(f"{author}: ratings across {len(data)} books")
    ax.legend()
    return fig


def plot_author_trend_distribution(trends: pd.DataFrame) -> plt.Figure:
    """Histogram of the rating trend (stars per decade) across authors."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(trends["slope_per_decade"], bins=25)
    ax.axvline(0, linestyle="--", color="black")
    ax.set_xlabel("Change in average rating per decade (stars)")
    ax.set_ylabel("Number of authors")
    ax.set_title(f"Do authors improve or decline? ({len(trends)} authors)")
    return fig