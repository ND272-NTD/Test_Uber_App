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

genre_counts = df['genres'].str.split('|').explode().value_counts()
genre_counts.columns = ['Genre', 'Movie Count']

# main dashboard setup and layout

col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('Movies 4 U stats')
    st.metric("Total Movies to watch", movie_count)

with col[1]:
    st.markdown('#### Number of Movies by genre')

    # Create an interactive bar chart using Plotly
    fig = px.bar(genre_counts,
                 x='Genre',
                 y='Movie Count',
                 title='Number of Movies per Genre',
                 labels={'Movie Count': 'Count of Movies', 'Genre': 'Movie Genre'},
                 color='Movie Count',  # Color bars based on the count
                 color_continuous_scale='Viridis')  # Color scale for bars

    # Display the interactive chart
    st.plotly_chart(fig)


with col[2]:
    st.markdown('#### Top Rated Movies of All-Time')
    
    # Display the sorted DataFrame with column configurations inside col3
    st.dataframe(
        df_selected_year_sorted[["title", "average_rating"]],  # Only display title and average_rating columns
        hide_index=True,  # Hide index to keep it clean
        width=None,  # Auto-adjust width
        column_config={
            "title": st.column_config.TextColumn("Title"),
            "average_rating": st.column_config.ProgressColumn(
                "Average Rating",
                format="%f",  # Display the average rating as a float
                min_value=0,  # Set the min value for the progress bar
                max_value=5  # Set the max value assuming ratings are out of 5
            )
        }
    )



   #with st.expander('About', expanded=True):
    #   st.write(''' 
     #      - This project has been carried out as part of my college project, with the task being to build an interactive dashboard.
      #     - :orange[**Movies available**]: Original movies dataset had 2,500 films, those with ratings equaled 2,496.
       #    - :orange[**Average ratings**]: Average ratings overall of all films in the database.
       #''')