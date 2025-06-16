# Movie Recommender System using Cosine Similarity

This project builds a **content-based movie recommendation system** using metadata from the **TMDB 5000 Movies Dataset**. It recommends similar movies based on shared characteristics like genre, keywords, cast, crew, and overview using **cosine similarity** on text features.

---

## Dataset

Source: [TMDB 5000 Movie Dataset (Kaggle)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

- `tmdb_5000_movies.csv`: Contains movie metadata like overview, genres, and keywords.
- `tmdb_5000_credits.csv`: Contains cast and crew information.


## Features Used

- **Overview**: Movie summary
- **Genres**
- **Keywords**
- **Top 3 Cast Members**
- **Director**

All features are processed and combined into a single text-based feature (`tags`) for similarity analysis.



## Workflow

1. **Data Loading & Merging**
   - Merge `movies` and `credits` datasets on the movie title.

2. **Data Cleaning**
   - Select relevant columns: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`.
   - Remove null entries.
   - Convert JSON-like strings into structured Python lists.

3. **Feature Engineering**
   - Combine text features into a `tags` column.
   - Normalize text (lowercase, remove spaces in multi-word tags like `"Science Fiction"`).

4. **Text Vectorization**
   - Use `CountVectorizer` to convert `tags` into numerical vectors.

5. **Similarity Calculation**
   - Use cosine similarity to measure closeness between movies.

6. **Recommendation Function**
   - Input a movie title.
   - Return top 5 most similar movies based on vector similarity.

---


