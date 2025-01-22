import streamlit as st
st.title('Movie Recommender Champ')
import pandas as pd
import pickle
import requests
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f6b7e70f7192c17572d5c95ccdcfa28a&language=en-US')
    data = response.json()
    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']

movie_dict= pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

selected_movie_name = st.selectbox(
    "Please Provide a Movie Name:",
    (movies['title']),
    index=None,
    placeholder="Movie Name",
)

def recommend(movie):
    movie_index  = movies[movies['title'] == movie].index[0]
    movie_list  =  sorted(list(enumerate(similarity[movie_index])),reverse=True,key = lambda x:x[1])[1:6]
    recom_movies = []
    recom_posters  = []
    for i in movie_list:
        recom_movies.append((movies.iloc[i[0]].title))
        recom_posters.append(fetch_poster((movies.iloc[i[0]].id)))
    return recom_movies , recom_posters

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i in range(len(names)):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

