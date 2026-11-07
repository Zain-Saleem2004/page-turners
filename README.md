# Page Turners

What makes a book loved by readers? This project analyses the
[goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k) dataset
(10,000 books and about 6 million ratings from Goodreads) to see how a book's
popularity, publication year, genre and author relate to how highly it is rated.

## Research questions

1. How are ratings distributed, and are popular books rated higher?
2. Are older books rated differently from recent ones?
3. Are some genres consistently rated higher than others?
4. How do an author's ratings evolve across their works?

## Main findings

- Readers are generous: about 73% of all ratings are 4 or 5 stars, and only 2.3%
  are 1 star. Differences between books are therefore small.
- Popularity says almost nothing about appreciation (Spearman correlation 0.065).
- Publication era has a small effect: mean ratings range from 3.94 (before 1900)
  to 4.05 (1950-1979), much less than the spread inside each era.
- Genre matters most. Graphic novels (4.21) stand clearly above all others and
  literary fiction (3.88) and chick-lit (3.89) are lowest, but most genres overlap heavily.
- There is no general pattern of authors improving or declining
  (median change -0.004 stars per decade across 229 authors).

## Data

The data comes from the goodbooks-10k repository (Goodreads ratings). The files
are not stored in this repository because of their size. Download them with:

```
python src/download_data.py
```

This creates the `data/` folder with `books.csv`, `ratings.csv`, `tags.csv` and
`book_tags.csv`. `ratings.csv` is only used by the exploration module; the app
needs the other three.

## Setup

Python 3.14 was used. From the project root (Windows PowerShell):

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/download_data.py
```

On macOS or Linux, activate with `source .venv/bin/activate`.

## Usage

Start the interactive app:

```
python -m streamlit run app.py
```

Print a summary of every table (types, unique values, missing values):

```
python -m src.exploration
```

## Project structure

```
page-turners/
├── app.py                  Streamlit app (layout only, calls src/)
├── requirements.txt        Libraries with versions
├── data/                   Dataset (not in git, see "Data")
└── src/
    ├── download_data.py    Downloads the dataset
    ├── loading.py          Reads the CSV files, checks they are usable
    ├── cleaning.py         Cleans the books table (year, main author, language)
    ├── exploration.py      Summarises each table
    ├── genres.py           Links books to genres through user tags
    ├── analysis.py         Eras, group summaries, correlation, author trends
    └── plots.py            All figures
```

## Method and design decisions

- **Two data sources.** `ratings.csv` is a sample (about 1% of all ratings) whose
  average is about 0.1 stars lower than the full population, so the main results
  use the star counts in `books.csv`.
- **Genres** come from user tags. I chose a list of tags that describe what a book
  is, merged spelling variants, and left out reader shelves such as "to-read".
  A book counts in every genre it carries. A tag must have been applied by at
  least 50 users (adjustable in the app); the ranking is stable for thresholds of
  20, 50 and 100.
- **Publication year** is grouped into eras because some books are very ancient
  (negative years) and the 21 books without a year are excluded only from year-based analyses.
- **Authors:** only the first author listed is used. "Anonymous" and "Unknown"
  are excluded.

## Limitations

- Only the 10,000 most-rated books are included, so the results do not describe
  books in general.
- The genre dictionary is a judgement call, and genres overlap.
- Differences between groups describe patterns, they do not show causes.
- Name-based grouping cannot detect pseudonyms (for example Nora Roberts and J.D. Robb).

## Libraries

pandas, numpy, scipy, matplotlib, seaborn, streamlit (versions in `requirements.txt`).

## Data source

Zygmunt Zajac, [goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k).