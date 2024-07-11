from database import retrieve_songs, add_songs, TrackInfo
from analysis import apply_pca, find_similarity, get_playlist_info
from local import print_data

## Based on a playlist, return a list of TrackInfos (track_id and cosine). The list has `amount` items, the most similar ones, based on cosine.
def find_songs(playlist: str, amount:int, adding:bool=False) -> list[TrackInfo]:
    user_infos, user_ids, user_songs = get_playlist_info(playlist)
    database_infos = retrieve_songs(filters=f"WHERE track_id NOT IN {user_ids}")
    if adding:
        add_songs(user_infos, user_songs) ## Add the playlist's songs to our database (slows down the process, but refines it)
    user_vector = apply_pca(user_infos)

    return find_similarity(user_vector, database_infos, amount)

if __name__ == "__main__":
    playlist = input("Playlist: ")
    amount = int(input("Amount: "))
    recommendations = find_songs(playlist, amount, adding=True)
    print_data(recommendations)