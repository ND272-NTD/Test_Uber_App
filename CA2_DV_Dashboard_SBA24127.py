import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
from wordcloud import WordCloud

st.set_page_config(
    page_title="Movies 4 U 🍿🍿🍿",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

df = pd.read_csv('movies_streamlit.csv')

#st.title('Movies 4 U 🍿🍿🍿')

with st.sidebar:
    st.title('🍿 Movies 4 U')
    
    year_list = list(df.year.unique())[::-1]
    
    all_genres = df['genres'].str.split('|').explode().unique()
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = df[df.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="average_rating", ascending=False)

    selected_genre = st.selectbox('Select a genre', ['All'] + list(all_genres))

    # Filter movies based on selected year and genre
    if selected_genre != 'All':
        df_filtered = df[df['genres'].str.contains(selected_genre)]
    else:
        df_filtered = df

    # Show filtered data
    st.write(f"Data for the year {selected_year} and genre {selected_genre}:")
    st.dataframe(df_filtered)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

movie_count = df['movieId'].nunique()

# main dashboard setup and layout

col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('Movies 4 U stats')
    st.metric("Total Movies to watch", movie_count)


