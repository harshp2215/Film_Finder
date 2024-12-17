import streamlit as st
import pickle
import requests
import base64

# Load movie data and similarity matrix
movies2 = pickle.load(open('movies.pkl', 'rb'))
similarity_matrix = pickle.load(open('matrix.pkl', 'rb'))

# Function to convert the icon to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set the browser tab title and favicon (icon.png placed in the same directory as your script)
icon_base64 = image_to_base64("icon.png")  # Use the local icon.png file

st.markdown(f"""
    <link rel="icon" href="data:image/png;base64,{icon_base64}" type="image/png">
    <title>MovieDekho - Movie Recommendations</title>
""", unsafe_allow_html=True)

# Custom CSS for title styling
st.markdown("""
    <style>
    /* Title styling */
    .title {
        font-size: 3em;
        font-weight: bold;
        color: #e50914;
        text-align: center;
        margin-top: -30px; /* Shift title upwards */
    }
    .title-icon {
        width: 1.2em; /* Decreased size of the icon */
        vertical-align: middle;
        margin-top: -20px;
    }
    
    /* Move dropdown and button down */
    .dropdown-container {
        margin-top: 50px; /* Add space between title and dropdown */
    }

    .button-container {
        margin-top: 10px; /* Move button closer to the dropdown */
    }

    .output-container {
        margin-top: 30px; /* Add space between button and output */
    }
    </style>
""", unsafe_allow_html=True)

# App title with the custom local icon
st.markdown(
    f'''
    <div class="title">
        MovieDekho <img class="title-icon" src="data:image/png;base64,{icon_base64}" />
    </div>
    ''', 
    unsafe_allow_html=True
)

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

# Dropdown, button, and output styling
st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)

movie_list = movies2['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="button-container">', unsafe_allow_html=True)

# When the button is clicked, show the recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Create columns for displaying recommended movies
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

st.markdown('</div>', unsafe_allow_html=True)
