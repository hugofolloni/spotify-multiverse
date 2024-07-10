from database import retrieve_songs
from analysis import apply_pca, find_similarity, get_playlist_info

def find_songs(playlist, amount):
    user_infos, user_ids = get_playlist_info(playlist)
    database_infos = retrieve_songs(filters=f"WHERE track_id NOT IN {user_ids}")
    user_vector = apply_pca(user_infos)

    return find_similarity(user_vector, database_infos, amount)
    
if __name__ == "__main__":    
    recommendations = find_songs('https://open.spotify.com/playlist/3vtjLAc8lbGRfw62X6RRN7?si=7d94077aab064e2b', 15)
    print(recommendations)