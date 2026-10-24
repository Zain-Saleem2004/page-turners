import pandas as pd

books = pd.read_csv("data/books.csv")
print(books.shape)
print(books.dtypes)
print(books.isna().sum())
books[["title", "authors", "original_publication_year", "average_rating", "ratings_count"]].head()