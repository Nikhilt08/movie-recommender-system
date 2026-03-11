import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d480e4336395c09d48e3837cd4a16461&language=en-US"

    data = requests.get(url)
    data = data.json()

    poster_path = data["poster_path"]

    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    distances = sorted(list(enumerate(similarity[movie_index])),
                       key=lambda x: x[1],
                       reverse=True)[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in distances:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters
movies_dict=pickle.load(open('movies_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl', 'rb'))
st.title("Movie Recommender System")
option = st.selectbox(
"HOW WOULD U LIKE TO BE CONTACTED",
movies['title'].values
)
if st.button("Recommend"):

    with st.spinner("Finding similar movies..."):
        names, posters = recommend(option)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
