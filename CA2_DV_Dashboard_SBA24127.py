import streamlit as st
import pandas as pd
import os

# Streamlit layout
st.title("Movie Finder 🍿 🤖")

# Specify the path to your local CSV file
csv_file_path = "movies.csv"  # Assuming the file is in the same folder as your app

# Debugging the file path
st.write(f"Looking for file: {csv_file_path}")
st.write(f"Current directory: {os.getcwd()}")

try:
    # Read the CSV file
    df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')  # Try using 'utf-8' if 'ISO-8859-1' fails
    st.write(f"Loaded {df.shape[0]} movies")

    # Check for required columns
    if 'movieId' not in df.columns or 'title' not in df.columns or 'genres' not in df.columns:
        st.error("CSV file must contain 'id', 'title', and 'overview' columns.")
    else:
        # Continue processing the data...
        st.write(df.head())  # Display first few rows to ensure it's read correctly

except FileNotFoundError:
    st.error(f"The file {csv_file_path} was not found in the current directory.")
except UnicodeDecodeError:
    st.error("Error reading the file. Try using a different encoding (e.g., 'ISO-8859-1').")
except Exception as e:
    st.error(f"An error occurred: {e}")
