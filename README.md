# spotify-multiverse

**spotify-multiverse** is a full-stack application that helps users discover new songs based on a playlist they already love. Through mathematical analysis, the project extracts the essential elements of the user's favorite songs, enabling the search for other tracks that will also be appealing.

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
- Data Analysis: NumPy, Pandas, Scikit-learn
- API: Spotify API

## Disclaimer

Errors may occur due to issues with the Spotify API.