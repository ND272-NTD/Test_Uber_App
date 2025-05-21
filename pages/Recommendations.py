import streamlit as st

st.title("Movies Recommended 4 U 🍿")

import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def load_data():
    movies = pd.read_csv("movies.csv", encoding='ISO-8859-1')
    ratings = pd.read_csv("rating.csv", encoding='ISO-8859-1') 
    return movies, ratings

movies, ratings = load_data()

# Create user-item matrix
user_item_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

# Compute cosine similarity between users
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)


st.title("Based on movies similar other users have reviewed, we think you'll love these!") 
selected_user = st.selectbox("Select your user ID to get your tailored recommendations", user_item_matrix.index)

def get_top_n_recommendations(user_id, n=10):
    # Similarity scores
    sim_scores = user_similarity_df[user_id].sort_values(ascending=False)

    # Get top similar users (excluding the user itself)
    top_similar_users = sim_scores.iloc[1:11]

    # Movies rated by top similar users
    similar_users_ratings = user_item_matrix.loc[top_similar_users.index]

    # Weighted sum of ratings
    weighted_ratings = similar_users_ratings.T.dot(top_similar_users)
    similarity_sum = top_similar_users.sum()

    # Final score
    scores = weighted_ratings / similarity_sum

    # Filter out movies already rated by the user
    unrated_movies = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] == 0].index
    recommended_scores = scores.loc[unrated_movies].sort_values(ascending=False).head(n)

    # Get movie titles
    top_movies = movies[movies['movieId'].isin(recommended_scores.index)][['movieId', 'title','genres']]
    top_movies = top_movies.set_index('movieId').loc[recommended_scores.index]
    top_movies['Predicted Rating'] = recommended_scores.values

    return top_movies

# Show recommendations
if selected_user:
    st.subheader(f"Top 10 Movie Recommendations for User {selected_user}")
    recommendations = get_top_n_recommendations(selected_user)
    st.table(recommendations.reset_index(drop=True))
