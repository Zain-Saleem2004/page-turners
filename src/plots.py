import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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


def plot_rating_by_era(books: pd.DataFrame) -> plt.Figure:
    """Box plot of book average ratings for each publication era."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(data=books, x="era", y="average_rating", ax=ax, outliers=False)
    ax.set_xlabel("Era")
    ax.set_ylabel("Average rating")
    ax.set_xlabel("Era of first publication")
    ax.set_ylabel("Average rating")
    ax.set_title("Do older books get different ratings?")
    return fig