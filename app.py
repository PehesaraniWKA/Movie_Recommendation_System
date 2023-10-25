# import libraries
import pickle
import streamlit as st
import requests


# Create a sidebar
st.sidebar.subheader("Feedback")
overall_rating = st.sidebar.slider('Recommendations satisfaction', 0, 5, 0)  # add overall rating for user experience
user_feedback = st.sidebar.text_area("\n\n\n\n\n\nPlease provide your feedback here", height=100)  # feedback section
submit_feedback = st.sidebar.button("Submit Feedback")    # create submit button


# create the function of get the URL of a movie poster using its API ID from TheMovieDB 
def fetch_poster(movie_id):
    # Construct the API URL
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)         # make a request to the API
    data = data.json()        # raise an exception for HTTP errors
    poster_path = data['poster_path']     # parse the response as JSON
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path    # return full path
    

# create function of recommends movies based on a given movie title
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]      # get the index of the given movie title
    distances = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda x: x[1])
    recommended_movies_name = []       # initialize list
    recommended_movies_poster = []      # initialize list
    
    for i in distances[1:7]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster


# def get_user_input_movies():
#     user_input = st.text_input('Enter your preferred movies (comma-separated)', 'Movie1, Movie2, Movie3')
#     return [movie.strip() for movie in user_input.split(',')]
    

# display header
st.markdown('<h1 style="color: #0a2857;">Penguins</h1>', unsafe_allow_html=True)
st.markdown('<h1 style="color: #0a2857;">Movie Recommendation System</h1>', unsafe_allow_html=True)


movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))    # load the 'movies' data from a pickle file
similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))    # load the 'similarity' data from a pickle file


movie_list = movies['title'].values     # retreive movie titles


# create header (markdown text)
st.markdown("<h1 style='font-size:18px; font-weight: bold;'>Type or select a movie to get recommendation</h1>", unsafe_allow_html=True)

# Create the selectbox
selected_movie = st.selectbox(
    'Select a movie',
    movie_list
)

# Center the "Show recommendations" button
st.write(
    """
    <style>
    .centered-button button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Check if the selected_movie is in the movie_list
if selected_movie in movie_list:
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)  # call recommended function
else:
    st.write("Selected movie not found in the database.")


# when click "Show recommendation" button
if st.button('Show recommendation', key='centered-button'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)    # call the recommand function
    col1, col2, col3 = st.columns(3)    # first row of colomns
    col4, col5, col6 = st.columns(3)    # second row of colomns

    with col1:  # display recommended movie in 1st colomn
        st.text(recommended_movies_name[0])          # display the name of the movie
        st.image(recommended_movies_poster[0])       # display the poster of the movie

    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])

    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])

    with col6:
        st.text(recommended_movies_name[5])
        st.image(recommended_movies_poster[5])

