# Import necessary modules from Flask
from flask import Flask, render_template, request, jsonify
import requests
from model.recommender import hybrid_filtering, steam_data

# Create an instance of the Flask class
app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    # Render the HTML template for the home page
    return render_template('index.html')

# Route for game search suggestions
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    # Retrieve query from GET request
    query = request.args.get('query', '').lower().strip()

    # Get matching games from the dataset (e.g., steam_data in recommender.py)
    matching_games = steam_data[steam_data['Name'].str.contains(query, na=False)]['Name'].unique()[:5]

    # Return the matches as a JSON response
    return jsonify({'suggestions': list(matching_games)})


# Route for getting game recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    # Retrieve data sent via the POST request
    preferred_game = request.form['preferred_game']
    platform = request.form['platform']

    # Implement hybrid filtering logic to get actual game recommendations
    recommendations = hybrid_filtering(preferred_game, platform)

    # Return the recommendations as a JSON response
    return jsonify({'recommendations': recommendations})

# Run the Flask application
if __name__ == '__main__':
    # Enable debug mode for development
    app.run(debug=True)