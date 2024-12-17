import streamlit as st
import pickle
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')  # Use .get() to avoid KeyError
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # Return a placeholder image for movies without posters
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

# Function to recommend movies
def recommend(movie):
    movie_index = movies2[movies2['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies2.iloc[i[0]].id
        recommended_movies.append(movies2.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

# Custom CSS with Netflix red theme
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #121212;  /* Deep black background */
}
[data-testid="stHeader"] {
    background-color: #0A0A0A;  /* Even darker header */
}
body {
    color: white;  /* White text for all body text */
}
.stSelectbox, .stTextInput {
    color: white;
}
.stButton>button {
    background-color: black;  /* Black background */
    color: #E50914;  /* Netflix red text */
    border: 1px solid #E50914;  /* Netflix red border */
    transition: none;
}
.stButton>button:hover {
    background-color: black;  /* Maintain black background */
    color: #E50914;  /* Maintain Netflix red text */
    border: 1px solid #E50914;  /* Maintain Netflix red border */
}
/* Ensure white text for dropdown and input */
.stSelectbox div[data-baseweb="select"] > div,
.stTextInput input {
    color: white !important;
    background-color: #1E1E1E !important;
}
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
}
.logo-container svg {
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# Load movie data and similarity matrix
movies2 = pickle.load(open('movies.pkl', 'rb'))
similarity_matrix = pickle.load(open('matrix.pkl', 'rb'))

# Streamlit UI with custom header and logo
st.markdown("""
<div class="logo-container">
    <h1 style='color: #E50914; text-align: center; margin-right: 10px;'>MovieDekho</h1>
    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#E50914" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-left: -10px;">
        <path d="M23 6l-6 6 6 6V6z"></path>
        <rect x="1" y="4" width="15" height="16" rx="2" ry="2"></rect>
        <circle cx="16" cy="16" r="2"></circle>
    </svg>
</div>
""", unsafe_allow_html=True)

movie_list = movies2['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Create columns with slightly reduced width to accommodate the dark theme
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0], use_container_width=True)
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1], use_container_width=True)
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2], use_container_width=True)
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3], use_container_width=True)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4], use_container_width=True)