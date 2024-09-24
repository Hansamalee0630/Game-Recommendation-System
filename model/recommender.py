import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import os

# Your RAWG API Key
api_key = os.getenv('RAWG_API_KEY')

# Function to search for a game and get its cover image
def get_game_image_url(game_name):
    """
    Search for a game by name and retrieve its cover image URL.
    
    Parameters:
        game_name (str): The name of the game to search for.
    
    Returns:
        str: The URL of the game's cover image or an error message.
    """

    search_url = f'https://api.rawg.io/api/games?key={api_key}&search={game_name}'
    
    # Make the request to the RAWG API
    response = requests.get(search_url)
    

    if response.status_code == 200:
        data = response.json()

        # Check if there are any results
        if data['results']:
            game = data['results'][0]  # Get the first result
            return game['background_image']  # Return the background image URL
        
        else:
            return "No image found"  # No game found
    else:
        print(f"Error {response.status_code}: {response.text}")  # Print the full error message
        return f"Error: {response.status_code}"

# Example: Get image for a game
game_name = "The Witcher 3"
cover_image_url = get_game_image_url(game_name)
print(cover_image_url)

# Load dataset
steam_data = pd.read_csv(r"Video_Games_Sales_as_at_22_Dec_2016.csv")

# Convert 'User_Score' to numeric, forcing errors to NaN
steam_data['User_Score'] = pd.to_numeric(steam_data['User_Score'], errors='coerce')

# Drop duplicates based on 'Name' and 'Platform'
steam_data = steam_data.drop_duplicates(subset=['Name', 'Platform'])

# Drop rows where 'User_Score' is NaN
steam_data = steam_data.dropna(subset=['User_Score'])

# Normalize game names in the DataFrame
steam_data['Name'] = steam_data['Name'].str.lower().str.strip()

# Prepare pivot table for user-game matrix
user_game_matrix = steam_data.pivot(index='Name', columns='Platform', values='User_Score').fillna(0)
print("User-Game Matrix Shape:", user_game_matrix.shape)

# Collaborative Filtering (Matrix Factorization)
svd = TruncatedSVD(n_components=17, random_state=42)
game_matrix_svd = svd.fit_transform(user_game_matrix)
print("Game Matrix SVD Shape:", game_matrix_svd.shape)

# Function for collaborative filtering
def collaborative_filtering(preferred_game):
    preferred_game = preferred_game.lower().strip()  # Normalize input
    if preferred_game not in user_game_matrix.index:
        return []  # Return an empty list if the game is not found

    game_index = user_game_matrix.index.get_loc(preferred_game)
    similarity_scores = np.dot(game_matrix_svd, game_matrix_svd[game_index])
    similar_games = np.argsort(-similarity_scores)[1:6]  # Top 5 similar games
    return user_game_matrix.index[similar_games].tolist()

# Content-Based Filtering using TF-IDF on 'Genre' column
if 'Genre' not in steam_data.columns:
    raise ValueError("The dataset must contain a 'Genre' column for content-based filtering.")

# Drop duplicates for content filtering
games_metadata = steam_data.drop_duplicates(subset=['Name']).reset_index()

# Create TF-IDF matrix using 'Genre'
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(games_metadata['Genre'])  # Create TF-IDF matrix based on Genre
print("TF-IDF Matrix Shape:", tfidf_matrix.shape)

# Function for content-based filtering
def content_based_filtering(preferred_game):
    preferred_game = preferred_game.lower().strip()  # Normalize input
    if preferred_game not in games_metadata['Name'].str.lower().values:
        return []  # Return an empty list if the game is not found
    
    game_index = games_metadata[games_metadata['Name'].str.lower() == preferred_game].index[0]
    cosine_similarities = cosine_similarity(tfidf_matrix[game_index], tfidf_matrix).flatten()
    similar_games_indices = np.argsort(-cosine_similarities)[1:6]  # Top 5 similar games
    return games_metadata['Name'].iloc[similar_games_indices].tolist()

# Hybrid Recommendation function with weighting
def hybrid_filtering(preferred_game, platform=None, weight_collab=0.7, weight_content=0.3):
    # Get recommendations from both methods
    collab_recommendations = collaborative_filtering(preferred_game)
    content_recommendations = content_based_filtering(preferred_game)

    # Combine recommendations and assign weights
    combined_scores = {}

    # Add collaborative filtering recommendations with weight
    for game in collab_recommendations:
        if game not in combined_scores:
            combined_scores[game] = 0
        combined_scores[game] += weight_collab

    # Add content-based filtering recommendations with weight
    for game in content_recommendations:
        if game not in combined_scores:
            combined_scores[game] = 0
        combined_scores[game] += weight_content

    # Sort the recommendations by combined scores
    hybrid_recommendations = sorted(combined_scores, key=combined_scores.get, reverse=True)

    # Optionally filter by platform if required
    if platform:
        hybrid_recommendations = [game for game in hybrid_recommendations if platform in user_game_matrix.columns]

    # Add image URLs to the recommendations
    recommendations_with_images = []
    for game in hybrid_recommendations[:5]:  # Return top 5 recommendations
        image_url = get_game_image_url(game)
        recommendations_with_images.append({'name': game, 'image_url': image_url})

    return recommendations_with_images

# Example usage
print(hybrid_filtering("Call of Duty: World at War", platform="PC"))