import streamlit as st
import pandas as pd

st.title('Movies 4 U 🍿🍿🍿')


movies = pd.read_csv(uploaded_movies_file, encoding='ISO-8859-1')
ratings = pd.read_csv(uploaded_ratings_file, encoding='ISO-8859-1')

st.subheader("Movies Data")
st.write(movies.head())

st.subheader("Ratings Data")
st.write(ratings.head())

# join movies and ratings datasets
merged_data = pd.merge(ratings, movies[['movieId', 'title']], on='movieId', how='inner')

st.subheader("Merged Data (Ratings + Movie Titles)")
st.write(merged_data.head())

st.subheader("Key Performance Indicators (KPIs)")
st.metric(label="Total Movies", value=len(movies))
st.metric(label="Total Ratings", value=len(ratings))

# user id entry for integration with recommender system built in MLB section of CA
user_id = st.number_input('Enter User ID for Recommendations', min_value=1, max_value=1000, value=1)
