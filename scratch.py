from pathlib import Path
from src.loading import load_books, load_ratings, load_tags, load_book_tags

books = load_books()
ratings = load_ratings()
print(books.shape, ratings.shape, load_tags().shape, load_book_tags().shape)
print(ratings.dtypes)
print(round(ratings.memory_usage(deep=True).sum() / 1e6), "MB")

try:
    load_books(data_dir=Path("nowhere"))
except FileNotFoundError as error:
    print("OK, caught:", error)

# import numpy as np
#
# books = load_books()
#
# # 1. Are the IDs unique?
# print(books["book_id"].is_unique, books["goodreads_book_id"].is_unique, books["work_id"].is_unique)
#
# # 2. Do the star counts add up to work_ratings_count?
# stars = books[[f"ratings_{i}" for i in range(1, 6)]]
# print((stars.sum(axis=1) != books["work_ratings_count"]).sum())
#
# # 3. Does average_rating match the mean recomputed from the star counts?
# recomputed = stars.to_numpy() @ np.arange(1, 6) / stars.sum(axis=1).to_numpy()
# print(np.abs(recomputed - books["average_rating"]).max())
#
# # 4. The very old books
# print(books.loc[books["original_publication_year"] < 1500,["title", "authors", "original_publication_year"]])
#
# # 5. The authors field
# multi = books["authors"].str.contains(",")
# print(multi.sum())
# print(books.loc[multi, "authors"].head(8).tolist())
#
# # 6. Language codes
# print(books["language_code"].value_counts(dropna=False).head(10))

from src.loading import load_books
from src.cleaning import clean_books

raw = load_books()
books = clean_books(raw)
print(books["original_publication_year"].dtype, books["original_publication_year"].isna().sum())
print(books["language"].value_counts().head(6))
print(raw["authors"].nunique(), books["main_author"].nunique())
print(books[["authors", "main_author"]].head(8))
print("raw untouched:", "isbn" in raw.columns)