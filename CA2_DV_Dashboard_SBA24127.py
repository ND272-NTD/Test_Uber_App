import streamlit as st
import pandas as pd

st.title('Movies 4 U 🍿🍿🍿')


uploaded_movies_file = st.file_uploader("Upload Movies CSV", type=["csv"])
uploaded_ratings_file = st.file_uploader("Upload Ratings CSV", type=["csv"])

if uploaded_movies_file is not None and uploaded_ratings_file is not None:
    try:
        # Read the uploaded files with ISO-8859-1 encoding
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

    except Exception as e:
        st.error(f"Error occurred while reading the files: {e}")

else:
    st.warning("Please upload both Movies and Ratings CSV files to proceed.")

# user id entry for integration with recommender system built in MLB section of CA
user_id = st.number_input('Enter User ID for Recommendations', min_value=1, max_value=1000, value=1)
