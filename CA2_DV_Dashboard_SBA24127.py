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
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = df[df.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="average_rating", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)