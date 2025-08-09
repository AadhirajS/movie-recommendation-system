import streamlit as st
import pickle
import pandas as pd
import requests

# Replace this with your actual TMDB API key
API_KEY = "8a1bea6d8699bcea7c6effbbab70d3c6"

# Load movie data
movies = pd.read_csv("movies.csv")
similarity = pickle.load(open("similarity.pkl", "rb"))

# Fetch poster using TMDb API
def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Image"

# Recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        release_date = movies.iloc[i[0]].release_date
        rating_str = movies.iloc[i[0]].vote_average

        try:
            rating = round(float(rating_str), 1)
        except:
            rating = "N/A"

        poster_url = fetch_poster(title)
        recommended_movies.append((title, poster_url, release_date, rating))
    return recommended_movies

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")
st.write("Get movie suggestions based on what you like!")

selected_movie = st.selectbox("Pick a movie you like:", movies['title'].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    st.write("## Recommended Movies:")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(recommendations[i][1])
            st.markdown(f"**{recommendations[i][0]}**")
            st.markdown(
                f"<span style='font-size: 14px;'>📅 {recommendations[i][2]} &nbsp;&nbsp;&nbsp; ⭐ {recommendations[i][3]}/10</span>",
                unsafe_allow_html=True
            )
