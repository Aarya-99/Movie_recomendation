from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the required files
movies = pickle.load(open('new_movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to recommend similar movies
def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = list(enumerate(similarity[movie_index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    
    # Only return movie names, not tuples
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies

# Homepage route
@app.route('/')
def home():
    return render_template('index.html', movie_list=movies['title'].values)

# Recommendation route
@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie_name = request.form['movie']
    recommendations = recommend(movie_name)
    return render_template('index.html', movie_list=movies['title'].values, recommendations=recommendations, selected_movie=movie_name)

if __name__ == '__main__':
    app.run(debug=True)
