import streamlit as st
import pickle
import pandas as pd
import requests

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommendation System")


# Load dataset
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)


# Create vectors
cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(movies["tags"]).toarray()

# Compute similarity
similarity = cosine_similarity(vectors)


# Fetch movie poster
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d480e4336395c09d48e3837cd4a16461&language=en-US"

    data = requests.get(url).json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


# Recommend similar movies
def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in distances:
        movie_id = movies.iloc[i[0]].id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# Search movies by genre
def search_by_genre(genre):

    results = movies[movies["tags"].str.contains(genre.lower())]

    top_movies = results.head(5)

    names = []
    posters = []

    for _, row in top_movies.iterrows():
        names.append(row["title"])
        posters.append(fetch_poster(row["id"]))

    return names, posters


# Search movies by actor
def search_by_actor(actor):

    results = movies[movies["tags"].str.contains(actor.lower())]

    top_movies = results.head(5)

    names = []
    posters = []

    for _, row in top_movies.iterrows():
        names.append(row["title"])
        posters.append(fetch_poster(row["id"]))

    return names, posters


# UI selector
search_option = st.radio(
    "Choose search type",
    ["Search by Movie", "Search by Genre", "Search by Actor"]
)


names = []
posters = []


# Movie recommender
if search_option == "Search by Movie":

    movie = st.selectbox(
        "Select a movie",
        movies["title"].values
    )

    if st.button("Recommend Movies"):
        with st.spinner("Finding similar movies..."):
            names, posters = recommend(movie)


# Genre search
elif search_option == "Search by Genre":

    genre = st.text_input("Enter genre (action, romance, comedy)")

    if st.button("Search Genre"):
        with st.spinner("Searching movies..."):
            names, posters = search_by_genre(genre)


# Actor search
elif search_option == "Search by Actor":

    actor = st.text_input("Enter actor name")

    if st.button("Search Actor"):
        with st.spinner("Searching movies..."):
            names, posters = search_by_actor(actor)


# Display results
if names:

    cols = st.columns(5)

    for i in range(len(names)):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])