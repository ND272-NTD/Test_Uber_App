import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.title('Movies 4 U 🍿🍿🍿')

movies_file_path = 'movies.csv'  # Path to your movies CSV file
ratings_file_path = 'ratings.csv'  # Path to your ratings CSV file
tags_file_path = 'tags.csv'  # Path to your tags CSV file

try:
    # Load the datasets with ISO-8859-1 encoding
    movies = pd.read_csv(movies_file_path, encoding='ISO-8859-1')
    ratings = pd.read_csv(ratings_file_path, encoding='ISO-8859-1')
    tags = pd.read_csv(tags_file_path, encoding='ISO-8859-1')

    # Display the first few rows of the datasets
    st.subheader("Movies Data")
    st.write(movies.head())

    st.subheader("Ratings Data")
    st.write(ratings.head())

    st.subheader("Tags Data")
    st.write(tags.head())

    # Perform a join between the movies and ratings datasets
    merged_data = pd.merge(ratings, movies[['movieId', 'title']], on='movieId', how='inner')

    # Display the first few rows of the merged data
    st.subheader("Merged Data (Ratings + Movie Titles)")
    st.write(merged_data.head())

except Exception as e:
    st.error(f"Error occurred while reading the files: {e}")