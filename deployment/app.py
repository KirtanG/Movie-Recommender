import gradio as gr
import requests as rq
import pandas as pd

# Load pre-trained model data
# movies.pkl contains movie information including titles and IDs
# similarity_vectors.pkl contains pre-calculated cosine similarity scores
movies = pd.read_pickle(r"movies.pkl")
similarity = pd.read_pickle(r"similarity_vectors.pkl")

def fetch_poster(moviedId: int) -> str:
    """
    Fetch movie poster from TMDB API for a given movie ID.
    
    Args:
        moviedId (int): The TMDB movie ID to fetch the poster for
        
    Returns:
        str: Complete URL for the movie poster image
        
    Note:
        Requires valid TMDB API key
        Returns image URL in w500 size format
    """
    URL = f"https://api.themoviedb.org/3/movie/{moviedId}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = rq.get(URL)
    data = response.json()
    poster_path = data["poster_path"]
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

def recommend_movies(title: str) -> tuple:
    """
    Generate movie recommendations based on similarity to input movie.
    
    Args:
        title (str): Title of the movie to base recommendations on
        
    Returns:
        tuple: Contains two lists:
            - List of recommended movie titles
            - List of poster URLs for recommended movies
            
    Note:
        Uses pre-calculated similarity vectors to find 5 most similar movies
        Excludes the input movie from recommendations
    """
    # Find the index of input movie
    movieIndex = movies[movies['title'] == title].index[0]
    
    # Get similarity scores for this movie
    vec = similarity[movieIndex]
    
    # Get top 5 most similar movies (excluding the input movie itself)
    movieList = sorted(list(enumerate(vec)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movie_names = []
    recommended_movie_posters = []

    # Fetch details for each recommended movie
    for i in movieList:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(moviedId=movie_id))
    
    return (recommended_movie_names, recommended_movie_posters)

def process_movie_recommendation(movie_title:str)->list:
    """
    Process movie recommendations and handle edge cases.
    
    Args:
        movie_title (str): Title of the movie to get recommendations for
        
    Returns:
        list: List of 5 poster URLs or None values if recommendations fail
    """
    if not movie_title:
        return [None] * 5
    try:
        names, posters = recommend_movies(movie_title)
        return posters
    except:
        return [None] * 5

# create Gradio interface
with gr.Blocks() as demo:
    # add title to the interface
    gr.Markdown("## Movie Recommender System")
    
    # create dropdown to select movie
    gradio_drop_down = gr.Dropdown(
        choices=list(movies['title']),
        label="Select any movie from the list.",
        multiselect=False,
        scale=1
    )
    
    # create a button
    submit_btn = gr.Button("Get Recommendations", scale=1, size="lg")
    
    # create output image grid
    with gr.Group():
        with gr.Row():
            outputs = [
                gr.Image(label=f"Recommendation {i+1}", show_label=True)
                for i in range(5)
            ]
    
    #  onnect button click to recommendation function
    submit_btn.click(
        fn=process_movie_recommendation,
        inputs=gradio_drop_down,
        outputs=outputs
    )


demo.launch()
