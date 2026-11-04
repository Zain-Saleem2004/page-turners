"""Streamlit app: what makes a book loved by readers?"""
import matplotlib.pyplot as plt
import streamlit as st
from src.analysis import (assign_era, popularity_rating_correlation, rating_distribution, summarize_by_group)
from src.cleaning import clean_books
from src.genres import books_by_genre, build_book_genres
from src.loading import load_book_tags, load_books, load_tags
from src.plots import (plot_popularity_vs_rating, plot_rating_by_era, plot_rating_by_genre, plot_rating_distribution)

st.set_page_config(page_title="Page Turners", layout="wide")

@st.cache_data
def get_data():
    """Load and clean the tables once; Streamlit reuses the result."""
    books = assign_era(clean_books(load_books()))
    return books, load_book_tags(), load_tags()

@st.cache_data
def get_genre_books(min_count: int):
    """Return the books table with one row per (book, genre) pair."""
    books, book_tags, tags = get_data()
    book_genres = build_book_genres(books, book_tags, tags, min_count=min_count)
    return books_by_genre(books, book_genres)

def show(fig) -> None:
    """Display a matplotlib figure and free its memory."""
    st.pyplot(fig)
    plt.close(fig)

try:
    books, _, _ = get_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

st.title("Page Turners: what makes a book loved by readers?")
st.caption("Based on goodbooks-10k: 10,000 books and their Goodreads ratings.")

st.sidebar.header("Options")
show_outliers = st.sidebar.checkbox("Show outliers in box plots", value=False)
min_count = st.sidebar.slider("Minimum tag count for a genre", 20, 200, 50, step=10)

overview_tab, era_tab, genre_tab = st.tabs(["Overview", "Eras", "Genres"])

with overview_tab:
    left, right = st.columns(2)
    with left:
        show(plot_rating_distribution(rating_distribution(books)))
    with right:
        show(plot_popularity_vs_rating(books))
    rho, p_value = popularity_rating_correlation(books)
    st.metric("Spearman correlation: popularity vs average rating", f"{rho:.3f}")
    st.write(f"p-value: {p_value:.1e}. The relationship is statistically "
             "detectable but very weak: popularity says almost nothing "
             "about how much a book is loved.")

with era_tab:
    show(plot_rating_by_era(books, show_outliers=show_outliers))
    n_missing = int(books["era"].isna().sum())
    st.caption(f"{n_missing} books without a publication year are excluded.")
    st.dataframe(summarize_by_group(books, "era").round(3))

with genre_tab:
    genre_books = get_genre_books(min_count)
    st.caption(f"{genre_books['book_id'].nunique()} books have at least one "
               "genre; a book counts in every genre it is tagged with.")
    show(plot_rating_by_genre(genre_books, show_outliers=show_outliers))
    summary = summarize_by_group(genre_books, "genre")
    st.dataframe(summary.sort_values("mean_rating", ascending=False).round(3))