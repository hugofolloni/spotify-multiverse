from database import retrieve_songs, add_songs, TrackInfo
from analysis import apply_pca, find_similarity, get_playlist_info

## Based on a playlist, return a list of TrackInfos (track_id and cosine). The list has `amount` items, the most similar ones, based on cosine.
def find_songs(playlist: str, amount:int) -> list[TrackInfo]:
    user_infos, user_ids, user_songs = get_playlist_info(playlist)
    database_infos = retrieve_songs(filters=f"WHERE track_id NOT IN {user_ids}")
    add_songs(user_infos, user_songs)
    user_vector = apply_pca(user_infos)

    return find_similarity(user_vector, database_infos, amount)

    

    