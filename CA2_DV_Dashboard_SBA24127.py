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

df['average_rating'] = df['average_rating'].round(2)

ratings_df = pd.read_csv('rating.csv', encoding='ISO-8859-1')

#st.title('Movies 4 U 🍿🍿🍿')

with st.sidebar:
    st.title('🍿 Movies 4 U')
    
    selected_year = st.slider('Select a year', min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=int(df['year'].max()))
    
    all_genres = df['genres'].str.split('|').explode().unique()
    
    df_selected_year = df[df.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="average_rating", ascending=False)

    selected_genre = st.selectbox('Select a genre', ['All'] + list(all_genres))

    # Filter movies based on selected year and genre
    if selected_genre != 'All':
        df_filtered = df[df['genres'].str.contains(selected_genre)]
    else:
        df_filtered = df

    # Show filtered data
    #st.write(f"Data for the year {selected_year} and genre {selected_genre}:")
#   st.dataframe(df_filtered)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

movie_count = df['movieId'].nunique()
ratings_count = ratings_df['movieId'].count()
formatted_movie_count = f"{movie_count:,}"
formatted_ratings_count = f"{ratings_count:,}"

# Exploding genres to get each genre in a separate row
exploded_genres = df['genres'].str.split('|').explode()

# Count the number of movies per genre
genre_counts = exploded_genres.value_counts().reset_index()
genre_counts.columns = ['Genre', 'Movie Count']

exploded_df = df.loc[exploded_genres.index, ['average_rating']].copy()
exploded_df['genre'] = exploded_genres

genre_avg_rating = exploded_df.groupby('genre')['average_rating'].mean().sort_values(ascending=False)

min_ratings = st.slider("Select minimum number of ratings", 0, int(movies['rating_count'].max()), 50)

filtered_movies = movies[movies['rating_count'] >= min_ratings]

# If there are no movies meeting the condition, show a message
if filtered_movies.empty:
    st.write("No movies found with the selected rating count threshold.")
else:
    # Sort the filtered movies by rating_count and take the top 10
    top_movies = filtered_movies.sort_values(by='rating_count', ascending=False).head(10)



# main dashboard setup and layout

col = st.columns((1, 4.5, 2.5), gap='medium')

with col[0]:
    st.markdown('Movies 4 U stats')
    st.metric("Total Movies to watch", formatted_movie_count)
    
   #st.markdown('Total User Ratings')
    st.metric("Total Ratings count", formatted_ratings_count)
    

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


     # Show filtered data
    st.write(f"Data for the year {selected_year} and genre {selected_genre}:")
    st.dataframe(df_filtered)

    st.markdown("#### Average Rating per Genre")
    st.line_chart(genre_avg_rating)

    chart = alt.Chart(top_movies).mark_bar().encode(
            x=alt.X('rating_count:Q', title='Number of Ratings'),
            y=alt.Y('title:N', title='Movie Title', sort='-x'),
            tooltip=['title:N', 'rating_count:Q']
        ).properties(
            title=f"Top Movies with at least {min_ratings} Ratings"
        )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

with col[2]:
    st.markdown('#### Top Rated Movies of All-Time')

    df_top_rated = df.sort_values(by='average_rating', ascending=False)
    
    # Display the sorted DataFrame with column configurations inside col3
    st.dataframe(
        df_top_rated[["title", "average_rating"]], 
       #df_selected_year_sorted[["title", "average_rating"]],  # Only display title and average_rating columns
        hide_index=True,  # Hide index to keep it clean
        height=1000,
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