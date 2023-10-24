from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load movies and similarity data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/recommend', methods=['GET'])
def get_recommendations():
    movie_name = request.args.get('movie')
    if movie_name is None:
        return jsonify({"error": "Please provide a 'movie' parameter."}), 400

    if movie_name not in movies['title'].values:
        return jsonify({"error": "Movie not found."}), 404

    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies.iloc[i[0]]['title'] for i in movies_list]

    return jsonify({"recommendations": recommended_movies})

if __name__ == '__main__':
    app.run(debug=True)

