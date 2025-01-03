# spotify-multiverse

**spotify-multiverse** is a full-stack application that helps users discover new songs based on a playlist they already love. Through mathematical analysis, the project extracts the essential elements of the user's favorite songs, enabling the search for other tracks that will also be appealing.

[Important!](#workaround)

## About 📝

This app was developed as a Final Project in Scientific Computing and Data Analysis by Hugo Folloni. The motivation behind the project stems from a personal love for music and the desire to find new songs that match the vibe of existing favorite playlists. The application leverages the Spotify API to analyze and recommend music based on user preferences.

## Math 🔢

The project employs concepts from linear algebra, such as vector and matrix operations, to analyze and compare songs. Each song is represented as a vector with specific attributes like danceability, energy, and loudness. By creating a matrix from a playlist of songs, Principal Component Analysis (PCA) is used to identify patterns and extract the most important components. This allows the application to generate a base vector that represents the user's musical taste and compare it with other songs in the Spotify database using Euclidean distance.

## How to Use 🎉

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/spotify-multiverse.git
    cd spotify-multiverse
    ```
2. **Install Dependencies**:
    ```bash
    cd server 
    pip install -r requirements.txt
    cd ../website
    npm install
    ```
3. **Set Up Environment Variables:** 

    Create a `.env` file in the `server` directory.

    ```
    SPOTIFY_CLIENT = 
    SPOTIFY_SECRET = 

    DB_DATABASE =
    DB_HOST =
    DB_USER = 
    DB_PASSWORD =
    DB_PORT = 

    API_KEY = 
    ```

4. **Run the backend**:

    ```bash
    cd server 
    app.py
    ```

5. **Start frontend**:
    
    ```bash
    cd ../website
    npm install
    ```
    
## Technologies 💻
- Frontend: JavaScript, React
- Backend: Python, Flask
- Database: PostgreSQL
- Data Analysis: NumPy, Scikit-learn
- API: Spotify API

## Workaround 

Due to the deprecation of Spotify's `audio-features` endpoint, the recommendation process of **spotify-multiverse** has been adjusted. Instead of retrieving audio features directly from the Spotify API, the application now uses a different approach:

1. **Extract Artists from Playlist:**  
   Given the user's playlist, the application identifies all unique artists featured in the playlist.

2. **Query Local Database:**  
   Using a pre-built database of 2500 songs, the application retrieves songs by the same artists found in the user's playlist. These songs serve as a proxy for analyzing the musical characteristics of the user's preferences.

3. **Analyze Local Audio Features:**  
   The application then uses the audio features of these locally stored songs (e.g., danceability, energy, loudness) to represent the user's musical taste.

4. **Recommendation Process:**  
   As before, Principal Component Analysis (PCA) is applied to extract the essence of the user's preferences, and Euclidean distance is used to recommend similar tracks from the database.

This workaround ensures the project remains functional and continues to deliver personalized recommendations despite changes in the Spotify API. However, recommendations are now limited to songs and artists available in the local database, which may affect the diversity of results.

## Disclaimer

Errors may occur due to issues with the Spotify API.